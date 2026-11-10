# Exploratory prediction of audio-only listener plurality

| Split (speakers) | Scored / selected | Macro-F1: model / majority | Balanced accuracy: model / majority |
|---|---:|---:|---:|
| train (20) | 432 / 480 | 0.886 / 0.110 | 0.953 / 0.167 |
| validation (5) | 113 / 120 | 0.355 / 0.117 | 0.376 / 0.167 |
| test (5) | 113 / 120 | 0.367 / 0.117 | 0.395 / 0.167 |

720 fixed clips, 30 speakers, 4 sentences. Unique-plurality targets; ties excluded. Actor 1001 is test-only. Training is resubstitution; validation selected C; test is held-out. Small subset, no clinical or coaching validation.
