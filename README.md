# VR-405 — Paediatric VR Speech Analysis and Feedback

NUS CDE4301 Innovation & Design Capstone, group interim working report.

- **Charlie Hee Ming Guan** (`Charlieheemg`): speech analysis and assessment.
- **Ang Kang Zhe** (`KayZzee17`): feedback presentation and end-user debriefing.
- **Supervisor:** A/Prof Khoo Eng Tat.

[Research report](https://Charlieheemg.github.io/VR-402/) · [Repository](https://github.com/Charlieheemg/VR-402)

**Official code is VR-405.** The repository name, local folder and Pages URL retain `VR-402` to preserve links/remotes; this is a technical address, not a separate project. The report has consecutive contributions; integration is not claimed. Part B is an explicitly incomplete handover awaiting Kang Zhe's authored materials.

## Read and reproduce

- [Evidence inventory and privacy](docs/research/evidence-audit.md)
- [Measurement definitions and reproduction](docs/methodology/reproduction.md)
- [Human-listener validation proposal and ethics](docs/methodology/listener-validation.md)
- [Rubric map / presentation / Part B handover](docs/research/interim-preparation.md)
- [Sources and claim boundaries](docs/references/source-audit.md)
- [Local Edinburgh demo](prototype/pvc/edinburgh/README.md)

Static HTML/CSS; no frontend framework or build step. Preview with `python3 -m http.server 8000 --bind 127.0.0.1` from this folder. Main report: `index.html`; style: `index.css`. `python3 scripts/check_report.py` checks local references, metadata and a conservative ≤4,000-word limit. Aggregate results are in `docs/results/`; three main-report figures (plus retained supplementary assets) have sources/renderers in `scripts/make_figures.py` (pandas/matplotlib needed only to regenerate figures).

Retain earlier PVC code and documents as historical evidence. Current direction: acoustic measurements and human speech intelligibility, with no clinical or intervention effectiveness established. Raw recordings, participant rows, model binaries, archives and phonetic annotations stay in ignored local locations. Public aggregates do not authorize raw corpus redistribution.

See [WORKFLOW.md](WORKFLOW.md) for collaboration and publishing. Pages publishes `main` at `/`; verify a successful deployment separately from a successful push.

## Focused refinement (review branch)

The refinement is proposed in a separate PR; `main` and the published report remain unchanged until review/merge. It adds construct/research-design matrices, conservative per-contribution word budgets, an annotation-coverage discrepancy audit and per-list summaries of existing OOF predictions. No model fitting is needed for this review:

```sh
prototype/pvc/.venv/bin/python scripts/audit_refinement.py
python3 scripts/check_report.py
```

See [measurement audit](docs/results/measurement-audit.md) and [refinement review](docs/research/refinement-review.md). The older `reproduce_evidence.py` is retained for full historical reproduction and does train models; it was **not** run during this refinement.
