# PVC v0.1 — acoustic evidence and supervised modelling scaffold

**Perceived Vocal Confidence (PVC) is the degree to which a listener judges, from a speaker's vocal delivery, that the speaker sounds certain and committed to what they are saying.** It is not internal confidence, correctness, expertise or general speaking quality. Read the [definition, rating anchors and academic references](../../docs/pvc_definition_v0_1.md).

Working now: local WAV → 88 openSMILE eGeMAPSv02 functionals + transparent temporal measurements → JSON/CSV/terminal summary. A separate training/prediction pipeline implements mean, Ridge and Random Forest regression. **No real PVC model has been trained; no confidence score is fabricated.** Tests use explicitly synthetic fixtures to verify mechanics only.

Also working: an **external perceived-reading-confidence benchmark** trained on 600 genuinely labelled children's reading recordings, with original Low/Medium/High classes. This separate classifier does not validate adult/domain-specific PVC or convert labels to 1–5. Read the [provenance and evaluation limits](../../docs/reading_confidence_benchmark.md), [aggregate results](results/reading_confidence/README.md), and [microphone/WAV demo instructions](../../docs/live_confidence_demo.md). Raw data, per-recording derived tables and models stay local; model files are not downloaded automatically.

```sh
# From the repository root, on the prepared Mac:
prototype/pvc/.venv/bin/python prototype/pvc/live_demo.py --record
prototype/pvc/.venv/bin/python prototype/pvc/live_demo.py "/absolute/path/to/my_recording.wav"
```

The default demo model is logistic regression, chosen before evaluating performance. Existing PVC extraction, regression training, sensitivity results and listener-rating tools remain separate.

## macOS installation

From the repository root, with Python 3.11+ installed (tested with Python 3.12.7 on Apple Silicon):

```sh
cd prototype/pvc
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest -v
```

`requirements-lock.txt` records the exact environment used for the demonstration. Use `python -m pip install -r requirements-lock.txt` to reproduce it on a compatible platform; use the bounded requirements file for other supported macOS/Python versions. openSMILE wheels include the native extractor. Check [openSMILE licensing](https://github.com/audeering/opensmile#license) before use outside research/education.

## Supervisor demo (prepared Mac)

From the repository root, one command:

```sh
prototype/pvc/.venv/bin/python prototype/pvc/demo.py "$HOME/Downloads/20260121_150424_AI_Sample/20260121_143844_AI_Before/Team Leader.wav"
```

It prints only the meeting-relevant subset and explicitly states: **These are candidate predictors of PVC, not a validated confidence score.** The complete JSON/CSV and a `.summary.txt` save under Git-ignored `prototype/pvc/private/demo/`. Optional `--transcript "..."` or `--transcript-file verbatim.txt` supplies word-rate/filler fields. `--sample-id` and `--output` distinguish additional recordings; repeated IDs replace prior demo exports. This wrapper reuses the existing extractor without changing it.

## Collect human ratings

[Local rating tool and protocol](annotation/README.md): `python3 prototype/pvc/annotation/serve.py --clips "/absolute/path/to/approved_clips"` from the repository root, then open http://127.0.0.1:8765. It saves each listener's responses locally and exports CSV; raters never see acoustic features. Prepare approved single-speaker clips first. No human ratings are included. Research choices and open questions are in the [living decision log](../../docs/pvc_decision_log.md).

## Reproduce temporal sensitivity

From the repository root on this Mac:

```sh
prototype/pvc/.venv/bin/python prototype/pvc/sensitivity.py
```

Defaults to the two supplied Team Leader WAVs in Downloads and five gates from −55 to −35 dBFS. Override with `--sample-root`, or `--before /path/before.wav --after /path/after.wav`; use `--thresholds -55 -45 -35` and `--output /path/results` if needed. It reuses the same temporal function and writes `temporal_sensitivity.csv`, metadata/source hashes and a [short interpretation](results/temporal_sensitivity.md). No normalization or VAD is applied. Activity and pause counts can change drastically with the gate; these are not validated speech/hesitation measurements.

## Extract evidence

```sh
python analyze.py sample.wav --transcript "Um, I think we should start." --output results/
python analyze.py sample.wav --transcript-file verbatim.txt --previous-turn-end 10.2 --response-start 10.8 --output results/
```

The WAV must contain the target analysis unit. Transcript text must correspond exactly to that audio. Timestamp arguments are seconds on the **same conversation clock**, not relative to two separately trimmed clips. Both are required together; negative latency is preserved as overlap. Existing sample `timestamps.json` needs reviewed turn/speaker pairing before use; it is not accepted blindly as an onset annotation.

To repeat the real demonstration on this Mac:

```sh
python analyze.py "$HOME/Downloads/20260121_150424_AI_Sample/20260121_143844_AI_Before/Team Leader.wav" --sample-id paediatrics_before_team_leader --output results/
python analyze.py "$HOME/Downloads/20260121_150424_AI_Sample/20260121_150424_AI_After/Team Leader.wav" --sample-id paediatrics_after_team_leader --output results/
```

Each run writes `<sample-id>.json` and `<sample-id>.csv`, replacing outputs with that ID. Use distinct IDs for different clips. JSON contains provenance (audio SHA-256, sample rate, channel count, extractor version/settings), all features, warnings and `pvc_score: null`. CSV contains one row with the same numeric features plus sample ID; it deliberately has no ground-truth label column. No raw waveform or transcript is exported. A smaller pitch/loudness/voice-quality subset is printed, alongside temporal measurements. These are candidate predictors motivated by the literature, not indicators with predetermined good/bad directions.

## What temporal fields mean

- `audio_duration_s`: total file duration, including leading/trailing silence and other-speaker waiting time.
- `energy_activity_ratio`: fraction of samples in non-overlapping 20 ms RMS frames above −35 dBFS. **Unvalidated energy-based speech-activity approximation, not VAD, speech recognition or voiced detection.** `energy_silence_ratio` is its complement, including boundary silence and gaps shorter than the pause threshold. Partial final frames are weighted by actual length.
- `pause_count`, `mean_pause_duration_s`, `max_pause_duration_s`: internal consecutive below-threshold runs of at least 0.2 s, excluding leading/trailing silence. Zero mean/max means no qualifying gap. May include noise gating or time when another person speaks; not necessarily hesitation.
- `rms_mean`, `rms_std`, `rms_range`: statistics of frame RMS in full-scale amplitude units; not calibrated physical loudness. eGeMAPS loudness and F0 retain native feature names/units. F0 fields are semitones relative to 27.5 Hz; `stddevNorm` is normalised SD, not Hz. Percentile range is not an absolute min–max range.
- Optional `word_count`, `words_per_minute`: regex-based word count and words / whole-file minutes, including fillers. English-like tokenisation is limited; not syllables/s, articulation rate or within-speech WPM. Missing transcript gives null, not zero.
- Optional `filled_pause_count`: literal case-insensitive um/uh/erm/hmm tokens only. ASR/cleaning may remove them. `immediate_token_repeat_count` counts adjacent identical tokens, not verified disfluencies. False starts are not detected.
- Optional `response_latency_s`: supplied response onset minus prior turn end. Missing context gives null.

Use `--energy-threshold-db -40 --min-pause 0.3` for a **sensitivity check**, not tuning against held-out labels. Keep preprocessing fixed across training and prediction and record it in the dataset manifest. Features alone cannot detect inconsistent extraction settings across imported CSV rows. For PVC training, first agree on short single-speaker units and manually check segmentation. The 8.6-minute session examples establish software operation only.

## Train once independent human ratings exist

CSV input mode 1: `audio_filename,pvc_score,speaker_id`, optionally `transcript,previous_turn_end_s,response_start_s`. Relative audio paths resolve against the CSV directory. Do not create `pvc_score` from guessed weights or an LLM.

Mode 2: combine extracted CSV rows, then join independently collected, aggregated listener ratings as `pvc_score` and verified `speaker_id`. The script uses only recognised feature names, excluding metadata, identity and targets. Do **not** keep `audio_filename` in a pre-extracted dataset: its presence explicitly selects re-extraction mode with default settings.

```sh
python train.py private/labelled_clips.csv --folds 5 --output models/
python predict.py models/ridge.joblib results/paediatrics_before_team_leader.json
# Or, for acoustic-only input:
python predict.py models/ridge.joblib approved_single_speaker_clip.wav
```

These commands require a real labelled dataset/model which is intentionally not shipped. The training and prediction CLI paths are exercised with temporary synthetic fixtures by the tests; their scores are not research findings. All three models are saved; inspect `models/evaluation.json` and `models/out_of_fold_predictions.csv` before deciding which model to use. Never load untrusted joblib files.

The script uses speaker-grouped cross-validation when all IDs exist. Incomplete IDs or a single speaker cause an error. With no ID column it prints and saves a prominent warning and uses shuffled row folds; this cannot establish unseen-speaker validity. A role such as “Team Leader” is not a speaker identity. Repeated/overlapping clips and shared sessions also need leakage control in a study protocol.

Median imputation and scaling fit inside each training fold. All-missing training columns are filled with zero by the imputer; missing counts are reported. Optional features missing at prediction time are imputed, so match annotation availability between training and deployment. Hyperparameters are fixed: Ridge alpha 10; Random Forest 200 trees, depth ≤5, minimum leaf 2. No tuning or deep network. Models report pooled and per-fold MAE/Spearman; undefined Spearman is null. A mean baseline has constant predictions within a fold; pooled correlations across differing fold means can be misleading. Final models are refit on all labelled rows after out-of-fold evaluation. Predictions are **unclipped** and flagged outside 1–5.

Interpretation: standardized Ridge coefficients (per training SD) and intercept; forest impurity importance plus held-out permutation MAE increase. Coefficients/importance do not establish causality, and correlated features can obscure importance. Small datasets and 88+ predictors require strong caution; the script's four-row technical minimum is not an adequate study sample size.

## Human reference and audio-LLM comparison

```text
human listeners -> PVC ground truth
 audio -> openSMILE/eGeMAPS + temporal features -> model -> predicted PVC
 same audio -> audio LLM -> predicted PVC
 compare both predictions with human ground truth
```

Use the same clips/definition for raters and models, blind raters to predictions, and pre-specify aggregation and agreement checks. Compare both pathways on held-out speakers, with MAE/Spearman and an appropriate reliability/ordinal-agreement analysis. Keep self-report and clinical correctness separate. See the [official-docs-verified audio-LLM template](audio_llm_benchmark.md); it has not been executed and uploads nothing automatically.

## Evidence and limitations

See [demonstration record](results/README.md). No valid human PVC labels were identified in the inspected sample JSON; the supplied teamwork assessments are a different construct. No external labelled dataset was integrated. Timing is unvalidated, recordings can contain overlap/background sounds, roles are not confirmed identities, transcripts can omit disfluencies, and whole-file F0 summaries hide contours. Boundary/threshold choices and recording gain affect results. Next work: expert review of construct and anchors, consented single-speaker clip selection, multiple independent listener ratings, manual measurement checks and speaker-held-out validation. Kang Zhe's feedback/debriefing evaluation remains a separate workstream.
