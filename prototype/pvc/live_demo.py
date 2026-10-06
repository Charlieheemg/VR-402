"""Offline microphone/WAV demonstration of the external reading-confidence classifier."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from math import gcd
from pathlib import Path
import sys

import joblib
import numpy as np
import pandas as pd
import soundfile as sf
from scipy.signal import resample_poly

from analyze import extract, save
from reading_benchmark import DISCLAIMER, HERE, LABELS, predictor_names, sha

MIC_HELP = ('Microphone unavailable. In macOS System Settings > Privacy & Security > Microphone, '
            'allow the terminal/app running Python, then restart it. Select the microphone in '
            'System Settings > Sound > Input, or use --list-devices and --device ID. '
            'An existing WAV works without microphone access.')


def load_model(path):
    if not Path(path).is_file():
        raise ValueError('Local benchmark model not found. Run reading_benchmark.py first; see docs/live_confidence_demo.md.')
    # joblib is executable serialization: load only locally trained/trusted artifacts.
    bundle = joblib.load(path)
    if bundle.get('kind') != 'external-reading-confidence-v1' or bundle.get('classes') != LABELS:
        raise ValueError('Not an external reading-confidence model with the original three classes')
    if not bundle.get('features') or not set(bundle['features']) <= set(predictor_names()):
        raise ValueError('Incompatible benchmark feature schema')
    if list(bundle['model'].classes_) != list(LABELS):
        raise ValueError('Model class/probability order is incompatible')
    if bundle.get('versions', {}).get('scikit-learn') != version('scikit-learn'):
        raise ValueError('scikit-learn version differs from training. Rebuild locally with the current environment.')
    signature = bundle.get('extraction_signature')
    if signature and (signature['analyze_sha256'] != sha(HERE/'analyze.py') or signature['opensmile'] != version('opensmile')):
        raise ValueError('Extractor/version differs from training. Rebuild the benchmark before demonstrating.')
    return bundle


def sounddevice_module():
    try:
        import sounddevice
        return sounddevice
    except (ImportError, OSError) as error:
        raise ValueError('Install optional microphone support: python -m pip install -r prototype/pvc/requirements-live.txt. '+MIC_HELP) from error


def record_audio(output, device=None):
    sd = sounddevice_module()
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise ValueError('Recording path already exists; choose a new path')
    try:
        info = sd.query_devices(device, 'input')
        rate = int(info['default_samplerate'])
        sd.check_input_settings(device=device, channels=1, dtype='float32', samplerate=rate)
        print(f"Microphone: {info['name']} ({rate} Hz, mono)")
        input('Press Enter to START recording; Ctrl-C cancels. ')
        chunks, statuses = [], []
        frames_seen = 0
        limit = rate*120
        def callback(data, frames, timing, status):
            nonlocal frames_seen
            if status:
                statuses.append(str(status))
            take = min(frames, limit-frames_seen)
            chunks.append(data[:take].copy())
            frames_seen += take
            if frames_seen >= limit:
                raise sd.CallbackStop
        with sd.InputStream(samplerate=rate, device=device, channels=1, dtype='float32', callback=callback):
            input('RECORDING — press Enter to STOP (capture capped at 120 s). ')
        if not chunks or frames_seen < rate*.25:
            raise ValueError('Recording too short; record at least 0.25 seconds')
        sf.write(output, np.concatenate(chunks), rate, subtype='PCM_16')
        if statuses:
            raise ValueError(f'Recording saved but capture reported {sorted(set(statuses))}; retry before analysis.')
        print(f'Recording saved locally: {output}')
        return output
    except (KeyboardInterrupt, EOFError):
        raise ValueError('Recording cancelled; no prediction generated') from None
    except sd.PortAudioError as error:
        raise ValueError(MIC_HELP + ' Details: ' + str(error)) from error


def analyze_recording(audio, bundle, output):
    """Preserve original, make a 16 kHz mono analysis copy, reuse the existing extractor."""
    audio, output = Path(audio), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    info = sf.info(audio)
    if info.format not in ('WAV','WAVEX','RF64'):
        raise ValueError('Supply a WAV recording')
    signal, sr = sf.read(audio, dtype='float32', always_2d=True)
    if sr < 8000 or len(signal)/sr < .25 or not np.isfinite(signal).all():
        raise ValueError('Use finite WAV audio, at least 0.25 seconds, at >=8000 Hz')
    mono = signal.mean(axis=1)
    if np.max(np.abs(mono)) < 1e-6:
        raise ValueError('Near-silent recording: no benchmark prediction generated; check microphone permissions/input')
    notes = ['Uncalibrated classifier probabilities; not clinical evidence or a PVC 1–5 score.',
             'No validated speech detector checks this input. Noise/tones can also produce predictions.',
             'Adult speech, microphone differences, acted delivery and short sentences are outside the training context.',
             'Being inside training duration or feature ranges does not establish validity for adult PVC.']
    context = dict(duration_s=len(signal)/sr, source_sample_rate_hz=sr, source_channels=info.channels,
                   source_rms_full_scale=float(np.sqrt(np.mean(signal.astype(float)**2))),
                   source_peak_full_scale=float(np.max(np.abs(signal))), analysis_sample_rate_hz=16000,
                   analysis_channels=1)
    if context['source_peak_full_scale'] >= .999:
        notes.append('Source samples near full scale: inspect possible clipping before interpreting any output.')
    if info.channels > 1:
        notes.append('Channels averaged to mono; overlapping speakers or phase cancellation may affect results.')
    source_hash = sha(audio)
    analysis_audio = audio
    if sr != 16000 or info.channels != 1:
        if sr != 16000:
            divisor = gcd(sr,16000)
            mono = resample_poly(mono,16000//divisor,sr//divisor)
        analysis_audio = output/'analysis_16k.wav'
        if analysis_audio.resolve() == audio.resolve():
            raise ValueError('Analysis output must not overwrite source recording')
        sf.write(analysis_audio,mono,16000,subtype='FLOAT')
        notes.append('Analysis copy resampled to training rate 16 kHz; original retained, no gain normalisation.')
    result = extract(analysis_audio, sample_id='evidence')
    result['source_audio_sha256'] = source_hash
    result['analysis_preprocessing'] = dict(source_sample_rate=sr, target_sample_rate=16000,
        source_channels=info.channels, normalization=False, resampler='scipy.signal.resample_poly' if sr != 16000 else None)
    save(result,output)
    X = pd.DataFrame([{k:result['features'][k] for k in bundle['features']}])
    probabilities = np.asarray(bundle['model'].predict_proba(X)[0],dtype=float)
    if probabilities.shape != (3,) or not np.isfinite(probabilities).all() or (probabilities<0).any() or (probabilities>1).any() or not np.isclose(probabilities.sum(),1):
        raise ValueError('Invalid model probabilities')
    durations = bundle.get('training_duration_range')
    if durations and not durations[0] <= result['features']['audio_duration_s'] <= durations[1]:
        notes.append(f'Input duration is outside observed training range {durations[0]:.2f}–{durations[1]:.2f} s.')
    output_result = dict(title='External Reading-Confidence Benchmark',disclaimer=DISCLAIMER,
        probabilities={name:float(probabilities[i]) for i,name in enumerate(LABELS.values())},
        predicted_class=list(LABELS.values())[int(np.argmax(probabilities))],
        source_audio_sha256=source_hash, analysis_audio_sha256=result['audio_sha256'],
        notes=notes, model_kind=bundle['kind'], recording_context=context,
        extractor_warnings=result['warnings'])
    write = json.dumps(output_result,indent=2,allow_nan=False)+'\n'
    (output/'prediction.json').write_text(write)
    f = result['features']
    def value(key):
        return 'unavailable' if f[key] is None else f'{f[key]:.4f}'
    lines = [output_result['title'], DISCLAIMER, '',
             *[f'{k}: {v:.4f}' for k,v in output_result['probabilities'].items()],
             'Predicted class: '+output_result['predicted_class'], '',
             'Acoustic measurements (not causal explanations of this prediction):',
             f"Duration: {value('audio_duration_s')} s",
             f"Source: {sr} Hz, {info.channels} channel(s); analysis: 16000 Hz, mono",
             f"Source RMS: {context['source_rms_full_scale']:.6f} full scale; peak {context['source_peak_full_scale']:.6f}",
             f"F0: normalised SD {value('F0semitoneFrom27.5Hz_sma3nz_stddevNorm')}; 20–80 percentile range {value('F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2')} semitones",
             f"Loudness: mean {value('loudness_sma3_amean')} (openSMILE units); normalised SD {value('loudness_sma3_stddevNorm')}",
             f"Voice quality: jitter {value('jitterLocal_sma3nz_amean')}; shimmer {value('shimmerLocaldB_sma3nz_amean')} dB; HNR {value('HNRdBACF_sma3nz_amean')} dB",
             'Fixed-energy pause/activity fields are excluded from classifier inputs.', '',
             *['NOTE: '+n for n in notes],
             *['EXTRACTOR: '+n for n in result['warnings']]]
    text='\n'.join(lines)+'\n'
    (output/'summary.txt').write_text(text)
    return output_result, text


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('audio',nargs='?',type=Path)
    p.add_argument('--record',action='store_true')
    p.add_argument('--list-devices',action='store_true')
    p.add_argument('--device',help='Input device ID or name; otherwise system default')
    p.add_argument('--model',type=Path,default=HERE/'private/reading_benchmark/logistic.joblib',help='Trusted locally trained joblib only')
    p.add_argument('--output',type=Path,help='New local run folder; defaults to ignored private/live_demo/<UTC timestamp>')
    a=p.parse_args()
    print(DISCLAIMER,flush=True)
    try:
        if a.list_devices:
            sd = sounddevice_module()
            try:
                devices = sd.query_devices()
            except sd.PortAudioError as error:
                raise ValueError(MIC_HELP) from error
            if not len(devices):
                raise ValueError('No audio devices visible in this process (a sandbox can hide them). '+MIC_HELP)
            print(devices)
            return
        if bool(a.audio) == a.record:
            raise ValueError('Choose either one WAV path or --record')
        if a.device is not None and not a.record:
            raise ValueError('--device is only used with --record')
        bundle=load_model(a.model)
        output=a.output or HERE/'private/live_demo'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        output.mkdir(parents=True,exist_ok=False)
        device=int(a.device) if a.device and a.device.isdecimal() else a.device
        audio=record_audio(output/'recording.wav',device) if a.record else a.audio
        result,text=analyze_recording(audio,bundle,output)
        print(text)
        print(f'Local recording/evidence/prediction files: {output}')
    except (ValueError,OSError,RuntimeError) as error:
        p.error(str(error))


if __name__ == '__main__':
    main()
