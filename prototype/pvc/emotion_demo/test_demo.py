"""Tests verify corpus controls and real exported audio evidence."""
import hashlib
import csv
import json
import tempfile
import unittest
from pathlib import Path
import numpy as np
import soundfile as sf
import opensmile
from build import HERE, EMOTIONS, selections, build

class SelectionTests(unittest.TestCase):
    def test_ravdess_controls(self):
        rows = [r for r in selections() if r['dataset']=='RAVDESS']
        self.assertEqual(len(rows),8)
        for a,b in zip(rows[::2], rows[1::2]):
            aa,bb=a['file'].split('-'),b['file'].split('-')
            self.assertNotEqual(aa[2],bb[2])
            self.assertEqual(aa[:2]+aa[3:],bb[:2]+bb[3:])
            self.assertEqual(a['transcript'],b['transcript'])

    def test_crema_controls(self):
        rows = [r for r in selections() if r['dataset']=='CREMA-D']
        self.assertEqual(len({r['emotion'] for r in rows}),5)
        self.assertEqual(len({(r['actor'],r['statement'],r['transcript']) for r in rows}),1)

class BuiltEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = HERE/'private/demo'
        cls.payload=json.loads((cls.output/'measurements.json').read_text())

    def test_all_clips_real_and_hashes_match(self):
        self.assertEqual(len(self.payload['clips']),13)
        for row in self.payload['clips']:
            path=HERE/'private/raw'/row['file']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),row['sha256'])
            y,sr=sf.read(path,always_2d=True)
            y=y.mean(axis=1)
            self.assertGreater(np.max(np.abs(y)),1e-6)
            self.assertTrue(np.isfinite(y).all())
            self.assertAlmostEqual(len(y)/sr,row['metrics']['duration_s'])
            self.assertAlmostEqual(20*np.log10(np.sqrt(np.mean(y*y))),row['metrics']['rms_dbfs'])
            self.assertEqual(row['evidence']['egemaps_feature_count'],88)

    def test_measurements_are_not_emotion_predictions(self):
        self.assertFalse(self.payload['perceptual_ratings_loaded'])
        for row in self.payload['clips']:
            self.assertIsNone(row['evidence']['pvc_score'])
            self.assertTrue(all(v is None or np.isfinite(v) for v in row['metrics'].values()))

    def test_offline_bundle_contains_every_audio(self):
        text=(self.output/'index.html').read_text()
        self.assertEqual(text.count('data:audio/wav;base64,'),13)
        self.assertNotIn('__DATA__',text)
        self.assertNotIn('<script src=',text)
        self.assertNotIn('fetch(',text)

    def test_manifest_decodes_to_source_metadata(self):
        with (HERE/'manifest.csv').open() as handle:
            rows=list(csv.DictReader(handle))
        self.assertEqual(len(rows),13)
        for row in rows:
            path=HERE.parents[2]/row['audio_path']
            self.assertTrue(path.is_file())
            self.assertEqual(path.name,row['filename'])
            self.assertEqual(row['human_perception_rating_included'],'False')
            if row['dataset']=='RAVDESS':
                modality,channel,emotion,intensity,statement,repetition,actor=path.stem.split('-')
                self.assertEqual((modality,channel),('03','01'))
                self.assertEqual((actor,statement,repetition),(row['actor'],row['sentence'],row['repetition']))
                self.assertEqual(EMOTIONS[emotion],row['delivery_label'])
                self.assertEqual(intensity,'01')
            else:
                actor,statement,emotion,intensity=path.stem.split('_')
                self.assertEqual((actor,statement,intensity),(row['actor'],row['sentence'],row['intensity']))
                self.assertEqual(EMOTIONS[emotion],row['delivery_label'])

    def test_pitch_reproduces_from_voiced_frames(self):
        extractor=opensmile.Smile(feature_set=opensmile.FeatureSet.eGeMAPSv02,feature_level=opensmile.FeatureLevel.LowLevelDescriptors)
        for row in self.payload['clips']:
            signal,sr=sf.read(HERE/'private/raw'/row['file'],dtype='float32',always_2d=True)
            pitch=extractor.process_signal(signal.mean(axis=1),sr)['F0semitoneFrom27.5Hz_sma3nz'].to_numpy()
            voiced=pitch[np.isfinite(pitch)&(pitch>0)]
            self.assertGreaterEqual(len(voiced),5)
            self.assertAlmostEqual(float(np.median(27.5*2**(voiced/12))),row['metrics']['f0_median_hz'])
            self.assertAlmostEqual(float(np.percentile(voiced,80)-np.percentile(voiced,20)),row['metrics']['f0_range_st'])

    def test_missing_audio_has_actionable_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(FileNotFoundError,'Run build.py --download or import'):
                build(Path(tmp)/'missing',Path(tmp)/'output')

if __name__=='__main__':
    unittest.main()
