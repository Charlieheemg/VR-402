# Follow-up validation — 19 October 2026

This extends the review branch; no research model was fitted and the original demo was not rewritten. Existing regression tests may fit temporary synthetic fixtures; those are not new scientific results.

## Executed checks

- **34 tests passed:** 19 existing PVC tests, 3 Edinburgh demo tests, 12 research/report tests (including 4 new quality/protocol tests).
- Actual pitch diagnostic executed on 12 originals at two Praat settings: 24 result rows. Known 100/150-Hz tones within 1 Hz; silence unvoiced. All three private review sheets generated and visually inspected by the assistant. No trained human reference review is claimed.
- All **125 original WAV SHA-256 hashes match the existing demo inventory**. Original source/demos/annotations have no tracked edits. No timing summary or historical benchmark was regenerated/replaced.
- Small CPC1 archive MD5 matches official release; two real label-file schemas counted. Included licence text read. No audio downloaded from this new source, no new audio/outcome join claimed, no evaluation-label modelling performed.
- Proposed assignment schedule regenerated and checked for no repeated text per listener, equal styles and speaker exposure, and two assignments per hypothetical clip. It contains **288 assignments**, not human responses or measured outcomes.
- Main report count: **2,279 words**, including **205 SVG words**; Charlie **1,837**, shared **356**, placeholder Part B **86**. Non-Part-B **2,193**; a replacement 1,500–1,600-word Part B yields **3,693–3,793**. Absolute replacement capacity **1,807**.
- Main HTML local links, unique IDs, image alt text, title/authorship metadata and group capacity checks passed. Refreshed the existing local report browser and confirmed the new evidence links and corrected source/access wording appear.
- New document links and staged whitespace/privacy checks are verified before committing. Original restricted WAVs, TextGrids, downloaded archives, individual label rows, dependency directories and private plots are excluded from Git.

## Run the checks

```sh
prototype/pvc/.venv/bin/python -m unittest discover -s scripts -p 'test_*.py'
prototype/pvc/.venv/bin/python -m unittest discover -s prototype/pvc -p 'test_*.py'
prototype/pvc/.venv/bin/python -m unittest discover -s prototype/pvc/edinburgh -p 'test_*.py'
python3 scripts/check_report.py
python3 scripts/pilot_assignments.py
python3 scripts/audit_dataset_access.py
```

Private input prerequisites and pitch dependency/plot instructions are linked from [pitch-quality-review.md](pitch-quality-review.md) and [dataset-decision.md](../research/dataset-decision.md). Existing demo remains at `http://127.0.0.1:8765/demo/`; branch report preview at `http://127.0.0.1:8766/`. The demo was not rebuilt and audio playback was not newly re-auditioned in this follow-up. The published main-branch site remains separate until PR review/merge.

Operational checks establish reproducibility and preservation, not human intelligibility benefits, clinical usefulness, trained annotator agreement, statistical power or an approved recruitment protocol.
