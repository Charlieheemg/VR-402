# Validation record — 31 October 2026

## Scope and status

Phase 1 complete: original RAVDESS archive verified against publisher MD5; four
same-actor/sentence/repetition/intensity pairs, happy versus sad; playback and
identical scripted transcripts; reproducible acoustic summaries and manifest.
Phase 2 complete: five CREMA-D expressions, original WAVs from pinned upstream
revision; local launcher, measured comparison text, provenance reveal, offline
bundle, CSV/JSON exports and short presentation script.
Exploratory perception study added: official CREMA-D audio-only vote distributions,
720 fixed clips, 30 disjointly split speakers, 88 acoustic predictors and regularised
logistic regression versus a training-majority baseline. Actor 1001 is test-only;
ties are displayed and excluded from single-label metrics. No audio-LLM is used.
See [study methods and actual results](study_results/METHODS.md),
[Tuesday mock table](study_results/MOCK_TABLE.md) and `study_results/results.json`.

The implementation brief is preserved in IMPLEMENTATION_BRIEF.md. Working brief
v0.3 was read as supporting context; no deck, PDF or existing report was rewritten.
The original repository mirror is untouched; this change is based on current
origin/main ab8ef1f in the outputs/VR-402 checkout.

## Tests run

- `python -m unittest test_demo -v`: 10 passed. Checks matching controls, filename
  decoding against manifest, SHA-256, actual WAV duration/RMS, all thirteen pitch
  medians/ranges recomputed from voiced frames, absent-input error, embedded audio,
  original build without study results, and rejection of stale study attachment.
- `python -m unittest test_study -v`: 11 passed. Checks vote/tie semantics, all
  720 matched filenames, actor/split separation, training-only preprocessing,
  metrics/confusion recomputation, baseline target and exact offline model replay.
- `python -m unittest test_pvc -v` from parent directory: 6 passed, including
  extractor roundtrip, temporal fixtures and training/prediction regression checks.
- Local preview at 127.0.0.1:8043 starts with standard-library launcher.
- Browser: RAVDESS and CREMA-D audio decoded with readyState 4 and no media error;
  playback clock advanced on selected RAVDESS A and CREMA-D B clips. Dataset and
  take changes, reveal/hide, provenance disclosure and identical displayed scripts
  checked. Default browser layout screenshot inspected.
- Extension browser check: optional CREMA-D panel displayed exact six-class votes,
  the 5/5 anger/disgust tie with exclusion status, wrong and matching predictions,
  uncalibrated probabilities and distinct split metrics. Existing acoustic panel
  remained usable simultaneously; CREMA-D playback clock advanced without error.
- Browser screenshots at forced desktop dimensions were clipped by the in-app
  capture surface; viewport was restored. Full laptop projection layout needs rehearsal.
- All audio is inline data, with no remote scripts, fonts, fetches or audio requests.

## Acceptance checks still requiring rehearsal

Wi-Fi was not physically disabled. The managed browser disallows file URLs, so
local-file-mode fallback was not tested there. A human has not confirmed audible
contrast, room-volume suitability, speaker intelligibility or presentation timing.
Use the local launcher with Wi-Fi off and listen through the intended speakers.
Exploratory classification metrics are limited to the prespecified held-out subset;
no broad perceptual validity, clinical benefit or pitch-reference agreement has
been established. RMS is recording level, not calibrated vocal SPL.
Neutral CREMA-D intensity is unspecified versus medium for the other four takes.
A same-take A/B comparison is permitted as an honest no-difference control.

## Measured feature table

RAVDESS takes are happy/sad in each actor/sentence group; all use normal intensity
and repetition 01. CREMA-D actor 1001 says “It's eleven o'clock.” All values below
are computed from the unmodified WAVs; duration includes leading/trailing silence.

| File | Dataset acted label | Duration (s) | RMS (dBFS) | Median F0 (Hz) | F0 range (st) |
|---|---|---:|---:|---:|---:|
| 03-01-03-01-01-01-01.wav | Happy | 3.470 | -42.89 | 141.26 | 3.83 |
| 03-01-04-01-01-01-01.wav | Sad | 3.837 | -48.55 | 124.42 | 4.06 |
| 03-01-03-01-02-01-01.wav | Happy | 3.537 | -43.86 | 131.55 | 4.03 |
| 03-01-04-01-02-01-01.wav | Sad | 3.503 | -50.40 | 110.20 | 2.53 |
| 03-01-03-01-01-01-02.wav | Happy | 3.604 | -38.02 | 237.39 | 8.38 |
| 03-01-04-01-01-01-02.wav | Sad | 3.837 | -46.53 | 215.14 | 4.14 |
| 03-01-03-01-02-01-02.wav | Happy | 3.770 | -38.33 | 228.83 | 6.28 |
| 03-01-04-01-02-01-02.wav | Sad | 3.737 | -44.64 | 208.85 | 2.30 |
| 1001_IEO_NEU_XX.wav | Neutral | 1.602 | -36.42 | 98.08 | 0.47 |
| 1001_IEO_ANG_MD.wav | Angry | 2.636 | -30.93 | 128.54 | 3.81 |
| 1001_IEO_FEA_MD.wav | Fearful | 1.602 | -26.86 | 147.38 | 3.09 |
| 1001_IEO_HAP_MD.wav | Happy | 1.668 | -27.79 | 163.25 | 5.91 |
| 1001_IEO_SAD_MD.wav | Sad | 1.735 | -38.18 | 95.16 | 0.74 |

Full precision, all inherited features, extraction settings and source URLs are in the JSON/manifest.
