"""Meeting summary over the existing extractor; all 88 eGeMAPS features still exported."""
import argparse
from pathlib import Path
from analyze import extract, save

DISCLAIMER = 'These are candidate predictors of PVC, not a validated confidence score.'


def summary(result):
    f = result['features']
    def value(key, digits=3):
        number = f[key]
        return 'unavailable' if number is None else f'{number:.{digits}f}'
    lines = ['PVC v0.1 — acoustic evidence', DISCLAIMER, '',
             f"Duration: {value('audio_duration_s')} s",
             f"Energy activity / silence: {100*f['energy_activity_ratio']:.2f}% / {100*f['energy_silence_ratio']:.2f}% "
             f"(unvalidated energy gate at {result['extraction']['energy_threshold_dbfs']:g} dBFS)",
             f"Internal gaps ≥{result['extraction']['minimum_internal_pause_s']:g} s: {f['pause_count']}; "
             f"mean {value('mean_pause_duration_s')} s; max {value('max_pause_duration_s')} s"]
    if f['word_count'] is not None:
        lines.append(f"Transcript: {f['word_count']} words; {value('words_per_minute',1)} words/min (whole clip); "
                     f"{f['filled_pause_count']} literal um/uh/erm/hmm fillers")
    else:
        lines.append('Speech rate / fillers: unavailable (no verbatim transcript supplied)')
    lines += [f"F0: mean {value('F0semitoneFrom27.5Hz_sma3nz_amean')} semitones relative to 27.5 Hz; "
              f"normalised SD {value('F0semitoneFrom27.5Hz_sma3nz_stddevNorm')}; "
              f"20–80 percentile range {value('F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2')} semitones",
              f"Loudness: mean {value('loudness_sma3_amean')} (openSMILE units); "
              f"normalised SD {value('loudness_sma3_stddevNorm')}; frame RMS mean {value('rms_mean',4)} (full scale)",
              f"Voice quality: local jitter {value('jitterLocal_sma3nz_amean')}; "
              f"local shimmer {value('shimmerLocaldB_sma3nz_amean')} dB; HNR {value('HNRdBACF_sma3nz_amean')} dB", '',
              'Gaps may include waiting for other speakers; do not infer hesitation or confidence from them.']
    # Surface recording-specific quality problems without the full feature dump.
    for warning in result['warnings']:
        if any(word in warning for word in ['Less than', 'More than', 'Near-silent', 'clipping', 'Channels', 'Non-finite']):
            lines.append('CHECK: ' + warning)
    return '\n'.join(lines)+'\n'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('audio',type=Path)
    t = p.add_mutually_exclusive_group()
    t.add_argument('--transcript')
    t.add_argument('--transcript-file',type=Path)
    p.add_argument('--sample-id')
    p.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'private/demo')
    a = p.parse_args()
    try:
        transcript = a.transcript_file.read_text() if a.transcript_file else a.transcript
        result = extract(a.audio,transcript=transcript,sample_id=a.sample_id)
        stem = save(result,a.output)
        text = summary(result)
        Path(str(stem)+'.summary.txt').write_text(text)
    except (ValueError,RuntimeError,OSError) as error:
        p.error(str(error))
    print(text)
    print(f'All 88 eGeMAPS features + temporal fields: {stem}.json / {stem}.csv')
    print(f'Meeting summary: {stem}.summary.txt')


if __name__ == '__main__':
    main()
