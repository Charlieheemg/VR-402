"""Scientific-contract and replay tests; no network or raw corpus required."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout
import io

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import study

class VoteTests(unittest.TestCase):
    def test_tied_plurality_is_not_resolved(self):
        counts=dict(zip(study.LABELS,[5,5,0,0,1,1]))
        v=study.votes_from_counts(counts)
        self.assertTrue(v['tied'])
        self.assertEqual(v['winners'],['A','D'])
        self.assertIsNone(v['target'])
        self.assertEqual(v['total'],12)

    def test_plurality_need_not_be_absolute_majority(self):
        v=study.votes_from_counts(dict(zip(study.LABELS,[0,3,5,0,3,0])))
        self.assertEqual(v['target'],'F')
        self.assertLess(v['agreement'],.5)

    def test_zero_votes_and_invalid_counts(self):
        v=study.votes_from_counts(dict.fromkeys(study.LABELS,0))
        self.assertIsNone(v['target'])
        self.assertFalse(v['tied'])
        with self.assertRaises(ValueError):
            study.votes_from_counts(dict.fromkeys(study.LABELS,-1))

class StudyEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=json.loads((study.RESULTS/'plan.json').read_text())
        cls.manifest=json.loads((study.RESULTS/'manifest.json').read_text())
        cls.result=json.loads((study.RESULTS/'results.json').read_text())
        cls.features=pd.read_csv(study.RESULTS/'features.csv',float_precision='round_trip')

    def test_all_720_inputs_match_and_have_only_acoustic_predictors(self):
        names=study.validate_inputs(self.plan,self.manifest,self.features)
        self.assertEqual(len(self.features),720)
        self.assertEqual(len(names),88)
        self.assertTrue(set(names).isdisjoint({'actor','intended_label','target','agreement','statement'}))
        self.assertEqual(self.result['predictor_count'],88)
        for filename,expected in self.result['derived_hashes'].items():
            self.assertEqual(study.sha(study.RESULTS/filename),expected)

    def test_partitions_and_actor_1001_isolation(self):
        p=self.plan['partitions']
        self.assertEqual([len(p[s]) for s in ['train','validation','test']],[20,5,5])
        self.assertEqual(len(set(sum(p.values(),[]))),30)
        self.assertNotIn('1001',p['train']+p['validation'])
        self.assertIn('1001',p['test'])
        bad=copy.deepcopy(self.plan)
        bad['partitions']['train'].append('1001')
        with self.assertRaisesRegex(ValueError,'Speaker leakage'):
            study.validate_inputs(bad,self.manifest,self.features)

    def test_targets_recomputed_from_audio_only_counts(self):
        for row in self.manifest['clips']:
            self.assertEqual(row['votes']['query_type'],1)
            self.assertTrue(row['votes']['source_row'].startswith('1'))
            v=study.votes_from_counts(row['votes']['counts'])
            self.assertEqual(v['target'],row['votes']['target'])
        bad=copy.deepcopy(self.manifest)
        tie=next(r for r in bad['clips'] if r['votes']['tied'])
        tie['votes']['target']=tie['votes']['winners'][0]
        with self.assertRaisesRegex(ValueError,'silently resolved tie'):
            study.validate_inputs(self.plan,bad,self.features)

    def test_original_five_include_actual_disagreement(self):
        demos=self.result['demo_clips']
        self.assertEqual(len(demos),5)
        self.assertTrue(all(r['actor']=='1001' and r['split']=='test' for r in demos.values()))
        angry=demos['1001_IEO_ANG_MD.wav']
        self.assertEqual(angry['human']['counts'],dict(zip(study.LABELS,[5,5,0,0,1,1])))
        self.assertIsNone(angry['correct'])
        for emotion in ['HAP','SAD']:
            self.assertEqual(demos[f'1001_IEO_{emotion}_MD.wav']['human']['target'],'N')

    def test_fit_preprocessing_uses_only_unique_target_training_rows(self):
        prep=json.loads((study.RESULTS/'preprocessing.json').read_text())
        files=[r['file'] for r in self.manifest['clips'] if r['split']=='train' and r['votes']['target']]
        self.assertEqual(prep['fit_files'],files)
        X=self.features.set_index('file').loc[files,prep['feature_names']].replace([np.inf,-np.inf],np.nan)
        imputer=SimpleImputer(strategy='median',keep_empty_features=True).fit(X)
        scaler=StandardScaler().fit(imputer.transform(X))
        np.testing.assert_allclose(prep['imputer_medians'],imputer.statistics_)
        np.testing.assert_allclose(prep['scaler_means'],scaler.mean_)
        np.testing.assert_allclose(prep['scaler_scales'],scaler.scale_)

    def test_all_metrics_and_confusion_matrices_recompute(self):
        for split,p in self.result['partitions'].items():
            rows=[r for r in self.result['clips'] if r['split']==split]
            scored=[r for r in rows if r['human']['target']]
            self.assertEqual(len(rows),p['selected_clips'])
            self.assertEqual(len(scored),p['scored_clips'])
            self.assertEqual(sum(r['human']['tied'] for r in rows),p['excluded_ties'])
            for field,key in [('prediction','model'),('baseline_prediction','majority_baseline')]:
                recomputed=study.score([r['human']['target'] for r in scored],[r[field] for r in scored])
                self.assertEqual(recomputed,p[key])
        for r in self.result['clips']:
            self.assertAlmostEqual(sum(r['probabilities'].values()),1)
            if r['human']['tied']:
                self.assertFalse(r['included_in_single_label_scoring'])
                self.assertIsNone(r['correct'])

    def test_baseline_is_training_target_majority(self):
        from collections import Counter
        counts=Counter(r['human']['target'] for r in self.result['clips'] if r['split']=='train' and r['human']['target'])
        majority=counts.most_common(1)[0][0]
        self.assertEqual(majority,self.result['majority_training_class'])
        self.assertTrue(all(r['baseline_prediction']==majority for r in self.result['clips']))

    def test_offline_refit_reproduces_all_predictions_and_metrics(self):
        saved=study.RESULTS
        try:
            with tempfile.TemporaryDirectory() as tmp:
                study.RESULTS=Path(tmp)
                for filename in ['plan.json','manifest.json','features.csv']:
                    (study.RESULTS/filename).write_bytes((saved/filename).read_bytes())
                with redirect_stdout(io.StringIO()):
                    replay=study.fit()
                self.assertEqual(replay['selected_C'],self.result['selected_C'])
                self.assertEqual(replay['partitions'],self.result['partitions'])
                self.assertEqual(replay['clips'],self.result['clips'])
        finally:
            study.RESULTS=saved

if __name__=='__main__':
    unittest.main()
