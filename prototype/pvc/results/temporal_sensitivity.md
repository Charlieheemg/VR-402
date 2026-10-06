# Temporal-feature sensitivity

Reproducible fixed-energy analysis; **energy activity is not validated speech activity**. No human PVC ratings or confidence scores are generated.

20 ms frames, internal gaps ≥0.2 s; no normalisation. Leading/trailing silence contributes to the silence ratio, not the pause count. Source hashes and settings are in `temporal_sensitivity_metadata.json`.

| Clip | Gate (dBFS) | Active (%) | Silence (%) | Gaps | Mean gap (s) | Max gap (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Before | -55 | 67.03 | 32.97 | 164 | 0.815 | 7.240 |
| Before | -50 | 58.01 | 41.99 | 175 | 1.020 | 8.780 |
| Before | -45 | 50.31 | 49.69 | 176 | 1.222 | 13.500 |
| Before | -40 | 43.40 | 56.60 | 169 | 1.428 | 15.900 |
| Before | -35 | 35.61 | 64.39 | 188 | 1.443 | 17.880 |
| After | -55 | 43.18 | 56.82 | 297 | 0.668 | 10.620 |
| After | -50 | 20.67 | 79.33 | 324 | 0.969 | 11.820 |
| After | -45 | 5.23 | 94.77 | 179 | 2.312 | 35.420 |
| After | -40 | 0.50 | 99.50 | 42 | 10.626 | 115.120 |
| After | -35 | 0.03 | 99.97 | 4 | 68.460 | 129.020 |

## Interpretation

- Before: measured activity ranges from 35.61% to 67.03%; qualifying gap count ranges from 164 to 188 with only the threshold changed.
- After: measured activity ranges from 0.03% to 43.18%; qualifying gap count ranges from 4 to 324 with only the threshold changed.

Lowering the gate admits more low-energy frames, which may be quiet speech or background noise. Gap counts need not change monotonically: gaps can split, merge or fall below the minimum duration. Zeros for mean/max gap mean no qualifying gap, not zero hesitation. Without manually marked speech/non-speech intervals, this cannot establish which gate is accurate. Whole-session role recordings also contain waiting time; these are not within-turn hesitation counts.

**Next improvement:** manually label a small set of representative quiet/noisy single-speaker clips, then compare a dedicated local VAD against those intervals before replacing the energy approximation. Gain normalisation is worth a controlled comparison, but rescales noise as well as speech and does not solve overlap or turn segmentation. Keep original audio for F0/loudness/voice-quality extraction; normalising it would change the energy predictors being studied. No normalisation or new VAD dependency is added in this minimal extension.

**Supervisor wording:** “The pause/activity outputs depend strongly on recording level and the energy threshold. They are useful diagnostics, not validated speech activity or evidence of confidence change. I need manual segmentation checks and a VAD comparison before interpreting them.”
