# Final academic and editorial review — 11 November 2026

This review follows the published PR #4 revision. The current branch is `review/final-academic-pass`; its proposed changes require review before publication. Earlier QA counts in [submission-review.md](submission-review.md) describe the preceding revision.

## Substantive decisions

- Rewrote Part A around the questions each experiment could answer and the problems it exposed. The revised rubric question is explicitly a later scope decision; no invented chronology or retrospective confirmatory hypothesis is assigned to the exploratory studies.
- Checked the manuscript's Table 1 and the adjacent closed-loop rule. Candidate audio uses concern recovering words/acknowledgements and attributing speakers. Confidence, laughter, emotion and intelligibility do not become rubric indicators by assertion.
- Recovered CREMA-D accuracy, macro-F1 and all confusion matrices from the original `276b179` results and checked exact equality with the aggregate snapshot. Main text and Appendix A now report the model's 51/113 correct versus the majority baseline's 61/113, as well as macro-F1 and the training–test gap. The existing metric test now independently recovers accuracy too.
- Revised the proposed clinical pilot to retain transcript-first reference judgements, audio-driven revisions and unresolved disagreement. Separate condition reviewers see each episode only once. Agreement is assessed against both reference stages; an audio-informed reference is explicitly not an independent gold standard. Reasons for changes and attribution errors matter alongside agreement. Feasibility and annotation burden precede sample-size claims.
- Reviewed Part B's educational argument, implementation and results. Strengthened the link between deterministic generation, inspectable defects and the need for user evaluation. The repeated template finding is retained; a synthetic example explains the intended design improvement.

## Public evidence and privacy

The Word concepts document and the HTML/Markdown output copies included transcript-derived quotations and worksheet pointers. Direct identifiers had been redacted in the generated-output copy, but no explicit public-redistribution permission was established in the reviewed records. Removed the Word attachment from the current tree and replaced source-derived example text with aggregate inspection and explicitly synthetic illustrations. Private review copies retain the inspected source material; the aggregate results and frozen generator are unchanged.

The public illustrations are not recordings, evaluated generator outputs or new experiments. Original quotations are not necessary to support the reported display counts or repeated-template analysis. No new participant data or restricted datasets are introduced.

**Earlier public copies remain in Git history and on the currently deployed revision until this PR is merged.** This is not a retrospective privacy purge. The source owner must confirm permission and whether historical copies require removal; rewriting shared history requires a separate coordinated decision. Screenshots and SVGs in the report/review assets were inspected as report layouts, conceptual diagrams and aggregate plots, not raw clinical screens. This audit does not establish consent for any underlying private study.

## PR #2 and reproducibility

PR #2 is conflicting at commit `276b179479be5fdf3a5cf8d09edc36d95c79643b`. It contains an offline demo, scripts and tests, but also feature rows, vote/clip manifests, coefficients and preprocessing artefacts. Preserve it as a separate software review. Appendix A links its exact implementation, methods and licence record; the main branch retains the compact aggregate snapshot. No row-level data or fitted parameters are copied into this submission PR. The conflict does not prevent inspection of the cited immutable files.

Reading, Edinburgh, R2SPIN and feedback code/results remain accessible through Appendix A, Appendix C and the repository guide. Clinical YAMNet inputs and implementation bundle remain private; its source inventory, hashes and limits are documented. A public checkout cannot replay every private experiment, and the report says so.

## Verification

Current word count and link counts are in [report-checks.json](results/report-checks.json) and [repository checks](results/submission-repository-checks.json). Main count includes references, headings, tables and captions. The original numerical evidence and research implementations were preserved. Existing citation audits support unchanged literature claims; the new rubric discussion was checked against the supplied manuscript, not inferred from category names.

All 12 README submission, aggregate and frozen-feedback tests passed. Main report: 3,598 words including references; 402 below the cap. Repository: 69 documentation files and 459 local link checks passed. Desktop/mobile checks and screenshots cover the report, evidence index and appendices A–E; the print preview is inspected separately. No private-data model refitting or participant evaluation is represented as part of this editorial pass.

## Human confirmations

1. Both authors approve the final representation of their work. Confirm the first rubric criterion and available clinical reviewers for the proposed pilot.
2. Source owner: confirm redistribution permission for previous source-derived examples and whether Git-history removal is required. Current public replacement examples are synthetic.
3. Confirm manuscript publication/citation status, the exact Canvas deadline and applicable declaration. One group member submits the deployed website URL.

## Focused pre-submission check — 11 November 2026

Corrected the introduction to state the intended study rather than implying a completed tested account. Reconciled Appendix D's title, navigation and descriptions across the feedback guide, appendices, source audit and main report: aggregate inspection of supplied output plus synthetic illustrations. Removed duplicated description text and explicitly corrected the unsupported historical “approved” label. Research results, methods and authorship are unchanged.

Publication status was checked: PR #5 is open, while Pages still serves merged PR #4 (`111793a`). Merging and successfully deploying PR #5 will replace the current-page excerpts; it will not remove earlier commits, PR diffs, clones, forks or cached copies. The source owner must establish the permission/sensitivity of the previously published material and decide whether removal is necessary. The repository owner must explicitly authorise and coordinate any history rewrite or other destructive cleanup. No such action was taken. GitHub describes the limitations and coordination required in its [sensitive-data removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

The report is editorially ready for merge. Public-history clearance remains a distinct owner decision; the replacement illustrations do not imply that permission has been granted for earlier source material.
