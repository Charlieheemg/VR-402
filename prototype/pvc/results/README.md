# Real-audio demonstration — 6 October 2026

Both supplied Team Leader WAVs were processed locally with openSMILE 2.6.0, eGeMAPSv02 Functionals. Each JSON and CSV retains all **88 acoustic + 14 additional/optional fields** (102 feature keys). Optional transcript/latency fields are null/blank, never invented. JSON/CSV numerical agreement was checked for every field. SHA-256 hashes identify exact inputs without publishing recordings, content or local absolute paths.

| Measurement | Before Team Leader | After Team Leader |
| --- | ---: | ---: |
| Duration (s) | 513.344 | 463.0613 |
| Sample rate / channels | 24,000 Hz / mono | 24,000 Hz / mono |
| Energy activity, −35 dBFS | 35.6135% | 0.0302% |
| Energy silence, −35 dBFS | 64.3865% | 99.9698% |
| Internal low-energy gaps ≥0.2 s | 188 | 4 |
| Mean qualifying gap (s) | 1.4434 | 68.4600 |
| Maximum qualifying gap (s) | 17.8800 | 129.0200 |
| Mean frame RMS (full-scale amplitude) | 0.0259 | 0.0020 |
| F0 mean (semitones relative to 27.5 Hz) | 34.5457 | 32.0614 |
| PVC ground truth / prediction | Not available / not generated | Not available / not generated |

**Do not interpret this table as before/after confidence improvement.** The meaning of the supplied Before/After condition labels and continuity of speaker identity have not been confirmed. The role WAVs have session-length timelines; silence can represent waiting while another person speaks. No listening-based validation, diarisation verification or manual pause annotation was performed.

## Important anomaly: threshold and recording level

The After WAV has much lower measured RMS. The fixed −35 dBFS gate flags less than 1% activity and emits a warning; this does not mean no speech occurred. `energy_threshold_sensitivity.csv` records:

| Gate | Before activity | After activity |
| --- | ---: | ---: |
| −35 dBFS | 35.61% | 0.03% |
| −45 dBFS | 50.31% | 5.23% |
| −55 dBFS | 67.03% | 43.18% |

There is no claim that any threshold is correct. The large shifts demonstrate why manual checking, consistent recording conditions and a better segmentation/VAD method are needed before interpreting temporal features. eGeMAPS extraction was not retuned for this comparison. The script deliberately applies no gain normalisation.

## Reproducible follow-up

The new [five-threshold analysis](temporal_sensitivity.md) and `temporal_sensitivity.csv` extend this initial three-gate snapshot. Run `prototype/pvc/.venv/bin/python prototype/pvc/sensitivity.py` from the repository root; metadata includes WAV hashes and exact settings. The original JSON/CSV demonstration files above are unchanged. The next validation step is manual speech/non-speech annotation and a dedicated VAD comparison, not interpreting a preferred threshold as correct.

## Inspected source material and provenance

User-confirmed folder: `~/Downloads/20260121_150424_AI_Sample/`.

- Before input: `20260121_143844_AI_Before/Team Leader.wav`.
- After input: `20260121_150424_AI_After/Team Leader.wav`.
- Also present: mixed-session, IV and Compressor WAVs; `TEAM Instrument.pdf`; transcript, cleaned/truncated/parsed/summarised JSON; timestamp JSON; and Excel debrief files. The prototype inspected WAV headers and the Before transcript/cleaning/discourse/summary/timestamp JSON structures. PDF and Excel content were not used to derive scores.
- Transcript records associate a role and sentence with an ID; timestamps associate IDs with start/end times and can overlap. Automatic pairing to a preceding response is not justified without checking turns.
- Cleaned JSON changes wording relative to raw ASR. It is unsuitable as verified verbatim disfluency annotation without listening checks. No transcript counts were attached to this demonstration.
- Inspected summary fields are teamwork categories/assessments, not independent human PVC ratings. No dataset labels were created from them.
- The project `sources/` mirror was empty; all source files were left untouched. No audio or transcript was copied into Git or sent to an audio API.

## Verification

Six automated tests cover known signal gaps/boundaries, silence/partial frames, transcript counts, overlapping/missing timestamps, 88-feature JSON/CSV round-trip, input rejection, label bounds, metadata exclusion, speaker-disjoint folds, missing-speaker handling, undefined correlations, mean/Ridge/forest training, held-out importance and prediction/CLI execution. Synthetic target values exist only inside temporary software fixtures and never label the paediatric recordings.

Rerun extraction and tests with the commands in the [prototype README](../README.md). The extractor/training scaffold working end-to-end is the result; PVC predictive validity remains untested.
