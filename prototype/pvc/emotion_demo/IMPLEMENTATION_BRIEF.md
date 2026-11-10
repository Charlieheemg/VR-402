# VR-402 — Codex Handoff: Audio Beyond Transcript Demo
**Version:** 0.1 | 31 October 2026
**Target:** Runnable, rehearsable offline demonstration by Sunday, 1 November. Full mock deck by Monday night, 2 November. Professor review Tuesday, 3 November. Slide submission Wednesday, 4 November.

## Objective
Build a **credible minimal demonstration** that two recordings of the **same sentence** carry different vocal-delivery information that disappears when each is represented only by its transcript. This is an initial *proof of information loss and acoustic measurement feasibility*, **not** a validated system that judges overall communication quality, medical performance, speaker's true emotion, or intelligibility.

The overall project asks whether acoustic and paralinguistic evidence extracted from original speech can complement transcript-only communication assessment and eventually support more nuanced feedback in paediatric VR emergency training.

## Source datasets and provenance (official sources)
1. **RAVDESS:** Livingstone & Russo, 2018; https://zenodo.org/records/1188976 ; speech-only 1,440 WAVs, 24 actors, 2 fixed sentences, multiple acted emotions and intensities. Licence: **CC BY-NC-SA 4.0**. Audio filenames encode: modality-channel-emotion-intensity-statement-repetition-actor; use the official naming guide, not guesses. Human validation ratings are available separately in publication/data supplements.
2. **CREMA-D:** Cao et al., 2014; https://github.com/CheyneyComputerScience/CREMA-D ; 7,442 clips, 91 actors, 12 fixed sentences, 6 acted emotions, 4 intensity codes. Licence: **ODbL 1.0 database, DbCL contents**, see original licence. The repository has `processedResults/tabulatedVotes.csv` and other ratings; be explicit whether an emotion displayed is the **acted label** or an independently aggregated **audio-only human perception** rating. Dataset homepage provides mirror details; avoid cloning large videos.
   - convenient preview/download mirror if necessary: https://huggingface.co/datasets/cfahlgren1/crema-d (record which mirror and transformations were used).

## Required deliverables
- A **local, offline-capable**, presentation-friendly web page or app, added under a self-contained `prototype/audio_beyond_transcript/` directory (or equivalent, after inspecting existing repo conventions). Do not break earlier prototypes.
- RAVDESS tab: 2 or more handpicked **same actor, same statement, same repetition** comparisons with distinct emotions (e.g. neutral vs angry), with playback A/B, plain transcript revealed side by side, waveform or simple figure, and clearly labelled acoustic metrics.
- CREMA-D tab: 3–5 same actor/same sentence examples across delivered emotions, with easy playback and source labels. Show a qualitative 'same words, different delivery' result, not 'same words, different literal meaning'.
- Metrics for each clip, carefully named: audio duration, RMS level in dBFS, median voiced pitch F0 and pitch range if robustly extractable, and a silence/low-energy fraction **only if the algorithm and caveats are documented**. Optional pitch contour, RMS envelope. Distinguish within-file relative volume measurements from real vocal SPL or absolute loudness. No invented articulation rate, vowel-space area, confidence score, clinical severity or 'communication quality %'.
- Comparison panel: values for A vs B and plain-language, **measurement-grounded** observations such as 'the measured median F0 is higher in B' or 'B has more variation in measured intensity'. Do not infer the speaker's internal emotional state. If optional perceptual labels are shown, mark them "dataset acted label" or "independent audio-only listener ratings".
- Optional (only after core works): a separate clearly identified *exploratory* model-prediction panel using a fixed pretrained audio emotion classifier, with documented model/version and zero-shot caveats, no train/test contamination claim and no conflation of source labels with predictions. Do not make this a critical path to Sunday success.
- Maintain a `manifest.csv` containing dataset, licence, source URL, filename, actor, sentence, delivery label, and whether any human-perception rating is actually included; audio paths relative to repo. Include citations in UI/README.
- A README with **one-command local launch**, setup requirements, sample provenance, expected output, demo script under 90 seconds, offline fallback and limitations.
- Automated sanity checks where feasible: pairing shares same sentence/actor; decoded filenames match manifest; transcript equality for the A/B samples; metric function gives reproducible output; missing data produce clear errors rather than silent fallbacks.

## Data access constraints
- First inspect repo and existing feature-extraction code and reuse components when practical.
- Download or select **only a handful of small WAV clips** initially. Avoid entire dataset download unless remote individual-file acquisition is impractical; RAVDESS official speech-only archive is ~215 MB if necessary.
- Never commit large full corpora or copyrighted/third-party data without reviewing sharing rights; `.gitignore` bulk datasets. Keep demo clips properly attributed and obey each licence.
- Do not assume HF clone supports direct filenames or that URL examples work; check remote availability. If download fails, provide an 'import sample WAVs' workflow and a sample selection list rather than fabricating audio.
- Preserve the audio source unmodified; if preprocessing/resampling is needed for measurement, log it.

## Presentation acceptance test
On the local laptop, with **Wi-Fi disabled**:
1. Launch the app within one minute.
2. Click RAVDESS clip A and clip B: they audibly differ but display identical transcripts.
3. Show 2–3 measurements with units and visibly different measured values.
4. Switch to CREMA-D and play multiple contrasting deliveries of a single sentence.
5. Clearly distinguish independent labels, measured features, and *any* model predictions.
6. State limitations: acted emotions and different recording conditions are not clinical outcome labels; no universal speech-quality score; no proof of improved VR learning yet.

## Implementation process
Work in three phases, in order, stopping at each checkpoint:
- **Phase 1:** source-data verification and clip manifest, reproducible measurements, RAVDESS A/B playback.
- **Phase 2:** CREMA-D examples, presentation layout, documentation and local/offline test.
- **Phase 3 (optional):** exploratory classification or LLM explanation, only if fully traceable and time permits.

At completion, output: exact command to run, created file paths, screenshots (if feasible), tested clip pairs, feature table and known limitations. Report honestly what was not built or verified.

## Do not do
- Do not call emotion labels a ground truth of actual feelings.
- Do not infer "better/worse communication" from acted anger/happiness alone.
- Do not invent or tune 'confidence 85 / intelligibility 42' scores for visual impact.
- Do not represent curated dataset metadata as an AI prediction.
- Do not spend the weekend building infrastructure instead of a two-clip live demonstration.
