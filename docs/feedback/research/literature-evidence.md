# Literature evidence and design implications

**Purpose:** distinguish what publications actually support from our proposed implementation. This is a focused reading matrix, **not** a systematic review, journal-quartile certification or claim of validated efficacy.

| Source | Evidence type / relevant contribution | Proposed application | Transfer limitation |
|---|---|---|---|
| Hattie & Timperley (2007) [1] | Influential conceptual/review account of feedback: goal, current performance and next steps; effects are not uniformly beneficial. | Show target behaviour, specific observation and next-practice suggestion. | Does not validate an AI-generated VR feedback card. |
| Nicol & Macfarlane-Dick (2006) [2] | Formative assessment/self-regulated learning framework, including self-assessment, dialogue and opportunities to close gaps. | Reflection prompt, learner-owned practice goal and instructor discussion prompt. | Primarily higher-education context; transfer to clinical teams is untested here. |
| Shute (2008) [3] | Review of formative feedback characteristics and design considerations. | Prefer task-specific, usable information over generic evaluative labels. | Not a direct comparison of this project's proposed interfaces. |
| Kluger & DeNisi (1996) [4] | Meta-analysis/theory showing feedback interventions can help or hinder performance. | Avoid person-level labels and unsupported blame. | Does not prescribe specific UI layout or priority weights. |
| Cheng et al. (2014) [5] | Systematic review/meta-analysis of debriefing for technology-enhanced simulation. | Position the proposed feedback as post-simulation debrief support. | Comparative evidence about particular debriefing features is limited/mixed. |
| Cooper et al. (2010) [6] and Malec et al. (2007) [7] | Teamwork measurement instruments relevant to clinical simulation. | Background for the project's SME-derived teamwork categories. | Neither is a validated scoring algorithm for our redesigned feedback. |
| Project manuscript [P1] | Existing rubric-labelled, utterance-linked assessment and worksheet; preliminary descriptive study. | Define available input evidence and a baseline presentation. | Publication status unverified; do not claim that this workstream generated its findings. |

## Theory-to-design map (hypotheses)

| Construct | Candidate element | Evidence check needed |
|---|---|---|
| Feed up / goal [1] | Approved behavioural target | Expert confirms rubric anchor |
| Feed back / current performance [1] | Short observation + original utterance link | Source and role attribution verified |
| Feed forward [1] | Specific next-practice suggestion | Mark as proposed; expert reviews appropriateness |
| Self-assessment [2] | Reflective learner question | Later comprehension/reflection testing |
| Feedback dialogue [2] | Instructor debrief question | Instructor usability review |
| Evidence traceability [P1] | Timestamp/utterance reference and context | Match against original annotation |

**Do not infer from theory alone:** a clinically valid top-three list, numeric severity weights, a mandatory card layout, or educational superiority of the proposed format. See [method alternatives](../methodology/feedback-transformation.md).


## Evaluation literature and construct boundaries

| Source | Evaluation rationale | Application limit |
|---|---|---|
| Carless & Boud (2018) | Judgement and action distinguish comprehension from actual feedback uptake. | Learning plans indicate intended action, not observed use. |
| Cook & Hatala (2016) | Evidence must support intended assessment interpretations and uses. | Upstream validity does not automatically validate the feedback transformation. |
| Johnson et al. (2021), FQI | Candidate domains for performance discussion and improvement planning. | Developed for conversations; not validated for static AI feedback. |
| Kirkpatrick Partners; Johnston et al. (2018) | Distinguish reactions, learning, behaviour and results in training evaluation. | Later simulation performance does not demonstrate workplace transfer or patient benefit. |
| Duran Espinoza et al. (2024) | Scoping review identifies limited digital-feedback assessment evidence. | Does not supply a validated instrument for this interface. |

See [verified bibliographic records](../references.md#evaluation-literature) and the [evaluation protocol](../report-evidence.html#evaluation). Fidelity, subjective quality, immediate educational usefulness and later performance remain separate constructs. RQ-B1 has partial mechanical evidence; feedback quality, RQ-B2 and RQ-B3 remain untested; full definitions are maintained in the [research scope](problem-and-scope.md#questions).


## Version 0.1 progress — 25 October 2026

The workbook-to-feedback generator is implemented in local deterministic mode. A new reproduction harness confirmed 21 workbooks and 371 populated annotation cells (AI 40, CT 268, NN 63), with zero count mismatches and exact extracted cell text for the tested layouts. Three learner/instructor report pairs retain displayed pointers and annotations and repeat deterministically. These are mechanical checks, not complete event-level fidelity or educational validation.

Observed issues are 40/40 unverified AI polarities, default AI display of 14/40 records, a missed ampersand-form category header, generic actions, unverified individual attribution and limited context. Five synthetic characterisation tests pass while preserving the frozen defects. Clinical review, independent full-event fidelity review, user testing, external-model execution and learning-effectiveness results remain outstanding.

See [the reproduced evaluation](../evaluation-v01.html), [source and run commands](../../../prototype/feedback/v0.1/README.md) and [aggregate results](../results/v01-aggregate.json). RQ-B1 is partially examined through mechanical checks; feedback quality, immediate educational usefulness (RQ-B2) and later performance (RQ-B3) remain unanswered.
