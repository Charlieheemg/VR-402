"""Local acoustic evidence extraction; deliberately produces no PVC score."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from importlib.metadata import version

import numpy as np
import opensmile
import pandas as pd
import soundfile as sf

TEMPORAL = ['audio_duration_s', 'energy_activity_ratio', 'energy_silence_ratio',
            'pause_count', 'mean_pause_duration_s', 'max_pause_duration_s',
            'rms_mean', 'rms_std', 'rms_range', 'word_count', 'words_per_minute',
            'filled_pause_count', 'immediate_token_repeat_count', 'response_latency_s']
HIGHLIGHTS = ['F0semitoneFrom27.5Hz_sma3nz_amean',
              'F0semitoneFrom27.5Hz_sma3nz_stddevNorm',
              'F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2',
              'loudness_sma3_amean', 'loudness_sma3_stddevNorm',
              'jitterLocal_sma3nz_amean', 'shimmerLocaldB_sma3nz_amean',
              'HNRdBACF_sma3nz_amean']


def smile():
    return opensmile.Smile(feature_set=opensmile.FeatureSet.eGeMAPSv02,
                           feature_level=opensmile.FeatureLevel.Functionals)


def feature_names():
    return list(smile().feature_names) + TEMPORAL


def temporal(signal, sr, threshold_db=-35.0, min_pause=0.2):
    """Non-overlapping 20 ms RMS windows; silence means below fixed dBFS gate."""
    if not np.isfinite(threshold_db) or not -120 <= threshold_db <= 0:
        raise ValueError('threshold_db must be finite and within [-120, 0] dBFS')
    if not np.isfinite(min_pause) or min_pause <= 0:
        raise ValueError('min_pause must be finite and positive')
    n = len(signal)
    frame = max(1, round(sr * 0.02))
    starts = np.arange(0, n, frame)
    lengths = np.minimum(frame, n - starts)
    rms = np.sqrt(np.add.reduceat(signal.astype(float)**2, starts) / lengths)
    active = rms > 10**(threshold_db / 20)
    edges = np.flatnonzero(np.diff(np.r_[False, ~active, False]))
    pauses = []
    for start, end in zip(edges[::2], edges[1::2]):
        duration = float(lengths[start:end].sum() / sr)
        # Leading/trailing silence is in silence ratio, not internal pause count.
        if start > 0 and end < len(active) and duration + 1e-9 >= min_pause:
            pauses.append(duration)
    activity = float(lengths[active].sum() / n)
    return dict(audio_duration_s=n / sr, energy_activity_ratio=activity,
                energy_silence_ratio=1-activity, pause_count=len(pauses),
                mean_pause_duration_s=float(np.mean(pauses)) if pauses else 0.0,
                max_pause_duration_s=max(pauses, default=0.0),
                rms_mean=float(np.average(rms, weights=lengths)),
                rms_std=float(np.sqrt(np.average((rms-np.average(rms, weights=lengths))**2, weights=lengths))),
                rms_range=float(np.ptp(rms)))


def extract(path, transcript=None, previous_turn_end=None, response_start=None,
            threshold_db=-35.0, min_pause=0.2, sample_id=None):
    path = Path(path)
    info = sf.info(path)
    if info.format not in ('WAV', 'WAVEX', 'RF64'):
        raise ValueError('Input must be a WAV recording')
    signal, sr = sf.read(path, dtype='float32', always_2d=True)
    if not len(signal) or len(signal)/sr < 0.25 or sr < 8000:
        raise ValueError('Use at least 0.25 seconds of WAV audio at >= 8000 Hz')
    if not np.isfinite(signal).all():
        raise ValueError('Audio contains non-finite samples')
    channels = signal.shape[1]
    signal = signal.mean(axis=1)
    warnings = ['Energy activity is an unvalidated speech-activity approximation, not VAD or a voiced ratio.',
                'Whole-file summaries are not speaker-level PVC evidence unless segmentation is verified.']
    if channels > 1:
        warnings.append('Channels averaged to mono; overlap and phase cancellation can affect measurements.')
    if np.max(np.abs(signal)) < 1e-6:
        warnings.append('Near-silent audio: acoustic descriptors are not meaningful speech evidence.')
    if np.any(np.abs(signal) >= 0.999):
        warnings.append('Samples near full scale: inspect possible clipping.')
    features = temporal(signal, sr, threshold_db, min_pause)
    if features['energy_activity_ratio'] < 0.01:
        warnings.append('Less than 1% energy activity at this gate: inspect recording level and threshold sensitivity; do not infer absence of speech.')
    elif features['energy_activity_ratio'] > 0.99:
        warnings.append('More than 99% energy activity: background noise or the threshold may hide pauses.')
    acoustic = smile().process_signal(signal, sr).iloc[0]
    if len(acoustic) != 88:
        raise RuntimeError(f'Expected 88 eGeMAPSv02 functionals, got {len(acoustic)}')
    features = {**{k: float(v) if np.isfinite(v) else None for k,v in acoustic.items()}, **features}
    if any(v is None for v in features.values()):
        warnings.append('Non-finite acoustic descriptors exported as null; inspect audio quality.')
    features.update({k: None for k in TEMPORAL if k not in features})
    if transcript is not None:
        words = re.findall(r"\b[^\W\d_]+(?:['’][^\W\d_]+)*\b", transcript.lower())
        features.update(word_count=len(words), words_per_minute=len(words)*60/features['audio_duration_s'],
                        filled_pause_count=sum(w in {'um','uh','erm','hmm'} for w in words),
                        immediate_token_repeat_count=sum(a == b for a,b in zip(words, words[1:])))
        warnings.append('Transcript counts require verbatim text for exactly this audio; repeats are tokens, not confirmed disfluencies.')
    if (previous_turn_end is None) != (response_start is None):
        raise ValueError('Supply both previous_turn_end and response_start in the same conversation timebase')
    if previous_turn_end is not None:
        if not all(np.isfinite(v) and v >= 0 for v in [previous_turn_end,response_start]):
            raise ValueError('Timestamps must be finite, nonnegative seconds')
        features['response_latency_s'] = response_start - previous_turn_end
        if response_start < previous_turn_end:
            warnings.append('Negative response latency indicates overlapping turns, not an error.')
    return dict(schema_version='pvc-evidence-0.1', sample_id=sample_id or path.stem,
                audio_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                sample_rate_hz=sr, channels=channels, egemaps_feature_count=88,
                opensmile_version=version('opensmile'), pvc_score=None,
                status='Acoustic evidence only; no human PVC labels or trained PVC model applied.',
                extraction=dict(frame_ms=20, energy_threshold_dbfs=threshold_db,
                                minimum_internal_pause_s=min_pause, mono='channel mean',
                                transcript_supplied=transcript is not None,
                                previous_turn_end_s=previous_turn_end, response_start_s=response_start),
                features=features, warnings=warnings)


def save(result, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    name = re.sub(r'[^A-Za-z0-9_.-]', '_', result['sample_id']).strip('.') or 'sample'
    stem = output / name
    Path(str(stem)+'.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    pd.DataFrame([dict(sample_id=result['sample_id'], **result['features'])]).to_csv(Path(str(stem)+'.csv'), index=False)
    return stem


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('audio', type=Path)
    t = p.add_mutually_exclusive_group()
    t.add_argument('--transcript')
    t.add_argument('--transcript-file', type=Path)
    p.add_argument('--previous-turn-end', type=float)
    p.add_argument('--response-start', type=float)
    p.add_argument('--energy-threshold-db', type=float, default=-35.0)
    p.add_argument('--min-pause', type=float, default=0.2)
    p.add_argument('--sample-id')
    p.add_argument('--output', type=Path, default=Path('results'))
    a = p.parse_args()
    try:
        result = extract(a.audio, a.transcript_file.read_text() if a.transcript_file else a.transcript,
                         a.previous_turn_end, a.response_start, a.energy_threshold_db, a.min_pause, a.sample_id)
        stem = save(result, a.output)
    except (ValueError, RuntimeError, OSError) as e:
        p.error(str(e))
    print(result['status'])
    for key in TEMPORAL + HIGHLIGHTS:
        value = result['features'][key]
        print(f'  {key}: {value:.4f}' if value is not None else f'  {key}: unavailable')
    for warning in result['warnings']:
        print('NOTE:', warning)
    print(f'JSON / CSV: {stem}.json / {stem}.csv')


if __name__ == '__main__':
    main()
