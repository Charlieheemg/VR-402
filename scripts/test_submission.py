"""Submission contracts: frozen evidence, metric consistency and link failures."""
import hashlib,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import check_report

ROOT=check_report.ROOT
class SubmissionTests(unittest.TestCase):
    def test_frozen_feedback_baseline(self):
        data=(ROOT/'prototype/feedback/v0.1/fyp_feedback_generator.py').read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(),'8bd8e2ef75f5bb0a77568fd6a5e8ad3688f5e744479f16550a224a241ff66f1f')
        r=json.loads((ROOT/'docs/feedback/results/v01-aggregate.json').read_text())
        self.assertEqual(sum(v['annotation_cells'] for v in r['groups'].values()),371)
        self.assertEqual(r['groups']['AI']['polarity']['unverified'],40)
        self.assertFalse(r['human_or_learning_evaluation'])

    def test_perception_metrics_recover_confusion_matrices(self):
        r=json.loads((ROOT/'docs/results/emotion-study-summary.json').read_text())
        self.assertEqual(sum(v['selected_clips'] for v in r['partitions'].values()),720)
        self.assertEqual(sum(v['excluded_ties'] for v in r['partitions'].values()),62)
        for split in r['partitions'].values():
            for label in ('model','majority_baseline'):
                v=split[label];m=v['confusion_matrix'];f1=[];recall=[]
                self.assertEqual(sum(map(sum,m)),split['scored_clips'])
                self.assertAlmostEqual(sum(m[i][i] for i in range(len(m)))/split['scored_clips'],v['accuracy'])
                for i,row in enumerate(m):
                    col=sum(x[i] for x in m);den=sum(row)+col
                    f1.append(2*row[i]/den if den else 0)
                    if sum(row):recall.append(row[i]/sum(row))
                self.assertAlmostEqual(sum(f1)/6,v['macro_f1'])
                self.assertAlmostEqual(sum(recall)/len(recall),v['balanced_accuracy'])

    def test_link_check_rejects_missing_file_and_fragment(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'index.html';p.write_text('<p id="real">Evidence</p>')
            with patch.object(check_report,'ROOT',root):
                for href in ('missing.html','#missing','../outside.md'):
                    obj=check_report.HTMLIds();obj.feed(f'<a href="{href}">link</a>')
                    with self.assertRaises(AssertionError):check_report.local_links(p,obj)
                obj=check_report.HTMLIds();obj.feed('<a href="#real">valid</a>')
                self.assertEqual(check_report.local_links(p,obj),1)

    def test_visible_diagram_and_references_are_counted(self):
        p=check_report.Report();p.feed('<main><section data-part="shared"><figure><div>visible diagram words</div></figure></section><section data-part="references">reference words<script>hidden words</script></section></main>')
        self.assertEqual(' '.join(p.by_bucket['shared']),'visible diagram words')
        self.assertEqual(' '.join(p.by_bucket['references']),'reference words')
        r=check_report.check()
        self.assertGreater(r['section_words']['references'],0)
        self.assertEqual(sum(r['section_words'].values()),r['main_words'])
        self.assertLessEqual(r['main_words'],4000)

if __name__=='__main__':unittest.main()
