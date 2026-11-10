# Examiner feedback and research revision

10 November 2026. Review proposal; supervisor approval remains pending. Prepared against main `2b31707f023bc8b5a5258edee57b902d7b68bbfe`. The contemporary interim page had an empty Part A and a newer authored Part B. Both report pages now share the revised Part A; each existing Part B and all `docs/feedback/` files are preserved byte-for-byte. Open PR #2 concerns a separate emotional-delivery study and is not incorporated here.

## Decision and provenance

The examiner feedback is paraphrased from Charlie's supplied handover, not a verbatim examiner transcript. The earlier idea of adding Professionalism and Confidence columns is superseded by a proposed comparison within the seven existing categories. A sound event does not itself establish a rubric judgement. The proposed question is whether correctly attributed audio improves identification or interpretation of an established behaviour compared with transcript-only review.

The supplied manuscript is identified in [the existing source register](../feedback/references.md) as *Structured Discourse Modelling for Automated Team Communication Feedback in Paediatric VR Resuscitation Training*. Its publication and peer-review status are unverified. The seven-category account and Clear Messages criteria are carried from the handover and existing project documentation; original operational definitions still need clinician confirmation. The exact 12-to-seven selection process has not been established from primary development records. Do not invent it or describe the present revision as independent validation of the upstream rubric.

The handover's workflow image is an original diagram designated suitable for publication. Its text is transcribed in `assets/figures/revised-workflow.txt` for conservative word accounting. The evidence-gates diagram was adapted to a selectable HTML table rather than repeating its stronger “validated categories” wording. No internal screenshots, recordings, participant rows, models or manuscript are added.

## Verified evidence

- Reading benchmark: committed `prototype/pvc/results/reading_confidence/evaluation.json` and [methods](../reading_confidence_benchmark.md) support 600 recordings, 92 predictors (88 eGeMAPS plus duration and three RMS descriptors), and recording-level macro-F1 0.7849 Forest / 0.7104 logistic. The demo uses the logistic model. No training or clinical revalidation was performed for this revision. Numeric class meanings are inferred from matching published counts; an explicit numeric legend and authoritative speaker map remain unresolved.
- YAMNet: the private `VR402_Demo_Hub` source inventory has eight entries; `candidate_events.csv` has 19 entries; all eight coverage records report complete processing and their candidate counts sum to 19. These are overlapping channels, not independent participants or episodes. The private bundle remains outside Git. Its `limitations.md` explicitly records that the user resolved the old tail report on 4 November; the handover's confirmed-tail-miss statement is therefore not repeated. No exhaustive listening annotation, accuracy calculation or independent clinical meaning is available. Other possible missed events are unadjudicated.
- Confidence application: the private hub summary confirms unchanged logistic inference and saved demonstrations. Claims of unreliability are qualitative prototype observations, not quantified transfer-performance estimates.
- Edinburgh and R2SPIN: retained [measurement audit](../results/measurement-audit.md), [Edinburgh summaries](../results/edinburgh_summary.csv), [R2SPIN fold results](../results/r2spin_per_fold.csv) and [reproduction record](../results/reproduction.json) provide the historical evidence. No new experiment was run. Production conditions are not listener-recognition labels; published audibility is not a trainee-derived intelligibility predictor.

Private file hashes used for the local aggregate check are recorded below. Hashes establish which artifacts were inspected, not accuracy or permission to redistribute their contents.

- `candidate_events.csv`: `d26f162f6d7d09233f22354cfb4f04e943784265944e275a79ce5ff2ea23c005`
- `source_inventory.csv`: `55c5542fc990b31ccccff457d00b9801869b9fcf2e72e1e43f321bc6946418b9`
- `coverage_report.json`: `698b5e1a820cf98abe127e3ade077bca600e51ebd1cd2208f26ca451ae9b5232`
- `limitations.md`: `6db2f9e39812602323198bbf39ef00835b40df44539eabca3dc85c8c50a0e760`
- `SUMMARY.md`: `b78e688da02f7cdada538f3c20a38cc10441e3494dac30e88d0a25dfce46d26b`

## Research assessment coverage

| Requirement | Report evidence | Outstanding work |
| --- | --- | --- |
| A1 problem and gap | Fixed-rubric question; examiner critique; specific candidate criterion | Supervisor and rubric-owner confirmation |
| A2 alternatives | Transcript/context, confidence/events and intelligibility comparison | Select one operational criterion |
| A3 implementation | Confidence extractor/classifiers and event pipeline; retained historical methods | No claim of integrated clinical scoring |
| A4 testing | Recording-fold benchmark, event coverage, production contrasts and held-out-list recognition | Independent clinical reference and controlled condition comparison |
| A5 analysis | Domain mismatch, cross-talk, measurement limits, construct validity | Quantified errors and reviewer disagreement |
| A6 plan | Four conditional gates over eight weeks after scope approval; fallback if annotation unavailable | Confirm access, reviewers, sample size and calendar dates |

This is a working coverage map to the handover's A1–A6 requirements, not an assessor score. The handover reports a Week 13 deadline and 4,000-word two-person limit excluding appendices. Exact submission date and final administrative requirements need course confirmation. Existing literature/protocol appendices describe historical investigations; they are not evidence that the narrowed clinical study is approved or complete.

## Questions for A/Prof Khoo and the team

1. Does the proposed within-seven question address the intended research contribution?
2. Which exact existing criterion should be investigated first, and can audio support it without redefining it? Is Clear Messages appropriate?
3. Can the original 12-to-seven development source and approved annotation guidance be provided?
4. Are independent clinical reviewers and an approved sample of attributable episodes feasible? What access and review approvals apply?
5. What outcome would be useful: improved criterion agreement, detection of an established behaviour, or evidence-supported review utility? What effect/precision would warrant further study?
6. Can the revised Part A be accepted alongside Kang Zhe's preserved Part B before merge/publication?

No message has been sent to the supervisor. The supplied Word documents remain local review material. Merge and live-site publication await professor/team review.

## Revision checks

Both report checkers pass: interim 3,515 words (shared 936, Part A 1,090, Part B 1,489); research page 2,880. Counts include the 74 visible words in the raster workflow, with references and appendices excluded. The existing three refinement tests pass after replacing their stale 1,800–2,000-word Part A assumption with the newer interim allocation and accounting for raster labels.

Desktop (1440×1000) and mobile (390×844) browser checks pass on both pages: no page overflow, failed images or runtime errors. Tables/figures scroll horizontally on mobile. [Desktop review](review/part-a-desktop.png) · [Mobile review](review/part-a-mobile.png). All local report links and cross-page HTML anchors resolve. The [external reachability audit](../results/revision-link-audit.json) records 40 URLs: 18 returned 200, ten 203, one 202 and eleven publisher/access 403 responses. No 404 was returned; non-200 responses do not establish content verification. These existing external references still need manual checking where access was blocked.

The source workbook and raw audio were neither uploaded nor used for new modelling. The diff preserves both Part B blocks and all feedback documentation. No deployment or merge is part of this revision.
