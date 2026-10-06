# Local external reading-confidence demonstration

This is a demonstration of an external three-class benchmark, not a PVC assessment. The exact warning appears on every run:

> This prediction comes from an external model trained on children's English reading-confidence ratings. It is a demonstration of the acoustic modelling pipeline, not a validated PVC assessment for adult paediatric communication.

## Run during the meeting

From the `VR-402` repository root, record yourself:

```sh
prototype/pvc/.venv/bin/python prototype/pvc/live_demo.py --record
```

Press Enter to start, speak, then Enter to stop. Capture stops after at most 120 seconds; press Enter to finish if the cap is reached. Ctrl-C cancels without a prediction. The command prints the selected microphone. It saves a local WAV, reuses our extractor and loads the locally trained **logistic** benchmark. It displays Low/Medium/High probabilities, the predicted class and a short acoustic summary. Internet/API access is not required after setup.

For an existing WAV:

```sh
prototype/pvc/.venv/bin/python prototype/pvc/live_demo.py "/absolute/path/to/my_recording.wav"
```

A new ignored `prototype/pvc/private/live_demo/<UTC timestamp>/` folder contains the personal recording (when captured), analysis copy if needed, full 88-feature JSON/CSV, `prediction.json` and `summary.txt`. No personal recording is committed. `--output` can choose a new folder; existing folders are rejected to avoid overwriting a previous demonstration. Keep custom folders inside Git-ignored `private/`.

The original recording is preserved. Stereo is averaged to mono and non-16-kHz audio is resampled using `scipy.signal.resample_poly` to match training; no gain normalisation. The model rejects near-silence and invalid probabilities, but **does not verify that audio contains speech**. Noise and synthetic tones can produce predictions. Short sentences may lie outside the training duration range; that is reported, not silently treated as equivalent to reading a paragraph. Probabilities are uncalibrated model outputs, not a psychological certainty measure.

## Setup and microphone fallback

The current checkout has the benchmark trained locally. On another checkout, first follow [benchmark reproduction](reading_confidence_benchmark.md); model files intentionally are not in Git. Install optional microphone support separately:

```sh
prototype/pvc/.venv/bin/python -m pip install -r prototype/pvc/requirements-live.txt
prototype/pvc/.venv/bin/python prototype/pvc/live_demo.py --list-devices
```

Use macOS **System Settings → Sound → Input** to choose the microphone. If necessary add `--device 1` using the actual current input ID printed by `--list-devices`; IDs can change. In **Privacy & Security → Microphone**, allow the app/terminal running Python and restart it after changing permission. Do not bypass macOS permissions. A device visible in a list does not prove recording permission or successful capture.

The pinned optional dependency is sounddevice 0.5.5. Its [official installation documentation](https://python-sounddevice.readthedocs.io/en/latest/installation.html) says pip supplies PortAudio on macOS. The WAV path needs no sounddevice dependency. No capture starts merely by listing devices. If capture fails, use a previously recorded WAV; keep one available before the meeting. Avoid Bluetooth/device changes during the demonstration.

**Verification status:** device discovery outside the execution sandbox found the MacBook Air Microphone. The sandbox itself showed no devices. Hardware microphone capture has not been exercised here; its start/stop/save logic is tested with a simulated device, and real trained-model inference is tested separately on a synthetic WAV. Rehearse actual capture once in your normal Mac terminal before the meeting. No claim is made that your voice has already been recorded.

## Controlled two-recording protocol

Use this exact same sentence for both recordings:

> I recommend that we administer the medication now and reassess the patient in two minutes.

This is a fixed reading stimulus, not medical advice or an instruction to administer anything.

1. Keep the microphone, distance, room and input gain the same. Use your own voice; avoid other speakers/background playback. Do not change words between recordings.
2. Demo A: read it with deliberately tentative/hesitant delivery. Save the run folder.
3. Demo B: read it with deliberately assured/confident delivery. Save the second run folder.
4. Show both three-class probability distributions and evidence summaries, including the caveat. Inspect the probability of High/Low and class changes without inventing a PVC 1–5 conversion. Do not repeatedly retake only to select a favourable result; retain attempts and describe any retries.

These are **intentionally acted conditions, not ground-truth PVC labels**. Holding text constant limits lexical variation; it does not control all acoustic, recording or perceptual differences. A change in the expected direction is a useful sanity check, not validation. Failure may reflect child-to-adult, reading-to-clinical-style, duration or recording-domain shift; it can also reflect model error. Neither outcome diagnoses internal confidence or competence.

The source consists of children's paragraph reading, whereas this adult clinical-style sentence is short and acted. It is not evidence about spontaneous adult teamwork. The fixed sentence may be shorter than the dataset's shortest recording even with natural pauses; retain that limitation rather than padding audio to manufacture an in-range result.

## What to say

“I have connected our existing acoustic extractor to a real external human-labelled reading-confidence dataset. This demo shows the local recording-to-classifier pipeline and its three-class probabilities. It is not a validated assessment of my confidence or adult paediatric PVC. The domain-specific listener study is still required.”

For performance, class counts, exact folds and important feature patterns, use the [benchmark results](../prototype/pvc/results/reading_confidence/README.md) and [provenance/method](reading_confidence_benchmark.md). Never describe the final all-data demo model's prediction on a training recording as held-out performance.

## Recorded software-check example

The actual trained logistic model was exercised on a **3-second amplitude-modulated synthetic tone**, not a person speaking and not a research label:

```text
External Reading-Confidence Benchmark
Low: 0.0005
Medium: 0.9995
High: 0.0000
Predicted class: Medium
```

The run also printed the full disclaimer and an out-of-training-duration warning, and preserved all 88 features. This only verifies the end-to-end software path. The highly concentrated probability on a non-speech tone illustrates why model probabilities must not be interpreted as validity or certainty. A real voice rehearsal is still necessary; the tone is not a useful substitute for the supervisor's two-reading demonstration.
