"""Checks prevent diagnostic and proposed design outputs being misrepresented."""
import unittest,json
from collections import Counter,defaultdict
import numpy as np
import pandas as pd
from pilot_assignments import assignments,ROOT
from audit_pitch import compare_frames

class QualityProtocolTests(unittest.TestCase):
    def test_frame_alignment_and_octave_difference(self):
        a=compare_frames(np.array([0.,.01,.02,.03]),np.array([100.,100.,0.,100.]),
                         np.array([0.,.01,.02]),np.array([100.,200.,0.]))
        self.assertEqual(a['compared_frames'],2)
        self.assertEqual(a['aligned_frames'],3)
        self.assertAlmostEqual(a['median_absolute_difference_st'],6)
        self.assertAlmostEqual(a['fraction_above_3st'],.5)
    def test_proposed_assignment_balance_and_no_repeated_text(self):
        rows=assignments();self.assertEqual(len(rows),288)
        self.assertEqual(set(Counter((r['speaker'],r['text'],r['style']) for r in rows).values()),{2})
        groups=defaultdict(list)
        for row in rows:groups[row['listener']].append(row)
        self.assertEqual(len(groups),24)
        for group in groups.values():
            self.assertEqual(len(set(r['text'] for r in group)),12)
            self.assertEqual(Counter(r['style'] for r in group),{'ordinary':6,'clear_instruction':6})
            self.assertEqual(set(Counter(r['speaker'] for r in group).values()),{2})
        self.assertEqual(rows,assignments())
    def test_real_diagnostics_cover_fixed_subset(self):
        d=pd.read_csv(ROOT/'docs/results/edinburgh_pitch_agreement.csv')
        self.assertEqual(len(d),24);self.assertEqual(d.file.nunique(),12)
        self.assertEqual(set(d.sentence),{1,6,9})
        self.assertTrue((d.compared_frames<=d.aligned_frames).all())
        audit=json.loads((ROOT/'docs/results/pitch-audit.json').read_text())
        self.assertTrue(audit['silence_check'])
        self.assertEqual(len(audit['recordings']),12)
    def test_dataset_join_remains_unverified(self):
        d=json.loads((ROOT/'docs/results/dataset-access-audit.json').read_text())
        self.assertFalse(d['audio_label_join_verified']);self.assertEqual(d['models_trained'],0)
        self.assertEqual([r['rows'] for r in d['label_files']],[2421,632])

if __name__=='__main__':unittest.main()
