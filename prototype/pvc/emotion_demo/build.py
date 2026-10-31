"""Build a self-contained offline acted-delivery comparison; no emotion inference."""
import argparse
import base64
import csv
import hashlib
import json
import os
import sys
import subprocess
import zipfile
from pathlib import Path

import numpy as np
import opensmile
import soundfile as sf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from analyze import extract

RAV_URL = 'https://zenodo.org/records/1188976/files/Audio_Speech_Actors_01-24.zip'
CREMA_ROOT = 'https://media.githubusercontent.com/media/CheyneyComputerScience/CREMA-D/'
CREMA_REV = '1658cd342dff90010aa843eaeebd53610a08b1dc'
EMOTIONS = {'01':'Neutral','02':'Calm','03':'Happy','04':'Sad','05':'Angry','06':'Fearful','07':'Disgust','08':'Surprised',
            'ANG':'Angry','DIS':'Disgust','FEA':'Fearful','HAP':'Happy','NEU':'Neutral','SAD':'Sad'}

def selections():
    rows = []
    # Fixed before extraction; no ranking by features or listener outcomes.
    for actor in ['01', '02']:
        for statement, text in [('01','Kids are talking by the door.'), ('02','Dogs are sitting by the door.')]:
            for emotion in ['03','04']:
                name = f'03-01-{emotion}-01-{statement}-01-{actor}.wav'
                rows.append(dict(dataset='RAVDESS', actor=actor, statement=statement, transcript=text,
                                 emotion=EMOTIONS[emotion], intensity='normal', repetition='01', file=name))
    for emotion in ['NEU','ANG','FEA','HAP','SAD']:
        # IEO has controlled intensity versions; neutral has XX, others MD.
        intensity = 'XX' if emotion == 'NEU' else 'MD'
        rows.append(dict(dataset='CREMA-D', actor='1001', statement='IEO', transcript="It's eleven o'clock.",
                         emotion=EMOTIONS[emotion], intensity=intensity, repetition=None,
                         file=f'1001_IEO_{emotion}_{intensity}.wav'))
    return rows

def download(url, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(target.suffix + '.part')
    # curl uses the host certificate store, including on macOS Python installs
    # whose bundled OpenSSL does not yet have a configured CA bundle.
    subprocess.run(['curl', '--fail', '--location', '--retry', '2', '--max-time',
                    '600', '--silent', '--show-error', url, '--output', str(partial)], check=True)
    partial.replace(target)

def prepare(raw, archive):
    if not archive.exists():
        print('Downloading original RAVDESS speech archive (~208 MB)', flush=True)
        download(RAV_URL, archive)
    if hashlib.md5(archive.read_bytes()).hexdigest() != 'bc696df654c87fed845eb13823edef8a':
        raise ValueError('RAVDESS archive MD5 differs from the publisher record')
    with zipfile.ZipFile(archive) as z:
        for row in selections():
            target = raw / row['file']
            if row['dataset'] == 'RAVDESS':
                target.write_bytes(z.read(f"Actor_{row['actor']}/{row['file']}"))
            elif not target.exists():
                download(CREMA_ROOT + CREMA_REV + '/AudioWAV/' + row['file'], target)

def build(raw, out):
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    pitch_extractor = opensmile.Smile(feature_set=opensmile.FeatureSet.eGeMAPSv02,
                                     feature_level=opensmile.FeatureLevel.LowLevelDescriptors)
    for selection in selections():
        path = raw / selection['file']
        if not path.is_file():
            raise FileNotFoundError(f'Missing selected WAV: {path}. Run build.py --download or import the original file into --raw.')
        evidence = extract(path, transcript=selection['transcript'])
        y, sr = sf.read(path, always_2d=True)
        y = y.mean(axis=1)
        if np.max(np.abs(y)) < 1e-6:
            raise ValueError(f'Silent selected clip: {path.name}')
        pitch = pitch_extractor.process_signal(y.astype('float32'), sr)['F0semitoneFrom27.5Hz_sma3nz'].to_numpy()
        voiced = pitch[np.isfinite(pitch) & (pitch > 0)]
        enough_pitch = len(voiced) >= 5
        if not enough_pitch:
            evidence['warnings'].append('Fewer than five positive voiced F0 estimates: median and range unavailable.')
        metrics = dict(duration_s=len(y)/sr, rms_dbfs=float(20*np.log10(np.sqrt(np.mean(y*y)))) ,
                       f0_median_hz=float(np.median(27.5*2**(voiced/12))) if enough_pitch else None,
                       f0_range_st=float(np.percentile(voiced,80)-np.percentile(voiced,20)) if enough_pitch else None)
        evidence['demo_pitch_method'] = dict(descriptor='F0semitoneFrom27.5Hz_sma3nz',
            voiced_rule='finite positive F0 estimates; minimum five frames', voiced_frames=int(len(voiced)),
            median='median of 27.5 * 2**(F0_semitones/12), Hz',
            range='80th minus 20th percentile of positive voiced F0, semitones',
            caveat='Algorithmic voiced pitch estimates, not human-validated pitch tracks.')
        source = RAV_URL if selection['dataset'] == 'RAVDESS' else CREMA_ROOT + CREMA_REV + '/AudioWAV/' + selection['file']
        rows.append(dict(**selection, source=source, sha256=evidence['audio_sha256'], sample_rate_hz=sr,
                         metrics=metrics, waveform=[float(np.max(np.abs(a))) for a in np.array_split(y, 180)],
                         evidence=evidence, audio='data:audio/wav;base64,' + base64.b64encode(path.read_bytes()).decode()))
        print(selection['file'], metrics, flush=True)
    payload = dict(schema='acted-delivery-demo-1', selection_policy='Fixed actors/statements/emotions before extraction; illustrative, not representative.',
                   transcript_source='Dataset scripts, not automatic speech recognition.',
                   perceptual_ratings_loaded=False, clips=rows)
    serial = json.dumps(payload, allow_nan=False)
    # Prevent data from terminating the inline script if metadata changes later.
    serial = serial.replace('<', '\\u003c')
    (out/'index.html').write_text((HERE/'template.html').read_text().replace('__DATA__', serial))
    audit = dict(payload, clips=[{k:v for k,v in row.items() if k not in ('audio','waveform')} for row in rows])
    (out/'measurements.json').write_text(json.dumps(audit, indent=2, allow_nan=False)+'\n')
    manifest_fields = ['dataset','licence','source_url','filename','actor','sentence','transcript','delivery_label',
                       'intensity','repetition','human_perception_rating_included','audio_path','sha256']
    with (HERE/'manifest.csv').open('w') as handle:
        writer=csv.DictWriter(handle,fieldnames=manifest_fields,lineterminator='\n')
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(dataset=row['dataset'],licence='CC BY-NC-SA 4.0' if row['dataset']=='RAVDESS' else 'ODbL 1.0; DbCL 1.0',
                source_url=row['source'],filename=row['file'],actor=row['actor'],sentence=row['statement'],transcript=row['transcript'],
                delivery_label=row['emotion'],intensity=row['intensity'],repetition=row['repetition'],
                human_perception_rating_included=False,audio_path=os.path.relpath((raw/row['file']).resolve(),HERE.parents[2]),sha256=row['sha256']))
    with (out/'measurements.csv').open('w') as handle:
        fields = ['dataset','file','actor','statement','emotion','intensity','sha256',*rows[0]['metrics']]
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        for row in rows:
            writer.writerow({**{k:row[k] for k in fields if k in row}, **row['metrics']})
    return rows

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw', type=Path, default=HERE/'private/raw')
    parser.add_argument('--archive', type=Path, default=HERE/'private/ravdess.zip')
    parser.add_argument('--output', type=Path, default=HERE/'private/demo')
    parser.add_argument('--download', action='store_true')
    args = parser.parse_args()
    args.raw.mkdir(parents=True, exist_ok=True)
    if args.download:
        prepare(args.raw, args.archive)
    build(args.raw, args.output)

if __name__ == '__main__':
    main()
