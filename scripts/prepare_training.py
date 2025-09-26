#!/usr/bin/env python3
"""Prepare training data from GS artifacts.

Usage:
  scripts/prepare_training.py --in <artifact_dir> --out <out_dir>

By default it looks for `gs_test_matrix.json` and `run_summary.json` under
`$HOME/UNIBOT_reports` (the default GS output) and `artifacts/*/reports`.

The script writes a compact `gs_training.json` with one entry per test case
containing basic fields useful for simple downstream training/analysis.
"""
import argparse
import json
import pathlib
import sys
from typing import Optional


def find_artifact_dir(search_paths):
    for p in search_paths:
        p = pathlib.Path(p).expanduser()
        if p.exists() and p.is_dir():
            return p
    # fallback: try artifacts/*/reports
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    for d in repo_root.glob('artifacts/*/reports'):
        return d
    return None


def load_json(p: pathlib.Path) -> Optional[object]:
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return None


def prepare(in_dir: pathlib.Path, out_dir: pathlib.Path):
    matrix_path = in_dir / 'gs_test_matrix.json'
    summary_path = in_dir / 'run_summary.json'

    matrix = load_json(matrix_path) or []
    summary = load_json(summary_path) or {}

    out = []
    for tc in matrix:
        entry = {
            'id': tc.get('id') or tc.get('name'),
            'name': tc.get('name'),
            'classname': tc.get('classname'),
            'time': tc.get('time'),
            'result': tc.get('result'),
        }
        # minimal features for training: pass (1/0), time
        entry['label'] = 1 if tc.get('result') == 'PASS' else 0
        entry['time_s'] = float(tc.get('time') or 0.0)
        out.append(entry)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'gs_training.json'
    out_file.write_text(json.dumps({'meta': summary, 'tests': out}, indent=2), encoding='utf-8')
    print('Wrote', out_file)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--in', dest='in_dir', default=None, help='Input artifact directory')
    p.add_argument('--out', dest='out_dir', default='training_data', help='Output directory')
    args = p.parse_args(argv)

    search_paths = []
    if args.in_dir:
        search_paths.append(args.in_dir)
    # common default
    search_paths.append('~/UNIBOT_reports')

    art = find_artifact_dir(search_paths)
    if art is None:
        print('No artifact directory found. Please run the GS battery first or pass --in.', file=sys.stderr)
        sys.exit(2)

    out_dir = pathlib.Path(args.out_dir)
    prepare(art, out_dir)


if __name__ == '__main__':
    main()
