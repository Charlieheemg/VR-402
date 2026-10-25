# Problem, scope and research questions

## Existing context (source-derived)

The project-supplied manuscript, *Structured Discourse Modelling for Automated Team Communication Feedback in Paediatric VR Resuscitation Training* [P1], describes speaker-attributed, timestamped transcripts, reconstructed discourse threads and expert-derived assessments of seven communication-behaviour categories. The output is a worksheet that links positive/negative judgements to utterance evidence. The manuscript reports an initial comparison of automated worksheet review and facilitated debriefing, with **four teams per condition**; differences were descriptive and the feedback formats were not matched. These are findings reported by the **existing research team**, not new feedback-design results.

## Research problem (design hypothesis)

Evidence-linked assessment does not, by itself, specify how a learner should understand a behaviour, reflect on their contribution or choose a next action. This workstream asks how to reorganise the *existing* evidence into educationally grounded post-simulation feedback for (a) learners and (b) instructors, without adding unsupported interpretations or conflating a team event with individual failure. The need for this redesign is motivated by feedback/debriefing literature [1–4], but has **not** yet been empirically established with this project's target users.

## Questions

RQ-B1 — Feedback fidelity and quality: Can learner- and instructor-facing feedback preserve assessment evidence, meaning, category/polarity and defensible individual/team attribution? How clear, relevant and actionable is the output when assessed separately? RQ-B2 — Immediate educational usefulness: Compared with generic feedback from identical evidence, does theory-guided feedback improve learner comprehension, corrective learning-plan quality and instructors’ preparation of accurate, actionable debriefs? RQ-B3 — Subsequent learning effectiveness: Does theory-guided feedback improve communication performance in subsequent simulation scenarios? These questions define the evaluation programme; mechanical aspects of RQ-B1 have now been tested as recorded below. The original assessments and expert annotations belong to the upstream research team.

## Scope

**Included:** feedback information architecture; evidence-linked explanation; role-aware routing; reflective questions; potential practice actions; instructor debrief support; methods for checking fidelity. **Excluded for now:** new ASR/discourse classifiers, automated clinical severity scores, claims about competence, validated learner modelling, and claims of intervention effectiveness.

**Seven categories described in [P1]:** Roles & Responsibilities; Closed Loop Communication; Clear Messages; Knowing One's Limitations; Constructive Intervention; Summarisation & Re-evaluation; Knowledge Sharing. The categories were refined with subject-matter expertise and informed by teamwork instruments; they were **not simply copied from one scale**.


## Version 0.1 progress — 25 October 2026

The workbook-to-feedback generator is implemented in local deterministic mode. A new reproduction harness confirmed 21 workbooks and 371 populated annotation cells (AI 40, CT 268, NN 63), with zero count mismatches and exact extracted cell text for the tested layouts. Three learner/instructor report pairs retain displayed pointers and annotations and repeat deterministically. These are mechanical checks, not complete event-level fidelity or educational validation.

Observed issues are 40/40 unverified AI polarities, default AI display of 14/40 records, a missed ampersand-form category header, generic actions, unverified individual attribution and limited context. Five synthetic characterisation tests pass while preserving the frozen defects. Clinical review, independent full-event fidelity review, user testing, external-model execution and learning-effectiveness results remain outstanding.

See [the reproduced evaluation](../evaluation-v01.html), [source and run commands](../../../prototype/feedback/v0.1/README.md) and [aggregate results](../results/v01-aggregate.json). RQ-B1 is partially examined through mechanical checks; feedback quality, immediate educational usefulness (RQ-B2) and later performance (RQ-B3) remain unanswered.
