"""Independent tracker agreement audit; never changes the demo or source audio.

Install optional praat-parselmouth==0.4.7, then run with the PVC Python.
An optional --parselmouth-path supports an isolated dependency directory.
Agreement is a diagnostic, not a human-validated accuracy measurement.
"""
from pathlib import Path
import argparse, hashlib, json, sys
import numpy as np
import pandas as pd
import opensmile
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT/'prototype/pvc/private/edinburgh'

def compare_frames(t, hz, pt, phz):
    """Nearest Praat frame, both voiced, within 5.1 ms; no interpolation of F0."""
    j = np.abs(t[:, None]-pt[None, :]).argmin(axis=1)
    covered = np.abs(t-pt[j]) <= .0051
    both = covered & (hz > 0) & (phz[j] > 0)
    errors = np.abs(12*np.log2(hz[both]/phz[j[both]]))
    return dict(compared_frames=int(both.sum()),
                aligned_frames=int(covered.sum()),
                voicing_disagreement_fraction=float(np.mean((hz[covered]>0)!=(phz[j[covered]]>0))),
                median_absolute_difference_st=float(np.median(errors)) if len(errors) else None,
                fraction_above_3st=float(np.mean(errors>3)) if len(errors) else None)

def run(extra_path=None):
    if extra_path: sys.path.insert(0, extra_path)
    import parselmouth
    private = ROOT/'prototype/pvc/private/quality-review'; private.mkdir(exist_ok=True)
    tracker = opensmile.Smile(feature_set=opensmile.FeatureSet.eGeMAPSv02,
                             feature_level=opensmile.FeatureLevel.LowLevelDescriptors)
    rows=[]; manifests=[]
    for sid in [1, 6, 9]:
        for code in [19, 20, 21, 22]:
            wav=RAW/'clear_speech_wavs'/f'MKH800_{code}_{sid:04d}.wav'
            y,sr=sf.read(wav); lld=tracker.process_file(str(wav))
            st=lld['F0semitoneFrom27.5Hz_sma3nz'].to_numpy()
            t=lld.index.get_level_values('start').total_seconds().to_numpy()
            hz=np.where(st>0,27.5*2**(st/12),0)
            sound=parselmouth.Sound(y,sampling_frequency=sr)
            for floor,ceiling in [(60,400),(75,600)]:
                pitch=sound.to_pitch_ac(time_step=.01,pitch_floor=floor,pitch_ceiling=ceiling)
                pt=pitch.xs(); phz=pitch.selected_array['frequency']
                values=12*np.log2(phz[phz>0]/27.5)
                result=compare_frames(t,hz,pt,phz)
                rows.append(dict(file=wav.name,code=code,sentence=sid,pitch_floor_hz=floor,
                    pitch_ceiling_hz=ceiling,praat_p80_p20_st=float(np.diff(np.percentile(values,[20,80]))[0]),
                    **result))
                if floor==60:
                    pd.DataFrame(dict(time_s=t,opensmile_hz=hz)).to_csv(private/(wav.stem+'-opensmile.csv'),index=False)
                    pd.DataFrame(dict(time_s=pt,praat_hz=phz)).to_csv(private/(wav.stem+'-praat.csv'),index=False)
            manifests.append(dict(file=wav.name,sha256=hashlib.sha256(wav.read_bytes()).hexdigest(),
                                  duration_s=len(y)/sr,peak=float(np.max(abs(y))),
                                  full_scale_samples=int(np.sum(abs(y)>=1))))
    pd.DataFrame(rows).to_csv(ROOT/'docs/results/edinburgh_pitch_agreement.csv',index=False)
    # Known signals check the instrument wiring, not the validity of speech tracking.
    synth=[]
    for freq in [100,150]:
        t=np.arange(16000)/16000
        p=parselmouth.Sound(.2*np.sin(2*np.pi*freq*t),sampling_frequency=16000).to_pitch_ac(time_step=.01,pitch_floor=60,pitch_ceiling=400)
        got=p.selected_array['frequency']; error=abs(float(np.median(got[got>0]))-freq)
        assert error<1
        synth.append(dict(input_hz=freq,median_error_hz=error))
    silence=parselmouth.Sound(np.zeros(16000),sampling_frequency=16000).to_pitch_ac()
    assert not np.any(silence.selected_array['frequency'])
    out=dict(status='Independent automated agreement only; no human pitch reference',
             selection='Sentences 0001,0006,0009 across plain,infant,computer,non-native; selected to cover both known TextGrid anomalies',
             recordings=manifests,parselmouth_version=parselmouth.__version__,
             praat_version=parselmouth.PRAAT_VERSION,opensmile_version=opensmile.__version__,
             numpy_version=np.__version__,synthetic_checks=synth,silence_check=True,
             script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (ROOT/'docs/results/pitch-audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(pd.DataFrame(rows).to_string(index=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--parselmouth-path');args=parser.parse_args()
    run(args.parselmouth_path)
