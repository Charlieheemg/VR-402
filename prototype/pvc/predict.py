"""Predict with a locally trained, trusted model; never creates default weights."""
import argparse
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from analyze import extract


def predict(bundle, features):
    missing = [c for c in bundle['features'] if c not in features]
    if missing:
        raise ValueError(f'Missing feature columns: {missing}. Re-extract using the training schema.')
    X = pd.DataFrame([{c:features[c] for c in bundle['features']}]).apply(pd.to_numeric,errors='raise')
    if np.isinf(X.to_numpy(dtype=float)).any() or not X.notna().any().any():
        raise ValueError('Features contain infinity or are entirely missing')
    score = float(bundle['model'].predict(X)[0])
    return dict(predicted_pvc=score, outside_rating_range=not 1 <= score <= 5,
                warning='Model estimate, not ground truth. Unclipped regression output; validation and calibration required.',
                training_evaluation=bundle['evaluation'])


def main():
    p = argparse.ArgumentParser(description=__doc__+' Only load trusted joblib files (pickle can execute code).')
    p.add_argument('model',type=Path)
    p.add_argument('input',type=Path,help='WAV or analyze.py JSON; use JSON to preserve transcript/timestamp features')
    p.add_argument('--output',type=Path)
    a = p.parse_args()
    try:
        bundle = joblib.load(a.model)
        result = json.loads(a.input.read_text()) if a.input.suffix.lower()=='.json' else extract(a.input)
        prediction = predict(bundle,result['features'])
    except (ValueError,OSError,KeyError) as e:
        p.error(str(e))
    text = json.dumps(prediction,indent=2,allow_nan=False)+'\n'
    print(text)
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(text)


if __name__ == '__main__':
    main()
