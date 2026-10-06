"""Paired external reading-confidence demonstration. No numeric confidence-change score."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

from live_demo import MIC_HELP, analyze_recording, load_model, record_audio, sounddevice_module
from reading_benchmark import DISCLAIMER, HERE, LABELS, sha

SCRIPTS = {
    'clinical': 'I recommend that we administer the medication now and reassess the patient in two minutes.',
    'reading': ('On Saturday morning, Maya walked to the local library to return a book about birds. '
                'She stopped beside the garden and watched a small bird carrying a leaf. Inside, the librarian '
                'showed her a shelf of new stories. Maya chose one, sat near the window, and read quietly '
                'until it was time to meet her friend outside.')}


def compare_takes(output, bundle, audio_a=None, audio_b=None, device=None, script='reading', model_path=None):
    if bool(audio_a) != bool(audio_b):
        raise ValueError('Supply both paired WAV paths or neither')
    if script not in SCRIPTS:
        raise ValueError('Unknown reading script')
    output=Path(output)
    output.mkdir(parents=True,exist_ok=False)
    print(DISCLAIMER,flush=True)
    print('Use identical words, microphone, distance, room and input gain for both takes.')
    print('Take A: deliberately tentative. Take B: deliberately assured. Acted conditions are NOT labels.')
    print('Reading:\n'+SCRIPTS[script],flush=True)
    # Freeze the selected device once for this pair rather than re-reading the system default for B.
    if audio_a is None and device is None:
        sd=sounddevice_module()
        try:
            device=int(sd.default.device[0])
        except sd.PortAudioError as error:
            raise ValueError(MIC_HELP) from error
        if device < 0:
            raise ValueError('No default microphone. Use live_demo.py --list-devices and select --device.')
    recordings=[]
    for label,source in [('a',audio_a),('b',audio_b)]:
        folder=output/f'take_{label}'
        folder.mkdir()
        target=folder/'recording.wav'
        if source is not None:
            shutil.copyfile(source,target)
        else:
            print(f'\nTake {label.upper()}',flush=True)
            record_audio(target,device)
        recordings.append(target)
    predictions=[]
    evidence=[]
    for label,audio in zip(['a','b'],recordings):
        prediction,_=analyze_recording(audio,bundle,output/f'take_{label}')
        predictions.append(prediction)
        evidence.append(json.loads((output/f'take_{label}/evidence.json').read_text()))
    rows=[]
    for name in LABELS.values():
        rows.append((name,*[f'{p["probabilities"][name]:.4f}' for p in predictions]))
    rows.append(('Predicted class',*[p['predicted_class'] for p in predictions]))
    for title,key in [('F0 range (semitones)','F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2'),
                      ('Loudness variation (norm SD)','loudness_sma3_stddevNorm'),
                      ('Duration (s)','audio_duration_s')]:
        rows.append((title,*['unavailable' if e['features'][key] is None else f'{e["features"][key]:.4f}' for e in evidence]))
    for title,key in [('Source RMS (full scale)','source_rms_full_scale'),('Source peak (full scale)','source_peak_full_scale'),
                      ('Source sample rate (Hz)','source_sample_rate_hz'),('Source channels','source_channels')]:
        rows.append((title,*[str(p['recording_context'][key]) if isinstance(p['recording_context'][key],int) else f'{p["recording_context"][key]:.6f}' for p in predictions]))
    lines=['External Reading-Confidence Benchmark — paired demonstration',DISCLAIMER,'',
           f'{"Measurement":<32} {"Take A":>14} {"Take B":>14}',
           *[f'{name:<32} {a:>14} {b:>14}' for name,a,b in rows], '',
           'Acted delivery conditions are not ground-truth labels. No numeric confidence-change score is computed.',
           'Acoustic differences are observations, not causal explanations of the model outputs.',
           'The same fixed model is used for both takes; do not choose another model to obtain a preferred ordering.']
    for label,prediction in zip(['A','B'],predictions):
        lines += ['',f'Take {label} notes:',*['- '+n for n in prediction['notes']+prediction['extractor_warnings']]]
    text='\n'.join(lines)+'\n'
    (output/'comparison.txt').write_text(text)
    result=dict(title='External Reading-Confidence Benchmark — paired demonstration',disclaimer=DISCLAIMER,
                script_name=script,suggested_reading=SCRIPTS[script],text_compliance_verified=False,
                model_sha256=sha(model_path) if model_path else None,
                model_estimator=type(bundle['model'][-1]).__name__,same_model_for_both=True,
                source_mode='paired WAV copies' if audio_a else 'microphone',
                takes={'A':predictions[0],'B':predictions[1]},comparisons=[dict(measurement=n,take_a=a,take_b=b) for n,a,b in rows],
                interpretation='Acted conditions are not labels; side-by-side measurements do not establish causal effects or adult PVC validity.')
    (output/'comparison.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    return result,text


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--wav-a',type=Path)
    p.add_argument('--wav-b',type=Path)
    p.add_argument('--script',choices=list(SCRIPTS),default='reading')
    p.add_argument('--device',help='One microphone ID or name used for both takes')
    p.add_argument('--model',type=Path,default=HERE/'private/reading_benchmark/logistic.joblib',help='Same trusted local model for both; default remains logistic')
    p.add_argument('--output',type=Path,help='New folder; default is ignored private/paired_demo/<UTC timestamp>')
    a=p.parse_args()
    print(DISCLAIMER,flush=True)
    try:
        if bool(a.wav_a)!=bool(a.wav_b):
            raise ValueError('Provide both --wav-a and --wav-b, or neither for microphone recording')
        if a.wav_a and a.device is not None:
            raise ValueError('--device is only relevant for microphone recording')
        bundle=load_model(a.model)
        output=a.output or HERE/'private/paired_demo'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        device=int(a.device) if a.device and a.device.isdecimal() else a.device
        _,text=compare_takes(output,bundle,a.wav_a,a.wav_b,device,a.script,a.model)
        print(text)
        print(f'Both recordings and outputs retained locally: {output}')
    except (ValueError,OSError,RuntimeError) as error:
        p.error(str(error))


if __name__=='__main__':main()
