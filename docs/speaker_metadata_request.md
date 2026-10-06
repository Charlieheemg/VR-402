# Speaker metadata request — draft only, not sent

Subject: Speaker-ID mapping for ReadingConfidenceDataset academic evaluation

Dear Dr Sabu and Prof Rao,

I am Charlie Hee, a CDE4301 final-year project student at the National University of Singapore. I am using your public ReadingConfidenceDataset as a non-commercial academic benchmark, with citation to your Interspeech 2020 paper.

Would you be able to provide an authoritative mapping from the 600 released recording IDs to pseudonymous speaker IDs, or a documented filename schema that reliably identifies the same speaker across recordings? We would like to evaluate models with speakers kept separate between training and testing. We do not need students' names or other personal information.

We have not assumed that filename prefixes identify speakers and currently describe our results as recording-level only. If a mapping is available, please let us know any conditions for its use or reporting. A clarification of the numeric confidence-label coding and any recommended evaluation splits would also be helpful.

Thank you for making this resource available and for considering our request.

Best regards,
Charlie Hee
National University of Singapore

## Search record and current conclusion

Checked 6 October 2026:

- The complete [public repository](https://github.com/KaminiSabu/ReadingConfidenceDataset), including its tracked file list and current remote state: 602 files, comprising 600 WAVs, `Readme.md` and `ratings.csv`; one branch, no tags, releases or issues at inspection. Commit remains `0bf2ea31ff8b5a8ef634084deb0420cbf08948ec`.
- The [accompanying paper](https://www.isca-archive.org/interspeech_2020/sabu20_interspeech.html), including the [author-lab PDF copy](https://www.ee.iitb.ac.in/course/~daplab/publications/2020/ks-pr-is2020.pdf), dataset/evaluation descriptions and references.
- The author's [publications/project page](https://kaminisabu.github.io/), the lab's [publication listing](https://www.ee.iitb.ac.in/course/~daplab/publications/index.html), and targeted public searches for the dataset plus speaker mapping/schema.

No authoritative released-ID-to-speaker mapping or filename schema was located in these inspected sources. This is a bounded search result, not a claim that none exists elsewhere. The paper's speaker count does not define an identity key. The observed 154 first-prefix groups versus 155 source-reported speakers remains unresolved. No identities have been guessed and no contact has been made. **Speaker-independent evaluation cannot currently be claimed.**
