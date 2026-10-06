# PVC meeting status — final refinement

6 October 2026. The meeting claim is **a defined research target, working extraction/annotation tools, and an audited external benchmark**. It is not a validated adult confidence detector.

## What is established

- PVC Definition v0.1 specifies how certain and committed a speaker sounds to listeners, with a proposed independent-listener 1–5 protocol. The definition itself is unchanged.
- Real paediatric WAVs run through the extractor and retain all 88 eGeMAPSv02 features. Fixed-energy activity/pause measurements remain explicitly unvalidated and threshold-sensitive.
- A real external dataset with 600 human-labelled children's reading recordings has been evaluated. Full-model balanced accuracy / macro F1: majority **0.3333 / 0.1916**, logistic **0.7160 / 0.7104**, Random Forest **0.7813 / 0.7849**.
- The exact-fold [ablation](reading_confidence_ablation.md) shows eGeMAPS-only performance **0.7327 / 0.7262** for logistic and **0.7686 / 0.7722** for Forest. Duration alone is informative, but removing duration and custom RMS does not collapse performance. Residual speaker/task/recording confounds remain.
- Local paired-WAV inference works and preserves both recordings, feature exports, probabilities and comparison output. Microphone capture/start-stop is implemented and tested with a simulated device. **Actual hardware voice capture remains to be rehearsed in the normal Mac terminal**; device discovery alone is not capture verification. Logistic stays the default, chosen before results were inspected.

## What is not established

- No speaker-independent external result: an authoritative speaker map was not found; the author request is drafted, not sent.
- Children's perceived reading confidence is not adult paediatric PVC.
- There are no domain-specific PVC human labels, measured listener agreement or validated paediatric PVC model yet.
- Neither acoustic features nor classifier probabilities establish internal confidence, clinical correctness, competence, teamwork improvement or learning outcomes.
- A successful acted A/B ordering is a sanity check, not validation. The classifier can produce concentrated probabilities for synthetic tones; it does not establish meaningful speech. In-range duration/features do not resolve domain shift.

## Demonstrate

From the repository root, use the longer reading passage first:

```sh
prototype/pvc/.venv/bin/python prototype/pvc/compare_demo.py --script reading
```

Then, if useful for illustrating domain relevance/shift, run `--script clinical`. Use identical text, microphone, distance, room and gain within each pair; A tentative and B assured. The [live-demo document](live_confidence_demo.md) contains both exact scripts, WAV fallback and permission instructions. Preserve every attempt; do not switch models or choose only favourable takes.

## Immediate research decision for the supervisor

Agree which step should take priority:

1. Proceed with a small **domain-specific PVC listener-rating pilot**, after agreeing the analysis unit, listener panel and rating anchors.
2. First improve **external validation with verified speaker identities**, acknowledging dependence on author metadata availability.
3. Revise the **definition/rating protocol after speech-expert input** before collecting labels.

Suggested discussion position: settle the minimum protocol questions with the speech expert, then pilot real listener ratings; request speaker metadata to strengthen the external result without treating it as a substitute for domain labels. This is a proposal, not an agreed supervisor decision. Assign an owner/date before leaving the meeting.

## 60-second explanation

“I have defined perceived vocal confidence as how certain and committed a speaker sounds to listeners, rather than internal confidence or clinical competence. The prototype extracts acoustic evidence from our recordings, and I have tested it on 600 externally labelled children's reading recordings. Logistic regression reached about 72% balanced accuracy and Random Forest about 78%, but these are recording-level results, not unseen-speaker results. Because duration looked influential, I repeated the comparisons on exactly the same folds. Duration alone predicts above baseline, but the 88 acoustic features alone still reach about 73% and 77%, so the result is not explained solely by the added duration and RMS fields. The paired demo illustrates the pipeline, not adult PVC validity. The decision now is whether to start a small domain-specific listener pilot, seek speaker-independent external validation first, or refine the rating protocol with the speech expert.”

Verification: all **19 software tests passed**; the real 600-recording ablation reproduced every original Full-model out-of-fold prediction; 15 aggregate condition/model results and 75 matched-fold rows were checked. Paired inference also ran with the actual trained model on two synthetic WAVs, preserving both originals and outputs. These are software checks, not human ratings or hardware-capture verification. No raw audio, identifying rows or fitted models are included in the commit.
