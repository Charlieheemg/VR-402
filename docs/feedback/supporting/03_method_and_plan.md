# Research design and evaluation plan

## Research objectives

- **O1:** derive explicit feedback structure from established formative-feedback and self-regulated-learning theory.
- **O2:** generate learner and instructor mockups from the *same* evidence-linked expert-aligned assessments.
- **O3:** assess fidelity and feasibility of transformation before clinical consultation.
- **O4 (future):** test whether theory-guided feedback adds value over existing worksheet and generic LLM summary.

## Research questions

- RQ1: Can behaviour-instance annotations be faithfully transformed into theory-structured feedback while preserving provenance and appropriate individual/team attribution?
- RQ2: Does theory-structured feedback improve identification of performance gaps and corrective actions versus raw worksheet or generic LLM summary?
- RQ3: Does feedback support better subsequent communication performance or instructor debrief preparation? (Requires future empirical study.)

## Initial feasibility protocol (planned; no results yet)

1. Select 2-3 de-identified, source-linked behavioural episodes from the expert files, covering positive and negative examples and at least two competencies.
2. Record source workbook, sheet, cell/span, category, polarity, speaker and contextual dialogue.
3. Produce raw worksheet excerpt, generic LLM summary (fixed documented prompt), and theory-guided learner/instructor versions from the same evidence.
4. Blind-check each factual statement against original span; tag unsupported or ambiguous inferences, role misattribution and omitted positive evidence.
5. Use a transparent checklist: source traceable? category preserved? polarity preserved? correct unit (individual/team)? target stated? gap stated? corrective suggestion labelled as proposal? no invented severity/score?
6. Summarise counts of passed checks and concrete revisions. Do not equate feasibility with learning effectiveness.

## Future study design (proposal)

Possible three conditions: raw Excel; standard-prompt LLM summary; theory-guided feedback. Use matched input evidence, random allocation where feasible, and blinded expert rating of action plans. Candidate immediate outcomes: gap-identification accuracy, corrective-plan quality, review time, perceived relevance, and instructor preparation quality. Candidate behavioural outcome: S1-to-S2 change in the existing study's balance rate B=(G-R)/(G+R), with careful handling of absent annotations and baseline differences. Retention/transfer requires additional scenarios and cannot be inferred from immediate S2.

## Data and validity risks

- Expert gold standard validates assessment annotations, **not feedback educational priority**.
- Prior research's 4 teams per condition did not permit inferential comparison of automated vs human feedback.
- Transcript-only scoring can miss non-verbal acknowledgment; individual attribution may be uncertain.
- Different consultant annotation density makes raw cell totals unsuitable as performance scores.
- Balance rate does not adjust for opportunity difficulty or clinical severity.
- Instructor summaries must retain positive evidence, uncertainty and original excerpts.

## Milestones

| Period | Deliverable | Gate |
|---|---|---|
| Before interim | literature/construct matrix and two audience mockups | theory mapping checked |
| Before interim if feasible | small traceability feasibility check | documented protocol/results |
| First expert meeting | confirm full rubric, source use permissions, role attribution and severity definitions | signed-off design assumptions |
| After interim | implement versioned transformation pipeline | reproducibility |
| Later | controlled feedback evaluation | ethics/participant availability |
