# Feedback transformation: methodology and alternatives

**Status:** design specification with a local deterministic v0.1 implementation and preliminary engineering evaluation. Individual routing and full-event source verification remain incomplete.

## Input and evidence contract

The existing research-team manuscript [P1] describes rubric category, positive/negative assessment and evidence-linked utterance spans; role/timestamped speech and thread structure underpin the pipeline. The **actual export schema, reliability fields, permissions and availability of audio replay remain to be verified**. Do not assume confidence values, clinical-severity ratings or stable playback URLs exist.

For each feedback instance, preserve where available: source reference, approved category/definition, observed polarity, supporting utterance IDs/span, timestamp, speaker/role, team context, evidence status and any explicit ambiguity. A generated explanation must never replace or silently alter source evidence.

## Proposed transformation steps

1. **Evidence gate:** check that the original rubric judgement and supporting span can be located. Flag incomplete or uncertain records; do not silently convert transcript absence into a definitive behavioural failure.
2. **Attribution gate:** decide whether the observation belongs to a speaker, role or team. Team-level observations must not automatically become individual blame.
3. **Audience routing:** learner view emphasises one's own observable actions and team context; instructor view emphasises team patterns and discussion opportunities.
4. **Educational structure:** display expected behaviour, observed evidence, cautious interpretation, self-reflection question and candidate next action, informed by [1–3]. Retain positive and negative examples.
5. **Navigation:** provide summary plus evidence-linked drill-down; show all seven categories without inventing a clinical severity hierarchy.
6. **Fidelity check (future):** compare each statement against the original annotation and transcript; log errors and revisions.

## Alternatives to compare

| Option | Plausible benefit | Risk or cost | Evidence status |
|---|---|---|---|
| Existing worksheet | Detailed instances and traceability | May require users to infer learning goals and actions | Existing project format [P1] |
| Generic LLM summary | Fast, compact presentation | Omission, unsupported inference and inconsistent attribution | Not yet benchmarked in this workstream |
| Theory-structured learner/instructor views | Explicit goal/evidence/reflection/action chain | Requires design effort, expert review and fidelity controls | Candidate concept, not validated |

## Selection and prioritisation

Separate **validity** (is this assessment supported?), **routing** (who should see it?) and **emphasis** (which items deserve discussion first?). Clinical severity, frequency and actionability may be discussed as candidate criteria, but there is no approved weighting model. Do not equate a red label with a clinically serious event. Do not conceal lower-ranked categories without a justified policy.



## Evaluation framework (25 October 2026)

RQ-B1 — Feedback fidelity and quality: Can learner- and instructor-facing feedback preserve assessment evidence, meaning, category/polarity and defensible individual/team attribution? How clear, relevant and actionable is the output when assessed separately? RQ-B2 — Immediate educational usefulness: Compared with generic feedback from identical evidence, does theory-guided feedback improve learner comprehension, corrective learning-plan quality and instructors’ preparation of accurate, actionable debriefs? RQ-B3 — Subsequent learning effectiveness: Does theory-guided feedback improve communication performance in subsequent simulation scenarios? All three questions remain unanswered. The original assessments and expert annotations belong to the upstream research team.

RQ-B1 has partial mechanical evidence; quality, RQ-B2 and RQ-B3 remain untested. The [evaluation protocol](../report-evidence.html#evaluation) distinguishes:

1. **Feedback fidelity and quality:** preserve source traceability, rubric/category/polarity, meaning, supported attribution and contextual repairs; log unsupported additions. Assess clarity, recipient relevance and actionability separately. There is no validated combined score.
2. **Immediate educational usefulness:** learner comprehension (including gap recognition) and corrective learning-plan quality; instructor accuracy, usefulness and quality of debrief preparation. Compare generic LLM and theory-guided outputs from identical evidence; worksheet is an optional baseline. Time is secondary. A plan or intention is not observed uptake.
3. **Subsequent learning effectiveness:** independently assessed communication in comparable later scenarios using the seven competencies. Candidate balance rate B=(G-R)/(G+R) is undefined at G+R=0 and depends on event definitions, annotation practices, team dependence and comparable behavioural opportunities. Later VR performance does not establish retention, workplace transfer or patient benefit.

This hierarchy is a project-specific synthesis. Design pedagogies remain Hattie–Timperley and Nicol–Macfarlane-Dick. Evaluation draws on Carless–Boud (feedback literacy), Cook–Hatala (validity), Johnson et al. (FQI), Kirkpatrick and digital-feedback assessment literature; see the [reference register](../references.md#evaluation-literature). The FQI concerns conversations and is not validated for a static AI report.

**Progress:** local v0.1 implementation and reproducible engineering checks are documented in the [evaluation](../evaluation-v01.html). Source-span fidelity, clinical expert review, external-model generation, user testing and educational outcomes remain pending.


## Version 0.1 progress — 25 October 2026

The workbook-to-feedback generator is implemented in local deterministic mode. A new reproduction harness confirmed 21 workbooks and 371 populated annotation cells (AI 40, CT 268, NN 63), with zero count mismatches and exact extracted cell text for the tested layouts. Three learner/instructor report pairs retain displayed pointers and annotations and repeat deterministically. These are mechanical checks, not complete event-level fidelity or educational validation.

Observed issues are 40/40 unverified AI polarities, default AI display of 14/40 records, a missed ampersand-form category header, generic actions, unverified individual attribution and limited context. Five synthetic characterisation tests pass while preserving the frozen defects. Clinical review, independent full-event fidelity review, user testing, external-model execution and learning-effectiveness results remain outstanding.

See [the reproduced evaluation](../evaluation-v01.html), [source and run commands](../../../prototype/feedback/v0.1/README.md) and [aggregate results](../results/v01-aggregate.json). RQ-B1 is partially examined through mechanical checks; feedback quality, immediate educational usefulness (RQ-B2) and later performance (RQ-B3) remain unanswered.
