# Perceived Vocal Confidence (PVC) — Definition v0.1

**Working definition:** Perceived Vocal Confidence (PVC) is the degree to which a listener judges, from a speaker's vocal delivery, that the speaker sounds certain and committed to what they are saying.

This is explicitly **Version 0.1**, to be refined through literature review, experiments and consultation with a speech expert. It is a listener-perceived communication construct, not a direct measure of internal/subjective confidence, correctness, competence/expertise, anxiety/stress, personality or overall communication quality. Perceived certainty and self-reported certainty can differ [3]. Expressed confidence research motivates this construct but does not establish its validity in paediatric VR [1].

## Operational target and ground truth

Use independent listener ratings on a 1–5 scale:

| Rating | Anchor |
| --- | --- |
| 1 | Very low perceived vocal confidence; strongly tentative or doubtful |
| 2 | Low |
| 3 | Neutral or unclear |
| 4 | High |
| 5 | Very high; strongly assured and committed |

Individual ratings are ordinal. A pre-specified aggregate (initial proposal: mean of multiple independent listeners) can be modelled as approximately continuous within 1–5. Preserve individual ratings, rater count, dispersion and disagreements; do not treat the mean as objective psychological truth. The neutral/unclear anchor conflates neutrality and insufficient evidence: record a separate inability-to-rate flag and resolve this with the speech expert before annotation. Do not assign 3 automatically to inaudible clips.

Proposed pilot: identify short, meaningful single-speaker turns; have several independent listeners hear identical clips with these instructions, blind to model predictions and clinical correctness. Record speaker, session and clip IDs; verify speaker identity rather than equating a role with a person. Agree rater recruitment, minimum ratings per clip, aggregation, exclusions and an ordinal reliability measure (or a justified ICC formulation for the aggregate) before collecting the main dataset. Natural audio retains lexical information despite instructions; quantify this limitation rather than claiming pure isolation of vocal delivery.

## Modelling formulation

```text
x = measurable acoustic/temporal feature vector
y = aggregated human PVC rating
PVC_hat = f(x)
```

Learn `f` so predicted PVC agrees with listener ratings. Acoustic measurements are **predictors**, not the definition or ground truth. No feature has a fixed universal sign or importance. In particular, do not encode “high pitch = low confidence”; reported effects depend on speakers, task and interacting cues [1,2].

## Candidate cue families and v0.1 implementation

| Family | Candidate measurements and basis | Prototype scope |
| --- | --- | --- |
| Temporal fluency | Speech/articulation rate, silence ratio, pause duration and frequency [1,2,6] | Duration, fixed-energy activity/silence ratios and internal gaps; transcript-based whole-clip words/minute. No validated VAD or syllable-based articulation rate. |
| Disfluency | Filled pauses, repetitions, false starts [2,6]; repetitions/false starts remain exploratory candidates here | Literal um/uh/erm/hmm counts and adjacent repeated-token counts from supplied verbatim text. No automatic false-start detection; no inference that every repeated word is a disfluency. |
| Response timing | Response/onset latency when conversational context is known [6] | Supplied response onset minus preceding turn end in a shared timebase; negative values mean overlap. No automatic turn pairing. |
| Pitch/prosody | F0 mean, range, SD and contour [1,2] | eGeMAPS semitone F0 mean, normalised SD, percentile range and slope summaries. Not a plotted framewise contour or raw-Hz SD. |
| Vocal energy | RMS/loudness mean, range and variability [1] | Frame RMS mean/SD/range plus standard eGeMAPS loudness statistics; not calibrated sound-pressure level. |
| Exploratory voice quality | Jitter, shimmer, HNR and spectral descriptors [4,5] | Standard eGeMAPSv02 functionals. GeMAPS standardises descriptors; it does not validate them as PVC predictors. |

All 88 eGeMAPSv02 functionals are retained. Literature motivates the prominent inspection subset; it does not provide score weights. Learn and validate signs, importance and interactions on human ratings. Voice quality, microphone gain, noise, accent, language, speaker physiology and overlap can confound features. Silence between turns is not necessarily within-turn hesitation.

## Evaluation and comparison

```text
human listeners -> PVC ground truth
 audio -> openSMILE/eGeMAPS + temporal features -> model -> predicted PVC
 same audio -> audio LLM -> predicted PVC
 compare both predictions with human ground truth
```

Use a mean baseline, Ridge regression and a small Random Forest; report out-of-fold MAE and Spearman correlation, with speaker-grouped folds wherever IDs exist. Fit imputation/scaling inside each training fold. Reserve independent speakers and ideally sessions/scenarios for final evaluation. The current script is a scaffold, not a sample-size justification or complete confirmatory protocol. Inspect rater agreement before judging models, and consider ordinal agreement/calibration, uncertainty intervals and subgroup errors in the validation study. Audio-LLM estimates are a benchmark, never ground truth. Keep correctness and Kang Zhe's feedback-usefulness evaluation separate.

**Current evidence boundary:** feature extraction works on supplied recordings. No PVC-labelled dataset was integrated, no real-data PVC model was trained, and no confidence-detection validity is claimed. Synthetic tests check software mechanics only.

## References

1. Jiang, X., & Pell, M. D. (2017). *The sound of confidence and doubt*. Speech Communication, 88, 106–126. [doi:10.1016/j.specom.2017.01.011](https://doi.org/10.1016/j.specom.2017.01.011). Controlled perceptual/acoustic evidence for temporal, pitch and intensity cues.
2. Kirkland, A., Lameris, H., Szekely, E., & Gustafson, J. (2022). *Where's the uh, hesitation? The interplay between filled pause location, speech rate and fundamental frequency in perception of confidence*. Interspeech 2022, 4990–4994. [doi:10.21437/Interspeech.2022-10973](https://www.isca-archive.org/interspeech_2022/kirkland22_interspeech.html). Synthesised spontaneous speech experiment; transfer to paediatric interactions is untested.
3. Pon-Barry, H., & Shieber, S. (2010). *Assessing self-awareness and transparency when classifying a speaker's level of certainty*. Speech Prosody 2010, paper 210. [doi:10.21437/SpeechProsody.2010-124](https://www.isca-archive.org/speechprosody_2010/ponbarry10_speechprosody.html).
4. Eyben, F., Scherer, K. R., Schuller, B. W., Sundberg, J., André, E., Busso, C., Devillers, L. Y., Epps, J., Laukka, P., Narayanan, S. S., & Truong, K. P. (2016). *The Geneva Minimalistic Acoustic Parameter Set (GeMAPS) for Voice Research and Affective Computing*. IEEE Transactions on Affective Computing, 7(2), 190–202. [doi:10.1109/TAFFC.2015.2457417](https://doi.org/10.1109/TAFFC.2015.2457417). Includes extended eGeMAPS.
5. Eyben, F., Wöllmer, M., & Schuller, B. (2010). *openSMILE: The Munich versatile and fast open-source audio feature extractor*. ACM Multimedia, 1459–1462. [doi:10.1145/1873951.1874246](https://doi.org/10.1145/1873951.1874246). [Current Python extraction documentation](https://audeering.github.io/opensmile-python/usage.html).
6. Brennan, S. E., & Williams, M. (1995). *The feeling of another's knowing: Prosody and filled pauses as cues to listeners about the metacognitive states of speakers*. Journal of Memory and Language, 34(3), 383–398. [doi:10.1006/jmla.1995.1017](https://doi.org/10.1006/jmla.1995.1017). Listener knowledge judgements are related evidence, not an identical PVC construct.
