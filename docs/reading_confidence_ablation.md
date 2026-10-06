# Fixed-fold reading-confidence ablation and confound audit

6 October 2026. **Recording-level, not speaker-independent.** This audits the existing external children's reading-confidence benchmark; it does not validate adult paediatric PVC or alter PVC Definition v0.1.

## Method

All 600 recordings use the **exact saved five CV fold assignments** from the original benchmark (480 training / 120 test per fold). The runner checks the feature-table and fold-file SHA-256 hashes against the committed `evaluation.json`; it does not generate new folds. Label/ID joins are validated, and predictors come only from explicit allowlists.

Same majority baseline, logistic regression and Random Forest; same hyperparameters and fold-local preprocessing as the original benchmark. No retuning, feature selection or choice of a preferred configuration after inspecting results. The original full model reproduces its pooled and each-fold metrics to tolerance 1e−12. The audit does not refit or replace the local demo models: **full-feature logistic remains the preselected default**.

## Results

Each cell below is **balanced accuracy / macro F1**, pooled across held-out predictions. The majority baseline is **0.3333 / 0.1916 in every condition**.

| Condition | Predictors | Logistic | Random Forest |
| --- | ---: | ---: | ---: |
| A. Full: eGeMAPS + duration + RMS | 92 | 0.7160 / 0.7104 | 0.7813 / 0.7849 |
| B. eGeMAPS only | 88 | 0.7327 / 0.7262 | 0.7686 / 0.7722 |
| C. Full without duration | 91 | 0.7269 / 0.7188 | 0.7682 / 0.7725 |
| D. Duration only | 1 | 0.5690 / 0.5487 | 0.5391 / 0.5357 |
| E. RMS mean/SD/range only | 3 | 0.4631 / 0.4052 | 0.4744 / 0.4684 |

[Aggregate CSV](../prototype/pvc/results/reading_confidence/ablation_results.csv) reports balanced accuracy, macro F1, **Low/Medium/High F1 for every condition and model**, and differences from the same model's full condition. [Fold CSV](../prototype/pvc/results/reading_confidence/ablation_fold_results.csv) includes all 75 condition/model/fold rows and matched-fold differences. [Metadata](../prototype/pvc/results/reading_confidence/ablation_metadata.json) records hashes, exact feature lists, settings and versions. Per-recording predictions stay private.

## What this says about confounding

**Useful signal remains without duration.** Removing duration changes logistic balanced accuracy by **+1.09 percentage points** and Random Forest by **−1.31 points**. Their macro-F1 changes are +0.0085 and −0.0125. There is no substantial collapse in this split.

**Duration is still a material potential shortcut.** On its own it predicts well above the majority baseline (balanced accuracy 0.5690 logistic / 0.5391 Forest). It can reflect reading speed, text length, silence or speaker/task differences. These data cannot distinguish those explanations or establish a causal confidence cue. Its usefulness alone warrants caution, even though it does not explain the full benchmark result.

**Simple RMS statistics also carry some signal**, reaching 0.4631 / 0.4744 balanced accuracy. This is weaker than the standardized acoustic representation, but recording level and microphone/context effects cannot be dismissed.

**eGeMAPS-only remains substantially above both simple-feature conditions.** Relative to Full, logistic improves by 1.67 balanced-accuracy points and Forest drops by 1.27 points; macro F1 changes by +0.0158 and −0.0127. This strengthens the case that performance is not explained solely by the four added duration/RMS fields. It is not a reason to replace the preselected demo model with whichever variant looks best.

Crucially, removing custom duration/RMS does **not** remove all timing or energy information: the 88 functionals include segment, loudness and other correlated descriptors. They may retain proxies for duration, speaker, text, school or microphone conditions. This is a limited predictor-set audit, not proof that the representation is free of confounding. The duration-only and RMS-only comparisons do not test every possible interaction among the four custom fields.

The same-fold differences are descriptive. Shared speakers and texts can make CV estimates optimistic, and fold variation is not an independent-speaker confidence interval. No causal, statistical-significance, clinical-validity or unseen-speaker claim is made. The [metadata search](speaker_metadata_request.md) did not resolve speaker identity.

## Reproduce on this checkout

```sh
prototype/pvc/.venv/bin/python prototype/pvc/reading_ablation.py
```

This consumes the already extracted real 600-recording private feature table and saved folds. If those local files are absent, reproduce the [original benchmark](reading_confidence_benchmark.md) first in its recorded environment. Do not silently substitute different folds. All 88 acoustic fields remain in the underlying evidence regardless of which fields are used in an ablation.
