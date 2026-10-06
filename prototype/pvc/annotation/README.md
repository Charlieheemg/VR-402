# Local PVC human-rating tool

Standard-library Python server; no package install, model download, external API or acoustic features in the rater view. Responses save after each clip, before moving on. This collects judgements; it does not establish their reliability automatically.

## Start

From the repository root:

```sh
python3 prototype/pvc/annotation/serve.py --clips "/absolute/path/to/approved_clips"
```

Open **http://127.0.0.1:8765**. Give each listener a distinct pseudonymous rater ID, e.g. `rater_01`. Each sees one randomly ordered clip at a time, the exact requested question/anchors/reminder, and an optional note. Ratings start blank. Playback must start before saving a numeric response (this is a UI check, not proof of full listening). “Unable to rate” records a blank score plus `rating_status=unrateable`; it does not assign 3. Reload and re-enter the same ID to resume remaining clips. The uncompleted order is reshuffled on resume.

The operator prepares the clip folder before rating. Use reviewed, consented **single-speaker** WAV segments with stable neutral filenames (`clip_001.wav`, etc.). A filename stem becomes `clip_id`; avoid names suggesting Before/After, expected confidence, participant identity or correctness. The UI shows clip number only, but filenames are visible in URLs/CSV to an inspecting user, so neutral IDs matter. Keep the same audio and playback policy for every listener. Do not use the full session-length Team Leader demonstrations as validated single-speaker annotation units.

A UI-only demonstration can use a disposable folder of test clips and a distinct output directory. Label those responses as software tests and never merge them into the study. **No actual human ratings are bundled here.**

## Save and export

Default storage: `prototype/pvc/private/annotation/<rater_id>.csv` (Git-ignored). Each save is atomic. A duplicate `(clip_id, rater_id)` is rejected instead of silently overwriting; corrected ratings need an explicitly reviewed data-cleaning decision. The export link downloads the same saved CSV, and the on-disk CSV remains available if the browser download fails. Stop the app with Ctrl-C after use.

CSV columns:

```text
clip_id,rater_id,pvc_score,notes,timestamp,rating_status,audio_sha256,definition_version
```

Scores are integers 1–5 or blank for unrateable. Timestamp is UTC ISO 8601. CSV quoting preserves commas, quotes, newlines and Unicode notes; import notes as text in spreadsheet software. Hashes allow checking that listeners heard identical audio. `definition_version` is `PVC v0.1`.

Use `--output /path/to/private/study_directory` for a different study and `--port 8766` if needed. Keep the source clip set unchanged during a study; use a new output folder for a revised clip set or protocol. Audio hashes are rechecked before serving a clip and before saving a rating; a changed or missing clip is rejected while the server is running. Changed audio under an already-rated clip ID is also detected after restarting. Do not run two server processes against the same output folder. This is a trusted local workstation tool, not an authenticated multi-user service; IDs distinguish raters but do not authenticate them. The server binds only to loopback and does not publish recordings.

## Multiple raters: minimal proposed protocol

1. Agree PVC v0.1 and the unit of judgement with the speech expert. Decide whether to retain the combined neutral/unclear anchor. Pilot the instructions on a separate practice set, then freeze them for collection.
2. Have multiple independent listeners rate the **same clips** using the same listening setup/policy, blind to one another's responses, acoustic features, clinical correctness and model predictions. Three or more raters is a practical pilot proposal, not a validated minimum or sample-size calculation. Retain separate speaker and session metadata with the researcher, not in the rating view.
3. Concatenate exports into long-format rows. Check `definition_version`, clip hashes, unique rater IDs and duplicate `(clip_id, rater_id)` pairs. Do not count repeated exports as new raters. Keep unrateable/missing entries explicitly missing and report their frequency/reasons; never replace them with 3.
4. Inspect rating distributions and disagreements **before** aggregation. Proposed `pvc_score` for training is the mean of valid independent listener ratings per clip, conditional on a pre-agreed minimum rater count. Retain each raw score, count, median, SD/range and missing count. The mean treats the ordinal scale as approximately continuous; this is a modelling choice, not proof that steps are perceptually equal. Do not fill low-coverage clips with guessed values.
5. Build a rater-by-clip matrix and assess agreement. An ordinal Krippendorff's alpha is a candidate for multiple raters and missing ratings; explicitly choose ordinal distances, inspect uncertainty and use a vetted implementation rather than writing a new estimator. If treating ratings as continuous, discuss an absolute-agreement ICC: identify random/fixed rater assumptions, single-rater versus mean-rating estimand, number of raters and confidence intervals. Correlation alone does not establish agreement. Do not declare a reliability cutoff or compute reliability from these software-test fixtures.
6. Resolve systematic disagreement with the speech expert; revise to v0.2 on a new pilot if needed. Join accepted aggregates to features by verified `clip_id`/audio hash and researcher-held `speaker_id`, then use the existing speaker-grouped training scaffold. Agreement supports consistency of measurement, not correctness/competence or internal-confidence validity.

References: [Krippendorff, Computing Alpha-Reliability](https://www.asc.upenn.edu/sites/default/files/2021-03/Computing%20Krippendorff%27s%20Alpha-Reliability.pdf); [Hughes, krippendorffsalpha package paper](https://journal.r-project.org/articles/RJ-2021-046/); [Koo & Li, ICC selection/reporting](https://pmc.ncbi.nlm.nih.gov/articles/PMC4913118/). See the [PVC construct definition](../../../docs/pvc_definition_v0_1.md).
