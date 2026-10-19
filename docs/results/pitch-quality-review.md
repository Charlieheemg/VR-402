# Edinburgh pitch and boundary quality review

**19 October 2026: independent automated diagnostic and assistant visual inspection, not a human reference annotation or a completed measurement-validation study.** Existing demo audio, annotations and cached results were not changed. No model was trained.

## What was checked

Twelve recordings: sentence IDs 0001, 0006 and 0009, each in plain (19), infant-directed (20), computer-directed (21) and non-native-listener-directed (22) conditions. This purposeful subset covers the principal comparisons and both previously detected annotation anomalies. It is not a random sample, and does not cover condition 25 or establish corpus-wide error rates.

`audit_pitch.py` extracts openSMILE eGeMAPSv02 low-level F0 and independently computes Praat autocorrelation F0 through Parselmouth 0.4.7. Praat uses 10-ms steps, 60–400 Hz limits and otherwise its defaults; a 75–600 Hz sensitivity run changes only those bounds. The package's recorded Praat version and exact source hashes appear in `pitch-audit.json`. The existing eGeMAPS functional is unchanged.

For frame diagnostics, the script matches openSMILE's **reported frame start** to the nearest Praat analysis centre within 5.1 ms. Different analysis windows, timestamp conventions, smoothing and voicing decisions remain; these are not sample-exact aligned independent references. It compares semitone differences only when both report F0, and separately reports voicing disagreement on matched frames. Voicing disagreement is not an error rate against truth. The Praat p80−p20 is calculated from its positive F0 frames; it is not interchangeable with openSMILE's smoothed nonzero functional.

## Actual findings

Full precision: [24 tracker/parameter comparisons](edinburgh_pitch_agreement.csv), [input hashes and instrument checks](pitch-audit.json).

- Across the 12 files at 60–400 Hz, median absolute differences on both-voiced matched frames range **0.495–1.492 semitones**. Per-file voicing disagreement ranges **12.9–24.0%**. Smoothing and timing conventions contribute; neither tracker adjudicates the other.
- Infant sentence 0006 has Praat p80−p20 **11.680 st** at 60–400 Hz versus **8.860 st** at 75–600 Hz. This parameter sensitivity is a flag for manual review, not evidence that one range is correct. Infant sentence 0009 has **19.2%** of both-voiced comparisons differing by over 3 st at 60–400 Hz.
- Known 100-Hz and 150-Hz synthetic tones are recovered within 1 Hz; digital silence yields no voiced frames. These checks verify instrument wiring only.
- All twelve selected WAVs have zero samples at digital full scale. That does not rule out upstream analogue clipping or other distortions.

The assistant inspected all three private waveform/spectrogram/track sheets, covering all twelve recordings. In 0001, most visible voiced contours follow similar shapes, with isolated high-frequency candidates. In infant 0006 and 0009, the TextGrid end is close to the end of the main waveform activity; most of the uncovered tail is visibly low amplitude. This supports further investigation of trailing-silence undercoverage, **not** a definitive boundary repair or proof that no speech was omitted. Infant 0006 has isolated Praat candidates near 330–390 Hz around 1.7 s; infant 0009 shows a broader high-F0 episode around 1.1–1.5 s and tracker differences. These observations do not establish which candidates are genuine harmonics/F0.

## Decision and remaining review

Retain the published within-speaker findings as **automated descriptive estimates**. Do not add a “validated pitch”, pause/hesitation, articulation-rate or vowel-space claim. Preserve the original 25-pair timing summaries and labelled sensitivity analysis; no silent correction/exclusion. Obtain a trained human review of pitch tracks and phone boundaries before using these features as evidence of listener benefit. Independently annotate a subset blind to condition where feasible, retain disagreements, and predefine adjudication rules. The assistant's visual inspection is not that second human review.

The private sheets are `prototype/pvc/private/quality-review/review-0001.png`, `review-0006.png` and `review-0009.png`; per-frame diagnostics are alongside them. They are kept out of Git with the source audio. A reviewer can open the corresponding originals in Praat; no restricted audio is embedded in the public report.

## Reproduce without changing the existing environment

From the repository, using a separate optional package directory:

```sh
python3 -m pip install --no-deps --target /tmp/vr405-praat praat-parselmouth==0.4.7
prototype/pvc/.venv/bin/python scripts/audit_pitch.py --parselmouth-path /tmp/vr405-praat
prototype/pvc/.venv/bin/python scripts/plot_quality_review.py
```

Plotting requires the optional `scripts/requirements-figures.txt` dependencies and soundfile. The audit imports the existing environment's numpy before loading Parselmouth; installed software versions are recorded. Raw files are prerequisites, not redistributed dependencies. Re-running writes only these audit outputs and private diagnostic files. [Praat/Parselmouth parameter documentation](https://parselmouth.readthedocs.io/en/stable/api_reference.html#parselmouth.Sound.to_pitch_ac).
