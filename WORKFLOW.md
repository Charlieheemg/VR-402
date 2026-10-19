# VR-405: editing and publishing the group report

Official title: Paediatric VR Speech Analysis and Feedback. Charlie Hee Ming Guan (speech analysis) and Ang Kang Zhe (feedback presentation), supervised by A/Prof Khoo Eng Tat. `VR-402` remains the repository/Pages address only. Historical PVC documents are preserved; the main report supersedes their earlier scope.

Run commands from this repository folder.

## Collaborative refinement review

For this academic refinement, branch from current main, push the dedicated branch and open a pull request. Do not merge or publish automatically: the live Pages report stays on `main` until review. Check remote commits/open PRs first, preserve both authors' work, and recheck the group word budget including new Part B tables/figures. The everyday publication workflow below applies only when a later reviewed merge/publication is authorized.

## Everyday workflow

1. Check for unfinished edits: `git status`. Commit those or ask for help before pulling.
2. Pull your latest saved work: `git pull --ff-only origin main`.
3. Edit `index.html`; put approved figures in `assets/`; change styling in `index.css`.
4. Preview: `python3 -m http.server 8000 --bind 127.0.0.1`, then open http://localhost:8000. Stop with Control-C.
5. Review: `git diff` and `git status --short`.
6. Stage only intended files, e.g. `git add index.html index.css`.
7. Review the exact commit: `git diff --cached` and `git diff --cached --check`.
8. Save a snapshot: `git commit -m "Update research question and objectives"`.
9. Upload: `git push origin main`.
10. Check the GitHub Pages deployment, then open the live site to confirm the update.

A commit is a local snapshot. A push uploads commits to GitHub. Pages publishes the report from those uploaded files. Pull downloads and incorporates updates from your own GitHub repository.

If a pull or push is rejected, stop and inspect the message; do not force-push or delete files. `--ff-only` makes pull stop if histories diverge, rather than creating an unexpected merge.

## Repository layout

- `index.html`: report home page and sections.
- `index.css`: report styling.
- `assets/`: FYP figures and media cleared for publication.
- `components/`: retained generic EDIC image/video, team-member, references and navigation helpers; unused example demos removed.
- `README.md`: project/setup overview.
- `WORKFLOW.md`: these instructions.
- `.nojekyll`: serve this as a plain static website.

## Remotes and Pages

`origin` must be your own fork. `upstream` is https://github.com/edic-nus/template.git. Check using `git remote -v`.

In your repository: Settings → Pages → Deploy from a branch → main → / (root) → Save.
The site URL will be https://Charlieheemg.github.io/VR-402/.
Do not automatically merge upstream template changes into the report; review them first.

## Before interim submission

- Confirm exact Week 12 presentation and Week 13 report deadlines; title and supervisor are now recorded above.
- Complete Kang Zhe’s Part B from his evidence; do not invent results. Target 3,600–3,800 group words; run `python3 scripts/check_report.py` (limit 4,000).
- Check citations, figure captions, links and mobile layout.
- Include only real results, clearly separating completed work from proposed work.
- Keep restricted papers, participant recordings, personal data and credentials out of this public report repository. Ignored folders are a convenience, not an access-control mechanism.
- Verify the live site after the final push. Record the submission commit hash with `git rev-parse HEAD` and optionally add a dated submission tag after agreeing the final version.

## Asking for help next time

“Update my FYP report in this repository. Pull first if the working tree is clean, make the changes, show me the diff, then commit and push.”
