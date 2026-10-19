"""Regression checks for the uncovered annotation tails and group-report capacity."""
import unittest
import pandas as pd
import numpy as np
from check_report import check,ROOT
class RefinementTests(unittest.TestCase):
 def test_uncovered_tails_are_retained_and_explicit(self):
  coverage=pd.read_csv(ROOT/'docs/results/edinburgh_annotation_coverage.csv')
  self.assertEqual(set(coverage.file),{'MKH800_20_0006.wav','MKH800_20_0009.wav'})
  self.assertTrue(np.allclose(coverage.wav_duration_s-coverage.textgrid_end_s,coverage.uncovered_tail_s))
  self.assertTrue(coverage.uncovered_tail_s.between(.50,.52).all())
  sensitivity=pd.read_csv(ROOT/'docs/results/edinburgh_coverage_sensitivity.csv')
  self.assertTrue((sensitivity[sensitivity.selection=='all_pairs'].n==25).all())
  self.assertTrue((sensitivity[sensitivity.selection=='exclude_flagged_sentence_ids'].n==23).all())
  for code in [21,22]:
   row=sensitivity[(sensitivity.code==code)&(sensitivity.metric=='annotated_span_s')&(sensitivity.selection=='all_pairs')].iloc[0]
   self.assertEqual(row.positive,25)
 def test_per_fold_summaries_recover_pooled_results(self):
  folds=pd.read_csv(ROOT/'docs/results/r2spin_per_fold.csv');summary=pd.read_csv(ROOT/'docs/results/r2spin_summary.csv').set_index('model')
  self.assertEqual(set(folds.held_out_list),set(range(1,9)))
  self.assertEqual(folds.responses.sum(),6400)
  for model in ['context','context_keyword']:
   for metric in ['accuracy','brier']:
    pooled=np.average(folds[f'{model}_{metric}'],weights=folds.responses)
    self.assertAlmostEqual(pooled,summary.loc[model,metric])
 def test_budget_accounts_for_replacing_placeholders_and_graphics(self):
  r=check()
  self.assertGreater(r['visible_svg_words'],0)
  self.assertEqual(r['main_words'],r['html_main_words']+r['visible_svg_words'])
  self.assertEqual(r['part_b_replacement_capacity'],4000-r['non_part_b_words'])
  self.assertLessEqual(r['completed_group_with_1800_word_part_b'],4000)
  self.assertGreaterEqual(r['section_words']['charlie'],1800)
  self.assertLessEqual(r['section_words']['charlie'],2000)
if __name__=='__main__':unittest.main()
