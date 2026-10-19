# Focused refinement audit — 19 October 2026

This audit checks the existing consolidation, without fitting models, changing recordings/annotations, or adding acoustic features. Run `prototype/pvc/.venv/bin/python scripts/audit_refinement.py` from the repository root. Existing raw data and row-level predictions are prerequisites and remain private. `refinement-audit.json` records input/script hashes and checks.

## Edinburgh annotation coverage discrepancy

All 125 hand-corrected TextGrids were reparsed against the original WAV durations. Two have more than 0.05 seconds of uncovered tail:

| Original file | WAV duration (s) | Last TextGrid boundary (s) | Uncovered tail (s) | Final hand label |
|---|---:|---:|---:|---|
| MKH800_20_0006.wav | 3.4495000 | 2.940 | 0.5095000 | n? |
| MKH800_20_0009.wav | 3.8114375 | 3.300 | 0.5114375 | @? |

The automatic `.lab` files label their last intervals `sil`, ending at 3.444 and 3.806 s, respectively. The uncovered waveform tails have RMS levels −43.54 and −42.45 dBFS and peaks 0.0640 and 0.0852 full scale. These are digital-amplitude observations, not VAD, human listening judgements or a proof that all speech was annotated. They are consistent with omitted trailing silence in the corrected files, but that explanation remains unvalidated. No time shift, padding, relabelling, trimming or replacement was applied. All originals and all 25 sentence pairs remain in the published analyses.

The earlier tests checked interval bounds/continuity, which allow annotations to end before the WAV. They did not establish complete coverage. New tests separately check the WAV–annotation end mismatch; this closes a coverage-check gap without treating software checks as perceptual validation.

### Effect on results

- Computer-directed and non-native-listener-directed contrasts use conditions 21/22 versus 19; neither includes the flagged condition-20 recordings. Their 25/25 span increases and +1.7305/+0.8045 s paired medians are unchanged.
- The infant timing result must be read as **annotated** timing. Its all-25 median paired span difference is +0.0208626 s (13 positive/12 negative). A supplementary analysis excluding sentence IDs 6 and 9 from both members of each pair yields +0.0348972 s for 23 pairs (13 positive/10 negative). No robust infant lengthening conclusion follows from these small mixed-direction changes.
- Phone-like infant duration median changes from −0.0055807 s to +0.0108964 s under that exclusion, demonstrating sensitivity of a near-zero summary. Internal silence-labelled median difference remains zero. See `edinburgh_coverage_sensitivity.csv`; analogous n=23 contrasts for other conditions are transparent sensitivity comparisons, not corrected replacements.
- Whole-file duration and F0 extraction use the full WAV independently of TextGrid endpoints. Those calculations are unchanged by annotation undercoverage. Their measurement interpretation is a separate question: automated pitch accuracy has not been manually validated.
- All published timing medians/direction counts and condition-median summaries reproduce from reparsed annotations or the unchanged existing measurement table. All nine demo F0-range outputs agree with the corresponding full-corpus cached estimates. We checked the metric/configuration and data consistency, not manual pitch truth.

### Six quantities that must remain distinct

| Quantity | Current definition / evidence | Validation limit |
|---|---|---|
| Whole-file duration | Samples ÷ sample rate | Includes edge silence; not speech time |
| Annotated span | First nonempty non-pure-silence onset to last offset | Includes internal labels; undercoverage and boundary uncertainty matter |
| Phone-like duration | Sum of non-pure-silence labelled intervals | Includes composites such as `sil+k`; not validated articulation time |
| Internal silence-labelled duration | Pure-silence-labelled intervals inside span | Corpus warns `sil` can mean unassignable spectrogram gap |
| Articulation rate | Would need verified syllable/word count and speech-time denominator | Not currently reported or validated |
| Perceptual pause | Listener/acoustic definition and independently reviewed segmentation required | Not established by `sil`, a threshold gate or a unit test |

Question-mark labels: 847 intervals; composite labels: 36. Pure-silence matching removes `?` and surrounding parentheses/spaces; composites remain indivisible. These are explicit operational rules, not a claim that ambiguity was resolved. Formants/vowel-space validity remains unestablished.

## R2SPIN per-fold check: no retraining

The pinned AllData.csv hash matches the consolidation record. Saved out-of-fold row order matches source Participant/List/WRR exactly. Aggregate probabilities reproduce all four published model summaries. For the primary context versus context+KWGP comparison:

| Held-out list | Responses | Context accuracy | +KWGP accuracy | Accuracy change (percentage points) | Brier change (+KWGP − context) |
|---|---:|---:|---:|---:|---:|
| 1 | 800 | 66.875% | 74.375% | +7.500 | −0.030844 |
| 2 | 800 | 70.375% | 70.750% | +0.375 | −0.000803 |
| 3 | 800 | 64.000% | 71.000% | +7.000 | −0.035726 |
| 4 | 800 | 67.250% | 67.750% | +0.500 | −0.011586 |
| 5 | 800 | 68.000% | 74.000% | +6.000 | −0.031812 |
| 6 | 800 | 68.500% | 73.500% | +5.000 | −0.034329 |
| 7 | 800 | 72.375% | 73.375% | +1.000 | −0.027675 |
| 8 | 800 | 75.750% | 78.250% | +2.500 | −0.031235 |

Machine-readable full-precision values: `r2spin_per_fold.csv`. Accuracy increases and Brier decreases in all eight folds. Magnitudes vary; list 2 improves little. These folds are not independent replications: training sets overlap, listeners/speakers recur, and keywords can recur across different contextual sentences. No sign-test p-value, naive row bootstrap, significance claim or population confidence interval is inferred from these eight directions.

The existing protocol used LeaveOneGroupOut(List), fold-local StandardScaler and L2 logistic regression (`C=1`, `lbfgs`, max_iter=1000), no tuning; see `scripts/reproduce_evidence.py` and `docs/methodology/reproduction.md`. The source is BBC R2SPIN, revision `a9893f5ada87be2373c366d666d0c47e08dab138`; the paper and README specify the original babble/timing dependence. KWGP is published acoustic audibility under masking, not an acoustic feature extracted here, and not speaker-side articulation, pausing, F0 or vowel distinctiveness. Direct RQ2 validation remains open.

## Research status

**Implemented:** extractor, historical classifiers and local demo. **Reproduced:** existing timing summaries and aggregate recognition metrics; this refinement adds only coverage/sensitivity and per-fold audits of existing evidence. **Preliminarily supported:** matched within-speaker production differences and incremental masking-related prediction in R2SPIN. **Not yet validated:** speaker-side intelligibility prediction, manual pitch/formant accuracy, clinical transfer, feedback efficacy or integrated-system usefulness.
