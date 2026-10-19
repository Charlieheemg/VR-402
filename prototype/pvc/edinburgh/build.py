"""Rebuild a local, private acoustic comparison from the Edinburgh deposit."""
import sys,json,re,hashlib,csv
from pathlib import Path
import numpy as np
import soundfile as sf
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from analyze import extract
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'private/edinburgh'
OUT=RAW/'demo'
CONDITIONS={'19':'Plain','20':'Infant-directed','21':'Computer-directed','22':'Non-native-listener-directed','25':'Speech-in-noise'}
def intervals(path):
    text=path.read_text()
    # Long TextGrid format: interval entries only, not tier bounds.
    return [(float(a),float(b),c) for a,b,c in re.findall(r'intervals \[\d+\]:\s*xmin = ([\d.eE+-]+)\s*xmax = ([\d.eE+-]+)\s*text = "([^"]*)"',text)]
def main():
    OUT.mkdir(exist_ok=True)
    prompts={line[:4]:line[5:].strip() for line in (RAW/'clear_speech_prompts.txt').read_text().splitlines() if line.strip()}
    wavs=sorted((RAW/'clear_speech_wavs').rglob('*.wav'))
    grids=[p for p in (RAW/'clear_speech_TextGrid').rglob('*.TextGrid') if '__MACOSX' not in p.parts]
    print('WAVs',len(wavs),'TextGrids',len(grids),flush=True)
    rows=[]
    # Fixed examples; no optimisation against any listener outcome.
    for sid in ['0001','0002','0016']:
      for cond in ['19','21','22']:
        candidates=[p for p in wavs if p.stem==f'MKH800_{cond}_{sid}']
        if len(candidates)!=1: raise ValueError((sid,cond,candidates))
        p=candidates[0]; result=extract(p); f=result['features']; y,sr=sf.read(p)
        gs=[g for g in grids if g.stem==p.stem]
        iv=intervals(gs[0]) if gs else []
        row=dict(sentence_id=sid,condition=CONDITIONS[cond],code=cond,prompt=prompts[sid],file=p.name,audio='../'+str(p.relative_to(RAW)),sha256=result['audio_sha256'],sample_rate=sr,duration_s=len(y)/sr,peak=float(np.max(np.abs(y))),rms_dbfs=float(20*np.log10(np.sqrt(np.mean(y*y)))),f0_range_st=f['F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2'],loudness_sone=f['loudness_sma3_amean'],annotations=len(iv))
        (OUT/(p.stem+'.features.json')).write_text(json.dumps(result,indent=2))
        rows.append(row)
    inventory=dict(wav_count=len(wavs),textgrid_count=len(grids),files=[dict(path=str(p.relative_to(RAW)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in wavs])
    (OUT/'inventory.json').write_text(json.dumps(inventory,indent=2))
    (OUT/'results.json').write_text(json.dumps(rows,indent=2))
    with (OUT/'results.csv').open('w') as h:
      w=csv.DictWriter(h,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    template=(Path(__file__).parent/'template.html').read_text()
    (OUT/'index.html').write_text(template.replace('__DATA__',json.dumps(rows)))
    print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
