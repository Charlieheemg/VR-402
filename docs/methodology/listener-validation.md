# Proposed listener validation and feedback study

**Status: proposal only; no recruitment, ethics approval or intervention result claimed.**

## Decision before recruitment

RQ1 concerns measurement reliability; RQ2 concerns predicting listener word recognition. Prefer an existing dataset if it provides consent-compatible access, a verified audio–target–outcome join, appropriate units of analysis and enough independent speakers. Audit SLUSI first for alignment of scored excerpts to source recordings and speaker IDs; transcription scores and 5-point listener ratings must remain separate. Inspect Clarity if hearing-aid/listener-conditioned prediction is acceptable; it is a domain shift from clinician delivery. R2SPIN supports a small audibility/context benchmark now, but its two speakers cannot support robust speaker-side modelling.

## Proposed hypotheses and gates

- H1: matched instructed styles alter specified timing and F0 descriptors. Edinburgh provides descriptive one-speaker evidence; generalization requires more speakers.
- H2: prespecified speaker-acoustic features improve held-out human-recognition prediction beyond a context-only and an ASR-only baseline. Compare pooled Brier score/calibration and word recognition prediction; require speaker-disjoint evaluation. R2SPIN KWGP is a masking measure, so it does not test H2 directly.
- H3: targeted feedback improves listener recognition while preserving correct words per minute and avoiding unacceptable effort. Future objective only; requires a controlled intervention after H1/H2 quality gates.

## Minimal human protocol if secondary data fail the gate

First agree the target listener population, clinical vocabulary, recording channel and quiet/noise/SNR conditions with the supervisor. Use a small multi-speaker feasibility pilot to estimate ceiling/floor performance and annotation reliability, then justify sample size from clustered uncertainty/power; do not invent an arbitrary statistically sufficient number. Do not recruit until the institution confirms ethics/consent requirements.

Use matched scripts, fixed equipment/gain/distance, original and instructed styles, and preregistered noise mixing. Randomize and counterbalance stimulus assignment so each listener hears at most one version of a sentence; avoid word memorization across A/B repeats. Present once unless repeat listening is an explicitly defined condition. Collect verbatim transcriptions blind to style/model output, score prespecified keywords or words against verified transcripts, and document allowed spelling variants. Collect clarity/ease ratings separately if wanted. Verify headset use and listening environment within practical limits.

Use independent spot annotations of boundaries and pitch tracks before extracting final features. Report boundary disagreement and sensitivity to silence thresholds. Fix a small feature list before seeing test outcomes: validated speech span/rate, internal pauses with explicit acoustic criteria, F0 distribution and defensible spectral measures. Require manual phone/vowel verification before vowel-space features.

Split by speaker; also separate text/listener units where feasible. Fit preprocessing, feature selection and tuning only within training data. Include intercept/context baselines and a frozen ASR-recognition baseline. Compare calibration and Brier/recognition error, report clustered uncertainty at speaker/listener levels, and avoid counting repeated responses as independent speakers. Model participant/item effects when analysis and sample size permit. Keep the final test untouched by design choices.

## Ethics and feedback boundaries

Use informed consent for voice recording/reuse, access controls, retention limits and a withdrawal procedure. Voices can identify people; remove patient identifiers and protect names in filenames. Obtain institutional review advice for clinicians, students and secondary data; public download alone does not settle all permitted uses. Do not upload restricted recordings to external AI services without permission. No scoring of clinical competence or psychological confidence from delivery cues. Explain accent/language/hearing/context effects and avoid turning unfamiliar accents into deficit labels.

Part B may prototype evidence-linked replay, uncertainty labels and specific improvement opportunities using synthetic examples. Test whether users understand the evidence and its limitations, separately from whether speech improves. Integrate only after a documented interface contract and consent/access review; separate consecutive contributions are sufficient at interim.

## Executable feasibility design v0.1 — supervisor approval pending

This section makes the fallback concrete; it does not override the secondary-data access gate in [dataset-decision.md](../research/dataset-decision.md). Counts below are **proposed logistical counts**, not a power calculation, recruitment claim or statistically sufficient validation sample.

| Item | Proposed default / decision |
|---|---|
| Objective | Check recording, allocation, playback, transcription/scoring and ceiling/floor feasibility before an efficacy or predictive study |
| Speakers | 6 consenting adult English-speaking volunteers, one recording session each; no patients, no diagnostic grouping |
| Material | 12 supervisor-approved short non-dosing logistics instructions, each recorded in ordinary and “make this easy for another person to understand” styles: 144 clips |
| Listeners | 24 consenting adult fluent-English listeners, separate from the speakers; report language/hearing self-reports and headset check; do not assume audiometric normality |
| Exposure | 12 scored trials per listener, one per distinct text across all speakers/styles; 6 ordinary and 6 clear-instruction trials, two clips per speaker, one of each style |
| Replication | 288 proposed responses total; each of 144 clips receives two responses. Sparse clip replication supports logistics checks, not stable clip-level intelligibility estimates |
| Listening | Quiet controlled room, same headset/device and comfortable fixed session volume; one playback, no target transcript or style shown; two separate practice sentences not reused in trials |
| Noise | No noise in this first logistics pilot. Quiet can produce a ceiling; if so, design and approve a separate fixed-masker/SNR feasibility stage using different listeners/texts before testing H2. Do not retrospectively select noise to maximise feature effects |
| Recording | Same microphone/interface/room, fixed documented mouth distance and gain; native lossless mono recording, no AGC/denoising if controllable. Record actual settings and channel deviations; preserve originals and checksums |
| Recording order | Counterbalance style block order across speakers; ordinary/clear takes of the same text separated by other items. Keep first complete usable take; log retakes for incorrect words/technical faults before outcome inspection |
| Primary output | Word recognition = prespecified correctly matched target words / target-word count; record raw transcription and numerator/denominator, not just a percentage |
| Secondary output | Separate optional ease rating; recording duration; quality flags. Correct words/minute only after reliable speech-span definition, and never substitute it for recognition |

`python3 scripts/pilot_assignments.py` produces [proposed-pilot-assignments.csv](proposed-pilot-assignments.csv), a deterministic **hypothetical schedule**, containing no names, recordings or outcomes. Test checks confirm each listener has 12 distinct texts and balanced styles/speakers; every clip is assigned twice. Trial ordering is shuffled with recorded fixed seeds. Map consenting participants to IDs only after approval; speaker identity and text must remain available for grouped analysis. Add practice/material IDs and trial exclusions in a private session log rather than invent participant rows here.

### Scoring and exclusion rules to freeze before collection

1. Have the supervisor approve the 12 scripts and a reference word-token list. Check spoken words against the reference before accepting a take; wrong-word takes are logged and re-recorded rather than silently changing the target.
2. Preserve raw listener text. For scoring, lowercase, remove punctuation and standardise a written list of contractions/numerals/spelling variants before seeing responses. Use monotonic word-sequence alignment; count correctly aligned target words once, with insertions not creating extra hits. Repeated words require their corresponding target position. Keep substitutions/deletions/insertions and reference version for audit. Report recognition and WER separately; WER includes insertions and is not simply one minus recognition.
3. Two reviewers independently score all pilot responses blind to style/metric output; report agreement and adjudicate disagreements with an explicit log. No scorer or second reviewer is claimed to exist yet. The scoring workflow is specified, not implemented or validated software.
4. Predefine technical exclusions: missing/corrupt audio, recorded equipment failure or skipped trial. Preserve reasons and denominators. An incorrect/blank attempted transcription is an outcome, not a reason for exclusion. Log dropout/failed headset checks; do not remove speakers because they weaken an effect.
5. Use a calibration clip and fixed device volume; log playback completion and response timing. Level settings are not calibrated SPL unless measured. Reject time stretching, pitch shifting and uncontrolled loudness normalisation; any future noise mix must record masker provenance, active-speech RMS definition, SNR and checksums.

### Pilot decision gate and subsequent validation

Report completeness, playback faults, retake/exclusion reasons, scorer disagreement, word-recognition distributions by condition/speaker, and evidence of ceiling/floor. Do not use the 288 proposed rows as 288 independent people. No efficacy p-value, model selection or clinical performance claim is planned from this sparse feasibility sample. A ceiling in quiet is useful feasibility information, not permission to invent a noise benefit.

For RQ2, obtain a larger speaker-diverse labelled source or justify a new study using speaker/listener/item variability and a prespecified precision/power simulation. Predefine outcome/feature list, held-out speakers, baseline comparisons and clustered uncertainty before the final test. Candidate features currently remain span and F0 descriptors with quality flags; pause/rate features require boundary review. Exclude unvalidated vowels/formants. Use intercept/context and frozen ASR baselines before acoustic increments. Record corpus-specific language/listener/channel limits. The six-speaker pilot is not a substitute for that evaluation.

Supervisor decisions: approve target population/task and material, consent/ethics route, recording/listening setup, need for a noise stage, scoring reviewers and the success criteria for proceeding. Until then this is a reviewable proposal, not a collection-ready approved study.
