"""External perceived-reading-confidence benchmark; never a PVC 1–5 model."""
import argparse
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import subprocess

import joblib
import numpy as np
import pandas as pd
import soundfile as sf
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from analyze import extract, smile

HERE = Path(__file__).resolve().parent
LABELS = {-1: 'Low', 0: 'Medium', 1: 'High'}
EXPECTED_COUNTS = {-1: 196, 0: 242, 1: 162}
SEED = 42
EXPLORATORY = ['energy_activity_ratio', 'energy_silence_ratio', 'pause_count',
               'mean_pause_duration_s', 'max_pause_duration_s']
ADDITIONS = ['audio_duration_s', 'rms_mean', 'rms_std', 'rms_range']
DISCLAIMER = ("This prediction comes from an external model trained on children's English "
              "reading-confidence ratings. It is a demonstration of the acoustic modelling "
              "pipeline, not a validated PVC assessment for adult paediatric communication.")
SPEAKER_LIMIT = ('Speaker identities are not verified. Recording-level cross-validation may share '
                 'speakers, texts and recording conditions across folds; no unseen-speaker generalisation claim.')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')


def predictor_names():
    return list(smile().feature_names) + ADDITIONS


def load_labels(dataset, expected_counts=EXPECTED_COUNTS):
    """Headerless release: exact WAV-stem join; third column is undocumented, not a split."""
    dataset = Path(dataset)
    table = pd.read_csv(dataset/'ratings.csv', header=None, dtype=str, keep_default_na=False)
    if table.shape[1] != 3:
        raise ValueError('Expected exactly three headerless ratings.csv columns')
    table.columns = ['source_sample_id', 'original_class', 'source_flag']
    if table.source_sample_id.eq('').any() or table.source_sample_id.duplicated().any():
        raise ValueError('Empty or duplicate label ID')
    if not table.original_class.isin(['-1', '0', '1']).all():
        raise ValueError('Labels must be original -1, 0, 1 codes')
    table['original_class'] = table.original_class.astype(int)
    if expected_counts is not None and table.original_class.value_counts().to_dict() != expected_counts:
        raise ValueError('Class counts differ from the verified release; recheck mapping/provenance')
    wavs = list((dataset/'audios').glob('*.wav'))
    if len({p.stem for p in wavs}) != len(wavs) or {p.stem for p in wavs} != set(table.source_sample_id):
        raise ValueError('WAVs and labels must match exactly, one to one, without extras or missing files')
    table = table.sort_values('source_sample_id').reset_index(drop=True)
    table.insert(0, 'sample_id', [f'rc_{i+1:04d}' for i in range(len(table))])
    table['class_name'] = table.original_class.map(LABELS)
    return table


def join_features(labels, features):
    if features.sample_id.duplicated().any() or labels.sample_id.duplicated().any():
        raise ValueError('Duplicate sample IDs in feature/label join')
    if set(features.sample_id) != set(labels.sample_id):
        raise ValueError('Feature and label IDs do not match exactly')
    return labels.merge(features, on='sample_id', validate='one_to_one', sort=False)


def extract_dataset(dataset, work):
    dataset, work = Path(dataset), Path(work)
    if work.resolve() == dataset.resolve() or dataset.resolve() in work.resolve().parents:
        raise ValueError('Derived outputs must be outside the raw dataset')
    work.mkdir(parents=True, exist_ok=True)
    cache = work/'evidence'
    cache.mkdir(exist_ok=True)
    labels = load_labels(dataset)
    records, infos, warnings = [], [], {}
    signature = {'analyze_sha256': sha(HERE/'analyze.py'), 'opensmile': version('opensmile'),
                 'numpy': version('numpy'), 'soundfile': version('soundfile')}
    for i, row in labels.iterrows():
        audio = dataset/'audios'/f'{row.source_sample_id}.wav'
        digest = sha(audio)
        path = cache/f'{row.sample_id}.json'
        result = json.loads(path.read_text()) if path.exists() else None
        if not result or result.get('audio_sha256') != digest or result.get('cache_signature') != signature:
            result = extract(audio, sample_id=row.sample_id)
            result['cache_signature'] = signature
            write_json(path, result)
        if result['egemaps_feature_count'] != 88:
            raise ValueError('Incomplete acoustic extraction')
        records.append(dict(sample_id=row.sample_id, audio_sha256=digest, **result['features']))
        info = sf.info(audio)
        infos.append(dict(duration=info.duration, sample_rate=info.samplerate,
                          channels=info.channels, subtype=info.subtype))
        for warning in result['warnings']:
            warnings[warning] = warnings.get(warning, 0) + 1
        if (i+1) % 25 == 0:
            print(f'Extracted/verified {i+1}/{len(labels)}', flush=True)
    table = join_features(labels, pd.DataFrame(records))
    if table.audio_sha256.duplicated().any():
        raise ValueError('Duplicate audio bytes found; resolve before cross-validation')
    table.to_csv(work/'features.csv', index=False)
    try:
        commit = subprocess.check_output(['git', '-C', str(dataset), 'rev-parse', 'HEAD'], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = 'unavailable (non-Git download)'
    provenance = dict(dataset_url='https://github.com/KaminiSabu/ReadingConfidenceDataset',
        dataset_commit=commit, ratings_sha256=sha(dataset/'ratings.csv'),
        readme_sha256=sha(dataset/'Readme.md'), recordings=len(table),
        class_counts={LABELS[k]: int(v) for k,v in table.original_class.value_counts().items()},
        numeric_mapping={str(k): v for k,v in LABELS.items()},
        mapping_evidence='Unique class counts match README and paper section 4; no explicit numeric-code legend is supplied.',
        source_flag_counts=labels.source_flag.value_counts().to_dict(),
        source_flag_interpretation='Undocumented; not used as a split or feature.',
        speaker_status=SPEAKER_LIMIT, undocumented_prefix_count=int(labels.source_sample_id.str.split('_').str[0].nunique()),
        speaker_count_reported_by_source=155, duplicate_audio_hashes=0,
        audio_formats=[dict(sample_rate=a, channels=b, subtype=c) for a,b,c in sorted({(x['sample_rate'],x['channels'],x['subtype']) for x in infos})],
        duration_seconds=dict(min=min(x['duration'] for x in infos), max=max(x['duration'] for x in infos),
                              mean=float(np.mean([x['duration'] for x in infos]))),
        extraction_signature=signature, extraction_settings=dict(frame_ms=20, energy_threshold_dbfs=-35, minimum_internal_pause_s=.2, normalization=False),
        exploratory_excluded_fields=EXPLORATORY, predictor_fields=predictor_names(),
        feature_table_sha256=sha(work/'features.csv'), warning_counts=warnings,
        use_conditions='Non-commercial research only; cite Sabu & Rao (2020). No separate LICENSE file or explicit redistribution grant found. Raw audio, row-level data and models kept local.')
    write_json(work/'provenance.json', provenance)
    return table, provenance


def split_folds(y, groups=None, n_splits=5):
    y = np.asarray(y)
    if set(y) != set(LABELS) or min(np.unique(y, return_counts=True)[1]) < n_splits:
        raise ValueError('Need all three original classes with at least n_splits observations each')
    if groups is None:
        splitter = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
    else:
        groups = np.asarray(groups)
        if len(groups) != len(y) or pd.isna(groups).any() or any(not str(g).strip() for g in groups):
            raise ValueError('Complete verified speaker IDs are required')
        if len(set(groups)) < n_splits:
            raise ValueError('Not enough independent speakers for requested folds')
        splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
    splits = list(splitter.split(np.zeros(len(y)), y, groups))
    for train, test in splits:
        if set(y[train]) != set(LABELS) or set(y[test]) != set(LABELS):
            raise ValueError('Every training and test fold must contain all three classes')
        if groups is not None and set(groups[train]) & set(groups[test]):
            raise ValueError('Speaker leakage detected')
    return splits


def models():
    return {
        'majority': make_pipeline(SimpleImputer(strategy='median', keep_empty_features=True), DummyClassifier(strategy='most_frequent')),
        'logistic': make_pipeline(SimpleImputer(strategy='median', keep_empty_features=True), StandardScaler(),
                                  LogisticRegression(C=1.0, solver='lbfgs', max_iter=3000, class_weight='balanced', random_state=SEED)),
        'random_forest': make_pipeline(SimpleImputer(strategy='median', keep_empty_features=True),
                                      RandomForestClassifier(n_estimators=300, min_samples_leaf=2, max_features='sqrt',
                                                             class_weight='balanced_subsample', random_state=SEED, n_jobs=1))}


def scores(y, prediction):
    return dict(balanced_accuracy=float(balanced_accuracy_score(y, prediction)),
                macro_f1=float(f1_score(y, prediction, labels=list(LABELS), average='macro', zero_division=0)),
                confusion_matrix=confusion_matrix(y, prediction, labels=list(LABELS)).tolist(),
                classification_report=classification_report(y, prediction, labels=list(LABELS),
                    target_names=list(LABELS.values()), output_dict=True, zero_division=0))


def evaluate(table, work, results, provenance=None, groups=None, group_source=None, columns=None, n_splits=5, permutation_repeats=5):
    work, results = Path(work), Path(results)
    work.mkdir(parents=True, exist_ok=True)
    results.mkdir(parents=True, exist_ok=True)
    columns = predictor_names() if columns is None else columns
    if not columns or not set(columns) <= set(predictor_names()):
        raise ValueError('Predictors must come from the explicit acoustic/non-gated allowlist')
    if table.sample_id.duplicated().any():
        raise ValueError('Duplicate samples')
    if groups is not None and not group_source:
        raise ValueError('A documented source for verified speaker IDs is required')
    X = table[columns].apply(pd.to_numeric, errors='raise')
    if np.isinf(X.to_numpy()).any():
        raise ValueError('Infinite features')
    y = table.original_class.to_numpy()
    splits = split_folds(y, groups, n_splits)
    folds = np.full(len(y), -1)
    fold_info = []
    for i, (train, test) in enumerate(splits):
        folds[test] = i+1
        fold_info.append(dict(fold=i+1, train_n=len(train), test_n=len(test),
                              train_counts={LABELS[k]:int(sum(y[train] == k)) for k in LABELS},
                              test_counts={LABELS[k]:int(sum(y[test] == k)) for k in LABELS},
                              speaker_overlap=None if groups is None else len(set(np.asarray(groups)[train]) & set(np.asarray(groups)[test]))))
    assignments = table[['sample_id','original_class']].copy()
    assignments['fold'] = folds
    if groups is not None:
        assignments['speaker_id'] = groups
    assignments.to_csv(work/'fold_assignments.csv', index=False)
    report = dict(title='External perceived-reading-confidence benchmark', disclaimer=DISCLAIMER,
        evaluation=f'{n_splits}-fold recording-level stratified CV; NOT speaker-independent' if groups is None else f'{n_splits}-fold verified speaker-disjoint stratified group CV',
        n_splits=n_splits, seed=SEED, speaker_independent=groups is not None,
        speaker_source=group_source, limitation=SPEAKER_LIMIT if groups is None else 'Speaker-disjoint; text/school/session/domain transfer still not established.',
        fold_details=fold_info, fold_assignments_sha256=sha(work/'fold_assignments.csv'),
        provenance=provenance, classes=LABELS, predictor_count=len(columns), predictors=columns,
        exploratory_excluded_fields=EXPLORATORY, models={},
        demo_model='logistic (chosen in advance for simplicity, not selected from CV performance)',
        preprocessing='Within each training fold: median imputation; logistic only: standard scaling. No tuning or feature selection.',
        hyperparameters=dict(majority='most_frequent', logistic=dict(C=1.0,solver='lbfgs',max_iter=3000,class_weight='balanced'),
                             random_forest=dict(n_estimators=300,min_samples_leaf=2,max_features='sqrt',class_weight='balanced_subsample',random_state=SEED)),
        permutation_repeats=permutation_repeats,
        uncertainty='Fold SD is descriptive, not a confidence interval. Repeated speakers may inflate performance; no independent final test set.',
        versions={p:version(p) for p in ['numpy','pandas','scikit-learn','opensmile','soundfile','joblib']})
    oof = assignments.copy()
    importance = []
    for name, template in models().items():
        pred = np.empty(len(y), dtype=int)
        probabilities = np.zeros((len(y), 3))
        fold_scores = []
        for i,(train,test) in enumerate(splits):
            model = clone(template).fit(X.iloc[train], y[train])
            pred[test] = model.predict(X.iloc[test])
            if list(model.classes_) != list(LABELS):
                raise ValueError('Unexpected probability class order')
            probabilities[test] = model.predict_proba(X.iloc[test])
            fold_scores.append(dict(fold=i+1, **scores(y[test], pred[test])))
            if name == 'random_forest' and permutation_repeats:
                imp = permutation_importance(model, X.iloc[test], y[test], scoring='f1_macro',
                                              n_repeats=permutation_repeats, random_state=SEED+i, n_jobs=1)
                importance.append(imp.importances)
            print(f'{name}: fold {i+1}/{n_splits}', flush=True)
        report['models'][name] = dict(pooled_oof=scores(y,pred), folds=fold_scores,
            fold_balanced_accuracy_sd=float(np.std([s['balanced_accuracy'] for s in fold_scores], ddof=1)),
            fold_macro_f1_sd=float(np.std([s['macro_f1'] for s in fold_scores], ddof=1)))
        oof[name+'_prediction'] = pred
        for j,label in enumerate(LABELS.values()):
            oof[name+'_'+label+'_probability'] = probabilities[:,j]
        final = clone(template).fit(X,y)
        if name != 'majority':
            joblib.dump(dict(kind='external-reading-confidence-v1', model=final, features=columns,
                            classes=LABELS, disclaimer=DISCLAIMER, extraction_signature=(provenance or {}).get('extraction_signature'),
                            provenance=provenance, training_duration_range=[float(table.audio_duration_s.min()),float(table.audio_duration_s.max())] if 'audio_duration_s' in table else None,
                            versions=report['versions']), work/f'{name}.joblib')
        if name == 'logistic':
            coef = pd.DataFrame(final[-1].coef_.T, index=columns, columns=list(LABELS.values()))
            coef.index.name = 'feature'
            coef.to_csv(results/'logistic_standardized_coefficients.csv')
    if importance:
        values = np.concatenate(importance,axis=1)
        pd.DataFrame(dict(feature=columns, mean_macro_f1_drop=values.mean(axis=1),
                          sd_across_fold_repeats=values.std(axis=1,ddof=1))).sort_values('mean_macro_f1_drop',ascending=False).to_csv(results/'rf_oof_permutation_importance.csv',index=False)
    oof.to_csv(work/'out_of_fold_predictions.csv', index=False)
    write_json(results/'evaluation.json', report)
    lines = ['# External perceived-reading-confidence benchmark', '', report['evaluation'], '', report['limitation'], '',
             '| Model | Pooled OOF balanced accuracy | Pooled OOF macro F1 |', '| --- | ---: | ---: |']
    for name,item in report['models'].items():
        s=item['pooled_oof']
        lines.append(f"| {name} | {s['balanced_accuracy']:.4f} | {s['macro_f1']:.4f} |")
    lines += ['', 'Confusion matrices: rows = true, columns = predicted; order Low, Medium, High.']
    for name,item in report['models'].items():
        lines += ['', '## '+name, '', '```text', *[' '.join(f'{v:4d}' for v in row) for row in item['pooled_oof']['confusion_matrix']], '```', '',
                  '| Class | Precision | Recall | F1 | n |','| --- | ---: | ---: | ---: | ---: |']
        for label in LABELS.values():
            c=item['pooled_oof']['classification_report'][label]
            lines.append(f"| {label} | {c['precision']:.4f} | {c['recall']:.4f} | {c['f1-score']:.4f} | {int(c['support'])} |")
    lines += ['', '## Interpretation boundaries', '', DISCLAIMER, '',
              'Probabilities are uncalibrated model outputs, not psychological certainty. No PVC 1–5 conversion is performed.',
              'All preprocessing is fit inside training folds. Fixed hyperparameters; no feature selection or tuning. Final local models refit all recordings for demonstration only.',
              f'RF permutation importance is held-out macro-F1 change ({permutation_repeats} repeats per fold); correlated features can mask or share importance. Its SD is not a confidence interval.',
              'Logistic coefficients are from the final all-data standardized model, not causal effects or explanations of an individual prediction.',
              'Raw audio, names, per-recording features, fold assignments, predictions and fitted models stay local. Aggregate metrics and feature summaries only are published.', '',
              'See [method/provenance](../../../../docs/reading_confidence_benchmark.md) and [live demo](../../../../docs/live_confidence_demo.md).']
    (results/'README.md').write_text('\n'.join(lines)+'\n')
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dataset',type=Path,required=True)
    p.add_argument('--work',type=Path,default=HERE/'private/reading_benchmark')
    p.add_argument('--results',type=Path,default=HERE/'results/reading_confidence')
    p.add_argument('--speaker-map',type=Path,help='Author-verified CSV: sample_id,speaker_id. Never guessed filename prefixes.')
    p.add_argument('--speaker-map-source',help='Provenance of verified mapping, required with --speaker-map')
    a=p.parse_args()
    try:
        table,provenance=extract_dataset(a.dataset,a.work)
        groups=None
        if a.speaker_map:
            mapping=pd.read_csv(a.speaker_map,dtype=str,keep_default_na=False)
            if set(mapping.columns) != {'sample_id','speaker_id'}:
                raise ValueError('Speaker map requires sample_id,speaker_id only')
            joined=join_features(table[['sample_id']],mapping)
            groups=joined.speaker_id.to_numpy()
        elif a.speaker_map_source:
            raise ValueError('Supply --speaker-map with its source')
        evaluate(table,a.work,a.results,provenance,groups,a.speaker_map_source)
    except (ValueError,OSError,RuntimeError) as error:
        p.error(str(error))
    print(f'Aggregate results: {a.results}\nLocal data/models: {a.work}')


if __name__ == '__main__':
    main()
