"""Contract checks for new annotation semantics and independently refitted aggregates."""
import unittest,json
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score,brier_score_loss
from reproduce_evidence import timing,ROOT,PRIV
class EvidenceTests(unittest.TestCase):
 def test_silence_is_not_split_from_stops(self):
  iv=[(0,.2,'sil'),(.2,.5,'a'),(.5,.7,'?sil'),(.7,1.,'sil+k'),(1.,1.2,'sil')]
  d=timing(iv)
  self.assertAlmostEqual(d['annotated_span_s'],.8)
  self.assertAlmostEqual(d['phone_like_s'],.6)
  self.assertAlmostEqual(d['internal_sil_label_s'],.2)
  self.assertEqual(d['composite_intervals'],1);self.assertEqual(d['uncertain_intervals'],1)
 def test_full_corpus_identity_format_and_annotation_bounds(self):
  import soundfile as sf
  import hashlib
  from reproduce_evidence import PVC,intervals
  raw=PVC/'private/edinburgh'
  original=json.loads((raw/'demo/inventory.json').read_text())
  self.assertEqual(len(original['files']),125)
  for r in original['files']:
   wav=raw/r['path'];info=sf.info(wav)
   self.assertEqual(info.channels,1);self.assertEqual(info.samplerate,16000)
   self.assertEqual(hashlib.sha256(wav.read_bytes()).hexdigest(),r['sha256'])
   grid=raw/'clear_speech_TextGrid'/wav.stem[:9]/(wav.stem+'.TextGrid')
   iv=intervals(grid)
   self.assertTrue(all(0<=a<=b<=info.duration+.02 for a,b,t in iv))
   self.assertTrue(all(abs(iv[i][1]-iv[i+1][0])<1e-6 for i in range(len(iv)-1)))
 def test_complete_pairs_and_accounting(self):
  d=pd.read_csv(PRIV/'edinburgh_recordings.csv');self.assertEqual(len(d),125)
  self.assertTrue(np.allclose(d.annotated_span_s,d.phone_like_s+d.internal_sil_label_s))
  for code,g in d.groupby('code'):self.assertEqual(set(g.sentence),set(range(1,26)))
  self.assertTrue((d.duration_s>=d.annotated_span_s).all())
 def test_r2spin_export_matches_oof(self):
  oof=pd.read_csv(PRIV/'r2spin_oof.csv');summary=pd.read_csv(ROOT/'docs/results/r2spin_summary.csv')
  self.assertEqual(len(oof),6400);self.assertEqual(oof.Participant.nunique(),16);self.assertEqual(oof.List.nunique(),8)
  for r in summary.itertuples():
   prob=oof[r.model];self.assertTrue(prob.between(0,1).all())
   self.assertAlmostEqual(accuracy_score(oof.WRR,prob>=.5),r.accuracy)
   self.assertAlmostEqual(brier_score_loss(oof.WRR,prob),r.brier)
 def test_paired_summary_not_difference_of_medians(self):
  d=pd.read_csv(PRIV/'edinburgh_recordings.csv');plain=d[d.code==19].set_index('sentence')
  p=pd.read_csv(ROOT/'docs/results/edinburgh_paired.csv')
  for r in p.itertuples():
   s=d[d.condition==r.condition].set_index('sentence')[r.metric]-plain[r.metric]
   self.assertAlmostEqual(s.median(),r.median_difference)
   self.assertEqual(int((s>1e-8).sum()),r.positive)
if __name__=='__main__':unittest.main()
