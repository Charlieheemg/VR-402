# Same words, different delivery

Offline RAVDESS A/B demo followed by a five-expression CREMA-D comparison.
Implements the core Phase 1 and Phase 2 requirements in the supplied
`VR402_Codex_Demo_Brief_2026-10-31.md`, cross-checked against working brief v0.3.
The equivalent directory under `prototype/pvc/` reuses the existing extractor.
Optional Phase 3 classification is not implemented.

## Run and rebuild

One-command local launch from the repository root:

```sh
python3 prototype/pvc/emotion_demo/launch.py
```

Or double-click `Start-Demo.command`. Open `private/demo/index.html` directly
in Chrome or Safari as the offline fallback after building.
The launcher uses Python's standard-library loopback server; it needs no external
network connection, API key or acoustic libraries. The direct HTML fallback needs
only a compatible browser. All original WAV data is embedded. Acoustic Python
dependencies are needed only to rebuild. The managed in-app browser blocks file
URLs, so browser checks use the supported local HTTP preview; direct file-mode
playback and a physical Wi-Fi-off rehearsal remain user acceptance checks.

From this directory, with Python 3.12 and curl available:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-lock.txt
.venv/bin/python build.py --download
.venv/bin/python -m unittest test_demo -v
```

The first build downloads the original ~208 MB RAVDESS archive and five CREMA-D
WAVs. Publisher MD5 checks the RAVDESS archive; CREMA-D URLs pin a repository
revision. Every clip has an exported SHA-256, extraction settings, package version,
all 88 eGeMAPSv02 functionals, and temporal features in `measurements.json`.
`measurements.csv` contains the displayed summaries. `manifest.csv` includes
licences, source URLs, labels, rating status and repository-relative audio paths.
`private/` stays out of Git. To import downloaded samples manually, put the exact
filenames from the manifest in `private/raw/` and run `python build.py` without
`--download`. Missing inputs fail with the required filename and recovery action.

## Selection and interpretation

RAVDESS: actors 01 and 02, both sentences, happy versus sad, normal intensity,
first repetition, audio-only speech. Within each pair only the emotion field
differs. CREMA-D: actor 1001, IEO sentence, five intended expressions; medium
intensity except neutral, which is unspecified. Thus neutral comparisons do not
hold intensity constant. These are fixed illustrations selected before extraction,
not optimized for feature separation or listener agreement. Listen before presenting;
no claim is made that these examples are perceptually the strongest.

The supplied transcripts come from dataset scripts, not ASR. Showing them equal
demonstrates information omitted by that representation; it is not a benchmark
of a transcript-only model. Numeric acoustic descriptors are not emotion
predictions, communication scores, intelligibility, or validated paediatric outcomes.
Whole-file duration includes silence; RMS depends on recording gain. Playback is
unmodified, with no normalisation. Waveform envelopes share full-scale amplitude
but each spans its own duration. openSMILE use is subject to its own licence.

Displayed F0 is the median of finite, positive eGeMAPSv02 low-level F0 estimates,
converted from semitones re 27.5 Hz into Hz. Range is the 80th minus 20th percentile
in semitones, over those same frames. Fewer than five estimates yield unavailable
pitch metrics, not a fabricated zero. The voiced selection is algorithmic; pitch
accuracy has not been validated against reference tracks. No silence fraction is
displayed. The full inherited extraction JSON retains its documented energy gate
and warnings, but these are not presented as a validated VAD result.

Human perception ratings exist in both sources but are not loaded or evaluated
here. Future assessment must map the correct audio-only stimulus ratings to each
file and use speaker-separated evaluation before claiming model agreement.

## Sources and attribution

RAVDESS: Livingstone SR, Russo FA (2018). PLoS ONE 13(5): e0196391.
https://doi.org/10.1371/journal.pone.0196391
Original files and metadata: https://zenodo.org/records/1188976
Audio licence: CC BY-NC-SA 4.0. Original clips are unmodified and embedded only
in the local build. Retain attribution and licence with copies.

CREMA-D: Cao H et al. (2014). IEEE Transactions on Affective Computing 5(4):377–390.
https://doi.org/10.1109/TAFFC.2014.2336244
https://github.com/CheyneyComputerScience/CREMA-D
Database: ODbL 1.0; individual contents: DbCL 1.0. Original clips unmodified.
Pinned revision: 1658cd342dff90010aa843eaeebd53610a08b1dc.

## Short presentation script (approximately 75 seconds)

1. Open RAVDESS, actor 01, sentence 01. Play A, then B, with measurements hidden.
2. “These recordings have the same script. Do they feel the same?”
3. Reveal: “A transcript retains the words. Our prototype also measures duration,
   recording level and pitch characteristics directly from the audio.”
4. “These measurements describe differences; they do not tell us which delivery
   is better, or prove that the system understands emotion.”
5. Switch to CREMA-D. Compare takes, then reveal intended labels separately.
   “We can explore several expressions while holding actor and sentence fixed.”
6. “Next we can test predictions against audio-only human judgements. That
   validation, and transfer to paediatric VR speech, remain future work.”
