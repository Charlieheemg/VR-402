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

Group interim weighting 40%; ≤30 minute presentation, Semester 1 Week 12; Pages due end Week 13; ≤4,000 main words excluding appendices. Complete group report target 3,600–3,800. `python3 scripts/check_report.py` conservatively counts main headings, tables, captions, draft Part B and visible SVG figure text; references and appendices are outside `main`. It also reports separate shared/Charlie/Kang Zhe allocations and replacement capacity. Do not add Part B without recounting and tightening Part A if needed.

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

Aim initially for **1,500–1,600 substantive words**, replacing the placeholders. The refinement conservatively counts visible figure labels as well as HTML. With 2,191 non-Part-B words, a 1,500–1,600-word Part B yields 3,691–3,791 group words. The replacement capacity is 1,809 words at the absolute 4,000 limit; 1,800 leaves only nine words of margin. Recount after adding tables, captions or figures, and rebalance if necessary. No artificial integration is needed. Proposed common fields: recording reference, time span, metric/value/unit, measurement method, quality flag, evidence status; agree them before implementing an exchange format.

Write invitation sent to KayZzee17; acceptance required. The normal Git workflow is in WORKFLOW.md. Coordinate edited sections, pull before work, and review staged changes; do not force push. Restricted audio stays local.

## Three next actions

1. Kang Zhe accepts the invite and contributes evidence-backed Part B material; group confirms Week 12/13 dates.
2. Charlie audits a multi-speaker human-labelled source (SLUSI first) for audio/excerpt/target alignment, rights and split feasibility; retain R2SPIN as an audibility/context benchmark.
3. Perform manual timing/pitch quality checks and agree the first speaker-disjoint validation protocol; rehearse the consecutive presentation against the 30-minute cap.

## Deliverables, prerequisites and contingencies

| Stage / responsibility | Deliverable | Prerequisites | Completion criterion | Major risk and contingency |
|---|---|---|---|---|
| Before interim — both; each owns authored section | Evidence-backed Parts A/B, cited figures, presentation | Kang Zhe supplies his materials; course confirms dates | Group main ≤4,000 words; aim 3,600–3,800; all claims linked to evidence; rehearsal ≤30 min | Missing evidence → keep draft explicit, agree minimum scope with supervisor; never fabricate results |
| Before interim — Charlie | Reviewed research evidence and PR | Current raw data/OOF caches; protected main | Annotation discrepancy and per-list audits attached; checks pass; PR reviewed before merge | Review delays → present current published version plus clearly labelled proposed revision |
| Next scientific milestone — Charlie | Measurement-quality audit and dataset-access/alignment decision | Permission-compatible multi-speaker human-labelled data; representative audio | Exact audio/excerpt/transcript/outcome join verified; speaker IDs usable; boundary and pitch review documented | Missing identities or access → audit alternative source; retain production claims only |
| Predictive validation — Charlie, supervisor approves design | Small interpretable feature-set evaluation with context/ASR baselines | Trustworthy measures/labels; enough independent speakers; fixed protocol | Speaker-disjoint splits where feasible; fold-local training; calibration/generalisation analysis; test set untouched | Too few speakers or label mismatch → narrow claims, seek better data; do not treat list CV as speaker CV |
| Longer term — Charlie for recognition/efficiency trial, Kang Zhe for feedback design, both coordinate | Approved feedback experiment and eventual exchange contract | Measurement/prediction gates; permissions and ethics; author-owned prototypes ready | Independent listener recognition and correct words/minute compared under controlled conditions; usable feedback evidenced separately | Approval/data delays → synthetic examples and permitted design walkthroughs; no efficacy claim or forced integration |

No firm experimental dates are assigned where access, feasibility or ethics are unresolved. Week 12/13 assessment timing is user-supplied and requires course confirmation. Sample sizes are undecided: use a feasibility pilot then power/precision considerations accounting for speaker/listener clustering.
