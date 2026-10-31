# Exploratory human-perceived emotional delivery — 31 October 2026

## Question and evidence boundary

Do 88 eGeMAPSv02 acoustic functionals predict independently collected audio-only
human emotion judgements on unseen CREMA-D speakers? Intended filename labels
are retained as stimulus metadata and never used as fitting/evaluation targets.
This is a limited subset experiment, not a full-dataset benchmark or evidence of
communication quality, internal emotion, clinical competence or VR learning benefit.

## Data and selection

Official upstream revision: `1658cd342dff90010aa843eaeebd53610a08b1dc`. `tabulatedVotes.csv` has 22,326 rows:
7,442 each for voice, face and multimodal judgements. Only queryType 1 is used.
The row identifier is `100000 * queryType + clipNum`, confirmed in upstream
`summarizeVotes.r`. All 7,442 voice distributions were checked for integer count
sums, agreement and complete winner sets against both `emoVote` and summary
`VoiceVote`; no face/multimodal labels are substituted.

Selection is fixed before downloading or fitting: SHA-256 order of actor IDs
using seed `vr402-perception-v1` after metadata-only eligibility screening; first 20 other actors train, next 5 validation, next 4 plus
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

Reuses `analyze.extract` (openSMILE 2.6.0) and selects only its 88
eGeMAPSv02 functionals. No actor ID, filename, intended emotion, transcript count,
human rating statistic, silence ratio or target-derived feature enters X. Audio
channels are averaged as in the existing extractor; no resampling/normalisation.
Median imputation and standard scaling are fit on non-tied training rows only.
The model is L2 logistic regression, lbfgs, class_weight=balanced, max_iter=5000.
C grid [0.01, 0.1, 1.0, 10.0]; choose highest validation macro-F1, keep smaller C for an exact tie.
Selected C = 10.0. No refit on validation data. Actor 1001 and
all other test speakers remain absent from imputation/scaling/fitting/selection.
Test evaluation is performed after selection. Baseline is the most frequent
training target (Neutral), fixed for all splits.
Standardised coefficients and fitted preprocessing arrays are exported for audit;
correlated predictors/regularisation prevent causal coaching interpretations.
Model probabilities are uncalibrated class probabilities, not validated confidence
in communication quality. No probability calibration or causal analysis was done.

## Results

| Split | Speakers | Scored / selected | Logistic macro-F1 | Majority macro-F1 | Logistic balanced acc. | Majority balanced acc. |
|---|---:|---:|---:|---:|---:|---:|
| train | 20 | 432 / 480 | 0.886 | 0.110 | 0.953 | 0.167 |
| validation | 5 | 113 / 120 | 0.355 | 0.117 | 0.376 | 0.167 |
| test | 5 | 113 / 120 | 0.367 | 0.117 | 0.395 | 0.167 |

Training values are resubstitution, not generalisation. Validation values are used
for model selection and therefore optimistic as an independent performance claim.
Test values concern only these five unseen speakers; no confidence interval or
population-level performance claim is provided. All results/failures are retained.
Training macro-F1 (0.886) is much higher than test macro-F1
(0.367), consistent with overfitting and sensitivity to new speakers.
Macro-F1 uses all six fixed classes with undefined precision/recall set to zero;
balanced accuracy is mean recall over classes present in that split. Per-class
support below makes the denominator auditable. Confusion rows are human target,
columns are predicted labels, ordered A, D, F, H, N, S. Ties are never scored.

### train

Speakers: 1056, 1026, 1039, 1030, 1020, 1003, 1080, 1059, 1060, 1070, 1044, 1007, 1014, 1033, 1079, 1008, 1038, 1011, 1042, 1058. Selected 480; scored 432; excluded ties 48; zero votes 0.

Human target class counts: `{"A": 78, "D": 44, "F": 43, "H": 30, "N": 212, "S": 25}`.

Logistic regression confusion matrix:

| Human / predicted | A | D | F | H | N | S |
|---|---:|---:|---:|---:|---:|---:|
| A | 75 | 0 | 1 | 0 | 2 | 0 |
| D | 0 | 43 | 0 | 0 | 1 | 0 |
| F | 0 | 0 | 43 | 0 | 0 | 0 |
| H | 0 | 0 | 0 | 30 | 0 | 0 |
| N | 8 | 15 | 13 | 4 | 165 | 7 |
| S | 0 | 0 | 0 | 0 | 0 | 25 |

Majority baseline confusion matrix:

| Human / predicted | A | D | F | H | N | S |
|---|---:|---:|---:|---:|---:|---:|
| A | 0 | 0 | 0 | 0 | 78 | 0 |
| D | 0 | 0 | 0 | 0 | 44 | 0 |
| F | 0 | 0 | 0 | 0 | 43 | 0 |
| H | 0 | 0 | 0 | 0 | 30 | 0 |
| N | 0 | 0 | 0 | 0 | 212 | 0 |
| S | 0 | 0 | 0 | 0 | 25 | 0 |

### validation

Speakers: 1065, 1068, 1012, 1018, 1050. Selected 120; scored 113; excluded ties 7; zero votes 0.

Human target class counts: `{"A": 19, "D": 14, "F": 11, "H": 4, "N": 61, "S": 4}`.

Logistic regression confusion matrix:

| Human / predicted | A | D | F | H | N | S |
|---|---:|---:|---:|---:|---:|---:|
| A | 10 | 3 | 1 | 2 | 3 | 0 |
| D | 1 | 2 | 2 | 0 | 7 | 2 |
| F | 1 | 2 | 4 | 0 | 2 | 2 |
| H | 0 | 1 | 0 | 0 | 3 | 0 |
| N | 2 | 4 | 3 | 3 | 44 | 5 |
| S | 0 | 0 | 0 | 0 | 2 | 2 |

Majority baseline confusion matrix:

| Human / predicted | A | D | F | H | N | S |
|---|---:|---:|---:|---:|---:|---:|
| A | 0 | 0 | 0 | 0 | 19 | 0 |
| D | 0 | 0 | 0 | 0 | 14 | 0 |
| F | 0 | 0 | 0 | 0 | 11 | 0 |
| H | 0 | 0 | 0 | 0 | 4 | 0 |
| N | 0 | 0 | 0 | 0 | 61 | 0 |
| S | 0 | 0 | 0 | 0 | 4 | 0 |

### test

Speakers: 1001, 1063, 1086, 1051, 1074. Selected 120; scored 113; excluded ties 7; zero votes 0.

Human target class counts: `{"A": 19, "D": 10, "F": 13, "H": 7, "N": 61, "S": 3}`.

Logistic regression confusion matrix:

| Human / predicted | A | D | F | H | N | S |
|---|---:|---:|---:|---:|---:|---:|
| A | 6 | 6 | 2 | 2 | 3 | 0 |
| D | 2 | 3 | 0 | 2 | 3 | 0 |
| F | 0 | 3 | 5 | 1 | 3 | 1 |
| H | 2 | 2 | 0 | 1 | 2 | 0 |
| N | 4 | 8 | 3 | 10 | 34 | 2 |
| S | 1 | 0 | 0 | 0 | 0 | 2 |

Majority baseline confusion matrix:

| Human / predicted | A | D | F | H | N | S |
|---|---:|---:|---:|---:|---:|---:|
| A | 0 | 0 | 0 | 0 | 19 | 0 |
| D | 0 | 0 | 0 | 0 | 10 | 0 |
| F | 0 | 0 | 0 | 0 | 13 | 0 |
| H | 0 | 0 | 0 | 0 | 7 | 0 |
| N | 0 | 0 | 0 | 0 | 61 | 0 |
| S | 0 | 0 | 0 | 0 | 3 | 0 |

## Original five demonstration recordings — all held out

| Filename | Intended | Audio-only votes A/D/F/H/N/S | Human plurality | Model | Scored? |
|---|---|---|---|---|---|
| 1001_IEO_ANG_MD.wav | ANG | 5 / 5 / 0 / 0 / 1 / 1 (n=12) | A:D | H | no, tied |
| 1001_IEO_FEA_MD.wav | FEA | 0 / 3 / 5 / 0 / 3 / 0 (n=11) | F | D | yes |
| 1001_IEO_HAP_MD.wav | HAP | 0 / 0 / 0 / 4 / 7 / 0 (n=11) | N | D | yes |
| 1001_IEO_NEU_XX.wav | NEU | 0 / 0 / 0 / 1 / 10 / 0 (n=11) | N | N | yes |
| 1001_IEO_SAD_MD.wav | SAD | 0 / 1 / 1 / 0 / 8 / 0 (n=10) | N | N | yes |

On these original five clips, the model matches 2/4 non-tied listener pluralities; the majority baseline matches 3/4. The tied angry clip is excluded. All five were retained, including failures; the demo subset is not representative of the overall test result.

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
