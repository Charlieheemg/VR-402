"""Synthetic tests of fixed-fold ablation and paired-demo contracts, not human labels."""
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import joblib
import numpy as np
import pandas as pd
import soundfile as sf
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer

import reading_ablation as ab
import reading_benchmark as rb
from compare_demo import compare_takes, SCRIPTS
from live_demo import analyze_recording


class AblationTests(unittest.TestCase):
    def fixture(self):
        rng=np.random.default_rng(7)
        table=pd.DataFrame(rng.normal(size=(30,92)),columns=rb.predictor_names())
        table['sample_id']=[f'synthetic_{i}' for i in range(30)]
        table['original_class']=np.tile([-1,0,1],10)
        assignments=table[['sample_id','original_class']].copy()
        assignments['fold']=np.repeat(np.arange(1,6),6)
        return table,assignments

    def test_feature_allowlist_and_saved_fold_join(self):
        sets=ab.feature_sets()
        self.assertEqual([len(v) for v in sets.values()],[92,88,91,1,3])
        self.assertEqual(sets['B_egemaps_only'],list(rb.smile().feature_names))
        self.assertNotIn('audio_duration_s',sets['C_no_duration'])
        for columns in sets.values():
            self.assertFalse(set(columns)&{'original_class','sample_id','source_sample_id','source_flag','fold',*rb.EXPLORATORY})
        table,assignments=self.fixture()
        a=ab.saved_splits(table,assignments)
        b=ab.saved_splits(table,assignments.sample(frac=1,random_state=2))
        for (train,test),(train2,test2) in zip(a,b):
            np.testing.assert_array_equal(train,train2)
            np.testing.assert_array_equal(test,test2)
            self.assertFalse(set(train)&set(test))
        self.assertEqual(sorted(np.concatenate([x[1] for x in a])),list(range(30)))
        invalid=assignments.copy();invalid.loc[0,'original_class']=1
        with self.assertRaises(ValueError):ab.saved_splits(table,invalid)
        invalid=assignments.copy();invalid.loc[0,'fold']=6
        with self.assertRaises(ValueError):ab.saved_splits(table,invalid)
        with self.assertRaises(ValueError):ab.saved_splits(table,assignments.iloc[:-1])
        with self.assertRaises(ValueError):ab.saved_splits(table,pd.concat([assignments,assignments.iloc[:1]]))

    def test_every_condition_uses_identical_splits_and_reproduces_full(self):
        table,assignments=self.fixture()
        original=rb.models
        def fast_models():
            templates=original()
            templates['random_forest'][-1].set_params(n_estimators=3)
            return templates
        y=table.original_class.to_numpy()
        splits=ab.saved_splits(table,assignments)
        reference={'models':{}}
        for name,template in fast_models().items():
            pred=np.empty(len(y),dtype=int);folds=[]
            for train,test in splits:
                fit=clone(template).fit(table.iloc[train][rb.predictor_names()],y[train])
                pred[test]=fit.predict(table.iloc[test][rb.predictor_names()])
                folds.append(rb.scores(y[test],pred[test]))
            reference['models'][name]={'folds':folds,'pooled_oof':rb.scores(y,pred)}
        from sklearn.pipeline import Pipeline
        original_fit=Pipeline.fit
        training_rows=[]
        def capture(self,X,*args,**kwargs):
            training_rows.append(tuple(X.index))
            return original_fit(self,X,*args,**kwargs)
        with tempfile.TemporaryDirectory() as tmp,patch.object(ab,'models',fast_models),patch.object(Pipeline,'fit',capture):
            root=Path(tmp)
            pooled,folds=ab.run(table,assignments,reference,root,root/'private_predictions.csv')
            self.assertEqual(len(pooled),15);self.assertEqual(len(folds),75)
            expected=[tuple(train) for train,_ in splits]*15
            self.assertEqual(training_rows,expected)
            self.assertTrue((pooled.query("condition == 'A_full'").filter(like='delta_full_')==0).all().all())
            self.assertTrue(pooled.filter(regex='^(balanced_accuracy|macro_f1|low_f1|medium_f1|high_f1)$').apply(lambda s:s.between(0,1).all()).all())
            self.assertNotIn('sample_id',(root/'ablation_results.csv').read_text())
            reference['models']['majority']['folds'][0]['macro_f1']=-1
            with self.assertRaises(ValueError):ab.run(table,assignments,reference,root/'bad')


class PairTests(unittest.TestCase):
    def bundle(self):
        feature=rb.predictor_names()[0]
        model=make_pipeline(SimpleImputer(),DummyClassifier(strategy='prior')).fit(pd.DataFrame({feature:[1.,2.,3.]}),[-1,0,1])
        return dict(kind='external-reading-confidence-v1',classes=rb.LABELS,features=[feature],model=model,
                    versions={'scikit-learn':version('scikit-learn')},training_duration_range=[9.7,71.77])

    def test_paired_wav_cli_preserves_outputs_and_disclaimer(self):
        self.assertTrue(50<=len(SCRIPTS['reading'].split())<=70)
        self.assertEqual(SCRIPTS['clinical'],'I recommend that we administer the medication now and reassess the patient in two minutes.')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            tone=.1*np.sin(2*np.pi*180*np.arange(32000)/16000)
            for name,gain in [('a',1),('b',.5)]:sf.write(root/f'{name}.wav',tone*gain,16000)
            hashes=[rb.sha(root/f'{n}.wav') for n in ['a','b']]
            model=root/'fixture.joblib';joblib.dump(self.bundle(),model)
            args=[sys.executable,str(rb.HERE/'compare_demo.py'),'--wav-a',str(root/'a.wav'),'--wav-b',str(root/'b.wav'),
                  '--model',str(model),'--output',str(root/'pair')]
            process=subprocess.run(args,check=True,capture_output=True,text=True)
            self.assertIn(rb.DISCLAIMER,process.stdout)
            self.assertIn('Source RMS',process.stdout)
            self.assertIn('not causal explanations',process.stdout)
            result=json.loads((root/'pair/comparison.json').read_text())
            self.assertEqual(result['disclaimer'],rb.DISCLAIMER)
            self.assertTrue(result['same_model_for_both'])
            self.assertEqual(result['model_sha256'],rb.sha(model))
            self.assertFalse(result['text_compliance_verified'])
            for label,digest in zip(['a','b'],hashes):
                self.assertEqual(rb.sha(root/f'{label}.wav'),digest)
                self.assertEqual(rb.sha(root/f'pair/take_{label}/recording.wav'),digest)
                for file in ['evidence.json','evidence.csv','summary.txt','prediction.json']:
                    self.assertTrue((root/f'pair/take_{label}'/file).exists())
                prediction=result['takes'][label.upper()]
                self.assertAlmostEqual(sum(prediction['probabilities'].values()),1)
                self.assertTrue(all(0<=v<=1 for v in prediction['probabilities'].values()))
                self.assertIn('outside observed training range',' '.join(prediction['notes']))
            preserved=rb.sha(root/'pair/comparison.json')
            repeat=subprocess.run(args,capture_output=True,text=True)
            self.assertNotEqual(repeat.returncode,0)
            self.assertEqual(rb.sha(root/'pair/comparison.json'),preserved)
            with self.assertRaises(ValueError):compare_takes(root/'partial',self.bundle(),root/'a.wav')

    def test_same_device_model_and_observable_warnings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);bundle=self.bundle()
            devices=[]
            def fake_record(path,device):
                devices.append(device)
                # Clipped synthetic waveform; this is not human speech.
                sf.write(path,np.tile([1.,-1.],16000),16000)
                return path
            with patch('compare_demo.record_audio',side_effect=fake_record), patch('compare_demo.sounddevice_module',return_value=SimpleNamespace(default=SimpleNamespace(device=(7,-1)))):
                result,text=compare_takes(root/'recorded',bundle)
            self.assertEqual(devices,[7,7])
            self.assertIn('possible clipping',text)
            self.assertEqual(result['takes']['A']['recording_context']['source_sample_rate_hz'],16000)
            sf.write(root/'silent.wav',np.zeros(16000),16000)
            with self.assertRaises(ValueError):analyze_recording(root/'silent.wav',bundle,root/'silent')
            sf.write(root/'tone.wav',np.ones(16000)*.1,16000)
            for invalid in [[[float('nan'),0,1]], [[-1,1,1]], [[.1,.1,.1]]]:
                with patch.object(bundle['model'],'predict_proba',return_value=np.array(invalid)):
                    with self.assertRaises(ValueError):analyze_recording(root/'tone.wav',bundle,root/'bad')


if __name__=='__main__':unittest.main()
