# Submission source and claim audit

Checked 10 November 2026. The main report references are limited to sources used in its argument. This is a targeted claim check, not a systematic literature review. Full historical reference registers remain available for appendix provenance.

## Primary project and assessment sources

- **[P1] supplied manuscript, submission ID 1911:** inspected the original 11-page PDF and visually checked Table 1 on page 5, §3.3. It states seven communication categories derived from teamwork instruments and refined with clinical subject-matter experts. Clear Messages includes directedness, specificity and brevity with referent/action/timing. Knowing One's Limitations concerns help-seeking, uncertainty disclosure and escalation. The report paraphrases these criteria. The document does not establish the reported 12-to-seven historical reduction. Publication/peer-review status remains unconfirmed. The manuscript and its figures are not redistributed.
- **Official CDE4301 AY2026 interim brief:** inspected all six pages. Page 1 specifies a GitHub website, 4,000 words for a two-person group excluding appendices, clear individual areas of work and submission at the end of Semester 1 Week 13. Pages 2–4 provide A1–A6. The report conservatively includes its reference list in the 4,000-word count; no assumption that references are exempt is required. The precise calendar deadline remains a course-level confirmation.

## Main-report literature

| Reference | Source inspected / evidence basis | Use in the report |
| --- | --- | --- |
| [1] Sohlin et al. (2026) | [Publisher full text](https://link.springer.com/article/10.1007/s00431-026-06898-3), abstract and study design | 24-professional randomised pilot; feasibility and need for a larger non-inferiority trial. No validation of our prototypes. |
| [2] Krause & Braida (2004) | [Primary article record](https://pubmed.ncbi.nlm.nih.gov/14759028/) and retained [source audit](source-audit.md) | Clear speech at normal rates motivates testing multiple acoustic dimensions rather than rewarding slowing alone. |
| [3] Sabu & Rao (2020) | [ISCA author paper/record](https://www.isca-archive.org/interspeech_2020/sabu20_interspeech.html); committed dataset provenance and evaluation | Reading-confidence source. Our three-class macro-F1 is not their correlation/binary-task result. Numeric mapping and speaker limitations remain explicit. |
| [4] Eyben et al. (2010, 2016) | [openSMILE DOI](https://doi.org/10.1145/1873951.1874246), [GeMAPS DOI](https://doi.org/10.1109/TAFFC.2015.2457417), retained source audit and code configuration | Extraction framework. The implemented configuration is eGeMAPSv02, not a claim that all 88 features are validated clinical predictors. |
| [5] Mayo (2013) | [Edinburgh deposit](https://datashare.ed.ac.uk/items/e0d78c30-c38d-41a5-947c-b03186a50a97), retained inventory and measurement audit | Corpus provenance. Paired changes are our measured results; no listener outcomes are attributed to the corpus analysis. |
| [6] Ward et al. (2019) | [ISCA author paper/record](https://www.isca-archive.org/interspeech_2019/ward19b_interspeech.html), pinned BBC table and code | R2SPIN provenance. Published audibility/context data are distinguished from our trainee-side features. |
| [7] Hattie & Timperley (2007) | [Publisher record](https://doi.org/10.3102/003465430298487), retained feedback source audit | Goal/current/next framework; no inference of local effectiveness. |
| [8] Nicol & Macfarlane-Dick (2006) | [Publisher record and abstract](https://doi.org/10.1080/03075070600572090) | Self-regulation, reflection and dialogue. Cite the 2006 volume, despite later online publication metadata. |
| [9] Little et al. (2024) | [Institutional repository abstract and metadata](https://opus.lib.uts.edu.au/handle/10453/179199) | Feedback-literacy development and limitations in study/intervention design. |
| [10] Alnazawi & Almarhabi (2026) | [Publisher full text](https://link.springer.com/article/10.1186/s41077-026-00447-6), Results and Discussion | Seven studies; analytics, facilitator support and learner reflection; limited, heterogeneous evidence. No claim of universal absence of educational findings. |
| [11] Duff et al. (2024) | [Publisher indexed abstract](https://doi.org/10.1097/SIH.0000000000000765) and retained source register | Limited robust comparative evidence for debriefing methods. No local superiority inferred. |
| [12] Kıyak et al. (2026) | [Publisher abstract](https://link.springer.com/article/10.1007/s40670-025-02621-3) | 42 studies; variable accuracy; none reported behaviour/patient-level outcomes. Scope is LLM feedback, distinct from our deterministic prototype. |
| [13] Cook & Hatala (2016) | [Publisher article](https://advancesinsimulation.biomedcentral.com/articles/10.1186/s41077-016-0033-y) and retained source register | Validity concerns the interpretation and intended use of an assessment. |

A reachable DOI or HTTP success is not proof that its full text was reviewed. Where full publisher access was unavailable, the table identifies abstract/record or retained-audit support. No new claim requires an inaccessible full-text result. Historic bibliographies: [speech source audit](source-audit.md), [feedback reference register](../feedback/references.md).

## Numerical and implementation provenance

- Reading: original `evaluation.json`, fixed-fold ablation tables and `docs/results/reading_reproduction.csv`.
- YAMNet: local inventory, candidate and coverage files checked; exact private-file hashes in [the prior decision log](../research/examiner-feedback-revision.md#verified-evidence). Only aggregate counts and limitations are public.
- CREMA-D: source commit `276b179479be5fdf3a5cf8d09edc36d95c79643b`. [Aggregate snapshot](../results/emotion-study-summary.json) preserves confusion matrices and metrics without copying row-level features or votes. The offline demo and study stay on their separate review branch; the main report acknowledges completed work rather than claiming it is merged software. [Original attribution and terms](https://github.com/Charlieheemg/VR-405/blob/276b179479be5fdf3a5cf8d09edc36d95c79643b/prototype/pvc/emotion_demo/study_results/DATA_LICENSE.md).
- Edinburgh/R2SPIN: committed paired/per-fold tables and measurement/pitch audits; no new fitting performed.
- Feedback: `docs/feedback/results/v01-aggregate.json`, frozen generator SHA-256 and aggregate inspection of a supplied output pair. Public source-derived excerpts were subsequently withheld pending permission; Appendix D now uses synthetic illustrations. Workbook extraction, report inspection and future educational tests are explicitly separated.

## 11 November rubric and Canvas reconciliation

Rechecked the newly supplied six-page file `CDE4301 assessment brief and rubrics - AY2026 - interim assessment.pdf` (SHA-256 `59396344579e27f343ad295a08b3d482f770333fb0c213afadd355cdc6592ff4`). Page 1 explicitly calls for research design matrices/protocols as well as design specifications for the respective project elements. The supplied Canvas text confirms website-URL submission and one submitter per group. Added [joint progress/design matrices](../project-design.html) and a [submission handoff](../submission.md). These sources specify assessment requirements; they do not establish project outcomes or approvals. The supplied course PDF is not redistributed.
