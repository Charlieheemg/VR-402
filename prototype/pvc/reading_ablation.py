"""Fixed-fold confound audit; never selects or replaces the live-demo model."""
import argparse
import json
from pathlib import Path
from importlib.metadata import version

import numpy as np
import pandas as pd
from sklearn.base import clone

from analyze import smile
from reading_benchmark import HERE, LABELS, SPEAKER_LIMIT, models, predictor_names, scores, sha, write_json


def feature_sets():
    acoustic = list(smile().feature_names)
    full = predictor_names()
    return {'A_full': full, 'B_egemaps_only': acoustic,
            'C_no_duration': [c for c in full if c != 'audio_duration_s'],
            'D_duration_only': ['audio_duration_s'],
            'E_rms_only': ['rms_mean', 'rms_std', 'rms_range']}


def saved_splits(table, assignments):
    if set(assignments.columns) != {'sample_id','original_class','fold'}:
        raise ValueError('Expected original recording-level fold assignment schema')
    if table.sample_id.duplicated().any() or assignments.sample_id.duplicated().any():
        raise ValueError('Duplicate sample IDs')
    if set(table.sample_id) != set(assignments.sample_id):
        raise ValueError('Feature/fold sample IDs differ')
    aligned = assignments.set_index('sample_id').loc[table.sample_id]
    if not np.array_equal(aligned.original_class.to_numpy(),table.original_class.to_numpy()):
        raise ValueError('Labels differ between features and saved folds')
    if aligned.fold.isna().any() or set(aligned.fold) != {1,2,3,4,5}:
        raise ValueError('Exactly the five saved CV folds are required')
    splits=[]
    y=table.original_class.to_numpy()
    for fold in range(1,6):
        test=np.flatnonzero(aligned.fold.to_numpy()==fold)
        train=np.flatnonzero(aligned.fold.to_numpy()!=fold)
        if set(y[train]) != set(LABELS) or set(y[test]) != set(LABELS):
            raise ValueError('All classes required in every training/test fold')
        splits.append((train,test))
    return splits


def compact(y,pred):
    result=scores(y,pred)
    return dict(balanced_accuracy=result['balanced_accuracy'], macro_f1=result['macro_f1'],
                **{label.lower()+'_f1':result['classification_report'][label]['f1-score'] for label in LABELS.values()})


def run(table, assignments, reference, results, private_output=None):
    splits=saved_splits(table,assignments)
    y=table.original_class.to_numpy()
    sets=feature_sets()
    rows,fold_rows=[],[]
    predictions=table[['sample_id','original_class']].copy()
    templates=models()
    for condition,columns in sets.items():
        if not columns or not set(columns)<=set(predictor_names()):
            raise ValueError('Feature set outside explicit allowlist')
        X=table[columns].apply(pd.to_numeric,errors='raise')
        if np.isinf(X.to_numpy()).any():
            raise ValueError('Infinite predictors')
        for name,template in templates.items():
            prediction=np.empty(len(y),dtype=int)
            for i,(train,test) in enumerate(splits):
                model=clone(template).fit(X.iloc[train],y[train])
                prediction[test]=model.predict(X.iloc[test])
                metrics=compact(y[test],prediction[test])
                fold_rows.append(dict(condition=condition,model=name,fold=i+1,train_n=len(train),test_n=len(test),**metrics))
                if condition=='A_full':
                    old=reference['models'][name]['folds'][i]
                    for metric in ['balanced_accuracy','macro_f1']:
                        if not np.isclose(metrics[metric],old[metric],rtol=0,atol=1e-12):
                            raise ValueError('Full model does not reproduce original same-fold results')
            metrics=compact(y,prediction)
            if condition=='A_full':
                old=reference['models'][name]['pooled_oof']
                for metric in ['balanced_accuracy','macro_f1']:
                    if not np.isclose(metrics[metric],old[metric],rtol=0,atol=1e-12):
                        raise ValueError('Full model does not reproduce original pooled results')
            rows.append(dict(condition=condition,model=name,n_features=len(columns),n_recordings=len(y),**metrics))
            predictions[condition+'_'+name]=prediction
            print(f'{condition} / {name}: balanced accuracy {metrics["balanced_accuracy"]:.4f}, macro F1 {metrics["macro_f1"]:.4f}',flush=True)
    pooled=pd.DataFrame(rows)
    folds=pd.DataFrame(fold_rows)
    for frame,keys in [(pooled,['model']),(folds,['model','fold'])]:
        baseline=frame[frame.condition=='A_full'].set_index(keys)
        for metric in ['balanced_accuracy','macro_f1','low_f1','medium_f1','high_f1']:
            frame['delta_full_'+metric]=[row[metric]-baseline.loc[tuple(row[k] for k in keys) if len(keys)>1 else row[keys[0]],metric] for _,row in frame.iterrows()]
    results=Path(results)
    results.mkdir(parents=True,exist_ok=True)
    pooled.to_csv(results/'ablation_results.csv',index=False)
    folds.to_csv(results/'ablation_fold_results.csv',index=False)
    if private_output:
        predictions.to_csv(private_output,index=False)
    return pooled,folds


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work',type=Path,default=HERE/'private/reading_benchmark')
    p.add_argument('--reference',type=Path,default=HERE/'results/reading_confidence/evaluation.json')
    p.add_argument('--results',type=Path,default=HERE/'results/reading_confidence')
    a=p.parse_args()
    try:
        reference=json.loads(a.reference.read_text())
        features=a.work/'features.csv'
        assignments=a.work/'fold_assignments.csv'
        if sha(features)!=reference['provenance']['feature_table_sha256'] or sha(assignments)!=reference['fold_assignments_sha256']:
            raise ValueError('Saved features/folds differ from the committed benchmark; do not silently generate new folds')
        if reference['speaker_independent'] or reference['n_splits']!=5:
            raise ValueError('This audit expects the original five recording-level folds')
        for package,expected in reference['versions'].items():
            if version(package)!=expected:
                raise ValueError(f'{package} differs from original benchmark environment')
        table=pd.read_csv(features)
        if len(table)!=600:
            raise ValueError('Expected all 600 recordings')
        run(table,pd.read_csv(assignments),reference,a.results,a.work/'ablation_out_of_fold_predictions.csv')
        write_json(a.results/'ablation_metadata.json',dict(
            feature_table_sha256=sha(features),fold_assignments_sha256=sha(assignments),reference_sha256=sha(a.reference),
            ablation_code_sha256=sha(Path(__file__)),benchmark_code_sha256=sha(HERE/'reading_benchmark.py'),
            feature_sets=feature_sets(),versions=reference['versions'],hyperparameters=reference['hyperparameters'],
            fold_details=reference['fold_details'],speaker_independent=False,limitation=SPEAKER_LIMIT,
            full_model_reproduced=True,retuning=False,model_selection=False,
            notes='Pooled out-of-fold metrics and matched-fold deltas; descriptive comparisons, not independent-speaker significance tests. No models refitted or replaced.'))
    except (ValueError,OSError,RuntimeError) as error:
        p.error(str(error))


if __name__=='__main__':main()
