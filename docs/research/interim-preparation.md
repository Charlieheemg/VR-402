# VR-405 interim preparation and Part B handover

## Assessment map

Requirements below are transcribed from the user-provided brief; confirm exact dates and final submission arrangements with the course.

| Criterion | Main report location | Review evidence / unresolved action |
|---|---|---|
| A1 Objective, scope, context | §§1–2 | Clinical communication context; construct boundary; original research citations |
| A2 Method / concept | §§2–4 | Alternative constructs; RQ1–3; labelled outcomes; fold and baseline choices |
| A3 Prototypes | §4; Part B B2 | Existing extractor, historical classifiers and paired/local demo; Part B artifact pending |
| A4 Testing | §§4–6 | Reproduction scripts, test suites, corpus/hash checks; listener protocol proposed |
| A5 Analysis | §§5–7 | Paired 25-item changes; R2SPIN OOF metrics; single-speaker/cluster limitations |
| A6 Problems and plan | §7; Part B B3 | Access obstacle addressed with public Edinburgh; measured labels still missing; gates and scope |

Group interim weighting 40%; ≤30 minute presentation, Semester 1 Week 12; Pages due end Week 13; ≤4,000 main words excluding appendices. Complete group report target 3,600–3,800. `python3 scripts/check_report.py` conservatively counts main headings/captions and draft Part B; references and appendices are outside `main`. Do not add Part B without recounting and tightening Part A if needed.

## Suggested consecutive presentation (28 minutes, with 2-minute margin)

- Shared problem and contribution boundary: 3 minutes.
- Charlie, construct choice and methods: 5 minutes.
- Charlie, matched audio and Edinburgh findings: 4 minutes.
- Charlie, R2SPIN scope, limitations and next validation: 4 minutes.
- Kang Zhe, feedback needs and alternatives: 4 minutes (requires his evidence).
- Kang Zhe, prototype, actual testing and limitations: 5 minutes (requires his evidence).
- Shared scope, milestones and decisions: 3 minutes.

Use readable units, paired-change definitions, speaker/listener/sample counts and citations beside claims. Prepare to explain why duration is not rate, `sil` is not a verified pause, ASR feedback differs from acting for a computer, and held-out lists do not imply held-out speakers. Do not fill Kang Zhe's slots with invented results.

## Kang Zhe's required Part B contribution

1. State the target users and debriefing decisions; provide literature/user evidence and design requirements.
2. Compare feedback representations and explain the chosen alternative.
3. Add authored sketches/prototype, implementation status and approved examples.
4. Define usefulness/usability/comprehension tests; report actual sample, procedure, observations and limits, or label them proposed.
5. Add references, figures/captions and a feasible work plan; identify authorship and any dependencies on Charlie's output.

Aim initially for approximately 800–950 substantive words; replace the draft placeholders and rebalance Part A to reach 3,600–3,800 for the completed group. No artificial integration is needed. Proposed common fields: recording reference, time span, metric/value/unit, measurement method, quality flag, evidence status; agree them before implementing an exchange format.

Write invitation sent to KayZzee17; acceptance required. The normal Git workflow is in WORKFLOW.md. Coordinate edited sections, pull before work, and review staged changes; do not force push. Restricted audio stays local.

## Three next actions

1. Kang Zhe accepts the invite and contributes evidence-backed Part B material; group confirms Week 12/13 dates.
2. Charlie audits a multi-speaker human-labelled source (SLUSI first) for audio/excerpt/target alignment, rights and split feasibility; retain R2SPIN as an audibility/context benchmark.
3. Perform manual timing/pitch quality checks and agree the first speaker-disjoint validation protocol; rehearse the consecutive presentation against the 30-minute cap.

## Conditional milestones

| Gate | Owner | Timing / completion evidence |
|---|---|---|
| Evidence and report consolidation | Charlie | Current commit: scripts, aggregate data, cited limitations |
| Part B evidence and rehearsal | Kang Zhe, then both | Before Week 12: attributable materials, tested presentation ≤30 minutes |
| Complete group report | Both | End of Week 13: replace placeholders, recount ≤4,000, inspect live Pages |
| Dataset and measurement audit | Charlie, supervisor decision | Next research block: verified label/audio join and manual quality results |
| Human validation | Charlie, with approved protocol | Only after access/ethics and evaluation gates; no recruitment date assumed |
