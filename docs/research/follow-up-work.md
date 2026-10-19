# Follow-up work completed for Charlie's interim contribution

19 October 2026. This extends the existing review branch/PR; it is not a new deployment or a new efficacy study.

## Completed

1. **Independent measurement diagnostic.** Re-extracted low-level F0 on 12 purposefully selected original recordings, compared Praat with openSMILE at two Praat pitch settings, recorded source hashes and instrument checks, and visually inspected all three private waveform/spectrogram sheets. [Results and interpretation](../results/pitch-quality-review.md). The comparison exposed tracker/parameter sensitivity; no annotations, demo results or source recordings were repaired/replaced.
2. **Concrete data-access decision.** Read the actual SLUSI release README and access requirements; downloaded and inspected the small official CPC1 evaluation-label archive, schema and included terms. Caught a landing-page/archive licence discrepancy. [Decision and remaining gates](dataset-decision.md). No multi-GB audio download or new model fitting.
3. **Executable proposed pilot allocation.** Expanded the protocol with speakers/listeners, materials, channel, listening, scoring, exclusions, ethics and progression gates. Generated 288 hypothetical assignments with no repeated text per listener and balanced style/speaker exposure. [Protocol](../methodology/listener-validation.md). No people recruited and no responses/results fabricated.
4. **Method justification.** Added implementation alternatives and required context/ASR baselines. [Comparison](../methodology/method-selection.md). The choice is conditional, not an observed performance ranking.
5. **Meeting preparation.** Added a decision sheet and answers to likely evidence/validity questions. [Meeting sheet](supervisor-decisions.md). Corrected the report's dataset-access status and linked these appendices; retained the group word-budget checks and Kang Zhe's author-owned contribution boundary.

## Still requires people, access or later experiments

- NUS/LDC access and scored-excerpt joins for SLUSI; or a scoped decision to use Clarity, whose audio join remains unverified.
- Trained human pitch/boundary review; no second annotator or validated perceptual pause/rate/formant measurement is claimed.
- Supervisor-approved task/population, institutional consent/ethics route and eventual confirmatory sample-size rationale.
- Current deployed system architecture evidence from its owner. No claim that it is transcript-only.
- Kang Zhe's substantive Part B evidence, group slides, actual timed rehearsal and course calendar dates.
- Direct validation of speaker-side recognition prediction and feedback benefit. These remain future research.

## Verification and preservation

See [follow-up validation record](../results/follow-up-validation.md) for checks and operational status. Public outputs contain derived diagnostics, provenance, protocol/design material and code. Raw audio, annotations, label rows, archives, environments and private review sheets remain outside Git. No source under `sources/` was edited. The live main-branch report awaits the existing PR review.
