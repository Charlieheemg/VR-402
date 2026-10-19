> Historical operational demo check, before the research-consolidation commit. For current publication/testing status see `docs/results/validation.md` at the repository root.

# Validation — 19 October 2026

- Existing repo clean before work; fast-forward pull reported already up to date. Existing extractor reused without modification.
- Public download completed without login. Actual archive inventory: 125 WAVs, 125 automatic labels, 125 genuine hand-corrected TextGrids; macOS resource fork entries excluded. All five conditions contain sentence IDs 0001–0025.
- New tests: 3 passed (complete matched corpus; independently recomputed duration/RMS, sample rate, hashes, annotation bounds, finite F0, 88 features; absence of listener-score fields).
- Existing prototype tests: 19 passed in 15.869 s.
- Browser: all nine selected WAVs loaded with readyState 4, finite durations and no media error. All nine play controls entered the playing state; exclusive playback observed. Sentence 0001 plain clip advanced to its end. This verifies browser decoding/playback behavior, not subjective listening quality or the laptop speaker volume.
- Desktop screenshot reviewed for three-column layout; saved full-page screenshots for all three sentence sets. Sentence navigation updates prompt, file paths and metrics.
- `git diff --check` passed. Raw corpus, screenshots, generated UI and results verified ignored by Git. Only new reusable demo source/docs remain untracked. No commit, push or public deployment performed.
- Operational: local offline UI, original audio playback, three metrics, result downloads, reproducible extraction and local download helper, presenter notes, screenshots. Local server listens only on 127.0.0.1:8765.
- Unvalidated: perceptual intelligibility/clarity/confidence, pitch-tracker accuracy, calibrated intensity, speaking/articulation rate, pause segmentation, vowel/formant measures, generalization beyond this single speaker. No predictor trained.
