#!/usr/bin/env python3
"""Compute basic metrics from GS artifacts using stochastic defaults.

By default this module introduces small nondeterministic variation (e.g. run ids)
to avoid deterministic outputs.
"""
import json
import pathlib
import sys
import os
from stochastic import random_hex

OUT = pathlib.Path.home() / 'UNIBOT_reports'
TEST_MATRIX = OUT / 'gs_test_matrix.json'
SUMMARY = OUT / 'run_summary.json'


def load_json(p):
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def compute():
    tm = load_json(TEST_MATRIX)
    run = load_json(SUMMARY)
    report = {'passed': [], 'failed': [], 'meta': {}}
    if isinstance(tm, list):
        for t in tm:
            name = t.get('name')
            result = t.get('result')
            entry = {'name': name, 'result': result}
            if result == 'PASS':
                report['passed'].append(entry)
            else:
                report['failed'].append(entry)

    # metadata: include a nondeterministic run id by default.
    # If the run summary already contains a run id, use it; otherwise generate
    # a fresh non-deterministic id. Do not read any environment variables.
    run_id = run.get('run_id') if run and 'run_id' in run else random_hex(8)
    report['meta'] = {
        'total_tests': run.get('total_tests') if run else (len(tm) if isinstance(tm, list) else None),
        'failures': run.get('failures') if run else None,
        'run_id': run_id
    }

    OUT.mkdir(parents=True, exist_ok=True)
    outp = OUT / 'REPORT.md'
    outp.write_text('# GS REPORT\n\n' + json.dumps(report, indent=2))
    print('Wrote', outp)


if __name__ == '__main__':
    compute()
