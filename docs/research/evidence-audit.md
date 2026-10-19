# VR-405 evidence audit — 19 October 2026

Official title: **Paediatric VR Speech Analysis and Feedback**. Charlie Hee Ming Guan: speech analysis. Ang Kang Zhe: feedback presentation. Supervisor: A/Prof Khoo Eng Tat. The repository and Pages URLs retain `VR-402` as a technical address, not the official project code.

## Repository before consolidation

Branch `main`, base `8bd5373`, origin `Charlieheemg/VR-402`, upstream `edic-nus/template`. Pages: legacy branch deployment, `main`, `/`, HTTPS, built. Fast-forward pull: already up to date. Only untracked `prototype/pvc/edinburgh/` belonged to the previously requested local demo; preserved and included as intended work. No tracked uncommitted changes, other student commits, or Part B deliverables found in the inspected checkout/history. No reset or force push.

| Evidence | Implemented | Tested / reproduced | Interpretation / missing evidence |
|---|---|---|---|
| Existing VR assessment | Context and example outputs documented | Exact deployed implementation not audited here | Transcript-based teamwork assessment is project context, not a new system built in this task |
| PVC extractor | 88 eGeMAPSv02 + temporal descriptors; local live/paired tools | Existing unit suite; local acoustic demonstrations | Not a universal confidence or competence score; energy gates are not validated VAD |
| Children's reading benchmark | 600 labelled items; classifiers; fixed-fold ablations | Independent refit from existing feature table reproduces balanced accuracy 0.3333 / 0.7160 / 0.7813 | Recording-level folds; no verified speaker map; no new extraction claimed |
| Edinburgh demo | Nine clips from three matched sentence sets, browser UI, original audio | Browser decoding/control checks and existing demo tests recorded previously | Operational demonstration does not validate intelligibility |
| Edinburgh full corpus | This consolidation extracts all 125 WAVs and parses all 125 genuine hand-corrected TextGrids | Paired annotation timing and F0 summaries recomputed; hashes retained locally | One speaker; uncertainty markers and composite labels; automatic F0 not manually validated |
| Exploratory vowel work | Legacy functionals include F1/F2 summaries | Separate phone-aligned formant validation package not located | No vowel-space plot or reliability claim published |
| R2SPIN | Public AllData.csv reacquired, 6,400 observations | Eight held-out-list folds independently refitted; earlier rounded figures reproduced | Two speakers, 16 shared listeners; keyword reuse across lists; no unseen-speaker claim |
| Part B | Responsibility established by user | No attributable design/research/test artifacts located | Explicit draft handover; nothing invented |
| RQ3 feedback intervention | Concept and protocol proposal | Not implemented or tested | No learning, efficiency or intelligibility benefit established |

The requested later Edinburgh/R2SPIN audit packages were not found in the checkout, project exports, attachments, or focused Documents/Downloads filename search. This task therefore recomputed the available analyses rather than attributing absent files as completed work.

## Preservation and privacy

Historical report snapshot: `docs/research/historical-pvc-report.html` (dated, superseded). Existing code, results, tests, templates and Git history retained. Historical documents describe the earlier research state; the current main report supersedes their forward-looking PVC plans. The original working local demo and private corpus were not overwritten by the new full-corpus analysis.

Keep WAVs, TextGrids, participant rows/demographics, named children's recordings, row-level features/OOF predictions, archives, models and screenshots containing private data under ignored local folders. Public evidence is our own code, documentation and aggregate summaries/figures. Do not publish the private audit ZIPs. Edinburgh lists a Depositor Agreement rather than an explicit general redistribution licence. R2SPIN README declares CC BY 4.0; we nonetheless publish aggregates only. Reading-confidence release: non-commercial research use; no raw redistribution assumed.

## Collaboration

GitHub API initially reported KayZzee17 read-only. A `permission=push` invitation was created successfully, invitation ID `338478568`, normal write permission. Acceptance remains pending; no administrator permission granted. Settings: https://github.com/Charlieheemg/VR-402/settings/access

## Assessment basis

User-supplied brief: group of two; interim 40%; ≤30 minute presentation in Semester 1 Week 12; Pages report due end of Week 13; ≤4,000 main words excluding appendices. No official brief attachment was located to independently authenticate these requirements or assign exact calendar deadlines. Target final group draft: 3,600–3,800 words after Part B is supplied. Do not equate an incomplete Part B scaffold with a completed group submission.
