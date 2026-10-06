# PVC progress summary and self-audit

Audit date: 6 October 2026. Implementation reviewed: `bc0ac37` and `89627fd`. This is a progress assessment, not a claim of supervisor approval or a predicted grade. The weekly expectation, as clarified by Charlie, is to define confidence properly in a measurable way and have a prototype ready.

## What the project is trying to do

Within the paediatric VR training project, Charlie's work investigates whether recorded speech can support an interpretable assessment of **perceived vocal confidence (PVC)**. The intended use is evidence for reflection and debriefing, with usefulness still to be tested. Kang Zhe's data-presentation workstream remains separate.

The working definition is:

> Perceived Vocal Confidence (PVC) is the degree to which a listener judges, from a speaker's vocal delivery, that the speaker sounds certain and committed to what they are saying.

This deliberately targets the listener's impression. Someone can sound assured while being incorrect, or sound tentative while being competent. Audio alone does not establish internal confidence, clinical correctness, expertise, anxiety, personality or overall communication quality.

**What makes this measurable:** independent listeners hear the same defined audio segment and answer a fixed question on an anchored 1–5 scale. Their individual ratings are retained; an aggregate, provisionally the mean, becomes the prediction target after coverage and agreement checks. Acoustic measurements are the inputs, not the definition:

`audio → measured features → learned model → predicted listener rating`

`independent listeners → ratings → agreement checks → reference target`

Individual ratings are ordinal. Treating their mean as approximately continuous is a modelling choice. This is an operational definition v0.1, not yet an established measurement instrument. Defining the clip unit, resolving the combined “neutral or unclear” midpoint, agreeing the listener population and demonstrating reliability remain part of defining PVC properly. Agreement would establish consistency, not by itself prove construct validity. Content, accent and listener expectations may still influence ratings despite the instructions.

## What has been built

| Component | Working capability | Evidence boundary |
| --- | --- | --- |
| Definition and decision history | Definition v0.1, literature-linked cue families, exclusions, human-rating formulation and reasons for modelling choices | Expert consultation and empirical refinement remain pending |
| Feature extractor | WAV input; all 88 eGeMAPSv02 functionals; duration, energy activity/silence and gap metrics; optional transcript counts and response latency | Energy gating is not validated speech detection; no automatic PVC score |
| Training/prediction scaffold | Mean baseline, Ridge and Random Forest; MAE/Spearman; coefficients/importances; speaker-grouped validation when IDs are supplied | Software is implemented, but no real labelled PVC model has been trained or evaluated |
| Local rating interface | One clip at a time; exact question, 1–5 anchors and reminder; no acoustic features; notes; save/resume/export | Collects ratings; does not establish reliability automatically |
| Sensitivity experiment | Five fixed energy gates on the existing Before/After demonstration recordings; CSV, settings/hashes and interpretation | Tests robustness to a setting, not speech-detection accuracy or confidence change |
| Meeting command | Short duration, activity, gap, pitch, loudness and voice-quality summary; transcript measures when supplied | Full 88 features remain in JSON/CSV; explicit warning that these are candidate predictors |
| Audio-LLM benchmark plan | Separate prompt/template using the same PVC definition | No benchmark scores have been obtained; an LLM is not ground truth |

The real demonstration used the two Team Leader WAVs, about 513.34 and 463.06 seconds long. These prove that real recordings can be processed end-to-end. They are session-length role recordings, not validated single-speaker rating units. No human ratings, arbitrary confidence weights, trained research model or confidence-improvement result was invented. Transcript measures remain absent for these examples rather than being guessed from cleaned text.

## The main experimental finding

Changing only the gate produced the following endpoints; the complete five-gate table is in [the sensitivity report](../prototype/pvc/results/temporal_sensitivity.md).

| Recording | Gate | Energy-active | Below-gate | Internal gaps ≥0.2 s | Mean gap | Longest gap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Before | −55 dBFS | 67.03% | 32.97% | 164 | 0.815 s | 7.24 s |
| Before | −35 dBFS | 35.61% | 64.39% | 188 | 1.443 s | 17.88 s |
| After | −55 dBFS | 43.18% | 56.82% | 297 | 0.668 s | 10.62 s |
| After | −35 dBFS | 0.03% | 99.97% | 4 | 68.460 s | 129.02 s |

The quieter After file is particularly sensitive. The default −35 dBFS gate classifies almost all of it as below threshold. This does **not** mean that the participant hardly spoke or was less confident. Lowering the gate admits both quiet speech and noise; without manually labelled intervals, no gate can be called accurate. Waiting time between turns also cannot be interpreted as within-turn hesitation.

The next defensible improvement is to mark representative speech/non-speech intervals manually and compare a dedicated VAD against them. Normalisation is a possible controlled comparison, but also raises noise and changes energy measurements. Original audio should remain available for loudness/voice-quality predictors. No optional VAD or model download was added merely to expand the prototype.

## Audit against the requests

Both implementation prompts are substantially fulfilled: the construct, extractor, modelling scaffold, real-audio examples, documentation, annotation interface, sensitivity analysis, meeting summary and decision log exist. The implementation was committed and pushed to main. The core extractor was reused, and the annotation server uses Python's standard library.

Verification in this audit:

- All 10 automated tests passed.
- A fresh sensitivity run exactly reproduced the committed table and metadata.
- A fresh Before demonstration reproduced the saved features and source hash.
- Both demonstration JSON/CSV pairs agreed across all 102 numeric feature fields, including the 88 acoustic features. PVC scores remain null.
- Working-tree and whitespace checks passed before this audit document was added. No WAVs or model files are tracked.

Earlier UI verification exercised playback, saving, next clip, unrateable responses and restart/resume with synthetic fixtures only. The CSV endpoint and saved file agreed, including quotes, Unicode and multiline notes. Browser-automated downloading failed, so a successful browser download is **not** claimed; the on-disk export remains usable. Synthetic UI scores are not research ratings.

**Confirmed weakness to fix before research collection:** the annotation server hashes clips at startup. Replacing a WAV while the server remains running can produce a saved row with the old hash even though the served audio changed. This was reproduced using a disposable synthetic file. The documented unchanged-clip-set rule mitigates it operationally, and restart detects mismatches with existing ratings, but the code does not enforce immutability during a session. Freeze the study clip set and add a hash-change rejection at playback/save before relying on hash provenance. This audit records the finding; it does not claim it was fixed.

**Remaining study safeguards:** prepare neutral-named, approved single-speaker clips and verified speaker/session metadata. The UI requires playback to start, not complete listening. Speaker grouping needs complete IDs; without them the scaffold warns and falls back to row-wise validation, which is unsuitable evidence of generalisation to new speakers. Session separation and consistent extraction settings need an explicit study protocol.

**Reporting cleanup:** the website still refers to an older “condition A” in its provisional baseline description. Align this with the narrowed PVC comparison and surface the new annotation/sensitivity outputs before formal submission. The deployed source pipeline itself remains to be confirmed; novelty must be argued from verified differences, not inferred from intermediate files.

## Are we meeting this week's expectation?

**Substantially yes, as a discussion-ready definition and working prototype.** We can explain what PVC is, distinguish it from neighbouring constructs, show how humans would measure it and demonstrate extraction from real audio. We can also show an actual robustness problem instead of pretending every number is meaningful.

The incomplete part is the empirical measurement argument: we have not shown that listeners interpret the definition consistently, that the proposed clip unit works, or that acoustic predictors recover their ratings. The appropriate meeting claim is “operational definition v0.1 plus a working measurement and annotation prototype,” not “validated confidence detector.”

## Fit with the wider CDE4301 project

The supplied AY2026 interim assessment brief asks for refined research scope/hypotheses, a research design/protocol, preliminary tests and analysis, novelty/value, and a viable project plan. Its A1–A6 criteria cover scope/context, methodology, prototype, testing, analysis and problems/planning. Against those expectations:

| Area | Current evidence | What is still needed |
| --- | --- | --- |
| Scope and context | A bounded listener-perception target and explicit exclusions | Confirm relevance to paediatric debriefing and the precise gap against existing work |
| Methodology | Human target, baseline/Ridge/Forest comparison and separate audio-LLM benchmark | Freeze questions, clip/rater protocol, sampling and speaker/session split design |
| Prototype | Working extraction, annotation and demo tools | Demonstrate the complete path with genuine ratings |
| Testing and analysis | Software checks and reproducible threshold sensitivity | Listener agreement, temporal measurement accuracy and held-out prediction results |
| Plan and limitations | Concrete limitations and staged next steps | Agreed owners, recruitment/data access and dated milestones |

The direction is coherent, but a calendar-based “on schedule” claim cannot be established without agreed project dates and access to raters/data. The brief specifies a Week 12 presentation and end-of-Week-13 online report; applicable individual/group arrangements should be confirmed. Software tests alone do not satisfy the research-testing requirement. Presentation skill, meeting participation and individual understanding cannot be audited from repository files.

The next three milestones should be evidence-producing:

1. **Agree and freeze the measurement protocol with the supervisor/speech expert.** Resolve the definition, midpoint, clip boundaries, listener population, missing-rating policy and aggregation/agreement approach. Record accepted choices or changes as v0.2.
2. **Run a small real rating and timing pilot.** Freeze approved clips, verify metadata, address the hash issue, collect independent ratings and manually mark representative speech intervals. Inspect disagreement before scaling collection. Decide whether the protocol and temporal measurements need revision.
3. **Evaluate prediction only after usable labels exist.** Compare the mean baseline, Ridge and Forest on held-out speakers/sessions with uncertainty and leakage checks; use the same clips for an audio-LLM benchmark if approved. Then assess whether the resulting evidence helps debriefing. Set dates for these milestones with the supervisor.

More interface polish is not the current bottleneck. Reliable labels, defensible measurement and a tractable evaluation design are.

## What to demonstrate and say

From the repository root, with the existing environment:

```sh
prototype/pvc/.venv/bin/python prototype/pvc/demo.py "$HOME/Downloads/20260121_150424_AI_Sample/20260121_143844_AI_Before/Team Leader.wav"
```

Annotation instructions: [prototype/pvc/annotation/README.md](../prototype/pvc/annotation/README.md). Start with `python3 prototype/pvc/annotation/serve.py --clips "/absolute/path/to/approved_clips"` and open `http://127.0.0.1:8765`.

Suggested meeting explanation:

> I have defined the target as perceived vocal confidence: how certain and committed a speaker sounds to listeners. I have a working extractor and a tool for collecting independent 1–5 listener ratings. These are candidate predictors of PVC, not a validated confidence score. The first robustness test shows that pause/activity estimates depend strongly on recording level and threshold. I need to agree the rating protocol, pilot listener agreement and check speech segmentation before training or interpreting a confidence model.

Key artifacts are [the definition](pvc_definition_v0_1.md), [decision log](pvc_decision_log.md), [meeting brief](pvc_meeting_brief.md), [prototype instructions](../prototype/pvc/README.md), annotation files, `demo.py`, `sensitivity.py`, training/prediction scripts, tests and example results. `index.html` contains the narrowed research framing. This audit adds this document only; it does not change the implementation or repair the outstanding findings.

Assessment source: *CDE4301 Innovation & Design Capstone: Interim Assessment*, supplied AY2026 brief and rubrics, pp. 1–6. Weekly expectation: Charlie's clarification in this conversation. No supervisor approval, research ratings or project grade is inferred.

## Follow-up implementation, 6 October 2026

The historical findings above describe the audited commits. A subsequent update adds the [external reading-confidence benchmark](reading_confidence_benchmark.md) and [local live demo](live_confidence_demo.md); it does not supply adult PVC labels or validate that construct. The annotation server now rechecks clip bytes against the startup hash before serving audio and before saving a response, with regression tests for changed/missing files. The website's stale “condition A” reference was replaced with the narrowed PVC comparison. These two implementation findings are addressed; the research gaps in this audit remain.
