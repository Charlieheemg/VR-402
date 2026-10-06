"""Software-only fixtures: no human PVC labels are created by these tests."""
import csv
from datetime import datetime
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
import soundfile as sf
from annotation.serve import Study, make_server
from analyze import temporal
from demo import DISCLAIMER
from sensitivity import run

HERE = Path(__file__).resolve().parent


class AnnotationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.clips = self.root/'clips'
        self.clips.mkdir()
        for name in ['clip_a','clip_b']:
            sf.write(self.clips/f'{name}.wav',np.zeros(16000),16000)
        self.study = Study(self.clips,self.root/'ratings')
        self.server = make_server(self.study,0)
        self.thread = threading.Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()
        self.url = f'http://127.0.0.1:{self.server.server_port}'

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.tmp.cleanup()

    def get(self,path):
        with urlopen(self.url+path,timeout=3) as response:
            return response.read()

    def post(self,body):
        request = Request(self.url+'/api/rating',data=json.dumps(body).encode(),
                          headers={'Content-Type':'application/json'})
        with urlopen(request,timeout=3) as response:
            return json.load(response)

    def rating(self,**changes):
        return dict(dict(clip_id='clip_a',rater_id='synthetic_test',pvc_score=4,
                         notes='TEST ONLY, "quoted"\nUnicode: α',rating_status='rated'),**changes)

    def test_save_export_resume_and_unrateable(self):
        session=json.loads(self.get('/api/session?rater_id=synthetic_test'))
        self.assertEqual(set(session['clips']),{'clip_a','clip_b'})
        self.assertEqual(self.get('/audio?clip_id=clip_a'),(self.clips/'clip_a.wav').read_bytes())
        saved=self.post(self.rating())
        self.assertTrue(saved['saved'])
        self.assertIsNotNone(datetime.fromisoformat(saved['timestamp']).tzinfo)
        resumed=json.loads(self.get('/api/session?rater_id=synthetic_test'))
        self.assertEqual(resumed['clips'],['clip_b'])
        self.assertEqual(resumed['completed'],1)
        self.post(self.rating(clip_id='clip_b',pvc_score=None,rating_status='unrateable'))
        exported=list(csv.DictReader(io.StringIO(self.get('/export?rater_id=synthetic_test').decode())))
        with (self.root/'ratings/synthetic_test.csv').open(newline='') as handle:
            stored=list(csv.DictReader(handle))
        self.assertEqual(exported,stored)
        self.assertEqual(exported[0]['notes'],self.rating()['notes'])
        self.assertEqual(exported[0]['pvc_score'],'4')
        self.assertEqual(exported[1]['pvc_score'],'')
        self.assertEqual(exported[1]['rating_status'],'unrateable')
        self.assertEqual(len(exported[0]['audio_sha256']),64)
        self.assertEqual(len(Study(self.clips,self.root/'ratings').rows('synthetic_test')),2)
        self.assertEqual(json.loads(self.get('/api/session?rater_id=another_rater'))['completed'],0)

    def test_invalid_and_duplicate_responses_do_not_overwrite(self):
        for score in [0,6,True,3.5,'4',None]:
            with self.assertRaises(HTTPError):
                self.post(self.rating(pvc_score=score))
        for changes in [dict(rater_id='../escape'),dict(clip_id='missing'),
                        dict(notes='x'*2001),dict(rating_status='unrateable')]:
            with self.assertRaises(HTTPError):
                self.post(self.rating(**changes))
        self.post(self.rating())
        with self.assertRaises(HTTPError):
            self.post(self.rating(pvc_score=1))
        self.assertEqual(self.study.rows('synthetic_test')[0]['pvc_score'],'4')
        sf.write(self.clips/'clip_a.wav',np.ones(16000)*.1,16000)
        with self.assertRaises(ValueError):
            Study(self.clips,self.root/'ratings').rows('synthetic_test')

    def test_rater_page_blinding_and_local_scope(self):
        page=self.get('/').decode()
        self.assertIn('Based on the speaker’s vocal delivery, how confident does the speaker sound in what they are saying?',page)
        self.assertIn('Judge how the speaker sounds. Do not judge whether the content is correct, whether the speaker is actually confident internally, or whether the speaker is competent.',page)
        self.assertNotIn('F0',page)
        self.assertNotIn('energy_activity_ratio',page)
        self.assertEqual(page.count('name="score"'),5)
        self.assertNotIn('checked',page)
        with self.assertRaises(HTTPError):
            urlopen(Request(self.url+'/api/session?rater_id=r1',headers={'Origin':'https://example.com'}),timeout=3)


class ResearchTests(unittest.TestCase):
    def test_threshold_sweep_and_demo_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            wav=root/'synthetic.wav'
            sr=16000
            tone=.1*np.sin(2*np.pi*180*np.arange(sr)/sr)
            sf.write(wav,np.r_[tone,np.zeros(6400),tone*.03],sr)
            inputs=[('Before',wav),('After',wav)]
            table=run(inputs,[-55,-45,-35],root/'sweep')
            self.assertEqual(len(table),6)
            x,_=sf.read(wav,dtype='float32')
            for _,row in table.iterrows():
                expected=temporal(x,sr,row.threshold_dbfs)
                for key in ['energy_activity_ratio','energy_silence_ratio','pause_count','mean_pause_duration_s','max_pause_duration_s']:
                    self.assertAlmostEqual(row[key],expected[key])
                self.assertAlmostEqual(row.energy_activity_ratio+row.energy_silence_ratio,1)
            csv_table=pd.read_csv(root/'sweep/temporal_sensitivity.csv')
            pd.testing.assert_frame_equal(table,csv_table,check_dtype=False)
            metadata=json.loads((root/'sweep/temporal_sensitivity_metadata.json').read_text())
            self.assertEqual(metadata['thresholds_dbfs'],[-55,-45,-35])
            self.assertIn('not validated speech activity',(root/'sweep/temporal_sensitivity.md').read_text())
            for thresholds in [[],[-35,-35],[float('nan')]]:
                with self.assertRaises(ValueError):run(inputs,thresholds,root/'invalid')
            demo=subprocess.run([sys.executable,str(HERE/'demo.py'),str(wav),'--transcript','Um I agree uh',
                                 '--output',str(root/'demo')],check=True,capture_output=True,text=True)
            self.assertIn(DISCLAIMER,demo.stdout)
            self.assertIn('2 literal um/uh/erm/hmm fillers',demo.stdout)
            result=json.loads((root/'demo/synthetic.json').read_text())
            self.assertEqual(result['egemaps_feature_count'],88)
            self.assertEqual(len(result['features']),102)
            self.assertIsNone(result['pvc_score'])
            self.assertTrue((root/'demo/synthetic.csv').exists())
            self.assertIn(DISCLAIMER,(root/'demo/synthetic.summary.txt').read_text())
            subprocess.run([sys.executable,str(HERE/'sensitivity.py'),'--before',str(wav),'--after',str(wav),
                            '--output',str(root/'cli')],check=True,capture_output=True)


if __name__ == '__main__':
    unittest.main()
