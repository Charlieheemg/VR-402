import unittest,json,hashlib,sys
from pathlib import Path
import numpy as np
import soundfile as sf
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build import RAW,OUT,intervals
class DemoTests(unittest.TestCase):
 def test_complete_matched_corpus(self):
  wavs=list((RAW/'clear_speech_wavs').glob('*.wav'))
  self.assertEqual(len(wavs),125)
  for c in ['19','20','21','22','25']:
   self.assertEqual({p.stem[-4:] for p in wavs if p.stem.startswith('MKH800_'+c+'_')},{f'{n:04}' for n in range(1,26)})
 def test_measurements_audio_and_annotations(self):
  rows=json.loads((OUT/'results.json').read_text());self.assertEqual(len(rows),9)
  for r in rows:
   p=(OUT/r['audio']).resolve();y,sr=sf.read(p)
   self.assertEqual(sr,16000);self.assertEqual(y.ndim,1)
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),r['sha256'])
   self.assertAlmostEqual(len(y)/sr,r['duration_s'])
   self.assertAlmostEqual(20*np.log10(np.sqrt(np.mean(y*y))),r['rms_dbfs'])
   self.assertGreater(np.max(np.abs(y)),.01)
   g=RAW/'clear_speech_TextGrid'/('MKH800_'+r['code'])/(p.stem+'.TextGrid')
   iv=intervals(g);self.assertGreater(len(iv),10)
   self.assertTrue(all(0<=a<=b<=len(y)/sr+.02 for a,b,_ in iv))
   self.assertTrue(np.isfinite(r['f0_range_st']))
   f=json.loads((OUT/(p.stem+'.features.json')).read_text())
   self.assertEqual(f['egemaps_feature_count'],88);self.assertIsNone(f['pvc_score'])
 def test_no_listener_claims(self):
  rows=json.loads((OUT/'results.json').read_text())
  self.assertFalse(any('intelligibility' in k for r in rows for k in r))
if __name__=='__main__':unittest.main()
