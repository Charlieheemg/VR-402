# Reproduction and measurement definitions

Use the existing environment from the repository root. No model binaries or raw datasets are committed.

```sh
# Obtain the Edinburgh deposit separately, with attribution and local-use restrictions.
prototype/pvc/.venv/bin/python prototype/pvc/edinburgh/download.py
# Acquire the pinned R2SPIN table; original data remain local.
mkdir -p prototype/pvc/private/r2spin
curl -fL https://raw.githubusercontent.com/bbc/r2spin/a9893f5ada87be2373c366d666d0c47e08dab138/AllData.csv -o prototype/pvc/private/r2spin/AllData.csv
# Requires the previously generated private reading_benchmark/features.csv too.
prototype/pvc/.venv/bin/python scripts/reproduce_evidence.py
prototype/pvc/.venv/bin/python -m unittest discover -s prototype/pvc -p 'test_*.py'
prototype/pvc/.venv/bin/python -m unittest discover -s prototype/pvc/edinburgh -p 'test_*.py'
prototype/pvc/.venv/bin/python -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/check_report.py
```

For a fresh checkout, install `prototype/pvc/requirements-lock.txt` in a suitable Python environment. The children’s dataset and feature-cache reproduction procedure are in `docs/reading_confidence_benchmark.md`; do not substitute guessed identities. The consolidation independently refits models from the saved 600-row feature table; it does not repeat raw feature extraction on that dataset. R2SPIN and Edinburgh components require their local inputs. If these are absent, analysis fails explicitly rather than fabricating outputs.

## Edinburgh

All 25 sentence IDs × conditions 19/20/21/22/25, fixed MKH800 microphone; one speaker. Whole-file extraction reuses `analyze.extract`, openSMILE 2.6.0, eGeMAPSv02. Parsed long-format hand-corrected TextGrids exclude `__MACOSX`. The original demo remains separate.

Definitions: file duration = samples/sample rate. Pure silence labels are `sil` after removing question marks and surrounding parentheses/spaces. Composite labels such as `sil+k` remain a single phone-like interval; their silence/stop parts cannot be recovered without new annotation. Nonempty non-pure-silence labels define phone-like intervals. Annotated span runs from the first such interval's start to the last one's end. Phone-like duration sums those intervals. Internal silence-labelled duration sums pure-silence intervals entirely within the span. Question-mark and composite counts are exported as quality indicators. These categories are reproducible proxies, **not validated articulation time or pauses**. Segmentation criteria explicitly warn that `sil` can mark unassignable spectrogram gaps.

Paired differences = condition minus plain for the same sentence. Report the median paired difference and direction counts across 25 items. This differs from subtracting condition medians. No inferential population confidence intervals: one speaker and repeated texts do not supply independent speaker replication. F0 range is the 80th–20th percentile eGeMAPS nonzero smoothed F0 range in semitones, not min–max Hz. Whole-file F1/F2 summaries do not define vowel-space area. Phone-aligned formant accuracy and vowel-category coverage remain unvalidated; no such result is published.

## R2SPIN

Source: BBC r2spin at commit `a9893f5ada87be2373c366d666d0c47e08dab138`; DOI 10.21437/Interspeech.2019-1281. `AllData.csv`: 6,400 rows, 16 participants, two re-recorded speakers, eight lists. Outcome `WRR` is binary keyword recognition, not whole-sentence transcription. `Pred` is sentence predictability; `KWGP` is published keyword glimpse proportion (percentage). The source table is not treated as acoustic measurements extracted by this project.

Four fixed logistic comparisons: Pred; Pred+speaker indicator; Pred+KWGP; Pred+speaker indicator+KWGP. StandardScaler and L2 LogisticRegression (`C=1`, `lbfgs`, max_iter=1000), fit inside each training fold. LeaveOneGroupOut on `List` gives eight folds. No tuning or feature selection. Response order, retake flag, participant identity/demographics and outcome are excluded. Every row has one OOF probability. Accuracy uses threshold 0.5. Brier score = mean((probability−binary outcome)²), lower is better. Equal response weighting.

List separation prevents the same list entering train and test; it does **not** establish separation of speakers, listeners or recurring keywords, or eliminate all dependence. Original stimuli deliberately reuse keywords across different contextual sentences. Speaker-identity adjustment is a sensitivity comparison, not a way to infer speaker generalization. Listener differences and keyword reuse preclude treating 6,400 responses as independent participants. No naive row-based confidence intervals reported. The exact original babble timing and SNR conditions govern validity; production in noise is a different experimental manipulation.

## Reading-confidence reproduction

Refit the existing fixed models on saved features using the existing seed-42 recording-level stratified splits; compare pooled balanced accuracy/macro F1 against historical `evaluation.json` to tolerance 1e-10. Saved feature-table hash and environment versions are recorded. The reported result is a reproduction of that evaluation configuration, not verification of speaker independence or a new human annotation study.

Outputs: public aggregate CSVs plus `reproduction.json`; private recording-level measurements, input hashes and listener-level OOF predictions under `prototype/pvc/private/consolidation/`. Scientific figures read only these aggregate outputs. See `scripts/make_figures.py`. The simple conceptual figures are explicitly labelled conceptual.

To regenerate SVGs in an isolated optional plotting environment: install `scripts/requirements-figures.txt`, then run `python scripts/make_figures.py`. The research extraction environment remains unchanged.

## Audit the refinement without retraining

Run `prototype/pvc/.venv/bin/python scripts/audit_refinement.py`. It reparses original annotations and checks unchanged WAV durations, verifies published aggregates against existing measurement/OOF tables, and writes coverage/sensitivity/per-list audit outputs. It calls no estimator fit and does not rerun feature extraction. The two undercovered TextGrids are retained unchanged; the n=23 exclusion is explicitly supplementary, not a correction. See [measurement audit](../results/measurement-audit.md). Actual pitch accuracy, perceptual pauses and articulation-rate validity remain separate, unfinished checks.
