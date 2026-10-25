# Part B — Feedback Presentation and End-User Debriefing (Working Draft)

**Project:** VR-405, Paediatric VR Speech Analysis and Feedback (repository URL: VR-402)  
**Contribution:** Ang Kang Zhe  
**Status:** Problem, pedagogical framework and proposed design methodology only. No feedback prototype or evaluation is claimed here. This supporting document is not yet incorporated into the word-limited main report.

## B1. Problem definition and research objectives

Multi-user paediatric resuscitation simulation allows teams to rehearse communication, but an automated assessment is not automatically effective educational feedback. Learners must be able to identify the observed behaviour, understand the evidence and criterion used to assess it, and decide what to practise next. Feedback effects vary with content and implementation; simply providing a score or judgement does not establish learning benefit [1]. A systematic review of technology-enhanced healthcare simulation found substantial research on debriefing but limited or mixed comparative evidence for particular debriefing features [2]. These sources motivate careful design and testing; they do not prove that the existing project worksheet is inadequate.

The project-supplied manuscript, *Structured Discourse Modelling for Automated Team Communication Feedback in Paediatric VR Resuscitation Training* [P1], describes role-attributed, timestamped transcripts, discourse-thread reconstruction and expert-rubric-aligned positive/negative communication-behaviour instances linked to supporting utterances. Its learner-facing output is a worksheet. Its preliminary feedback comparison included four teams in each condition, and the automated worksheet and human debrief differed in interactivity as well as content. The findings are promising but cannot establish that a new presentation format is superior. Publication and external peer-review status of this manuscript remain to be confirmed.

**Design question:** How can evidence-linked automated communication assessments be presented as role-relevant, comprehensible post-simulation feedback that supports reflection and actionable next steps without overstating certainty or clinical importance?

**Objectives:** (1) preserve traceability from each feedback claim to an observed communication event; (2) tailor feedback to the learner's role and observed behaviours while retaining team context; (3) connect an approved performance criterion, observed evidence, reflective question and next-practice action; and (4) justify the proposed presentation format against alternatives before prototype testing. Personalisation here means role- and performance-specific feedback; it does not imply knowledge of a learner's preferences, psychological attributes or underlying competence.

## B2. Pedagogical framework

**Hattie and Timperley — feedback information [1].** Their review organises feedback around three questions: where am I going, how am I going, and where to next? We propose mapping these to an expert-approved communication criterion, the relevant observed utterances and a feasible improvement opportunity. This is a design translation, not an experimentally validated VR adaptation.

**Healthcare simulation debriefing — INACSL [3].** The Healthcare Simulation Standards of Best Practice provide the clinical-education context for structured post-event debriefing. Our proposed interface should support reflection and appropriate facilitator involvement rather than claim to replace expert-led discussion. The current edition and bibliographic details of the debriefing standard should be verified before final submission.

**Nicol and Macfarlane-Dick — self-regulated learning [4].** Their framework argues for formative feedback that supports learners in monitoring and regulating their learning. We therefore propose including a reflection prompt and a learner-selected next-practice goal. Because the original framework addresses higher education broadly, its transfer to paediatric emergency trainees remains a hypothesis.

These frameworks have distinct roles: feedback content, simulation-debriefing process and learner agency. Their combination is an **author-proposed synthesis**, not a separately validated educational framework.

| Principle | Proposed interface element | Evidence boundary |
| --- | --- | --- |
| Clear goal [1] | Named communication behaviour and approved criterion | Final seven-category behavioural anchors require expert confirmation |
| Evidence of current performance [1] | Relevant utterances, timestamps and context | Transcript and discourse-model errors are possible |
| Next step [1] | Concrete reflection or practice suggestion | A suggestion is not proven to improve performance |
| Structured debrief [3] | Post-simulation guided review, compatible with facilitation | A static interface is not equivalent to human debriefing |
| Learner agency [4] | Reflection question and learner-selected goal | Learner engagement and comprehension remain untested |

## B3. Proposed design methodology

**Inputs and provenance.** The project manuscript describes instance-level outputs with speaker/role attribution, utterance identifiers and timestamps, rubric categories, positive/negative assessments and supporting evidence [P1]. Before implementation, the actual available export schema, permission to display excerpts or replay audio, and rubric definitions must be checked with the system owner and clinical experts. Do not assume a validated confidence score, severity rating or audio-replay link already exists.

**Alternatives.** A score dashboard offers a rapid overview but can obscure the evidence behind a judgement. A transcript-first timeline preserves sequence and context but may require extensive reading. Evidence-linked cards with a compact summary and timeline links may combine relevance and traceability, at the cost of additional selection logic and interface complexity. These are qualitative design trade-offs, **not measured rankings**. Cards are the provisional preferred format, subject to review and testing.

**Proposed processing and presentation steps:**

1. **Verify:** retain only attributable instances with sufficient supporting evidence and a defensible link to an approved rubric criterion; flag uncertainty and missing context. Absence of a transcript acknowledgement does not necessarily prove absence of non-verbal acknowledgement.
2. **Select:** organise examples by participant role and observed behaviour, while retaining team context. Consider reliability, educational relevance and redundancy. Do not equate negative polarity with clinical severity; severity-based prioritisation needs clinical-expert criteria.
3. **Compose:** for each selected instance, show the target behaviour, a concise observation, evidence link/timestamp, carefully bounded interpretation, reflection question and possible next-practice action. Include examples of effective behaviour, not only shortcomings.
4. **Navigate:** offer a concise overview and links to the relevant episode rather than an unsupported overall competence score.
5. **Review:** subsequently compare design variants for traceability, clarity, actionability, burden and feasibility. No such testing has yet been performed.

**Provisional design requirements:** DR1 source traceability; DR2 approved rubric alignment; DR3 role relevance; DR4 actionable reflection; DR5 explicit uncertainty and avoidance of unsupported clinical judgements; DR6 navigation to original context; DR7 suitability for post-simulation debriefing. These are proposed requirements, not verified specifications.

**Open decisions:** obtain the seven-category rubric and behavioural anchors; verify the existing pipeline's actual output fields; ask clinical experts about selection and severity; confirm data permissions; and assess how erroneous or ambiguous assessments should be handled. Prototype status, evaluation, analysis and future milestones are deliberately deferred to later updates.

## References and source boundaries

1. Hattie, J., & Timperley, H. (2007). The power of feedback. *Review of Educational Research*, 77(1), 81–112. https://doi.org/10.3102/003465430298487 — conceptual/review foundation; not a VR trial.
2. Cheng, A., Eppich, W., Grant, V., Sherbino, J., Zendejas, B., & Cook, D. A. (2014). Debriefing for technology-enhanced simulation: A systematic review and meta-analysis. *Medical Education*, 48(7), 657–666. https://doi.org/10.1111/medu.12432 — healthcare simulation synthesis; specific format comparisons require caution.
3. INACSL Standards Committee. *Healthcare Simulation Standards of Best Practice: The Debriefing Process*. https://www.inacsl.org/healthcare-simulation-standards-of-best-practice — check current edition and complete citation before final submission.
4. Nicol, D. J., & Macfarlane-Dick, D. (2006). Formative assessment and self-regulated learning: A model and seven principles of good feedback practice. *Studies in Higher Education*, 31(2), 199–218. https://doi.org/10.1080/03075070600572090 — higher-education framework; clinical transfer is proposed.
5. [P1] Project-supplied manuscript: *Structured Discourse Modelling for Automated Team Communication Feedback in Paediatric VR Resuscitation Training*, Online Submission ID 1911. Publication and peer-review status unverified; do not reproduce figures without appropriate permission.

**Evidence status:** This is a targeted foundational reading list, not a systematic review or a verified journal-quartile ranking. No new user testing, expert review, implementation or educational effectiveness is claimed.
