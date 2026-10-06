# Supervisor meeting: PVC v0.1

**Definition:** Perceived Vocal Confidence (PVC) is the degree to which a listener judges, from a speaker's vocal delivery, that the speaker sounds certain and committed to what they are saying.

**What works:** real paediatric WAV → 88 eGeMAPSv02 acoustic features plus transparent temporal measurements → JSON, CSV and terminal summary. Training and prediction scripts implement mean, Ridge and Random Forest models with speaker-grouped evaluation, MAE/Spearman and interpretable feature information. They await human labels. Software tests cover extraction, modelling, the annotation CSV API, threshold analysis and demo commands; synthetic fixtures are not research results.

**Example:** Before Team Leader recording: 513.344 s, 35.6% activity under a −35 dBFS energy gate, 188 internal low-energy gaps ≥0.2 s, mean gap 1.443 s, maximum 17.88 s. These are not a confidence score. The After recording has lower RMS and extreme threshold sensitivity, so raw before/after timing comparisons are not valid evidence of improved confidence.

**Unvalidated:** listener construct/anchors, rating reliability, single-speaker segmentation, energy-based timing accuracy, predictor relevance and transfer across speakers/recording conditions. No real PVC model has been trained; no audio-LLM benchmark was executed. No claim about correctness, competence or inner confidence follows from these features.

**Next step for a defensible score:** agree the construct and clip unit with a speech expert; select consented single-speaker clips; obtain multiple independent 1–5 listener ratings; quantify agreement and pre-specify aggregation; train and evaluate on held-out speakers. The audio LLM is a comparison against that human reference, never a replacement ground truth. Kang Zhe retains the separate feedback/debriefing presentation workstream.

**Show these:**

1. [Definition, anchors and references](pvc_definition_v0_1.md).
2. [Updated report](../index.html), especially PVC Definition and status sections.
3. [Before JSON](../prototype/pvc/results/paediatrics_before_team_leader.json), [CSV](../prototype/pvc/results/paediatrics_before_team_leader.csv), and [measurement limitations](../prototype/pvc/results/README.md).
4. [README](../prototype/pvc/README.md), [training script](../prototype/pvc/train.py) and [audio-LLM template](../prototype/pvc/audio_llm_benchmark.md).

From the repository root on the prepared Mac:

```sh
prototype/pvc/.venv/bin/python prototype/pvc/demo.py "$HOME/Downloads/20260121_150424_AI_Sample/20260121_143844_AI_Before/Team Leader.wav"
```

The demo prints: **These are candidate predictors of PVC, not a validated confidence score.** Full JSON/CSV and a summary text file save in `prototype/pvc/private/demo/`.

Also show the [human-rating tool and protocol](../prototype/pvc/annotation/README.md), [five-threshold table](../prototype/pvc/results/temporal_sensitivity.md) and [decision log](pvc_decision_log.md). Supervisor wording: “The energy-based pause/activity measurements change markedly with threshold and recording level. I need manual segmentation checks and a VAD comparison before treating them as speech measurements, let alone PVC evidence.”

Annotation command (repository root, after preparing consented single-speaker clips):

```sh
python3 prototype/pvc/annotation/serve.py --clips "/absolute/path/to/approved_clips"
```

Then open http://127.0.0.1:8765. No independent human ratings have yet been collected.

Once real labels exist (run from `prototype/pvc` with its virtual environment active; not a currently runnable meeting demonstration):

```sh
python train.py private/labelled_clips.csv --folds 5 --output models/
python predict.py models/ridge.joblib results/paediatrics_before_team_leader.json
```
