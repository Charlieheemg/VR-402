> Current official project: **VR-405 — Paediatric VR Speech Analysis and Feedback**. The local repository folder remains `VR-402`; measurements and original demo workflow are preserved.

# Supervisor meeting: a working acoustic evidence demo

**20 October 2026 · Suggested duration: 3–5 minutes**

**Opening (20 seconds):** “While waiting for Ferguson access, I used Edinburgh's publicly downloadable acted clear speech corpus to make the measurement pipeline observable. We can hear the same speaker say the same sentence under different instructions, and inspect actual extracted features.”

**Play (60 seconds):** Open the local demo. On sentence 0001, play Plain then Computer-directed, then Non-native-listener-directed. Keep laptop volume fixed. Repeat sentence 0002 if useful. Sentence 0016 offers a short third example. Playback stops the other clip automatically.

**Point to results (45 seconds):** For sentence 0001, plain / computer / non-native-listener-directed file durations are **4.25 / 5.85 / 5.77 s**; estimated F0 percentile ranges **4.48 / 3.93 / 4.04 semitones**; recorded RMS levels **−18.4 / −19.9 / −19.7 dBFS**. The instructed styles take longer here, but pitch range does not increase. No single acoustic direction defines better speech. Duration includes silence; these are not speaking-rate results. Digital level is not calibrated vocal intensity.

**Explain the evidence boundary (30 seconds):** “These are speaking-style instructions and acoustic measurements, not human intelligibility labels. The download has phonetic annotations but I found no listener word-recognition outcomes. I have not trained an intelligibility or confidence predictor, and cannot claim an intelligibility percentage.”

**Connect literature (30 seconds):** Gutz, Maffei & Green (2023) found overlapping Clear and ASR-elicited acoustic changes, especially rate and vowel distinctiveness, while intelligibility, clarity and ASR accuracy related to different features. Edinburgh is an acted instruction study with one speaker, so this demonstration is not a replication of their intervention or perceptual validation. [Paper](https://pubs.asha.org/doi/10.1044/2023_AJSLP-23-00030)

**Propose a next experiment (30 seconds):** “I propose collecting controlled listener transcriptions on a multi-speaker sample, with specified noise/listening conditions. We can then test which features relate to held-out intelligibility. For VR delivery feedback, acoustic observations should remain distinct from competence or confidence claims.” Ask the supervisor to confirm the target construct and feasible listener protocol before modelling.

**If the browser fails:** Use the saved sentence screenshots and CSV under `prototype/pvc/private/edinburgh/demo/`; play WAVs directly from `clear_speech_wavs/`. No network is needed. Do not share the raw corpus folder publicly: the deposit lists a Depositor Agreement without a clear redistribution licence. [Corpus](https://doi.org/10.7488/ds/138)
