# Refinement validation record

## Branch and preservation

Base `668000db0c78ed59d672a2b588c88e48bcf68572`; dedicated `refine-interim-evidence-and-word-budget` branch. Main was unchanged and no open collaborator PR/material was found at initial audit. The refinement will be pushed as a PR, not merged or deployed. No prototype, original acoustic aggregate, original annotation, WAV, historical report or fitted model was modified. Existing historic tests/docs are retained.

## Checks actually run

- `scripts/audit_refinement.py`: all 125 original TextGrids reparsed; duration/annotation summaries match the existing recording table; published paired and condition-median timing summaries reproduce. Exactly two >0.05-s undercoverage cases found; n=25 retained with separate n=23 sensitivity summaries. No automatic repair.
- Existing R2SPIN table SHA-256 matches the pinned source record. Saved OOF response order/targets match; all four pooled model summaries reproduce. Per-list metrics calculated from those existing predictions, with no research estimator fit or tuning. Both primary metrics improve across all eight lists, with dependence and magnitude limits stated.
- Existing nine-demo F0 values agree with the full-corpus cache. Definition/configuration checked. No fresh feature family, manual pitch validation, vowel-space result or human study added.
- Tests: 19 existing prototype tests + 3 local Edinburgh demo tests + 8 evidence/report contract tests passed (30 total). Some existing unit tests fit synthetic toy estimators; no new research benchmark was trained. Raw WAV identity, mono/16-kHz format, annotation bounds/continuity and new coverage/budget regressions are included. Coverage completeness is separate from interval bounds.
- HTML5 parsing: no errors. CSS parse: no errors. All SVG assets parse. Main report remains static HTML/CSS; no JavaScript added or changed.
- Main-report local links/anchors, metadata, duplicate IDs, image alt text and separate word budgets checked. Count now includes visible SVG labels as well as tables/captions/headings: see `report-checks.json`. Masthead/navigation/references/appendices and duplicated SVG accessibility titles excluded. Text-only count retained for comparison with the older 3,027-word method.
- Browser inspected at requested desktop and narrow-screen viewports (rendered CSS widths 984 and 300 in the app). Figures load, page scroll width matches viewport, tables keep readable columns with their own horizontal overflow, and keyboard-right scrolling of the focused design matrix was observed (~30.77 CSS pixels). Desktop matrix/context and mobile screenshots retained locally under project `exports/`. Viewport override reset.
- All report external links requested: no 404/410. ACM, Gutz, Bosker and AHRQ endpoints return 403 to automated direct requests; sources were corroborated via primary publisher/official/author records in the web tool. Reachability is distinct from claim validity. See `external-link-checks.json` and the updated source audit.
- Staged-file privacy and diff checks required before commit: only documentation, own code, derived aggregate audits and a conceptual SVG; no raw WAV/annotations, participant rows, archives, credentials or models intended for staging.

## Limits

These checks establish implementation/data consistency under declared rules, not human-perception validity. Infant tail silence is an automatic-label interpretation, not independently confirmed. Single-speaker production results, automated F0, R2SPIN two-speaker/shared-listener dependencies, untested speaker-side RQ2 and future RQ3 efficacy remain explicit. Kang Zhe must author Part B; supervisor input is still needed on target conditions, access/ethics and pilot/precision criteria.
