"""Synthetic fixtures test software contracts, never human confidence ground truth."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import joblib
import numpy as np
import pandas as pd
import soundfile as sf

import reading_benchmark as rb
from live_demo import analyze_recording, load_model, record_audio


class LabelsTests(unittest.TestCase):
    def test_mapping_and_exact_join(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'audios').mkdir()
            (root/'ratings.csv').write_text('b,0,T\na,-1,T\nc,1,T\n')
            for name in ['a','b','c']:
                sf.write(root/'audios'/f'{name}.wav',np.zeros(8000),16000)
            labels=rb.load_labels(root,{-1:1,0:1,1:1})
            self.assertEqual(labels.original_class.tolist(),[-1,0,1])
            self.assertEqual(labels.class_name.tolist(),['Low','Medium','High'])
            features=pd.DataFrame({'sample_id':labels.sample_id.tolist()[::-1],'audio_duration_s':[3,2,1]})
            joined=rb.join_features(labels,features)
            self.assertEqual(joined.audio_duration_s.tolist(),[1,2,3])
            for invalid in [features.iloc[:2],pd.concat([features,features.iloc[:1]])]:
                with self.assertRaises(ValueError):rb.join_features(labels,invalid)
            with self.assertRaises(ValueError):rb.load_labels(root)
            (root/'ratings.csv').write_text('a,-1,T\na,0,T\nc,1,T\n')
            with self.assertRaises(ValueError):rb.load_labels(root,None)
            (root/'ratings.csv').write_text('a,-1,T\nb,4,T\nc,1,T\n')
            with self.assertRaises(ValueError):rb.load_labels(root,None)
            (root/'ratings.csv').write_text('a,-1,T\nb,0,T\nx,1,T\n')
            with self.assertRaises(ValueError):rb.load_labels(root,None)


class BenchmarkTests(unittest.TestCase):
    def table(self):
        rng=np.random.default_rng(42)
        y=np.tile([-1,0,1],10)
        return pd.DataFrame(dict(sample_id=[f'test_{i}' for i in range(30)],original_class=y,
                                 audio_duration_s=20+y+rng.normal(0,.5,30),rms_mean=.2+.03*y+rng.normal(0,.01,30)))

    def test_group_splits_and_invalid_groups(self):
        y=self.table().original_class.to_numpy()
        groups=np.repeat(np.arange(10),3)
        splits=rb.split_folds(y,groups,n_splits=3)
        seen=[]
        for train,test in splits:
            self.assertFalse(set(groups[train]) & set(groups[test]))
            seen.extend(test)
        self.assertEqual(sorted(seen),list(range(30)))
        for invalid in [np.repeat('one',30),np.repeat('',30),[None]*30]:
            with self.assertRaises(ValueError):rb.split_folds(y,invalid,n_splits=3)
        first=rb.split_folds(y,n_splits=3)
        second=rb.split_folds(y,n_splits=3)
        for a,b in zip(first,second):np.testing.assert_array_equal(a[1],b[1])

    def test_evaluation_preprocessing_and_live_wav_cli(self):
        table=self.table()
        columns=['audio_duration_s','rms_mean']
        groups=np.repeat(np.arange(10),3)
        original_models=rb.models
        def fast_models():
            models=original_models()
            models['random_forest'][-1].set_params(n_estimators=10)
            return models
        from sklearn.preprocessing import StandardScaler
        original_fit=StandardScaler.fit
        scaler_inputs=[]
        def capture_fit(self,X,*args,**kwargs):
            scaler_inputs.append(np.asarray(X).copy())
            return original_fit(self,X,*args,**kwargs)
        with tempfile.TemporaryDirectory() as tmp, patch.object(rb,'models',fast_models), patch.object(StandardScaler,'fit',capture_fit):
            root=Path(tmp)
            report=rb.evaluate(table,root/'local',root/'aggregate',groups=groups,group_source='Synthetic test groups only',
                               columns=columns,n_splits=3,permutation_repeats=1)
            self.assertTrue(report['speaker_independent'])
            self.assertEqual(len(scaler_inputs),4) # one per fold plus final all-data fit
            for observed,(train,test) in zip(scaler_inputs,rb.split_folds(table.original_class,groups,3)):
                np.testing.assert_allclose(observed,table.iloc[train][columns])
                self.assertLess(len(observed),len(table))
            for name,data in report['models'].items():
                metrics=data['pooled_oof']
                self.assertEqual(np.asarray(metrics['confusion_matrix']).sum(),30)
                self.assertTrue(0<=metrics['macro_f1']<=1)
                self.assertTrue(0<=metrics['balanced_accuracy']<=1)
                self.assertEqual(set(metrics['classification_report']) & set(rb.LABELS.values()),set(rb.LABELS.values()))
            self.assertAlmostEqual(report['models']['majority']['pooled_oof']['balanced_accuracy'],1/3)
            oof=pd.read_csv(root/'local/out_of_fold_predictions.csv')
            for name in rb.models():
                probs=oof[[name+'_'+x+'_probability' for x in rb.LABELS.values()]]
                np.testing.assert_allclose(probs.sum(axis=1),1)
            self.assertTrue((root/'aggregate/rf_oof_permutation_importance.csv').exists())
            self.assertNotIn('source_sample_id',(root/'aggregate/evaluation.json').read_text())
            wav=root/'synthetic.wav'
            # 48 kHz stereo exercises mono conversion and resampling to training rate.
            tone=.1*np.sin(2*np.pi*180*np.arange(96000)/48000)
            sf.write(wav,np.column_stack([tone,tone]),48000)
            original=rb.sha(wav)
            model=root/'local/logistic.joblib'
            run=subprocess.run([sys.executable,str(rb.HERE/'live_demo.py'),str(wav),'--model',str(model),'--output',str(root/'demo')],
                               capture_output=True,text=True,check=True)
            self.assertIn(rb.DISCLAIMER,run.stdout)
            self.assertIn('Predicted class:',run.stdout)
            prediction=json.loads((root/'demo/prediction.json').read_text())
            self.assertEqual(set(prediction['probabilities']),{'Low','Medium','High'})
            self.assertAlmostEqual(sum(prediction['probabilities'].values()),1)
            self.assertNotIn('pvc_score',prediction)
            evidence=json.loads((root/'demo/evidence.json').read_text())
            self.assertEqual(evidence['egemaps_feature_count'],88)
            self.assertEqual(evidence['sample_rate_hz'],16000)
            self.assertEqual(evidence['source_audio_sha256'],original)
            self.assertEqual(rb.sha(wav),original)
            self.assertIsNone(evidence['pvc_score'])
            bundle=load_model(model)
            with patch.object(bundle['model'],'predict_proba',return_value=np.array([[np.nan,0,1]])):
                with self.assertRaises(ValueError):analyze_recording(wav,bundle,root/'bad_probability')
            sf.write(root/'silence.wav',np.zeros(16000),16000)
            with self.assertRaises(ValueError):analyze_recording(root/'silence.wav',bundle,root/'silent')
            bundle['kind']='PVC-model'
            joblib.dump(bundle,root/'wrong.joblib')
            with self.assertRaises(ValueError):load_model(root/'wrong.joblib')
            with self.assertRaises(ValueError):
                rb.evaluate(table,root/'bad',root/'badout',groups=groups,columns=columns,n_splits=3)
            with self.assertRaises(ValueError):
                rb.evaluate(table,root/'bad',root/'badout',columns=['original_class'],n_splits=3)

    def test_microphone_start_stop_with_simulated_device(self):
        # Tests capture plumbing without enabling the user's microphone.
        class FakeSD:
            class PortAudioError(Exception):pass
            class CallbackStop(Exception):pass
            def query_devices(self,*args):return dict(default_samplerate=16000,name='SIMULATED microphone')
            def check_input_settings(self,**kwargs):pass
            class InputStream:
                def __init__(self,**kwargs):self.callback=kwargs['callback']
                def __enter__(self):
                    self.callback(np.full((8000,1),.1,dtype=np.float32),8000,None,None)
                    return self
                def __exit__(self,*args):pass
        with tempfile.TemporaryDirectory() as tmp, patch('live_demo.sounddevice_module',return_value=FakeSD()), patch('builtins.input',return_value=''):
            path=Path(tmp)/'recording.wav'
            record_audio(path)
            self.assertEqual(sf.info(path).frames,8000)
            with self.assertRaises(ValueError):record_audio(path)


if __name__=='__main__':unittest.main()
