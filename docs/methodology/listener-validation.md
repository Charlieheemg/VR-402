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
