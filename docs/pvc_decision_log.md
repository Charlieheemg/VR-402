# PVC decision log

Living research history. Add dated entries for v0.2, v0.3, etc.; preserve earlier decisions and say what evidence changed them. These are working choices, not validated findings.

## 6 October 2026 — PVC Definition v0.1

| Decision | Reasoning / evidence boundary |
| --- | --- |
| Target **perceived vocal confidence**, not internal confidence | Delivery can be heard and rated. The speaker's internal state requires a different measurement such as self-report; perceived and self-reported certainty can differ [Pon-Barry & Shieber, 2010]. |
| Exclude correctness and competence | An assured delivery can accompany an incorrect answer. Clinical knowledge and performance need separate labels/rubrics, avoiding a claim that vocal assurance establishes expertise. |
| Human listener judgement defines the target | PVC concerns how speech sounds to listeners. Independent ratings operationalise that perception; their agreement and disagreement must be measured. An aggregate is a fallible reference, not psychological truth. |
| Use a working 1–5 scale | Five anchored categories provide a simple pilot task with an intermediate category. This is a pragmatic choice, not a literature-established optimal PVC scale. Individual ratings are ordinal; modelling a mean as continuous is an approximation. |
| Acoustic/temporal measurements are predictors | Defining confidence through rate, pitch or pauses would make acoustic prediction circular. Literature motivates candidate cue families, while listener ratings remain the outcome [Jiang & Pell, 2017; Kirkland et al., 2022]. |
| Learn weights rather than assign them | Cue directions and interactions can depend on context and speaker. Fixed rules such as high pitch = low confidence would encode an unvalidated assumption. Learn from labels and evaluate on unseen speakers. |
| Start with Ridge and Random Forest | Ridge provides a regularised linear baseline for correlated features; a constrained forest tests nonlinear relationships. Both are manageable small-data starting points and are compared with a trivial mean baseline. Neither is presumed best or immune to overfitting. |
| Audio LLM is a benchmark, not ground truth | It provides another prediction of the same listener-defined construct. Plausible evidence text does not establish validity; compare it with the same independent human ratings. |

Full definition, anchors and exact academic citations: [PVC Definition v0.1](pvc_definition_v0_1.md).

### This iteration: annotation and demo readiness

- Added a local blinded rating interface with immediate CSV saving, neutral clip numbering, independent rater IDs and missing scores for unrateable clips. No human ratings were invented or collected by the agent.
- Retained the extractor unchanged. A thin demo wrapper prints a concise summary and preserves all 88 eGeMAPS features in underlying exports.
- Made the temporal sensitivity sweep reproducible at −55, −50, −45, −40 and −35 dBFS. On the After recording, measured energy activity ranges from 0.03% to 43.18%; this demonstrates sensitivity, not speech-detection accuracy or confidence change.
- Deferred normalisation and a new VAD dependency. Next: annotate speech/non-speech intervals in representative clips, then compare a dedicated local VAD and a controlled normalisation condition. Normalising waveform level also changes noise and energy predictors; it is not automatically a fix.

### Questions for the speech expert / supervisor

- Is the wording sufficiently specific to vocal certainty and commitment? How much lexical influence is acceptable in natural audio?
- What clip length/context and speaker-segmentation standard are appropriate? Which role files actually correspond to stable speaker identities?
- Does “3 = neutral or unclear” combine distinct judgements? When should raters use unrateable instead?
- Who should rate, how many raters/clips are feasible, and what practice, listening-volume and repeat-play policy should be fixed?
- Which aggregation rule, minimum coverage and agreement analysis fit the study? How should rater, accent, session and recording-condition effects be handled?
- What manual annotations are needed to evaluate temporal measurements, and which normalization/VAD comparison should come first?

No PVC score becomes defensible merely because the extraction, annotation UI or model-training code runs.
