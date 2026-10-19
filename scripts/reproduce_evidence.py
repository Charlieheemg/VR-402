"""Recompute interim aggregate evidence; raw audio and row-level data remain private.
Run from repository root with prototype/pvc/.venv/bin/python.
"""
from pathlib import Path
import sys,json,hashlib,re,collections
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,brier_score_loss,balanced_accuracy_score,f1_score
from sklearn.model_selection import LeaveOneGroupOut
ROOT=Path(__file__).resolve().parents[1];PVC=ROOT/'prototype/pvc'
sys.path[:0]=[str(PVC),str(PVC/'edinburgh')]
from analyze import extract
from build import intervals,CONDITIONS
OUT=ROOT/'docs/results';PRIV=PVC/'private/consolidation';OUT.mkdir(exist_ok=True);PRIV.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def timing(iv):
    if not iv:raise ValueError('Empty annotation')
    # Include uncertain pure-silence spellings, but never split composite sil+stop labels.
    pure=lambda t:t.replace('?','').strip('() ')=='sil'
    speech=[(a,b,t) for a,b,t in iv if t and not pure(t)]
    start,end=speech[0][0],speech[-1][1]
    return dict(annotated_span_s=end-start,phone_like_s=sum(b-a for a,b,t in speech),internal_sil_label_s=sum(b-a for a,b,t in iv if pure(t) and a>=start and b<=end),uncertain_intervals=sum('?' in t for a,b,t in iv),composite_intervals=sum('+' in t for a,b,t in iv),strict_sil_total_s=sum(b-a for a,b,t in iv if t=='sil'))
def edinburgh():
    raw=PVC/'private/edinburgh';rows=[];manifest=[]
    for c in CONDITIONS:
      for sid in range(1,26):
        stem=f'MKH800_{c}_{sid:04}';wav=raw/'clear_speech_wavs'/(stem+'.wav');grid=raw/'clear_speech_TextGrid'/('MKH800_'+c)/(stem+'.TextGrid')
        t=timing(intervals(grid));result=extract(wav);f=result['features']
        row=dict(sentence=sid,code=c,condition=CONDITIONS[c],duration_s=f['audio_duration_s'],f0_range_st=f['F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2'],**t);rows.append(row)
        manifest.append(dict(stem=stem,audio_sha256=sha(wav),textgrid_sha256=sha(grid)))
    df=pd.DataFrame(rows);df.to_csv(PRIV/'edinburgh_recordings.csv',index=False)
    summary=[]
    for c,name in CONDITIONS.items():
      sub=df[df.code==c];row=dict(code=c,condition=name,n=len(sub))
      for m in ['duration_s','annotated_span_s','phone_like_s','internal_sil_label_s','f0_range_st']:
        row[m+'_median']=float(sub[m].median())
      row['uncertain_intervals']=int(sub.uncertain_intervals.sum());row['composite_intervals']=int(sub.composite_intervals.sum());summary.append(row)
    pd.DataFrame(summary).to_csv(OUT/'edinburgh_summary.csv',index=False)
    paired=[]
    for c in ['20','21','22','25']:
      a=df[df.code=='19'].set_index('sentence');b=df[df.code==c].set_index('sentence');assert a.index.equals(b.index)
      for m in ['annotated_span_s','phone_like_s','internal_sil_label_s','f0_range_st']:
        d=b[m]-a[m];paired.append(dict(condition=CONDITIONS[c],metric=m,n=25,median_difference=float(d.median()),mean_difference=float(d.mean()),positive=int((d>1e-8).sum()),negative=int((d< -1e-8).sum()),zero=int((abs(d)<=1e-8).sum())))
    pd.DataFrame(paired).to_csv(OUT/'edinburgh_paired.csv',index=False)
    (PRIV/'edinburgh_manifest.json').write_text(json.dumps(manifest,indent=2))
    return dict(recordings=len(df),speakers=1,matched_sentences=25,uncertain_intervals=int(df.uncertain_intervals.sum()),composite_intervals=int(df.composite_intervals.sum()),raw_manifest_sha256=sha(PRIV/'edinburgh_manifest.json'))
def r2spin():
    raw=PVC/'private/r2spin/AllData.csv';df=pd.read_csv(raw);df.columns=df.columns.str.strip();assert df.shape==(6400,11);assert df.Participant.nunique()==16
    assert set(df.WRR)=={0,1} and set(df.Pred)=={0,1} and df.KWGP.between(0,100).all()
    # IDs, response order, demographics, retake and outcome never enter predictors.
    X=pd.DataFrame(dict(Pred=df.Pred,male=(df.GenderS=='M').astype(int),KWGP=df.KWGP))
    y=df.WRR.to_numpy();rows=[];oof=df[['Participant','List','WRR']].copy()
    for name,cols in [('context',['Pred']),('context_speaker',['Pred','male']),('context_keyword',['Pred','KWGP']),('context_speaker_keyword',['Pred','male','KWGP'])]:
      prob=np.full(len(df),np.nan)
      for train,test in LeaveOneGroupOut().split(X,y,df.List):
        assert not set(df.List.iloc[train])&set(df.List.iloc[test])
        model=make_pipeline(StandardScaler(),LogisticRegression(C=1.,max_iter=1000,solver='lbfgs'))
        model.fit(X.iloc[train][cols],y[train]);prob[test]=model.predict_proba(X.iloc[test][cols])[:,1]
      assert np.isfinite(prob).all()
      rows.append(dict(model=name,predictors=cols,accuracy=float(accuracy_score(y,prob>=.5)),brier=float(brier_score_loss(y,prob)),n=6400,folds=8));oof[name]=prob
    oof.to_csv(PRIV/'r2spin_oof.csv',index=False)
    pd.DataFrame(rows).to_csv(OUT/'r2spin_summary.csv',index=False)
    return dict(source_commit='a9893f5ada87be2373c366d666d0c47e08dab138',source_sha256=sha(raw),rows=6400,listeners=16,speakers=2,folds='LeaveOneGroupOut(List), eight held-out lists; listeners/speakers shared',models=rows)
def reading():
    import reading_benchmark as rb
    table=pd.read_csv(PVC/'private/reading_benchmark/features.csv');X=table[rb.predictor_names()];y=table.original_class.to_numpy();records=[]
    # Independent refit from saved features; avoid overwriting prior models/results.
    for name,template in rb.models().items():
      from sklearn.base import clone
      pred=np.empty(len(y),dtype=int)
      for tr,te in rb.split_folds(y):pred[te]=clone(template).fit(X.iloc[tr],y[tr]).predict(X.iloc[te])
      records.append(dict(model=name,balanced_accuracy=float(balanced_accuracy_score(y,pred)),macro_f1=float(f1_score(y,pred,average='macro'))))
    historical=json.loads((PVC/'results/reading_confidence/evaluation.json').read_text())
    for r in records:
      for k in ['balanced_accuracy','macro_f1']:assert abs(r[k]-historical['models'][r['model']]['pooled_oof'][k])<1e-10
    pd.DataFrame(records).to_csv(OUT/'reading_reproduction.csv',index=False)
    return dict(n=600,feature_table_sha256=sha(PVC/'private/reading_benchmark/features.csv'),status='Independent refit from saved feature table agrees within 1e-10; extraction not rerun; speaker independence not established',models=records)
def main():
    results=dict(edinburgh=edinburgh(),r2spin=r2spin(),reading=reading())
    from importlib.metadata import version
    results['versions']={p:version(p) for p in ['numpy','pandas','scikit-learn','opensmile','soundfile']}
    results['script_sha256']=sha(Path(__file__))
    (OUT/'reproduction.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
if __name__=='__main__':main()
