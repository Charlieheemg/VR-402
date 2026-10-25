# FYP interim research documentation (Semester 1, 2026)

**Project:** VR-405 — Paediatric VR Speech Analysis and Feedback (repository URL retains VR-402). The broader research package also uses the working title “Virtual Paediatric Patient Simulation: Immersive VR for Respiratory Emergency Training and AI Instructor Feedback (2610-00172)”; confirm the official naming with the supervisor before final submission.  
**Working subproject:** Theory-guided post-simulation communication feedback for learners and instructors  
**Status:** Interim research and concept development; redesigned feedback has **not** been validated. This is a supplementary research folder, not the final word-limited group report.

## Research problem and value proposition (CDE4301 A1)

An existing VR training and automated evaluation pipeline already extracts evidence-linked, positive/negative communication-behaviour instances across seven expert-derived categories. Its output is a detailed worksheet. This project investigates the *downstream educational design problem*: how to reorganise those existing assessments into feedback supporting individual self-regulation and instructor-led team debriefing, without claiming to improve the upstream classifier.

**Working research question:** How can formative-feedback and self-regulated-learning principles guide the restructuring of existing AI-derived communication assessments into useful post-simulation feedback for learners and instructors?

**Hypotheses for later testing, not results:** structured feedback may improve comprehension of performance gaps, corrective-action planning and instructor debrief preparation compared with the current worksheet. Whether it improves later simulation performance is unknown.

## Existing work and boundaries (A1, A5)

The project team's *Structured Discourse Modelling for Automated Team Communication Feedback in Paediatric VR Resuscitation Training* manuscript describes speech transcription, discourse-thread reconstruction, seven SME-derived communication categories, evidence-linked worksheet output and expert-comparison results. Study 1 compares a structured pipeline with a flat-transcript baseline; Study 2 compares automated worksheet review and human debrief across two simulations. These results belong to the **existing research team**, not to the current feedback-redesign contribution. The manuscript is labelled an online submission; publication status is unverified.

Study 2's primary outcome is change in balance rate, B=(G-R)/(G+R), from S1 to S2, where G and R are positive and negative annotated behaviour instances. Its small four-team-per-condition sample supports descriptive interpretation only. The balance rate is a possible future behavioural outcome, not proof of learning retention or transfer.

The seven categories are: Roles & Responsibilities; Closed Loop Communication; Clear Messages; Knowing One's Limitations; Constructive Intervention; Summarisation & Re-evaluation; Knowledge Sharing. The manuscript says these were informed by TEAM and the Mayo High Performance Teamwork Scale, with clinical expert refinement; they were **not solely derived from TEAM**.

## Method and concept selection (A2)

The primary educational foundation is Hattie & Timperley (2007), *The Power of Feedback*, and Nicol & Macfarlane-Dick (2006), *Formative Assessment and Self-Regulated Learning*. The first distinguishes feed up (goal), feed back (current performance), feed forward (next step), and task/process/self-regulation/self feedback levels. The second proposes seven principles including clarifying standards, self-assessment, feedback dialogue, opportunities to close gaps, and assessment information for teaching.

Theories justify a *structured feedback process*, not a numeric clinical-risk score, an arbitrary top-three ranking, or individual blame from team events. Self-prioritisation was considered but is not the primary pedagogy. The working design deliberately retains all seven competency categories, evidence links, and positive as well as negative examples.

## Proposed outputs (A3)

- **Learner report:** expected behaviour -> evidence-linked observed behaviour -> discrepancy -> self-assessment prompt -> next-practice action. Role attribution must be checked; team findings are not automatically individual failures.
- **Instructor report:** team-level overview across seven categories -> positive/negative observations and their evidence -> possible debrief questions -> potential group practice goals. No unsupported severity or competency ranking.

See [theory-to-design matrix](docs/02_theory_to_design.md) and [feedback examples](examples/feedback_concepts.md).

## Preliminary work and what it does *not* establish (A4, A5)

Twenty expert-annotation workbooks from ten matched session IDs (CT and NN) were inventoried in a separate working analysis. A previous preliminary extraction found 268 CT and 63 NN populated annotation cells; these are **cells**, not independent events, comparable rates, or inter-rater reliability estimates. Annotation density and span alignment differ, so raw counts must not be interpreted as learning need or severity. The inventory is a data-feasibility check, **not a completed prototype test or validated outcome analysis**.

A proposed lightweight feasibility test before interim: choose 2-3 expert-annotated episodes, transform them using a written rule sheet into learner/instructor mockups, and independently check evidence traceability, rubric-category fidelity, role attribution, and unsupported claims. Record pass/fail and revisions. This test is planned; results must not be fabricated.

## Risks and milestones (A6)

1. **Now:** freeze theoretical constructs, document source evidence and draft paired mockups. Preserve expert workbook provenance.
2. **Before interim:** run a small documented traceability/attribution feasibility check; compare old worksheet, generic LLM summary, and theory-structured mockup conceptually, without implying user-study results.
3. **After expert access:** confirm full SME rubric, individual attribution rules, clinical-severity judgments, and feedback-priority criteria.
4. **Later:** implement transformation and conduct expert review; then recruit learners/instructors for appropriately approved evaluation.

## Research ownership and confidentiality

Existing VR/LLM pipeline, manuscript results and consultant gold standards were supplied by the research team. The current proposed contribution is the **downstream educational feedback structure and its planned evaluation**. Clearly identify each student's individual work in the final group report. Do not upload identifiable patient/participant data, raw consultant workbooks, private manuscript, or unapproved transcripts to a public repository. Obtain permission before sharing research-team assets even in a private repository.

## Repository integration note

This folder is intentionally self-contained. It does not replace the repository root `README.md`, the existing `kang-zhe-feedback-foundation.md`, or `index.html`. The original foundation draft remains as an earlier snapshot; this package adds later research material for review. No changes to Charlie’s files or the published website are included.

## Documentation map

- [Interim rubric alignment](docs/01_interim_rubric_alignment.md)
- [Theory-to-design matrix](docs/02_theory_to_design.md)
- [Research method and evaluation plan](docs/03_method_and_plan.md)
- [Presentation preparation and full discussion summary](docs/04_presentation_brief.md)
- [Feedback concept examples](examples/feedback_concepts.md)
- [References](docs/05_references.md)
