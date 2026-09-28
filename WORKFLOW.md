# Editing and publishing the report

Run commands from this repository folder.

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
- `assets/`: figures and media cleared for publication; includes original template examples.
- `components/`: original EDIC reusable components, available for later use.
- `README.md`: project/setup overview.
- `WORKFLOW.md`: these instructions.
- `.nojekyll`: serve this as a plain static website.

## Remotes and Pages

`origin` must be your own fork. `upstream` is https://github.com/edic-nus/template.git. Check using `git remote -v`.

In your repository: Settings → Pages → Deploy from a branch → main → / (root) → Save.
The site URL will be https://Charlieheemg.github.io/VR-402/.
Do not automatically merge upstream template changes into the report; review them first.

## Before interim submission

- Confirm official title, supervisor and required submission process.
- Replace every scaffold paragraph with actual report content.
- Check citations, figure captions, links and mobile layout.
- Include only real results, clearly separating completed work from proposed work.
- Keep restricted papers, participant recordings, personal data and credentials out of this public report repository. Ignored folders are a convenience, not an access-control mechanism.
- Verify the live site after the final push. Record the submission commit hash with `git rev-parse HEAD` and optionally add a dated submission tag after agreeing the final version.

## Asking for help next time

“Update my FYP report in this repository. Pull first if the working tree is clean, make the changes, show me the diff, then commit and push.”
