# Method comparison and bounded selection

**Decision for the next experiment:** a small prespecified acoustic feature set with transparent regularised prediction is the primary candidate, conditional on trustworthy human labels and measurement review. Compare simpler baselines first. Nothing here is a new trained model or an observed ranking.

| Alternative | What it can test | Requirements / limitations | Role |
|---|---|---|---|
| Intercept and available context/listener variables | Whether added acoustics improve on task difficulty and listener context | Appropriate grouped splits; contextual variables must be available at prediction time | Required baseline |
| Frozen ASR recognition against verified target | Whether machine recognition explains human word recognition | Freeze recogniser/settings; accents/noise/domain errors; ASR correctness is not human ground truth | Required comparison if permitted audio processing is available |
| Prespecified acoustics + regularised regression | Incremental association of timing/F0 with human recognition, conditional on context | Reliable features, real human responses, fold-local preprocessing; limited causal interpretation and sensitivity to speaker/channel | Primary interpretable candidate after data gate |
| Nonlinear tree/ensemble | Nonlinear associations and interactions | More tuning/data; easy speaker/channel shortcuts; feature importance does not establish mechanism | Defer until a simple baseline is justified |
| Speech embeddings / fine-tuned deep model | Learned signal representations | More independent speakers/data/computation; difficult explanation and potential identity leakage | Defer for interim scope |
| Audio-LLM or model-generated clarity rating | Agreement of a frozen model judgement with independent human outcomes | Access/consent/versioning, reproducibility, potential opaque construct mixing; cannot supply its own ground truth | Optional later benchmark, no fabricated scores |
| Clinical/expert perceptual rating | Expert judgements on a defined rubric | Trained raters, reliability and explicit construct definition; ratings differ from transcription recognition | Separate outcome if needed, not a replacement for recognition |

This table compares implementation approaches, complementing the main report's construct comparison. The choice favours interpretability, current extractor reuse and the ability to test an acoustic increment. It does not imply that engineered acoustics outperform ASR or embeddings. Existing R2SPIN uses published masking/audibility information and cannot settle that comparison.

For binomial words-correct outcomes, preserve correct/total counts and item/listener dependencies; do not automatically reuse a binary keyword classifier for sentence percentages. Choose a compatible likelihood or clearly bounded score model when the acquired labels are known. Freeze evaluation units and speaker splits before tuning; report calibration and suitable probability/error metrics with uncertainty at the actual independent-unit level. No confidence, hesitation cause or clinical competence is inferred from one feature.
