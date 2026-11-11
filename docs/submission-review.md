> Prior revision QA. See the [final academic review](final-review.md) and current machine-readable checks for the latest branch. Counts and publication statements below describe the PR #4 preparation snapshot.

> Correction to the historical privacy statements below: “approved redacted specimen” was not supported by documented redistribution permission in the final review. PR #5 withholds source-derived excerpts and retains aggregate inspection with synthetic illustrations. The earlier wording is preserved here as a dated record, not evidence of approval.

# Submission review and quality assurance

Completed 11 November 2026 on a dedicated review branch. This document records editorial and technical readiness; it does not certify supervisor approval, live deployment or course submission.

## Substantial changes

- Consolidated the two competing report pages into one authoritative `index.html`, with a hash-preserving compatibility page at the old interim URL.
- Rebuilt the narrative around inherited assessment → two distinct research questions → methods → measured findings → interpretation → conditional future tests. Both authors' research content, evidence and attribution are retained.
- Incorporated the completed CREMA-D perception study through its immutable existing evidence, without merging its software branch. Kept confidence, laughter and intelligibility results distinct from clinical rubric validation.
- Verified the original seven-category definitions against the supplied manuscript. Preserved the examiner's narrowed scope; retained the unverified 12-to-seven origin as an explicit source limit.
- Added a responsive, text-based contribution diagram, result/design tables, clear section navigation and an appendix index. Removed unused main-report references; technical depth remains in appendices and historical sources.
- Replaced stale front-door documentation, labelled superseded plans, removed unused inherited UI helpers and consolidated word-count commands. The evaluated feedback generator and original numerical files remain unchanged.

The first refinement pass clarified metric definitions and model attribution, prevented cross-task F1 comparisons, specified episode selection and reviewer recall controls for the proposed studies, explained consultant-source labels, and strengthened the synthesis. No results or prototype implementations were changed.

## Rubric-driven repository refinement — 11 November

The newly attached six-page brief matches the previously inspected brief. The Canvas text additionally confirms that one group member submits the website URL. The report now makes the mixed research/design requirements explicit:

- Added a concise value proposition and intended deliverables, working feedback specifications, explicit proposed H-A/H-B, and a feasibility stopping rule in the main report.
- Added [Appendix E](project-design.html): documented progress, completed-study design matrix, specification-to-test matrix and proposed-study gates. Experimental units and sample sizes are kept distinct; no new studies or approvals are implied.
- Reconciled the feedback protocol across the main report, scope, methodology and Appendix B: the existing worksheet is the primary comparator; a generic summary is optional. Removed obsolete section-number references and contradictory unanswered-question wording.
- Corrected definitive Low/Medium/High wording to identify the inferred numeric-label mapping. Original code, labels and results are preserved.
- Labelled older intelligibility plans, feedback working documents and validation snapshots at their entry points. Extended repository checking to prototype Markdown documentation.
- Added the [Canvas handoff](submission.md), including live-site/deployed-SHA verification and the single group submitter requirement. Fixed mobile-only table instructions leaking into print layout.

| Repository decision | Action and reason |
| --- | --- |
| Change substantially | Strengthened the main narrative and linked claims, specifications, tests and deliverables through Appendix E; aligned current supporting protocols. |
| Add | Joint design/progress appendix and concrete Canvas handoff, filling requirements that were previously dispersed or missing. |
| Consolidate / remove | The overall PR replaces the competing interim page with a compatibility redirect, removes unused inherited UI components and eliminates stale active-scope statements. |
| Preserve with context | Original prototypes, numerical evidence, authored design concepts, old plans and validation records remain inspectable. Deleting research history would impair provenance. |
| Defer research changes | Feedback v0.2 repairs, new model training and participant studies belong to subsequent research; the evaluated v0.1 must remain reproducible. |

## Academic coverage

| Assessment area | Evidence in the final report |
| --- | --- |
| A1 objective, scope and context | Shared value/deliverables, individual objectives, inherited boundary and working specifications |
| A2 methods and concepts | Speech alternatives; feedback theory-to-design choices; completed/proposed design matrices |
| A3 prototype creation | Acoustic extraction/classifiers/event pipeline and deterministic feedback generator |
| A4 testing | Dataset/split definitions, recorded metrics, workbook and synthetic test procedure |
| A5 analysis | Domain/generalisation limits, attribution and construct validity, fidelity/coverage defects |
| A6 problems and plan | Observed shortcomings linked to requirements, four conditional milestones and explicit stopping/fallback rules |

## Final checks

- [x] **Academic accuracy:** checked original manuscript §3.3/Table 1 and the official six-page brief; mapped each numerical result to its actual experiment. Completed, preliminary and proposed work remain distinct.
- [x] **Completeness:** both authors have explicit questions, rationale, methods, results, interpretation and future tests. Confidence, laughter, CREMA-D, Edinburgh/R2SPIN and feedback v0.1 are represented; detailed evidence remains accessible through appendices A–E.
- [x] **Word limit:** 3,537 words, including references, headings, captions, tables and diagram text. Shared narrative 718; Charlie 1,225; Kang Zhe 1,158; references 436. Headroom: 463. Masthead/navigation/footer and separate appendices are excluded.
- [x] **Citations:** targeted primary-source/record checks and retained source audits documented. The 26 main-report/speech/source-audit external destinations returned 18 HTTP 200, two 203, one 202 and five 403 responses. No missing/retired destination (404/410) was observed; access-blocked responses are not full-text verification.
- [x] **Visual presentation:** inspected the complete report and key section captures; seven examiner-facing pages tested at 1440×1000 and 390×844. No page overflow, failed images, empty links or JavaScript errors. Tables have horizontal mobile access; scientific figures link to full-size SVGs. Desktop/mobile compatibility redirects preserve section fragments. An 11-page A4 print preview was rendered and inspected; print CSS removes screen-only scroll instructions and keeps section labels with headings.
- [x] **Repository integrity:** 68 documentation files and 457 local link checks pass (root/docs plus prototype Markdown). One authoritative report, separate appendix bibliography, dated historical records and no unused inherited UI helpers.
- [x] **Tests:** four submission-contract tests, three existing aggregate/refinement tests and five frozen-feedback characterisation tests pass. Tests independently recover CREMA-D macro-F1/recall from confusion matrices, retain the exact feedback generator hash and exercise broken-link rejection.
- [x] **Evidence preservation and privacy:** no changes to original speech/feedback prototype code, feedback result aggregates or Edinburgh/R2SPIN numerical evidence. No newly published raw audio, participant workbooks, private models or manuscript; tracked-file type/path check passes. Existing redacted specimen is retained.
- [x] **Review workflow:** dedicated branch based on current main plus prior examiner-feedback work; no force-push, merge, deployment or course submission.

Machine-readable records: [word count](results/report-checks.json), [repository links](results/submission-repository-checks.json), [browser checks](results/submission-browser-checks.json), [external reachability](results/submission-external-links.json). [Desktop preview](research/review/submission-desktop.png) · [Mobile preview](research/review/submission-mobile.png).

The private 21-workbook run and raw-audio experiments were not rerun during editing. Their historical results remain attributable to the frozen implementations; current checks exercise public aggregates and synthetic inputs. No new research model was fitted.

## Human confirmations

1. **Academic sign-off:** both authors should approve their final representation and the supervisor should confirm the narrowed first criterion and feasible clinical review. This is a proposed next study, not completed validation.
2. **Source status:** confirm the upstream manuscript's publication/citation status and obtain the original 12-to-seven development record if that historical account is required. The report does not rely on an invented derivation.
3. **Administration and publication:** confirm the exact Week 13 calendar deadline, applicable AI-assistance declaration and the authorised submitter/merge timing. The supplied Canvas instructions settle the submission mechanism: one group member submits the published website URL. No course submission or supervisor message has been sent. Existing clinical examples are restricted to the previously approved redacted specimen; no new participant material is published.

Independent annotation, participant recruitment and educational evaluation are future research dependencies, not missing completed results. The report states these limits directly.
