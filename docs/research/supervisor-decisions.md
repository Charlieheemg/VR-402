# Charlie's interim meeting sheet

## What I can show now

An operational matched-audio Edinburgh demo and reproduced one-speaker acoustic contrasts; existing R2SPIN human keyword-recognition benchmark with its two-speaker/list-fold limitations. A new 12-recording independent pitch check finds tracker/parameter sensitivity, so pitch remains an automated estimate. Two TextGrid end gaps remain explicit and unrepaired. No direct speaker-side intelligibility improvement, feedback efficacy or clinical transfer has been demonstrated.

## Decisions to leave the meeting with

| Decision | Recommendation / prepared evidence | Who needs to resolve it |
|---|---|---|
| Data route | Check NUS access to SLUSI/LDC2024S02 first; require exact scored-excerpt alignment. Clarity only if the hearing-aid/listener-conditioned question is acceptable | Charlie + supervisor/library; no purchase or agreement accepted |
| Research scope | Keep recognition as outcome, with speaker delivery as candidate predictors; do not rename style labels as intelligibility | Supervisor |
| Measurement review | Ask for a phonetics-capable reviewer for flagged pitch/boundaries; use the 12-clip review sheets and retain original annotations | Charlie + reviewer |
| Human fallback | Review the proposed 6-speaker / 24-listener logistics pilot and consent/ethics route; counts are not a power argument | Supervisor/institution |
| Existing VR pipeline | Obtain current architecture/code or a system owner walkthrough: what audio enters WhisperX/MERaLiON/fusion, what outputs exist, where timestamps/labels are retained | Supervisor/system owner; current repo does not establish deployed capabilities |
| Group submission | Kang Zhe supplies his authored Part B evidence; confirm course dates and consecutive presentation split | Both students |

No messages have been sent to the supervisor, library or collaborator as part of this work.

## Answers to rehearse

**What did Edinburgh establish?** Matched delivery differences for one speaker across 25 texts. It has no verified human recognition labels, so it cannot establish intelligibility improvement.

**Why not simply reward slower speech or greater pitch range?** Those are measurements, not universal objectives. Instructions can alter different features, and recognition depends on listeners, words, context and channel. Efficiency also matters; the effect must be tested against listener outcomes.

**What changed after quality checking?** We found two annotation coverage gaps and now quantify tracker disagreement/parameter sensitivity. We preserved the source and demo and narrowed the interpretation. Instrument checks and tracker agreement do not replace human reference review.

**Why R2SPIN?** It provides real human keyword correctness for a bounded masking/context benchmark. Its acoustic glimpse measure concerns audibility; it does not validate our timing/F0 predictors or unseen-speaker transfer.

**Why not train on Clarity immediately?** Only its small evaluation-label package has been inspected. The training audio/metadata join is unverified, the population is hearing-aid users, and archive terms differ from the landing-page badge. We must first settle the intended question and use training-only development.

**What is the concrete next contribution?** A verified speaker-diverse human-outcome join, reviewed measurements, and a prespecified acoustic-increment comparison against context and frozen ASR baselines. New participants are a fallback after access/ethics decisions.

**Is the existing system transcript-only?** No such claim is justified. Previous project context describes audio components; their exact deployed inputs/outputs are not independently verified in this repository. The proposed contribution is explicit, auditable delivery evidence and outcome validation, subject to a system audit.

## Before presenting

Select one A/B audio pair and its units/limitations; keep a screenshot ready. Rehearse Charlie's slot against the shared presentation allocation; record actual timings and unanswered questions. The slides, human review, system-owner confirmation and rehearsal have not been completed by these documents.
