"""Small-data PVC regression with leakage-aware out-of-fold evaluation."""
import argparse
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.base import clone
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GroupKFold, KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from analyze import extract, feature_names


def load_data(path):
    path = Path(path)
    df = pd.read_csv(path)
    if 'audio_filename' in df:
        if df.audio_filename.isna().any():
            raise ValueError('Every audio_filename must be populated')
        rows = []
        for _, row in df.iterrows():
            audio = Path(str(row.audio_filename))
            if not audio.is_absolute():
                audio = path.parent / audio
            transcript = row.get('transcript')
            transcript = None if pd.isna(transcript) else str(transcript)
            prev, start = row.get('previous_turn_end_s'), row.get('response_start_s')
            prev = None if pd.isna(prev) else float(prev)
            start = None if pd.isna(start) else float(start)
            rows.append(extract(audio, transcript, prev, start)['features'])
        # Audio mode replaces pre-extracted values, never mixes stale features.
        df = pd.concat([df.drop(columns=[c for c in feature_names() if c in df]), pd.DataFrame(rows)], axis=1)
    return df


def get_xy(df):
    if 'pvc_score' not in df:
        raise ValueError('Missing pvc_score: real aggregated human ratings from 1 to 5 are required')
    y = pd.to_numeric(df.pvc_score, errors='raise').to_numpy(dtype=float)
    if not np.isfinite(y).all() or not ((y >= 1) & (y <= 5)).all():
        raise ValueError('pvc_score must contain finite human ratings between 1 and 5')
    if len(y) < 4 or np.unique(y).size < 2:
        raise ValueError('Need >=4 labelled rows and >=2 distinct ratings for a pipeline run; this is not a sufficiency criterion')
    columns = [c for c in feature_names() if c in df]
    if not columns:
        raise ValueError('No recognised acoustic/temporal features (or audio_filename) supplied')
    X = df[columns].apply(pd.to_numeric, errors='raise')
    if np.isinf(X.to_numpy(dtype=float)).any() or not X.notna().any().any():
        raise ValueError('Features must not contain infinity or be entirely missing')
    return X, y


def splits_for(df, folds):
    if folds < 2:
        raise ValueError('Use at least two folds')
    if 'speaker_id' in df:
        if df.speaker_id.isna().any() or df.speaker_id.astype(str).str.strip().eq('').any():
            raise ValueError('speaker_id is partially missing; supply all speaker IDs or remove the column explicitly')
        groups = df.speaker_id.astype(str).to_numpy()
        n = len(np.unique(groups))
        if n < 2:
            raise ValueError('Speaker-grouped evaluation requires at least two speakers')
        return list(GroupKFold(n_splits=min(folds, n)).split(df, groups=groups)), 'speaker-grouped GroupKFold'
    return list(KFold(n_splits=min(folds, len(df)), shuffle=True, random_state=42).split(df)), 'WARNING: NO SPEAKER IDS; random row CV can leak speaker identity and is not evidence of unseen-speaker generalisation'


def metrics(y, pred):
    rho = None
    if len(y) >= 2 and np.unique(y).size > 1 and np.unique(pred).size > 1:
        value = float(spearmanr(y, pred).statistic)
        rho = value if np.isfinite(value) else None
    return dict(mae=float(mean_absolute_error(y, pred)), spearman=rho,
                spearman_note='null when target or prediction is constant or fold too small')


def train(df, output, folds=5):
    X, y = get_xy(df)
    splits, evaluation = splits_for(df, folds)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    print(evaluation)
    candidates = {'mean': DummyRegressor(strategy='mean'), 'ridge': Ridge(alpha=10.0),
                  'random_forest': RandomForestRegressor(n_estimators=200, min_samples_leaf=2,
                                                         max_depth=5, random_state=42, n_jobs=1)}
    report = dict(status='Pipeline evaluation, not validation of PVC construct or deployment readiness',
                  evaluation=evaluation, rows=len(y), features=list(X.columns),
                  missing_counts={c:int(v) for c,v in X.isna().sum().items()},
                  folds=len(splits), models={},
                  caveats=['Hyperparameters fixed in advance, no model selection or independent final test here.',
                           'Pooled out-of-fold Spearman mixes folds; inspect per-fold metrics, especially mean baseline.',
                           'Same scenario/session leakage remains possible even with speaker grouping.',
                           'Correlated predictors make coefficients and permutation importance unstable; neither is causal.',
                           'Ordinal ratings are treated as approximately continuous; inspect ordinal agreement separately.'])
    predictions = pd.DataFrame({'row_index':np.arange(len(y)), 'pvc_score':y})
    if 'speaker_id' in df:
        predictions['speaker_id'] = df.speaker_id
    predictions['fold'] = -1
    for name, estimator in candidates.items():
        pipe = make_pipeline(SimpleImputer(strategy='median', keep_empty_features=True), StandardScaler(), estimator)
        oof = np.zeros(len(y))
        fold_results, importances = [], []
        for fold, (tr, va) in enumerate(splits):
            fitted = clone(pipe).fit(X.iloc[tr], y[tr])
            pred = fitted.predict(X.iloc[va])
            oof[va] = pred
            predictions.loc[va, 'fold'] = fold
            entry = dict(fold=fold, training_rows=tr.tolist(), validation_rows=va.tolist(), **metrics(y[va], pred))
            if 'speaker_id' in df:
                entry['training_speakers'] = sorted(set(df.iloc[tr].speaker_id.astype(str)))
                entry['validation_speakers'] = sorted(set(df.iloc[va].speaker_id.astype(str)))
            fold_results.append(entry)
            if name == 'random_forest':
                perm = permutation_importance(fitted, X.iloc[va], y[va], scoring='neg_mean_absolute_error', n_repeats=5, random_state=42)
                importances.append(perm.importances_mean)
        predictions[f'{name}_prediction'] = oof
        final = clone(pipe).fit(X, y)
        joblib.dump(dict(schema_version='pvc-model-0.1', model=final, features=list(X.columns),
                         evaluation=evaluation, target='aggregated human PVC rating 1–5', training_rows=len(y)), output / f'{name}.joblib')
        details = dict(**metrics(y, oof), folds=fold_results)
        if name == 'ridge':
            details['standardized_coefficients'] = dict(zip(X.columns, map(float,final[-1].coef_)))
            details['intercept'] = float(final[-1].intercept_)
        if name == 'random_forest':
            details['held_out_permutation_mae_increase'] = dict(zip(X.columns, map(float,np.mean(importances,axis=0))))
            details['impurity_importance'] = dict(zip(X.columns, map(float,final[-1].feature_importances_)))
        report['models'][name] = details
        print(name, metrics(y,oof))
    predictions.to_csv(output/'out_of_fold_predictions.csv',index=False)
    (output/'evaluation.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv',type=Path)
    p.add_argument('--output',type=Path,default=Path('models'))
    p.add_argument('--folds',type=int,default=5)
    a = p.parse_args()
    try:
        train(load_data(a.csv),a.output,a.folds)
    except (ValueError, OSError) as e:
        p.error(str(e))


if __name__ == '__main__':
    main()
