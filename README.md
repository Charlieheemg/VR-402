# VR-405 · Paediatric VR Speech Analysis and Feedback

NUS CDE4301 interim report by **Charlie Hee Ming Guan** (speech analysis) and **Ang Kang Zhe** (educational feedback), supervised by **A/Prof Khoo Eng Tat**.

**[Read the report](index.html)** · **[Appendices and evidence](docs/evidence.html)** · **[Submission QA](docs/submission-review.md)**

`index.html` is the authoritative report. `interim-report.html` is a compatibility redirect that preserves section links. The official project code is VR-405; `Charlieheemg/VR-402` remains the repository and Pages address. The live [GitHub Pages site](https://Charlieheemg.github.io/VR-402/) serves `main`; review-branch changes appear there only after an approved merge and deployment.

## What was investigated

- **Charlie:** whether acoustic evidence could support interpretation within the existing seven-category rubric. Completed work includes reading-confidence classification, private laughter-event demonstrations, emotional-delivery perception, Edinburgh production analysis and the R2SPIN recognition precursor. Their evaluation scopes differ; none establishes clinical rubric improvement.
- **Kang Zhe:** transformation of existing assessment worksheets into learner/instructor feedback. A frozen deterministic v0.1 and engineering evaluation establish extraction/report feasibility and identify fidelity/coverage defects. Educational benefit remains to be tested.

The feedback prototype does not consume speech-model predictions. Both contributions and their limitations are presented in the report; historical hypotheses are labelled in the [history register](docs/history.md).

## Preview and verify

No frontend installation or build is required. From this directory:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
# Open http://127.0.0.1:8000/
python3 scripts/check_report.py
python3 scripts/check_repository.py
python3 -m unittest discover -s scripts -p 'test_submission.py'
```

The report checker includes headings, tables, diagram text, captions, inline citations **and references** in the 4,000-word cap. Appendices are separate. The repository check validates published HTML and Markdown destinations and checks the tracked tree for prohibited raw-data types.

Additional checks use the project's scientific/feedback dependencies:

```sh
python3 scripts/test_refinement.py
python3 prototype/feedback/v0.1/test_generator.py -v
```

`test_refinement.py` requires pandas/numpy; feedback tests require openpyxl. These inspect committed aggregates and synthetic inputs. They do not require clinical data or fit research models. Full historical tests/reproduction that need private data are documented separately in [speech reproduction](docs/methodology/reproduction.md) and the [frozen feedback README](prototype/feedback/v0.1/README.md). Do not interpret an unavailable private-data rerun as a completed check.

## Repository map

| Location | Purpose |
| --- | --- |
| `index.html`, `index.css` | Authoritative report and shared academic styling |
| `docs/evidence.html` | Examiner entry point to appendices A–D |
| `docs/speech-evidence.html`, `docs/results/` | Speech methods, aggregates and diagnostics |
| `docs/feedback/` | Feedback research, engineering evidence and approved redacted specimen |
| `prototype/feedback/v0.1/` | Frozen evaluated baseline; do not silently repair it |
| `prototype/pvc/` | Retained speech implementations; PVC naming is historical |
| `scripts/` | Checks and historical analysis/reproduction tools |
| `docs/history.md` | Superseded plans, prior report revisions and immutable study links |

## Data and publication

No clinical recordings, identifiable workbooks, restricted reading audio, private feature rows or fitted models should be committed. `.gitignore` is not an access-control system. Clinical event demonstrations remain private; public aggregate evidence does not make the underlying recordings redistributable. The CREMA-D study is cited at its existing immutable commit; its separate software PR is not implicitly merged.

Use a dedicated branch and review PR. See [WORKFLOW.md](WORKFLOW.md). This submission-preparation branch does not merge, deploy or submit on behalf of the authors.
