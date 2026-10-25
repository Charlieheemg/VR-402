# Feedback research decision log

A record of **working decisions**, not approvals or test outcomes. Update this file when evidence or supervisor feedback changes a decision.

| Decision | Current position | Basis | Unresolved gate |
|---|---|---|---|
| Educational framing | Use goal → evidence → next step, plus self-reflection and instructor dialogue | Hattie & Timperley [1]; Nicol & Macfarlane-Dick [2] | Test fit with intended users |
| Primary audience | Distinct learner and instructor views, linked to the same source evidence | Existing worksheet and project needs [P1]; proposed design | Confirm users and use cases |
| Unit of attribution | Retain team-level attribution unless source evidence supports individual role attribution | Risk of false individual blame | Confirm role and SME rules |
| Feedback presentation | Compare raw worksheet, generic summary and theory-structured views | Alternative-method rationale | Prototype and empirical comparison pending |
| Priority | No automatic clinical severity score or fixed top-three ranking | No validated prioritisation rule available | Clinical expert review |
| Evidence | Keep traceable spans, category, polarity and uncertainty | Existing manuscript [P1] | Inspect real export schema and permissions |
| Validation | Start with source-fidelity checks before learner-effectiveness studies | Research design logic | Mechanical v0.1 checks reproduced; independent fidelity/quality and user studies pending |

## How to update

Add a dated entry documenting the question, alternatives, evidence reviewed, decision, responsible reviewer and consequences. Preserve earlier decisions rather than rewriting history. Do not label an assumption “validated” until actual evidence supports it.


## 25 October 2026 — evaluation constructs

Broadened the principal immediate outcomes from gap identification to feedback comprehension, corrective learning-plan quality and instructor debrief preparation quality. Gap recognition remains a component of comprehension. Fidelity and quality are assessed separately; later communication performance addresses learning effectiveness. This is a design decision, not a result or approval. Full unanswered RQ-B1–B3 and status are recorded in the [research scope](problem-and-scope.md#questions) and [evaluation protocol](../report-evidence.html#evaluation).


## Version 0.1 progress — 25 October 2026

The workbook-to-feedback generator is implemented in local deterministic mode. A new reproduction harness confirmed 21 workbooks and 371 populated annotation cells (AI 40, CT 268, NN 63), with zero count mismatches and exact extracted cell text for the tested layouts. Three learner/instructor report pairs retain displayed pointers and annotations and repeat deterministically. These are mechanical checks, not complete event-level fidelity or educational validation.

Observed issues are 40/40 unverified AI polarities, default AI display of 14/40 records, a missed ampersand-form category header, generic actions, unverified individual attribution and limited context. Five synthetic characterisation tests pass while preserving the frozen defects. Clinical review, independent full-event fidelity review, user testing, external-model execution and learning-effectiveness results remain outstanding.

See [the reproduced evaluation](../evaluation-v01.html), [source and run commands](../../../prototype/feedback/v0.1/README.md) and [aggregate results](../results/v01-aggregate.json). RQ-B1 is partially examined through mechanical checks; feedback quality, immediate educational usefulness (RQ-B2) and later performance (RQ-B3) remain unanswered.
