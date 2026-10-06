# External perceived-reading-confidence benchmark

5-fold recording-level stratified CV; NOT speaker-independent

Speaker identities are not verified. Recording-level cross-validation may share speakers, texts and recording conditions across folds; no unseen-speaker generalisation claim.

| Model | Pooled OOF balanced accuracy | Pooled OOF macro F1 |
| --- | ---: | ---: |
| majority | 0.3333 | 0.1916 |
| logistic | 0.7160 | 0.7104 |
| random_forest | 0.7813 | 0.7849 |

Confusion matrices: rows = true, columns = predicted; order Low, Medium, High.

## majority

```text
   0  196    0
   0  242    0
   0  162    0
```

| Class | Precision | Recall | F1 | n |
| --- | ---: | ---: | ---: | ---: |
| Low | 0.0000 | 0.0000 | 0.0000 | 196 |
| Medium | 0.4033 | 1.0000 | 0.5748 | 242 |
| High | 0.0000 | 0.0000 | 0.0000 | 162 |

## logistic

```text
 135   59    2
  58  147   37
   0   24  138
```

| Class | Precision | Recall | F1 | n |
| --- | ---: | ---: | ---: | ---: |
| Low | 0.6995 | 0.6888 | 0.6941 | 196 |
| Medium | 0.6391 | 0.6074 | 0.6229 | 242 |
| High | 0.7797 | 0.8519 | 0.8142 | 162 |

## random_forest

```text
 145   51    0
  34  185   23
   0   26  136
```

| Class | Precision | Recall | F1 | n |
| --- | ---: | ---: | ---: | ---: |
| Low | 0.8101 | 0.7398 | 0.7733 | 196 |
| Medium | 0.7061 | 0.7645 | 0.7341 | 242 |
| High | 0.8553 | 0.8395 | 0.8474 | 162 |

## Interpretation boundaries

This prediction comes from an external model trained on children's English reading-confidence ratings. It is a demonstration of the acoustic modelling pipeline, not a validated PVC assessment for adult paediatric communication.

Probabilities are uncalibrated model outputs, not psychological certainty. No PVC 1–5 conversion is performed.
All preprocessing is fit inside training folds. Fixed hyperparameters; no feature selection or tuning. Final local models refit all recordings for demonstration only.
RF permutation importance is held-out macro-F1 change (5 repeats per fold); correlated features can mask or share importance. Its SD is not a confidence interval.
Logistic coefficients are from the final all-data standardized model, not causal effects or explanations of an individual prediction.
Raw audio, names, per-recording features, fold assignments, predictions and fitted models stay local. Aggregate metrics and feature summaries only are published.

See [method/provenance](../../../../docs/reading_confidence_benchmark.md) and [live demo](../../../../docs/live_confidence_demo.md).

## Fixed-fold ablation

See [ablation_results.csv](ablation_results.csv) for all five conditions, three models, balanced accuracy, macro/per-class F1 and differences from Full. [ablation_fold_results.csv](ablation_fold_results.csv) contains matched-fold comparisons; [metadata](ablation_metadata.json) records frozen inputs and settings. [Interpretation](../../../../docs/reading_confidence_ablation.md): standardized features retain signal without custom duration/RMS, but speaker/task/recording confounds remain. The preselected live-demo model is unchanged.
