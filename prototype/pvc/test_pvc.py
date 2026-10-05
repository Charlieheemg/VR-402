"""Synthetic fixtures test mechanics only; no PVC research results are implied."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import joblib
import numpy as np
import pandas as pd
import soundfile as sf
from analyze import extract, save, temporal, feature_names
from train import get_xy, load_data, metrics, splits_for, train
from predict import predict


class PVCTests(unittest.TestCase):
    def test_known_gap_and_boundary_silence(self):
        sr = 16000
        x = np.r_[np.zeros(3200), np.full(16000,0.1), np.zeros(6400),
                  np.full(16000,0.1), np.zeros(3200)]
        f = temporal(x,sr)
        self.assertAlmostEqual(f['audio_duration_s'],2.8)
        self.assertAlmostEqual(f['energy_activity_ratio'],2/2.8)
        self.assertEqual(f['pause_count'],1)
        self.assertAlmostEqual(f['mean_pause_duration_s'],0.4)
        self.assertAlmostEqual(f['max_pause_duration_s'],0.4)

    def test_silence_and_partial_frame(self):
        for x, activity in [(np.zeros(16001),0),(np.ones(16001)*0.1,1)]:
            f = temporal(x,16000)
            self.assertEqual(f['energy_activity_ratio'],activity)
            self.assertEqual(f['pause_count'],0)
        with self.assertRaises(ValueError):
            temporal(np.zeros(10),16000,min_pause=float('nan'))

    def test_extractor_roundtrip_and_cli(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            wav = root/'synthetic.wav'
            sr = 16000
            t = np.arange(sr)/sr
            sf.write(wav,0.1*np.sin(2*np.pi*180*t),sr)
            result = extract(wav,'Um, I I agree uh.',2.0,1.5)
            self.assertEqual(result['egemaps_feature_count'],88)
            self.assertEqual(len(result['features']),len(feature_names()))
            self.assertIsNone(result['pvc_score'])
            dotted = dict(result, sample_id='clip.v1')
            save(dotted,root/'dotted')
            self.assertTrue((root/'dotted/clip.v1.json').exists())
            self.assertEqual(result['features']['filled_pause_count'],2)
            self.assertEqual(result['features']['word_count'],5)
            self.assertEqual(result['features']['immediate_token_repeat_count'],1)
            self.assertEqual(result['features']['response_latency_s'],-0.5)
            stem = save(result,root/'out')
            reread = json.loads(stem.with_suffix('.json').read_text())
            row = pd.read_csv(stem.with_suffix('.csv')).iloc[0]
            for key,val in reread['features'].items():
                self.assertAlmostEqual(row[key],val,places=7) if val is not None else self.assertTrue(pd.isna(row[key]))
            subprocess.run([sys.executable,'analyze.py',str(wav),'--output',str(root/'cli')],check=True,capture_output=True,cwd=Path(__file__).parent)
            with self.assertRaises(ValueError):
                extract(wav,previous_turn_end=1)
            with self.assertRaises(ValueError):
                extract(wav,previous_turn_end=1,response_start=float('nan'))
            sf.write(root/'empty.wav',np.array([]),sr)
            with self.assertRaises(ValueError):
                extract(root/'empty.wav')
            pd.DataFrame({'audio_filename':['synthetic.wav'],'pvc_score':[3]}).to_csv(root/'audio.csv',index=False)
            self.assertEqual(load_data(root/'audio.csv').shape[0],1)

    def fixture(self):
        return pd.DataFrame({'audio_duration_s':[1.,2.,3.,4.,5.,6.,7.,8.],
                             'rms_mean':[.1,np.nan,.2,.3,.1,.3,.2,.4],
                             'word_count':[np.nan]*8,
                             'pvc_score':[1.,2.,3.,4.,2.,3.,4.,5.],
                             'speaker_id':['a','a','b','b','c','c','d','d'],
                             'clinical_correctness':[0,1,0,1,0,1,0,1]})

    def test_group_split_and_metadata_exclusion(self):
        df = self.fixture()
        splits,_ = splits_for(df,4)
        for tr,va in splits:
            self.assertFalse(set(df.iloc[tr].speaker_id)&set(df.iloc[va].speaker_id))
        X,_ = get_xy(df)
        self.assertNotIn('clinical_correctness',X)
        self.assertNotIn('pvc_score',X)
        self.assertIn('WARNING',splits_for(df.drop(columns='speaker_id'),4)[1])
        df.loc[0,'speaker_id'] = None
        with self.assertRaises(ValueError):
            splits_for(df,4)

    def test_labels_and_constant_metrics(self):
        df = self.fixture()
        df.loc[0,'pvc_score'] = 6
        with self.assertRaises(ValueError):
            get_xy(df)
        with self.assertRaises(ValueError):
            get_xy(df.drop(columns='pvc_score'))
        self.assertIsNone(metrics([1,2,3],[2,2,2])['spearman'])

    def test_training_prediction_and_cli(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            df = self.fixture()
            with contextlib.redirect_stdout(io.StringIO()):
                report = train(df,root/'models',4)
            self.assertEqual(set(report['models']),{'mean','ridge','random_forest'})
            self.assertIn('standardized_coefficients',report['models']['ridge'])
            self.assertIn('held_out_permutation_mae_increase',report['models']['random_forest'])
            self.assertTrue((root/'models/out_of_fold_predictions.csv').exists())
            bundle = joblib.load(root/'models/ridge.joblib')
            prediction = predict(bundle,df.iloc[0].to_dict())
            self.assertTrue(np.isfinite(prediction['predicted_pvc']))
            with self.assertRaises(ValueError):
                predict(bundle,{})
            # Check fold-only mean and imputation: held-out targets do not enter training.
            for fold in report['models']['mean']['folds']:
                expected = np.mean(df.iloc[fold['training_rows']].pvc_score)
                oof = pd.read_csv(root/'models/out_of_fold_predictions.csv')
                self.assertTrue(np.allclose(oof.iloc[fold['validation_rows']].mean_prediction,expected))
            df.to_csv(root/'synthetic.csv',index=False)
            subprocess.run([sys.executable,'train.py',str(root/'synthetic.csv'),'--folds','2','--output',str(root/'cli')],check=True,capture_output=True,cwd=Path(__file__).parent)
            (root/'features.json').write_text(json.dumps({'features':{'audio_duration_s':1,'rms_mean':.1,'word_count':None}}))
            subprocess.run([sys.executable,'predict.py',str(root/'cli/ridge.joblib'),str(root/'features.json')],check=True,capture_output=True,cwd=Path(__file__).parent)


if __name__ == '__main__':
    unittest.main()
