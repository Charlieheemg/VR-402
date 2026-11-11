# Editing and publishing VR-405

The authoritative report is `index.html`; `interim-report.html` preserves older links. The official code and repository name are VR-405; the remote is `Charlieheemg/VR-405`.

1. Inspect `git status`, recent remote commits and open PRs. Preserve collaborators' uncommitted work.
2. Fetch `origin` and create a dedicated branch from the agreed base. Never force-push or reset shared work.
3. Edit the report and relevant documentation. Preserve original results and the frozen feedback v0.1; changes to research methods require separate validation.
4. Run `python3 scripts/check_report.py`, `python3 scripts/check_repository.py` and the relevant tests in the README. Recount references, captions and diagram text. Inspect desktop/mobile and print layouts.
5. Review the exact staged diff, privacy boundaries and `git diff --check`. Commit only intended files and push the review branch.
6. Open a PR documenting changes, tests and unresolved decisions. Obtain author/team review before merge. Supervisor/clinical decisions apply to the proposed study, not retrospective approval invented by the report.
7. After an explicitly authorised merge, verify the Pages deployment from `main` at `/`, open the published report and record the submission SHA. A successful push is not evidence of a successful deployment or course submission.

Do not upload raw clinical audio, identifiable workbooks, restricted datasets, private model files or the supplied manuscript. Prior report versions remain recoverable through Git history; do not create a second competing report at the root.

Official brief checked: CDE4301 AY2026 interim assessment, page 1, two-person group maximum 4,000 words excluding appendices, due end of Semester 1 Week 13. The supplied Canvas instructions require the published website URL, submitted by one group member. Follow the [Canvas handoff](docs/submission.md); confirm the exact calendar deadline and required declarations with the course. No deployment, supervisor message or course submission is automatic.
