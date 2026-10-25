# Feedback generator v0.1

Frozen local prototype for Ang Kang Zhe's Part B contribution. It reads existing assessment workbooks and produces learner and instructor Markdown drafts, source-record JSON and an uncompleted audit template. It retains the seven competencies; it does not replace the upstream assessment model.

The generator is byte-identical to the supplied v0.1 file. SHA-256:
`8bd8e2ef75f5bb0a77568fd6a5e8ad3688f5e744479f16550a224a241ff66f1f`.

## Run locally

From the repository root, using Python 3.12:

```sh
python -m pip install -r prototype/feedback/v0.1/requirements.txt
python prototype/feedback/v0.1/synthetic_demo.py --output private/feedback-demo
python prototype/feedback/v0.1/fyp_feedback_generator.py private/input.xlsx --output private/feedback-output
```

The demo uses invented text and colours, not participant material. Keep real workbook inputs and all derived drafts under ignored `private/` paths. The generator's default output directory is not private automatically: specify `--output` explicitly. The `.gitignore` is a convenience, not an access-control mechanism.

## Reproduce the evaluation

```sh
python prototype/feedback/v0.1/test_generator.py -v
python prototype/feedback/v0.1/evaluate.py --inputs private/feedback-v01/inputs --output private/feedback-v01/reproduced
```

Private source workbooks are required for the 21-workbook rerun and are not distributed. The evaluator writes draft reports and an input-hash manifest privately. Its aggregate JSON contains no source quotations, session filenames or participant identifiers. Publish only reviewed aggregates. See [evaluation and interpretation](../../../docs/feedback/evaluation-v01.html) and [aggregate results](../../../docs/feedback/results/v01-aggregate.json).

The supplied evaluation scripts used absolute `/mnt/data` paths and assumed reports already existed. `evaluate.py` is a new portable reproduction harness, not a modified generator. It uses an independent header lookup for populated-cell counting, checks exact extracted cell text, generates reports for the AI source and one consultant pair, and repeats deterministic generation. It does not assess clinical meaning or educational usefulness.

## Known limitations

- AI-workbook fill codes `FF5FA052` and `FFCB4C4E` remain `unverified`.
- The first two records per competency are displayed; omitted-item counts are not printed by v0.1 itself. Source-record JSON retains all extracted records.
- `Summarisation & Re-evaluation` is not recognised as an input header; `Summarisation and Re-evaluation` is recognised. Unknown headers can silently exclude source cells.
- Context uses a two-row window either side and displays at most six nearby entries. This is not a complete discourse thread.
- Attribution stays `team_or_unverified`. Reflection, practice and debrief suggestions are generic.
- Workbook handles are left to garbage collection; the Windows tests emit resource warnings. Explicit closure is a v0.2 task.
- Neither clinical appropriateness nor user benefit has been evaluated.

## Optional external drafting

The frozen file includes an opt-in API branch requiring both `--use-llm` and `--allow-external-data`. It submits at most 30 records. This branch and the source's default model identifier have not been validated. Model access, output schema, source fidelity and coverage require separate tests. No external call was made in this evaluation. Do not enable it for research data without the required permission and de-identification review.

## Version policy

Keep v0.1 unchanged so its results remain attributable. Polarity mapping, header validation, coverage reporting, source-span representation and workbook closure belong in v0.2, followed by the same regression suite and a documented comparison. Behaviour-specific actions and recipient routing require expert-reviewed rules before user evaluation.
