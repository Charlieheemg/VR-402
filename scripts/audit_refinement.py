"""Audit existing measurements/OOF predictions without model fitting or changing source data."""
from pathlib import Path
import sys,json,hashlib,re
import numpy as np
import pandas as pd
import soundfile as sf
ROOT=Path(__file__).resolve().parents[1];PVC=ROOT/'prototype/pvc';OUT=ROOT/'docs/results'
sys.path[:0]=[str(ROOT/'scripts'),str(PVC/'edinburgh')]
from reproduce_evidence import timing
from build import intervals

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def metrics(y,p):
 y=np.asarray(y);p=np.asarray(p)
 return float(((p>=.5)==y).mean()),float(((p-y)**2).mean())
def audit():
 raw=PVC/'private/edinburgh';old=pd.read_csv(PVC/'private/consolidation/edinburgh_recordings.csv');rows=[];anomalies=[]
 for code in [19,20,21,22,25]:
  for sid in range(1,26):
   stem=f'MKH800_{code}_{sid:04d}';wav=raw/'clear_speech_wavs'/(stem+'.wav');grid=raw/'clear_speech_TextGrid'/f'MKH800_{code}'/(stem+'.TextGrid')
   info=sf.info(wav);iv=intervals(grid);t=timing(iv);previous=old[(old.code==code)&(old.sentence==sid)].iloc[0]
   for k,v in t.items():assert abs(v-previous[k])<1e-8,(stem,k)
   assert abs(info.duration-previous.duration_s)<1e-9
   rows.append(dict(code=code,sentence=sid,**t))
   end=iv[-1][1];gap=info.duration-end
   if gap>.05:
    y,sr=sf.read(wav);tail=y[round(end*sr):]
    lab=(raw/'clear_speech_labs'/(stem+'.lab')).read_text()
    annotations=re.findall(r'^\s*([\d.]+)\s+\d+\s+(\S+)\s*;',lab,re.M)
    anomalies.append(dict(file=wav.name,wav_duration_s=info.duration,textgrid_end_s=end,uncovered_tail_s=gap,last_hand_label=iv[-1][2],tail_rms_dbfs=float(20*np.log10(np.sqrt(np.mean(tail**2)))),tail_peak=float(np.max(abs(tail))),automatic_last_label=annotations[-1][1],automatic_last_end_s=float(annotations[-1][0]),audio_sha256=sha(wav),textgrid_sha256=sha(grid)))
 assert {r['file'] for r in anomalies}=={'MKH800_20_0006.wav','MKH800_20_0009.wav'}
 pd.DataFrame(anomalies).to_csv(OUT/'edinburgh_annotation_coverage.csv',index=False)
 # Sensitivity is an explicitly labelled comparison, not a replacement for the published n=25 table.
 df=pd.DataFrame(rows);sens=[]
 for c in [20,21,22,25]:
  for mode,ids in [('all_pairs',list(range(1,26))),('exclude_flagged_sentence_ids',[i for i in range(1,26) if i not in [6,9]])]:
   a=df[(df.code==19)&df.sentence.isin(ids)].set_index('sentence');b=df[(df.code==c)&df.sentence.isin(ids)].set_index('sentence')
   for m in ['annotated_span_s','phone_like_s','internal_sil_label_s']:
    d=b[m]-a[m];sens.append(dict(code=c,selection=mode,metric=m,n=len(d),median_difference_s=float(d.median()),positive=int((d>1e-8).sum())))
 pd.DataFrame(sens).to_csv(OUT/'edinburgh_coverage_sensitivity.csv',index=False)
 paired=pd.read_csv(OUT/'edinburgh_paired.csv');summary=pd.read_csv(OUT/'edinburgh_summary.csv')
 for r in paired.itertuples():
  x=old[old.condition==r.condition].set_index('sentence')[r.metric]-old[old.code==19].set_index('sentence')[r.metric]
  assert abs(x.median()-r.median_difference)<1e-8
 for r in summary.itertuples():
  group=old[old.code==r.code]
  for col in summary.columns:
   if col.endswith('_median'):assert abs(group[col[:-7]].median()-getattr(r,col))<1e-8
 # Verify pinned input identity and saved response order before deriving per-fold results.
 source=PVC/'private/r2spin/AllData.csv';rep=json.loads((OUT/'reproduction.json').read_text())
 assert sha(source)==rep['r2spin']['source_sha256']
 oofpath=PVC/'private/consolidation/r2spin_oof.csv';oof=pd.read_csv(oofpath);data=pd.read_csv(source)
 assert len(oof)==6400 and oof.Participant.nunique()==16
 for c in ['Participant','List','WRR']:assert np.array_equal(oof[c],data[c])
 fold=[]
 for lid,g in oof.groupby('List'):
  a,b=metrics(g.WRR,g.context);c,d=metrics(g.WRR,g.context_keyword)
  fold.append(dict(held_out_list=int(lid),responses=len(g),context_accuracy=a,context_brier=b,context_keyword_accuracy=c,context_keyword_brier=d,accuracy_change=c-a,brier_change=d-b))
 pd.DataFrame(fold).to_csv(OUT/'r2spin_per_fold.csv',index=False)
 for r in pd.read_csv(OUT/'r2spin_summary.csv').itertuples():
  a,b=metrics(oof.WRR,oof[r.model]);assert abs(a-r.accuracy)<1e-12 and abs(b-r.brier)<1e-12
 # Cross-check stored nine-example F0 values against full-corpus cached estimates.
 for r in json.loads((raw/'demo/results.json').read_text()):
  row=old[(old.code==int(r['code']))&(old.sentence==int(r['sentence_id']))].iloc[0]
  assert abs(row.f0_range_st-r['f0_range_st'])<1e-7
 result=dict(models_trained=0,annotations_reparsed=125,existing_summaries_match=True,undercovered_textgrids=len(anomalies),r2spin_source_sha256=sha(source),r2spin_oof_sha256=sha(oofpath),r2spin_folds=8,folds_with_accuracy_improvement=sum(r['accuracy_change']>0 for r in fold),folds_with_lower_brier=sum(r['brier_change']<0 for r in fold),f0_status='Existing automated estimates/configuration checked; nine demo values agree with full-corpus cache; no manual pitch validation',script_sha256=sha(Path(__file__)))
 (OUT/'refinement-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':audit()
