# Consolidation validation — 19 October 2026

## Completed checks

- Independent full-corpus Edinburgh extraction and annotation parsing: 125 original MKH800 recordings, one speaker, 25 sentence IDs in five conditions. Paired timing/F0 summaries recomputed; 125 audio hashes match the earlier local inventory; all WAVs mono/16 kHz; annotation bounds and continuity checked.
- R2SPIN pinned `AllData.csv` matches the downloaded table byte-for-byte. 6,400 responses/16 listeners; four fixed logistic comparisons independently refitted with eight held-out-list folds. Earlier context / context+KWGP figures reproduced. No demographic/identifier/response-order/retake predictors; scaling inside folds. Shared speaker/listener and recurring-keyword limitations documented.
- Reading-confidence models independently refitted from saved 600-row acoustic feature table; pooled balanced accuracy and macro F1 match historical metrics to 1e-10. Raw feature extraction and human ratings were not repeated.
- 19 existing prototype tests pass; 3 Edinburgh demo tests pass; 5 new evidence contract tests pass (27 total). These tests do not establish perceptual validity.
- Main report: 3,027 conservative whitespace words including main headings, captions and draft Part B. Title/navigation/references/appendices excluded. Regenerate with `python3 scripts/check_report.py`. Below 4,000; complete group target 3,600–3,800 after Part B replaces placeholders.
- HTML5 parser: no errors. CSS stylesheet parser: no errors. Existing demo JavaScript syntax check passes. No JavaScript in main report.
- Internal main-report file references/anchors, unique IDs, image alt text and official metadata checked. All five SVG images load in browser. Conceptual figures labelled; empirical figures generated from aggregate CSVs with units/sample sizes, zero baselines and no invented uncertainty intervals.
- Browser review at desktop and narrow mobile sizes: readable text; document scroll width equals viewport width; figures have independent horizontal scrolling on small screens. Screenshots retained locally in project `exports/`. Browser viewport override reset afterwards.
- External report links checked: no 404/410 responses. Two publisher endpoints return 403 to automated direct requests (ACM openSMILE and ASHA Gutz); their canonical sources were corroborated through the web research tool. A 2xx response confirms reachability, not citation correctness; claim scope was reviewed separately in the source audit.
- Original demo measurements/audio preserved; visible branding updated to official VR-405. The historical PVC report and methods are retained and explicitly marked superseded.

## Remaining scientific limitations

Single-speaker Edinburgh effects cannot support population/clinical inference. `sil` labels do not necessarily represent perceptual pauses; composite labels remain indivisible. Pitch accuracy, phone-aligned formants and vowel-space analysis remain unvalidated. No human Edinburgh recognition labels identified. R2SPIN keyword glimpse proportion is audibility under masking, not validated speaker-side delivery assessment. No intervention efficacy or integrated-system claim. No Part B implementation or test results supplied.

See `reproduction.json` for environment and source hashes, `report-checks.json` for machine-readable checks and `external-link-checks.json` for per-URL status. Deployment is verified after the repository push; commit/push and live publication are distinct steps.
