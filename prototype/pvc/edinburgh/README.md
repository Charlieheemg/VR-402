> Current official project: **VR-405 — Paediatric VR Speech Analysis and Feedback**. The local repository folder remains `VR-402`; measurements and original demo workflow are preserved.

# Edinburgh meeting demo — 20 October 2026

Open **http://127.0.0.1:8765/demo/** while the server is running. No internet or new packages needed for the prepared demo.

From the VR-402 repository:

```sh
python3 prototype/pvc/edinburgh/serve.py
```

Then open the URL above. Control-C stops the server. Alternatively double-click `Start-Demo.command` in Finder (if its first browser attempt races the server, refresh the page). Set laptop volume before presenting.

## What is ready

Three fixed matched sentence sets (0001, 0002, 0016), nine original WAVs, native audio controls with exclusive playback, measured duration, estimated F0 percentile range and whole-file RMS dBFS. Static local UI needs only Python's standard library. Results include CSV, JSON, complete extractor outputs and source-audio hashes. Screenshots are in `prototype/pvc/private/edinburgh/demo/sentence-*.jpg`. Original WAVs can also be opened directly from `prototype/pvc/private/edinburgh/clear_speech_wavs/` if the browser fails.

## Verified source and access

[Mayo (2013), Acted clear speech corpus](https://datashare.ed.ac.uk/items/e0d78c30-c38d-41a5-947c-b03186a50a97), DOI 10.7488/ds/138. Public download without login was successful on 19 October 2026. Readme: one male native English RP talker, approximately 40; 25 TIMIT prompts; five conditions: normal (19), infant-directed (20), computer-directed (21), foreigner-directed (22, displayed as non-native-listener-directed), speech-in-noise (25). Natural quiet/noise versus three acted recipient conditions. Hemi-anechoic recording, two microphones described, headphones throughout, downsampled to 16 kHz.

Actual WAV archive: **125 mono 16 kHz MKH800 files**, all 25 sentence IDs in all five conditions. No DPA WAVs in this archive despite the readme describing that microphone. Automatic Festival labels: 125 `.lab` files. Hand-corrected phone labels: 125 actual `.TextGrid` files (exclude macOS resource-fork duplicates). Accompanying segmentation criteria and 25 prompt texts downloaded. The matching keys are microphone + sentence ID + condition, with the speaker fixed by the corpus design. Downloaded files include no identified human listener recognition or clarity/intelligibility ratings. Phonetic annotations describe production, not listener performance.

The deposit lists only a **Depositor Agreement**, granting distribution rights to the repository, not an explicit Creative Commons/end-user redistribution licence. Preserve attribution; no broad reuse licence is claimed. Raw files, derived local demo and screenshots remain under ignored `private/`; nothing uploaded or publicly hosted. Confirm permission before redistribution or commercial reuse.

## Rebuild / check (existing environment)

```sh
prototype/pvc/.venv/bin/python prototype/pvc/edinburgh/download.py
prototype/pvc/.venv/bin/python prototype/pvc/edinburgh/build.py
prototype/pvc/.venv/bin/python -m unittest discover -s prototype/pvc/edinburgh -p 'test_*.py'
```

The downloader is standard-library only and retains archives/documentation locally. Rebuilding uses the existing `analyze.extract`, openSMILE 2.6.0/eGeMAPSv02 with 88 functionals. Selected examples are fixed rather than selected for a desired outcome. UI only displays three metrics; full extraction files include legacy threshold-energy descriptors which are **not validated pause/VAD measurements** and must not be presented as such.

## Measurement limits

Duration is whole-file time, including edge silence. F0 uses `F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2` (80th minus 20th percentile, semitones), an automated estimate without manual pitch review. RMS is `20 log10(sqrt(mean(samples²)))` relative to digital full scale, not dB SPL; no gain calibration or perceived-loudness claim. Playback is original, unnormalized. Rate, segmentation-based pauses, F1/F2 and vowel space are deliberately omitted pending validation. No model was trained.

## Literature

[Gutz, Maffei & Green (2023), DOI 10.1044/2023_AJSLP-23-00030](https://pubs.asha.org/doi/10.1044/2023_AJSLP-23-00030): ASR feedback elicited changes overlapping clear speech, including decreased rate and increased vowel distinctiveness. Their ASR accuracy, intelligibility and clarity correlated with different features. This motivates measuring separate acoustic dimensions; it does not validate our three metrics as intelligibility predictors. Edinburgh's acted computer condition is not ASR feedback. This is a within-speaker demonstration, not a replication or population study.
