#!/usr/bin/env python3
import json, pathlib, sys

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
    # Minimal: treat each test that mentions 'win_rate' or 'pnl' in name as strategy metric
    if isinstance(tm, list):
        for t in tm:
            name = t.get('name')
            result = t.get('result')
            entry = {'name': name, 'result': result}
            # crude pass criteria: PASS tests go to passed
            if result == 'PASS':
                report['passed'].append(entry)
            else:
                report['failed'].append(entry)
    report['meta'] = {'total_tests': run.get('total_tests') if run else None, 'failures': run.get('failures') if run else None}
    outp = OUT / 'REPORT.md'
    outp.write_text('# GS REPORT\n\n' + json.dumps(report, indent=2))
    print('Wrote', outp)

if __name__ == '__main__':
    compute()
