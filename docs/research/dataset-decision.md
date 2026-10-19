# Human-labelled data decision — 19 October 2026

**Decision:** pursue SLUSI/L2-USI as the preferred secondary source for speaker-side recognition research, conditional on institutional access and an exact scored-excerpt audit. Keep the existing R2SPIN result as the operational audibility/context benchmark. Clarity CPC1 is an accessible secondary option only if we explicitly accept a hearing-aid/listener-conditioned prediction question. No new corpus is yet ready for our proposed speaker-side prediction experiment; no new model has been trained.

## SLUSI / L2-USI: good fit, access and alignment gates remain

The [official LDC release LDC2024S02](https://catalog.ldc.upenn.edu/LDC2024S02) and its [downloadable README](https://catalog.ldc.upenn.edu/docs/LDC2024S02/L2USI_Readme.txt), actually downloaded and read, describe 10.5 hours, 66 speakers, 15 language backgrounds and 127 university speech events. Approximately 73% of recordings have intelligibility scores. Word-aligned TextGrids, transcripts and spreadsheet metadata are described. These are adult academic monologues, not clinical-team utterances or matched clear/ordinary instructions.

The [originating laboratory description](https://sites.google.com/nau.edu/applied-ling-speech-lab-nau/projects/osim-project/slusi-corpus) separates transcription-based recognition (five listeners on selected excerpts) from 5-point ratings (15 listeners). A file-level score attached to a long recording must not be treated as a listener label for every segment. The LDC catalogue describes 16-kHz FLAC, while the lab describes 48-kHz WAV; the release README itself uses both format terms. Verify the acquired release rather than assuming audio format or interchangeability.

Full distribution is through LDC login and an [institutional user agreement](https://www.ldc.upenn.edu/sites/default/files/second-lang-univ-speech-intelligibility-corpus-user-agreement.pdf). NUS access and any applicable fee have not been verified. No agreement has been accepted, no payment made and no restricted full corpus downloaded.

Before extraction, verify: speaker→event identity; exact scored sentence/phrase times; reference text and scoring rules; which listeners rated/transcribed each item; whether individual responses or only aggregates are supplied; redacted/indecipherable material; permitted processing/storage. A score only for a few excerpts cannot label whole-event acoustics. Split multiple events from the same speaker together. If only event aggregates and no excerpt mapping are available, stop direct segment-level modelling or explicitly narrow the research unit and interpretation.

**Concrete next action for Charlie/supervisor:** check NUS Library/LDC access. If available, obtain the authorised release, verify 5 example joins including missing-score and redacted cases, then enumerate scored speakers before committing to RQ2. This is an access decision, not a request to recruit now.

## Clarity CPC1: actual small-package audit, not an audio benchmark

The [official specification](https://claritychallenge.org/docs/cpc1/data/cpc1_data) supplies a useful audio→prompt→listener-response schema. It concerns hearing-aid-processed signals heard by hearing-impaired listeners. Six talkers and around 25 listeners are described; system/noise/listener differences are central to the outcome. Its challenge split does not establish speaker-disjoint validation.

I downloaded only the **129,392-byte label archive** from the [official Zenodo record](https://zenodo.org/records/17046604). Its published MD5 matches `db62ba9c018dca184453fc60901519df`; SHA-256 and schema are in [dataset-access-audit.json](../results/dataset-access-audit.json). It contains 2,421 test-label rows and 632 test-independent-label rows. Both expose prompt, response, word count, hits, correctness, scene, listener, system, volume and signal identity. These are evaluation labels, not the training package. Only schema/counts were reported; no outcome analysis, feature selection or fitting was performed. Do not tune against these evaluation files; use a preregistered training-only development split for any later work.

**Licensing discrepancy caught:** the Zenodo metadata advertises CC BY 4.0; the archive README/LICENSE specify **CC BY-SA 4.0**, with a separate **Clarity speech database license 1.00** for target speech. That speech license also restricts replay/broadcast, with a limited noncommercial research-example exception. Preserve and check the archive terms for the actual material before reuse; do not assume the landing-page badge grants unrestricted audio playback or redistribution. No audio has been downloaded or published.

The training archive is approximately 14.2 GB and evaluation audio approximately 6.5 GB. A full audio–label join is **unverified**. Before use, retrieve authorised training metadata/audio, resolve signal filename conventions against the actual HA output, join scene→target talker, retain listener audiograms/system/noise/volume, and check sample identities/durations. The clean target alone is not the audio heard by a listener. Word-level outcomes are not IID speaker observations. Clarity could test conditional audibility prediction; it cannot establish that our feedback or a clear-speech instruction improves clinician intelligibility.

## Gate outcome

| Source | Human outcome | Locally verified now | Decision |
|---|---|---|---|
| Edinburgh | None found | Original recordings, pairs, annotations, acoustic estimates | Keep for production demonstration only |
| R2SPIN | Human binary keyword correctness | Existing 6,400-row labels/OOF audit; two voices | Keep bounded audibility/context benchmark |
| SLUSI / L2-USI | Selected-excerpt recognition and separate ratings described | Release README and access requirements; no scored audio join | Preferred source, conditional access/alignment |
| Clarity CPC1 | Listener word recognition | Small evaluation-label archive/schema/terms; no audio join | Conditional domain-specific fallback; no training now |

A new study remains a fallback after this access decision. The [proposed pilot](../methodology/listener-validation.md) provides a concrete feasibility design without pretending that those observations already exist.

## Reproduce the small audit

Save the two public documents and the small label archive under the ignored `prototype/pvc/private/dataset-audit/` directory as `slusi-readme.txt`, `cpc1-record.json` and `cpc1-labels.tar.gz`. URLs:

- `https://catalog.ldc.upenn.edu/docs/LDC2024S02/L2USI_Readme.txt`
- `https://zenodo.org/api/records/17046604`
- `https://zenodo.org/api/records/17046604/files/clarity_CPC1_data.labels.v1_0.tar.gz/content`

Run `python3 scripts/audit_dataset_access.py`. The script checks the archive hash, reads selected members without extracting arbitrary paths, exports only provenance/schema, and fits no models. Do not download the multi-GB audio archives until the research scope and terms are settled.
