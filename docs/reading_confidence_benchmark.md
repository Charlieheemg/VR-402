# External perceived-reading-confidence benchmark

This is a separate three-class external benchmark, not validated ground truth for adult paediatric PVC v0.1. Original codes remain **−1 = Low, 0 = Medium, 1 = High**. There is no conversion to a PVC 1–5 value.

## Provenance and release verification

Source: [KaminiSabu/ReadingConfidenceDataset](https://github.com/KaminiSabu/ReadingConfidenceDataset), commit `0bf2ea31ff8b5a8ef634084deb0420cbf08948ec`, obtained 6 October 2026. The clone is outside VR-402 at `../external_reading_confidence/`. Raw WAVs are not copied into Git.

The actual release has **600 WAVs and 600 unique matching label rows**, with no missing/extra WAV stems. All files are mono, 16 kHz, PCM 16-bit. Observed durations are 9.708–71.770 s (mean 26.389 s). Counts are:

| Original code | Meaning | Recordings |
| --- | --- | ---: |
| −1 | Low | 196 |
| 0 | Medium | 242 |
| 1 | High | 162 |

**Mapping evidence:** the headerless `ratings.csv` supplies these numeric codes; its three distinct counts uniquely match the named class counts in the README and paper §4. Neither source provides a separate explicit numeric-code legend. This is a cross-check against documented counts, not an assumption that arbitrary integers imply an ordering. The loader rejects changed release counts. The third CSV column is always `T`; its meaning is undocumented and it is not treated as a train/test assignment.

The README describes 155 L2 English learners, grades 5–8, aged 10–14, in Maharashtra, India. Children read story paragraphs of 50–70 words from an Android app, recorded by headset in relatively quiet school rooms. It states that two independent raters judged perceived reading confidence and that released items have agreement, after filtering lexical miscues below 20%. These are source-reported collection details, not independently re-established by our extraction. [Dataset documentation](https://github.com/KaminiSabu/ReadingConfidenceDataset/blob/main/Readme.md)

The accompanying paper identifies the raters as English teachers and the collection as spanning eight schools near Mumbai. From 2,295 rated recordings, 803 had agreement; removing some medium-rated items produced the 600-item set. Selecting agreement cases does not establish high reliability in the full population. The release lacks both individual raters' full responses, so we cannot independently recompute agreement. [Sabu & Rao (2020), §§2, 4](https://www.isca-archive.org/interspeech_2020/sabu20_interspeech.pdf)

## Use conditions and local artifacts

The README grants **non-commercial research use only** and requests citation of Sabu & Rao (2020). No separate LICENSE or explicit redistribution terms for derived rows/models were found. Public availability is not a general open-source/commercial licence. This project keeps raw audio, potentially identifying filenames, row-level features and predictions, fold assignments and trained models local. Only our code, aggregate results and aggregate feature summaries are committed. Do not redistribute the dataset or models or use them commercially without clarifying permission with the authors. The README also retains an email contact for dataset access, despite the current public WAV release; no email was sent.

Citation: Kamini Sabu and Preeti Rao. 2020. *Automatic Prediction of Confidence Level from Children's Oral Reading Recordings*. Interspeech 2020, pp. 3141–3145. DOI: [10.21437/Interspeech.2020-2276](https://doi.org/10.21437/Interspeech.2020-2276).

Local outputs under ignored `prototype/pvc/private/reading_benchmark/`:

- `features.csv`: exact feature/label join, opaque `sample_id`, original source ID/code, audio hash, all 88 eGeMAPSv02 fields and existing additional fields. No invented transcripts or speaker IDs.
- `evidence/`: complete extraction JSONs with null PVC score and cache signatures.
- `provenance.json`: source hashes, commit, formats, counts, settings, warnings and feature-table hash.
- `fold_assignments.csv`, `out_of_fold_predictions.csv`: exact reproducible evaluation membership/results.
- `logistic.joblib`, `random_forest.joblib`: final all-data models for local demonstration. Load only trusted locally trained joblib files.

## Speaker identity and evaluation scope

**Speaker-independent evaluation was not possible from verified release metadata.** There is no documented filename schema or speaker map. First-underscore prefixes have cardinality **154**, whereas the source reports **155** speakers. Filenames use mixed naming styles, and apparent names/initials are not an authoritative identity key. We do not resolve this discrepancy by guessing. The paper describes five-fold evaluation but does not establish speaker-disjoint folds in the inspected method.

Our primary evaluation is **5-fold StratifiedKFold, shuffle=True, seed=42**, over lexicographically sorted source IDs. Each recording is tested once; each fold trains on 480 and tests on 120. Speakers, texts, schools and sessions may overlap. Results are recording-level exploratory estimates, not evidence of generalisation to unseen speakers. They may be optimistic. No separate final held-out test set, hyperparameter search or post-hoc feature selection is used.

The optional `--speaker-map` route accepts a complete, independently verified `sample_id,speaker_id` CSV plus `--speaker-map-source`; it uses StratifiedGroupKFold and checks disjointness. This route is tested with synthetic groups only and is **not** claimed for the released dataset. Requesting an author-verified mapping is the next improvement; do not supply guessed prefixes as verified IDs.

## Predictors, models and leakage controls

Reuse `analyze.extract` unchanged. Retain every standard eGeMAPSv02 functional, plus applicable duration and frame-RMS descriptors. Classifiers use **92 fields: 88 functionals + duration + RMS mean, SD and range**. These additions avoid the fixed gate, but remain sensitive to recording/task conditions; none is declared a validated confidence cue.

The five added fields `energy_activity_ratio`, `energy_silence_ratio`, `pause_count`, `mean_pause_duration_s`, and `max_pause_duration_s` remain in the private table as **exploratory, threshold-sensitive measurements** and are excluded from classifier inputs. Existing eGeMAPS voicing/segment descriptors are retained as standard functionals; retaining them does not validate speech segmentation. Transcript/response-context fields are missing and excluded. Identifiers, labels and the undocumented `T` flag are never predictors. No gain normalisation is applied.

Fixed comparisons:

- Most-frequent-class baseline, fitted on each training fold.
- Multinomial logistic regression: L2 regularisation, `C=1`, `lbfgs`, `max_iter=3000`, balanced class weights. Median imputation and standard scaling inside each training fold.
- Random Forest classifier: 300 trees, minimum leaf size 2, square-root feature subsampling, balanced-subsample class weights, seed 42. Median imputation inside each training fold.

The **logistic model was chosen for the demo before inspecting results**, for simplicity; its displayed probabilities are not calibrated estimates of psychological confidence. Both learned models are refitted on all 600 recordings after out-of-fold evaluation. Performance comes only from held-out fold predictions, not those final fits. Fold SD is descriptive, not a confidence interval accounting for speaker dependence.

See [aggregate results](../prototype/pvc/results/reading_confidence/README.md), `evaluation.json` for fold/class metrics and provenance, `logistic_standardized_coefficients.csv`, and `rf_oof_permutation_importance.csv`. The latter measures held-out macro-F1 change over five shuffles per feature per fold. Correlated predictors can share/mask importance. Neither importance nor coefficients establishes causality or explains why an individual recording was classified that way.

## Comparison with the paper

Sabu & Rao use task-specific prosodic features, including ASR-derived alignment/rates and recording/window summaries. Their agreed-set regression reports Pearson correlation 0.76; their low-versus-rest task reports F1 0.70. Our three-class macro F1 is a different metric/task. Their three-class individual-rater experiment uses the larger 2,295-recording set. Different features, preprocessing, subsets and folds prevent a direct replication or superiority claim. [Paper, Tables 3–5](https://www.isca-archive.org/interspeech_2020/sabu20_interspeech.pdf)

## Reproduce

From the repository root, after the existing extractor environment is installed:

```sh
# Clone once, outside the FYP repository.
git clone https://github.com/KaminiSabu/ReadingConfidenceDataset.git ../external_reading_confidence
git -C ../external_reading_confidence checkout 0bf2ea31ff8b5a8ef634084deb0420cbf08948ec
prototype/pvc/.venv/bin/python prototype/pvc/reading_benchmark.py --dataset ../external_reading_confidence
```

Extraction caches are reused only when audio hashes and extractor/library signatures match. Model evaluation is rerun, with deterministic saved fold membership. Source data is never modified. The existing environment lock records package versions; aggregate metadata records the actual versions used in this run. Keep the same environment for reproduction.

## Relationship to the final PVC study

**External benchmark:** children's reading audio → published confidence labels → our features → three-class classifier → recording-level benchmark performance.

**Final PVC study:** adult/domain-relevant speech → PVC v0.x listener protocol → independent human ratings → our features → PVC model → speaker-disjoint validation and debriefing usefulness evaluation.

This benchmark asks whether our acoustic pipeline can recover an existing human-labelled confidence-related construct under the stated evaluation limitations. It does not validate PVC for paediatric VR, internal confidence, correctness, competence or learning outcomes. The adult listener-rating study remains necessary.

## Observed results and feature patterns (6 October 2026)

Pooled out-of-fold balanced accuracy / macro F1: majority **0.3333 / 0.1916**; logistic **0.7160 / 0.7104**; Random Forest **0.7813 / 0.7849**. These demonstrate label-recovery signal in this recording-level benchmark, subject to possible speaker/text overlap and the agreement-selected sample. They do not establish speaker-independent performance.

The largest RF held-out permutation drops in macro F1 were F0 20–80 percentile range (**0.0258**), recording duration (**0.0253**), loudness falling-slope (**0.0112**), loudness peaks/second (**0.0097**) and voiced segments/second (**0.0091**). Fold/repeat variability is substantial; this is a descriptive ranking, not a stable universal ordering. Duration is **not** speech rate: without word/syllable counts it can reflect paragraph length, reading speed, silence or other task differences. Retained eGeMAPS segmentation descriptors are not validated VAD outputs.

The final logistic model assigns different signs to different pitch and loudness descriptors (e.g. High has a positive F0-range coefficient and negative normalised-F0-SD coefficient). With correlated inputs, such signs are conditional model associations, not general rules about confidence. Full coefficients and permutation summaries are exported rather than selectively presenting only intuitive patterns.
