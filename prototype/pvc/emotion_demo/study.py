"""Exploratory CREMA-D audio-only perception study, with held-out speakers.

Full reproduction: python study.py --download
Model-only reproduction from committed derived data: python study.py --fit-only
"""
import argparse
import csv
import hashlib
import json
import platform
import shutil
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, confusion_matrix, f1_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from build import HERE, CREMA_REV, CREMA_ROOT, download, selections
from analyze import extract, smile

PRIVATE = HERE/'private/study'
RESULTS = HERE/'study_results'
SOURCE = f'https://raw.githubusercontent.com/CheyneyComputerScience/CREMA-D/{CREMA_REV}/'
LABELS = ['A','D','F','H','N','S']
NAMES = dict(zip(LABELS,['Anger','Disgust','Fear','Happy','Neutral','Sad']))
CS = [.01,.1,1.,10.]
STATEMENTS = ['IEO','TIE','IOM','IWW']
SEED = 'vr402-perception-v1'
SOURCE_HASHES = {'tabulatedVotes.csv':'774d9d759cb5caf2542758a39eca8c0f1d2777f9987ff5d5adf8066d192f377b',
                 'summaryTable.csv':'fb0e382700d32c0d9adc0c6815292215a36bcf912f2657048862c91e3bd2b317'}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def dump(path, obj):
    Path(path).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')

def votes_from_counts(counts):
    if set(counts)!=set(LABELS) or any(type(v) is not int or v<0 for v in counts.values()):
        raise ValueError('Expected six nonnegative integer emotion counts')
    total=sum(counts.values())
    winners=[k for k in LABELS if counts[k]==max(counts.values())] if total else []
    return dict(counts=counts,total=total,winners=winners,tied=len(winners)>1,
                target=winners[0] if len(winners)==1 else None,
                agreement=max(counts.values())/total if total else None)

def load_votes(table, summary):
    """Upstream R defines row ID = 100000*queryType + clipNum; type 1 = voice."""
    with Path(summary).open() as f:
        summaries={r['FileName']:r['VoiceVote'].split(':') for r in csv.DictReader(f)}
    result={}
    modality_counts=Counter()
    with Path(table).open() as f:
        for row in csv.DictReader(f):
            query_type=int(row[''])//100000
            modality_counts[query_type]+=1
            if query_type!=1:
                continue
            name=row['fileName']+'.wav'
            if name in result:
                raise ValueError('Duplicate audio-only vote row: '+name)
            votes=votes_from_counts({k:int(row[k]) for k in LABELS})
            if votes['total']!=int(row['numResponses']):
                raise ValueError('Vote count sum mismatch: '+name)
            if set(votes['winners'])!=set(row['emoVote'].split(':')):
                raise ValueError('Recomputed plurality differs from upstream emoVote: '+name)
            if set(votes['winners'])!=set(summaries[row['fileName']]):
                raise ValueError('Audio votes differ from summary VoiceVote: '+name)
            if votes['agreement'] is not None and not np.isclose(votes['agreement'],float(row['agreement'])):
                raise ValueError('Agreement mismatch: '+name)
            result[name]=dict(**votes,source_row=row[''],query_type=query_type)
    if modality_counts!={1:7442,2:7442,3:7442}:
        raise ValueError(f'Unexpected source inventory: {modality_counts}')
    return result

def plan_subset(filenames):
    """Only filenames/actor IDs enter selection, never vote counts or features."""
    groups={}
    for filename in sorted(filenames):
        actor,statement,emotion,intensity=Path(filename).stem.split('_')
        groups.setdefault((actor,statement,emotion),{})[intensity]=filename
    actors=sorted({k[0] for k in groups})
    # Upstream README documents 1064_IEO_DIS_MD as an anomalous all-displays
    # presentation; avoid the speaker before any extraction or model fitting.
    excluded={'1064':'Upstream-documented IEO_DIS_MD all-displays presentation anomaly'}
    for actor in actors:
        for statement in STATEMENTS:
            for emotion in ['ANG','DIS','FEA','HAP','NEU','SAD']:
                desired='MD' if statement=='IEO' and emotion!='NEU' else 'XX'
                if desired not in groups.get((actor,statement,emotion),{}):
                    excluded[actor]='Incomplete prespecified filename cells'
    eligible=[a for a in actors if a not in excluded]
    others=sorted((a for a in eligible if a!='1001'),key=lambda a:hashlib.sha256((SEED+':'+a).encode()).hexdigest())
    partitions={'train':others[:20],'validation':others[20:25],'test':['1001',*others[25:29]]}
    selected=[]
    for split,speakers in partitions.items():
        for actor in speakers:
            for statement in STATEMENTS:
                for emotion in ['ANG','DIS','FEA','HAP','NEU','SAD']:
                    available=groups[(actor,statement,emotion)]
                    desired='MD' if statement=='IEO' and emotion!='NEU' else 'XX'
                    if desired not in available:
                        raise ValueError(f'Missing prespecified cell: {actor}/{statement}/{emotion}/{desired}')
                    selected.append(dict(file=available[desired],actor=actor,statement=statement,
                                         intended_label=emotion,intensity=desired,split=split))
    assert len(selected)==720
    assert {r['file'] for r in selections() if r['dataset']=='CREMA-D'} <= {r['file'] for r in selected}
    return dict(schema='crema-perception-study-1',seed=SEED,upstream_revision=CREMA_REV,
                policy='30 speakers; four fixed sentences; six intended expressions per sentence; IEO MD except neutral XX, all others XX. Selection uses filenames only.',
                statements=STATEMENTS,partitions=partitions,c_grid=CS,refit_validation=False,
                available_speakers=len(actors),eligible_speakers=len(eligible),speaker_exclusions=excluded,
                target='Unique plurality of independent audio-only votes; tied/zero-vote clips excluded from fitting and single-label metrics, retained in distributions/predictions.',
                selected=selected)

def prepare(allow_download):
    PRIVATE.mkdir(parents=True,exist_ok=True)
    RESULTS.mkdir(parents=True,exist_ok=True)
    for filename,expected in SOURCE_HASHES.items():
        path=PRIVATE/filename
        if not path.exists():
            if not allow_download:
                raise FileNotFoundError(f'Missing {path}; use --download')
            download(SOURCE+'processedResults/'+filename,path)
        if sha(path)!=expected:
            raise ValueError('Pinned upstream source SHA-256 mismatch: '+filename)
    voices=load_votes(PRIVATE/'tabulatedVotes.csv',PRIVATE/'summaryTable.csv')
    plan=plan_subset(voices)
    # Written before audio acquisition, extraction, or fitting; not outcome-driven.
    dump(RESULTS/'plan.json',plan)
    audio=PRIVATE/'audio'
    audio.mkdir(exist_ok=True)
    def acquire(row):
        path=audio/row['file']
        if not path.exists():
            existing=HERE/'private/raw'/row['file']
            if existing.exists():
                shutil.copy2(existing,path)
            elif allow_download:
                download(CREMA_ROOT+CREMA_REV+'/AudioWAV/'+row['file'],path)
            else:
                raise FileNotFoundError(f'Missing WAV {path}; use --download')
        # Fail on LFS pointers and malformed downloads before extraction.
        if path.read_bytes()[:4]!=b'RIFF':
            raise ValueError('Expected actual RIFF WAV, not LFS pointer: '+path.name)
        return path
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(acquire,plan['selected']))
    print('Downloaded/verified 720 selected WAVs',flush=True)
    cache=PRIVATE/'cache'
    cache.mkdir(exist_ok=True)
    names=list(smile().feature_names)
    extractor_sha=sha(HERE.parent/'analyze.py')
    records=[]
    manifest=[]
    for i,row in enumerate(plan['selected']):
        path=audio/row['file']
        digest=sha(path)
        cached=cache/(path.stem+'.json')
        evidence=json.loads(cached.read_text()) if cached.exists() else None
        if evidence is None or evidence['audio_sha256']!=digest or evidence['opensmile_version']!=version('opensmile') or evidence.get('extractor_source_sha256')!=extractor_sha:
            evidence=extract(path)
            evidence['extractor_source_sha256']=extractor_sha
            dump(cached,evidence)
        records.append(dict(file=row['file'],**{k:evidence['features'][k] for k in names}))
        manifest.append(dict(**row,sha256=digest,sample_rate_hz=evidence['sample_rate_hz'],channels=evidence['channels'],
            source_url=CREMA_ROOT+CREMA_REV+'/AudioWAV/'+row['file'],
            audio_path='prototype/pvc/emotion_demo/private/study/audio/'+row['file'],
            votes=voices[row['file']],extraction_warnings=evidence['warnings']))
        if (i+1)%60==0:
            print(f'Extracted {i+1}/720',flush=True)
    pd.DataFrame(records).to_csv(RESULTS/'features.csv',index=False,float_format='%.17g')
    dump(RESULTS/'manifest.json',dict(source_hashes=SOURCE_HASHES,source_urls={f:SOURCE+'processedResults/'+f for f in SOURCE_HASHES},
        source_scope='queryType 1, independently checked against summaryTable VoiceVote for all 7442 clips',
        extractor='Existing analyze.extract; 88 eGeMAPSv02 functionals only, channel-mean mono, no resampling or level normalization',
        opensmile_version=version('opensmile'),extractor_source_sha256=extractor_sha,feature_names=names,clips=manifest))

def validate_inputs(plan,manifest,features):
    names=manifest['feature_names']
    if len(names)!=88 or len(set(names))!=88:
        raise ValueError('Expected exactly 88 distinct eGeMAPSv02 predictors')
    if list(features.columns)!=['file',*names] or features['file'].duplicated().any():
        raise ValueError('Feature schema/duplicate file error')
    expected={r['file'] for r in plan['selected']}
    if set(features['file'])!=expected or {r['file'] for r in manifest['clips']}!=expected:
        raise ValueError('Features, manifest and plan must match by filename exactly')
    for a,actors in plan['partitions'].items():
        for b,others in plan['partitions'].items():
            if a!=b and set(actors)&set(others):
                raise ValueError('Speaker leakage between splits')
    if '1001' not in plan['partitions']['test'] or any('1001' in plan['partitions'][s] for s in ['train','validation']):
        raise ValueError('Actor 1001 must be isolated in test')
    planned={r['file']:r for r in plan['selected']}
    for row in manifest['clips']:
        spec=planned[row['file']]
        if any(row[k]!=spec[k] for k in ['actor','statement','intended_label','intensity','split']):
            raise ValueError('Manifest differs from prespecified split')
        if row['actor'] not in plan['partitions'][row['split']]:
            raise ValueError('Clip speaker assigned to wrong split')
        computed=votes_from_counts(row['votes']['counts'])
        if any(computed[k]!=row['votes'][k] for k in computed) or row['votes']['query_type']!=1:
            raise ValueError('Invalid audio-only target or silently resolved tie')
    return names

def score(truth,predicted):
    support=Counter(truth)
    return dict(n=len(truth),class_counts={k:support[k] for k in LABELS},
        macro_f1=float(f1_score(truth,predicted,labels=LABELS,average='macro',zero_division=0)),
        balanced_accuracy=float(balanced_accuracy_score(truth,predicted)),
        accuracy=float(np.mean(np.array(truth)==np.array(predicted))),
        confusion_matrix=confusion_matrix(truth,predicted,labels=LABELS).tolist())

def model(c):
    return make_pipeline(SimpleImputer(strategy='median',keep_empty_features=True),StandardScaler(),
                         LogisticRegression(C=c,class_weight='balanced',solver='lbfgs',max_iter=5000,random_state=402))

def fit():
    plan=json.loads((RESULTS/'plan.json').read_text())
    manifest=json.loads((RESULTS/'manifest.json').read_text())
    features=pd.read_csv(RESULTS/'features.csv',float_precision='round_trip')
    names=validate_inputs(plan,manifest,features)
    rows=manifest['clips']
    matrix=features.set_index('file').loc[[r['file'] for r in rows],names].replace([np.inf,-np.inf],np.nan).to_numpy()
    masks={s:np.array([r['split']==s and r['votes']['target'] is not None for r in rows]) for s in plan['partitions']}
    targets=np.array([r['votes']['target'] or '' for r in rows])
    train=masks['train'];val=masks['validation']
    if set(targets[train])!=set(LABELS):
        raise ValueError('Training set does not cover all six perception classes')
    tuning=[]
    best=None
    for c in plan['c_grid']:
        candidate=model(c)
        candidate.fit(matrix[train],targets[train])
        val_score=score(targets[val],candidate.predict(matrix[val]))
        tuning.append(dict(C=c,validation_macro_f1=val_score['macro_f1'],validation_balanced_accuracy=val_score['balanced_accuracy']))
        # Equal selection scores keep the smaller C; never consult test.
        if best is None or val_score['macro_f1']>best[0]:
            best=(val_score['macro_f1'],c,candidate)
    _,selected_c,estimator=best
    baseline=DummyClassifier(strategy='most_frequent').fit(matrix[train],targets[train])
    predicted=estimator.predict(matrix)
    probabilities=estimator.predict_proba(matrix)
    base_pred=baseline.predict(matrix)
    partitions={}
    for split,mask in masks.items():
        total=sum(r['split']==split for r in rows)
        partitions[split]=dict(speakers=plan['partitions'][split],selected_clips=total,scored_clips=int(mask.sum()),
            excluded_ties=sum(r['split']==split and r['votes']['tied'] for r in rows),
            excluded_zero_votes=sum(r['split']==split and r['votes']['total']==0 for r in rows),
            model=score(targets[mask],predicted[mask]),majority_baseline=score(targets[mask],base_pred[mask]))
    per_clip=[]
    classes=list(estimator[-1].classes_)
    for i,row in enumerate(rows):
        per_clip.append(dict(file=row['file'],actor=row['actor'],split=row['split'],intended_label=row['intended_label'],
            human=row['votes'],prediction=predicted[i],probabilities={k:float(probabilities[i,classes.index(k)]) for k in LABELS},
            baseline_prediction=base_pred[i],included_in_single_label_scoring=row['votes']['target'] is not None,
            correct=bool(predicted[i]==row['votes']['target']) if row['votes']['target'] else None))
    demo_names=[r['file'] for r in selections() if r['dataset']=='CREMA-D']
    results=dict(schema='crema-perception-study-1',labels=LABELS,label_names=NAMES,selected_C=selected_c,
        upstream_revision=CREMA_REV,majority_training_class=base_pred[0],predictor_count=88,
        source_hashes=SOURCE_HASHES,derived_hashes={f:sha(RESULTS/f) for f in ['plan.json','manifest.json','features.csv']},
        software=dict(python=platform.python_version(),**{p:version(p) for p in ['numpy','pandas','scikit-learn','opensmile']}),
        partitions=partitions,selection_results=tuning,clips=per_clip,
        demo_clips={r['file']:r for r in per_clip if r['file'] in demo_names},
        interpretation='Exploratory audio-only perceived-emotion classification. Uncalibrated model probabilities are not communication-quality scores. Coefficients are associations, not causal coaching evidence.')
    dump(RESULTS/'results.json',results)
    pd.DataFrame(tuning).to_csv(RESULTS/'tuning.csv',index=False)
    pd.DataFrame([dict(class_code=label,class_name=NAMES[label],feature=feature,standardized_coefficient=float(coef))
        for label,weights in zip(classes,estimator[-1].coef_) for feature,coef in zip(names,weights)]).to_csv(RESULTS/'coefficients.csv',index=False)
    # Save learned preprocessing for auditing, not an unsafe serialized estimator.
    dump(RESULTS/'preprocessing.json',dict(imputer_medians=estimator[0].statistics_.tolist(),
        scaler_means=estimator[1].mean_.tolist(),scaler_scales=estimator[1].scale_.tolist(),feature_names=names,
        fit_speakers=plan['partitions']['train'],fit_files=[r['file'] for r,m in zip(rows,train) if m],
        intercepts=estimator[-1].intercept_.tolist(),classes=classes,iterations=estimator[-1].n_iter_.tolist()))
    write_reports(results,manifest)
    print(json.dumps({k:{'n':v['scored_clips'],'model':v['model']['macro_f1'],'baseline':v['majority_baseline']['macro_f1']} for k,v in partitions.items()},indent=2))
    return results

def write_reports(results,manifest):
    concise='| Split | Speakers | Scored / selected | Logistic macro-F1 | Majority macro-F1 | Logistic balanced acc. | Majority balanced acc. |\n|---|---:|---:|---:|---:|---:|---:|\n'
    for split,p in results['partitions'].items():
        m,b=p['model'],p['majority_baseline']
        concise+=f"| {split} | {len(p['speakers'])} | {p['scored_clips']} / {p['selected_clips']} | {m['macro_f1']:.3f} | {b['macro_f1']:.3f} | {m['balanced_accuracy']:.3f} | {b['balanced_accuracy']:.3f} |\n"
    slide='| Split (speakers) | Scored / selected | Macro-F1: model / majority | Balanced accuracy: model / majority |\n|---|---:|---:|---:|\n'
    for split,p in results['partitions'].items():
        m,b=p['model'],p['majority_baseline']
        slide+=f"| {split} ({len(p['speakers'])}) | {p['scored_clips']} / {p['selected_clips']} | {m['macro_f1']:.3f} / {b['macro_f1']:.3f} | {m['balanced_accuracy']:.3f} / {b['balanced_accuracy']:.3f} |\n"
    (RESULTS/'MOCK_TABLE.md').write_text('# Exploratory prediction of audio-only listener plurality\n\n'+slide+'\n720 fixed clips, 30 speakers, 4 sentences. Unique-plurality targets; ties excluded. Actor 1001 is test-only. Training is resubstitution; validation selected C; test is held-out. Small subset, no clinical or coaching validation.\n')
    methods=f'''# Exploratory human-perceived emotional delivery — 31 October 2026

## Question and evidence boundary

Do 88 eGeMAPSv02 acoustic functionals predict independently collected audio-only
human emotion judgements on unseen CREMA-D speakers? Intended filename labels
are retained as stimulus metadata and never used as fitting/evaluation targets.
This is a limited subset experiment, not a full-dataset benchmark or evidence of
communication quality, internal emotion, clinical competence or VR learning benefit.

## Data and selection

Official upstream revision: `{CREMA_REV}`. `tabulatedVotes.csv` has 22,326 rows:
7,442 each for voice, face and multimodal judgements. Only queryType 1 is used.
The row identifier is `100000 * queryType + clipNum`, confirmed in upstream
`summarizeVotes.r`. All 7,442 voice distributions were checked for integer count
sums, agreement and complete winner sets against both `emoVote` and summary
`VoiceVote`; no face/multimodal labels are substituted.

Selection is fixed before downloading or fitting: SHA-256 order of actor IDs
using seed `{SEED}` after metadata-only eligibility screening; first 20 other actors train, next 5 validation, next 4 plus
1001 test. Each speaker contributes IEO, TIE, IOM and IWW in six intended
expressions: 720 recordings total. IEO uses medium intensity except neutral XX;
the other statements use XX. This bounds runtime/download cost and includes all
five original demo files. It does not establish unseen-sentence or corpus-wide
generalisation. Same sentences appear across splits; speakers never overlap.
`plan.json` is written before extraction and fitting and contains the full selection.
Actor 1002 is ineligible because a prespecified TIE-neutral filename is absent;
1064 is excluded before extraction because upstream documents its IEO_DIS_MD
presentation as anomalous (a one-minute all-expression recording). The remaining
89 speakers are eligible; none is selected/excluded based on votes or performance.
Vote distributions, WAV hashes/URLs, channel counts and extractor warnings are
in `manifest.json`. The original WAVs are not modified.

## Target, ties and disagreement

The target is the unique **plurality**, not necessarily >50% majority, of the six
audio-only vote counts A/D/F/H/N/S. All ties and zero-vote clips are excluded from
fitting, hyperparameter selection and single-label metrics, but retained in the
manifest, predictions and demo. No tie-breaking chooses an arbitrary human label.
Distributions, denominators, tied winners and largest vote fraction remain visible.
Collapsing non-tied distributions still loses disagreement; these are noisy,
finite-sample judgements from listeners, not a speaker's true emotional state.
Audio-only study participants heard the upstream MP3 presentation; measurements
use corresponding original WAVs matched by stem. Codec effects were not evaluated.

## Features, model and leakage controls

Reuses `analyze.extract` (openSMILE {version('opensmile')}) and selects only its 88
eGeMAPSv02 functionals. No actor ID, filename, intended emotion, transcript count,
human rating statistic, silence ratio or target-derived feature enters X. Audio
channels are averaged as in the existing extractor; no resampling/normalisation.
Median imputation and standard scaling are fit on non-tied training rows only.
The model is L2 logistic regression, lbfgs, class_weight=balanced, max_iter=5000.
C grid {CS}; choose highest validation macro-F1, keep smaller C for an exact tie.
Selected C = {results['selected_C']}. No refit on validation data. Actor 1001 and
all other test speakers remain absent from imputation/scaling/fitting/selection.
Test evaluation is performed after selection. Baseline is the most frequent
training target ({NAMES[results['majority_training_class']]}), fixed for all splits.
Standardised coefficients and fitted preprocessing arrays are exported for audit;
correlated predictors/regularisation prevent causal coaching interpretations.
Model probabilities are uncalibrated class probabilities, not validated confidence
in communication quality. No probability calibration or causal analysis was done.

## Results

{concise}
Training values are resubstitution, not generalisation. Validation values are used
for model selection and therefore optimistic as an independent performance claim.
Test values concern only these five unseen speakers; no confidence interval or
population-level performance claim is provided. All results/failures are retained.
Training macro-F1 ({results['partitions']['train']['model']['macro_f1']:.3f}) is much higher than test macro-F1
({results['partitions']['test']['model']['macro_f1']:.3f}), consistent with overfitting and sensitivity to new speakers.
Macro-F1 uses all six fixed classes with undefined precision/recall set to zero;
balanced accuracy is mean recall over classes present in that split. Per-class
support below makes the denominator auditable. Confusion rows are human target,
columns are predicted labels, ordered A, D, F, H, N, S. Ties are never scored.
'''
    for split,p in results['partitions'].items():
        methods+=f"\n### {split}\n\nSpeakers: {', '.join(p['speakers'])}. Selected {p['selected_clips']}; scored {p['scored_clips']}; excluded ties {p['excluded_ties']}; zero votes {p['excluded_zero_votes']}.\n\nHuman target class counts: `{json.dumps(p['model']['class_counts'])}`.\n"
        for name,key in [('Logistic regression','model'),('Majority baseline','majority_baseline')]:
            methods+=f'\n{name} confusion matrix:\n\n| Human / predicted | A | D | F | H | N | S |\n|---|---:|---:|---:|---:|---:|---:|\n'
            for label,values in zip(LABELS,p[key]['confusion_matrix']):
                methods+='| '+label+' | '+' | '.join(map(str,values))+' |\n'
    methods+='\n## Original five demonstration recordings — all held out\n\n| Filename | Intended | Audio-only votes A/D/F/H/N/S | Human plurality | Model | Scored? |\n|---|---|---|---|---|---|\n'
    for file,r in results['demo_clips'].items():
        h=r['human'];methods+=f"| {file} | {r['intended_label']} | {' / '.join(str(h['counts'][k]) for k in LABELS)} (n={h['total']}) | {':'.join(h['winners'])} | {r['prediction']} | {'yes' if r['included_in_single_label_scoring'] else 'no, tied'} |\n"
    demo_scored=[r for r in results['demo_clips'].values() if r['human']['target']]
    methods+=f"\nOn these original five clips, the model matches {sum(r['correct'] for r in demo_scored)}/{len(demo_scored)} non-tied listener pluralities; the majority baseline matches {sum(r['baseline_prediction']==r['human']['target'] for r in demo_scored)}/{len(demo_scored)}. The tied angry clip is excluded. All five were retained, including failures; the demo subset is not representative of the overall test result.\n"
    methods+='''
## Reproduction and limits

From this directory with the locked dependencies installed:

```sh
python study.py --download   # pinned sources + 720 WAVs, extract, fit, report
python study.py --fit-only   # offline refit from committed derived features/votes
python -m unittest test_study -v
python build.py             # attaches study_results/results.json if present
python launch.py
```

`features.csv` and `manifest.json` enable model-only reproduction without corpus
downloads. `results.json` records input hashes and package versions; source hashes
are pinned in study.py. Cached extraction is reused only for the same audio hash
and openSMILE version and extractor source hash. No unsafe pickled model is needed. Exact numerical replay
depends on the recorded dependencies/platform. No test-derived model revisions
or favourable-example selection were performed after this run.

Limits: small prespecified subset, few test speakers, shared sentences, deliberate
intensity selection, acted recordings, noisy finite listener votes and discarded
ties in the primary metric. Neutral judgements can dominate despite balanced
intended stimuli; class-balanced training mitigates but does not remove imbalance.
No speaker-demographic stratification, unseen-sentence test, cross-corpus test,
probability calibration, prospective human study or clinical/paediatric validation.
Disagreement is a result to inspect, not an annotation error to silently correct.

## Sources / redistribution

- Cao et al. (2014), CREMA-D: https://doi.org/10.1109/TAFFC.2014.2336244
- Official data: https://github.com/CheyneyComputerScience/CREMA-D
- Pinned modality mapping: https://github.com/CheyneyComputerScience/CREMA-D/blob/1658cd342dff90010aa843eaeebd53610a08b1dc/summarizeVotes.r
- Pin/hash/URLs for both vote tables and each WAV are in manifest.json.
- Derived vote/feature tables retain ODbL 1.0 database / DbCL 1.0 contents terms;
  see DATA_LICENSE.md. No raw audio, full corpus or participant IDs are committed.
'''
    (RESULTS/'METHODS.md').write_text(methods)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download',action='store_true')
    parser.add_argument('--fit-only',action='store_true')
    args=parser.parse_args()
    if not args.fit_only:
        prepare(args.download)
    fit()

if __name__=='__main__':
    main()
