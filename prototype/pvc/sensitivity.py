"""Re-run fixed-energy threshold sensitivity, reusing the existing temporal extractor."""
import argparse
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform

import numpy as np
import pandas as pd
import soundfile as sf
from analyze import temporal

KEYS = ['energy_activity_ratio', 'energy_silence_ratio', 'pause_count',
        'mean_pause_duration_s', 'max_pause_duration_s']
DEFAULT_ROOT = Path.home()/'Downloads/20260121_150424_AI_Sample'


def run(inputs, thresholds, output, min_pause=0.2):
    if not thresholds or len(set(thresholds)) != len(thresholds):
        raise ValueError('Provide at least one distinct threshold; duplicates are not allowed')
    rows, sources = [], []
    for sample, path in inputs:
        info = sf.info(path)
        if info.format not in ('WAV', 'WAVEX', 'RF64'):
            raise ValueError('Inputs must be WAV recordings')
        signal, sr = sf.read(path, dtype='float32', always_2d=True)
        if not len(signal) or not np.isfinite(signal).all():
            raise ValueError('Inputs must contain finite, non-empty audio')
        channels = signal.shape[1]
        signal = signal.mean(axis=1)
        sources.append(dict(sample_id=sample, audio_sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),
                            sample_rate_hz=sr, channels=channels, duration_s=len(signal)/sr))
        for threshold in sorted(thresholds):
            f = temporal(signal, sr, threshold, min_pause)
            rows.append(dict(sample_id=sample, threshold_dbfs=threshold, **{key:f[key] for key in KEYS}))
    frame = pd.DataFrame(rows)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output/'temporal_sensitivity.csv', index=False)
    metadata = dict(method='Fixed RMS energy gate; not validated speech activity or VAD',
                    thresholds_dbfs=sorted(thresholds), frame_ms=20, minimum_internal_pause_s=min_pause,
                    mono='channel mean', normalization='none', boundary_silence='included in ratio, excluded from pause count',
                    sources=sources, python=platform.python_version(), numpy=version('numpy'), soundfile=version('soundfile'))
    (output/'temporal_sensitivity_metadata.json').write_text(json.dumps(metadata,indent=2,allow_nan=False)+'\n')
    lines = ['# Temporal-feature sensitivity', '',
             'Reproducible fixed-energy analysis; **energy activity is not validated speech activity**. '
             'No human PVC ratings or confidence scores are generated.', '',
             f'20 ms frames, internal gaps ≥{min_pause:g} s; no normalisation. '
             'Leading/trailing silence contributes to the silence ratio, not the pause count. '
             'Source hashes and settings are in `temporal_sensitivity_metadata.json`.', '',
             '| Clip | Gate (dBFS) | Active (%) | Silence (%) | Gaps | Mean gap (s) | Max gap (s) |',
             '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for row in rows:
        lines.append(f"| {row['sample_id']} | {row['threshold_dbfs']:g} | {100*row[KEYS[0]]:.2f} | "
                     f"{100*row[KEYS[1]]:.2f} | {row['pause_count']} | "
                     f"{row[KEYS[3]]:.3f} | {row[KEYS[4]]:.3f} |")
    lines += ['', '## Interpretation', '']
    for sample, part in frame.groupby('sample_id', sort=False):
        lines.append(f"- {sample}: measured activity ranges from {100*part[KEYS[0]].min():.2f}% to "
                     f"{100*part[KEYS[0]].max():.2f}%; qualifying gap count ranges from "
                     f"{part.pause_count.min()} to {part.pause_count.max()} with only the threshold changed.")
    lines += ['', 'Lowering the gate admits more low-energy frames, which may be quiet speech or background noise. '
              'Gap counts need not change monotonically: gaps can split, merge or fall below the minimum duration. '
              'Zeros for mean/max gap mean no qualifying gap, not zero hesitation. '
              'Without manually marked speech/non-speech intervals, this cannot establish which gate is accurate. '
              'Whole-session role recordings also contain waiting time; these are not within-turn hesitation counts.', '',
              '**Next improvement:** manually label a small set of representative quiet/noisy single-speaker clips, '
              'then compare a dedicated local VAD against those intervals before replacing the energy approximation. '
              'Gain normalisation is worth a controlled comparison, but rescales noise as well as speech and '
              'does not solve overlap or turn segmentation. Keep original audio for F0/loudness/voice-quality '
              'extraction; normalising it would change the energy predictors being studied. '
              'No normalisation or new VAD dependency is added in this minimal extension.', '',
              '**Supervisor wording:** “The pause/activity outputs depend strongly on recording level and the '
              'energy threshold. They are useful diagnostics, not validated speech activity or evidence of '
              'confidence change. I need manual segmentation checks and a VAD comparison before interpreting them.”', '']
    (output/'temporal_sensitivity.md').write_text('\n'.join(lines))
    return frame


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sample-root', type=Path, default=DEFAULT_ROOT)
    p.add_argument('--before', type=Path)
    p.add_argument('--after', type=Path)
    p.add_argument('--thresholds', type=float, nargs='+', default=[-55,-50,-45,-40,-35])
    p.add_argument('--min-pause', type=float, default=0.2)
    p.add_argument('--output', type=Path, default=Path(__file__).resolve().parent/'results')
    a = p.parse_args()
    inputs = [('Before',a.before or a.sample_root/'20260121_143844_AI_Before/Team Leader.wav'),
              ('After',a.after or a.sample_root/'20260121_150424_AI_After/Team Leader.wav')]
    try:
        frame = run(inputs,a.thresholds,a.output,a.min_pause)
    except (ValueError,OSError) as error:
        p.error(str(error))
    print(frame.to_string(index=False,float_format=lambda v:f'{v:.4f}'))
    print(f'CSV, metadata and interpretation: {a.output.resolve()}')
    print('Energy activity is not validated speech activity; no PVC score is produced.')


if __name__ == '__main__':
    main()
