# Feedback transformation: methodology and alternatives

**Status:** proposed research method, not implemented or experimentally compared.

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

## Candidate fidelity evaluation (not yet performed)

Choose a small permission-cleared set of source-linked positive and negative instances across at least two categories; construct baseline and candidate views from the **same evidence**. Independently check source traceability, category/polarity preservation, role attribution, omitted context, unsupported claims, balanced positive evidence and action-label clarity. Record denominators, discrepancies and revisions. This evaluates transformation fidelity, **not** learning improvement. Subsequent expert/learner studies require their own protocols and approvals.
