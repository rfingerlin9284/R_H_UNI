#!/usr/bin/env python3
"""Parse a JUnit XML file and produce GS artifacts (non-deterministic run ids).

This script uses non-deterministic run ids and timestamps by default so
artifacts are not produced from any special environment flag.
"""
import argparse
import datetime
import json
import pathlib
import xml.etree.ElementTree as ET
from stochastic import random_hex


def parse_junit(path):
    tree = ET.parse(path)
    root = tree.getroot()
    tests = []
    for case in root.findall('.//testcase'):
        tc = {
            'id': (case.get('classname') + '.' + case.get('name')) if case.get('classname') else case.get('name'),
            'name': case.get('name'),
            'classname': case.get('classname'),
            'time': float(case.get('time') or 0.0),
            'result': 'PASS'
        }
        if case.find('failure') is not None:
            tc['result'] = 'FAIL'
            tc['message'] = case.find('failure').text or ''
        tests.append(tc)
    return tests


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--junit', required=True)
    p.add_argument('--out', required=True)
    args = p.parse_args()
    outdir = pathlib.Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    tests = parse_junit(args.junit)
    (outdir / 'gs_test_matrix.json').write_text(json.dumps(tests, indent=2))

    # Generate a non-deterministic run id; env vars are not used to make runs reproducible.
    #!/usr/bin/env python3
    """Parse a JUnit XML file and produce GS artifacts (non-deterministic run ids).

    This script uses non-deterministic run ids and timestamps by default so
    artifacts are not produced from any special environment flag.
    """
    import argparse
    import datetime
    import json
    import pathlib
    import xml.etree.ElementTree as ET
    from stochastic import random_hex


    def parse_junit(path):
        tree = ET.parse(path)
        root = tree.getroot()
        tests = []
        for case in root.findall('.//testcase'):
            tc = {
                'id': (case.get('classname') + '.' + case.get('name')) if case.get('classname') else case.get('name'),
                'name': case.get('name'),
                'classname': case.get('classname'),
                'time': float(case.get('time') or 0.0),
                'result': 'PASS'
            }
            if case.find('failure') is not None:
                tc['result'] = 'FAIL'
                tc['message'] = case.find('failure').text or ''
            tests.append(tc)
        return tests


    def main():
        p = argparse.ArgumentParser()
        p.add_argument('--junit', required=True)
        p.add_argument('--out', required=True)
        args = p.parse_args()
        outdir = pathlib.Path(args.out)
        outdir.mkdir(parents=True, exist_ok=True)
        tests = parse_junit(args.junit)
        (outdir / 'gs_test_matrix.json').write_text(json.dumps(tests, indent=2))

        # Generate a non-deterministic run id; env vars are not used to make runs reproducible.
        run_id = random_hex(8)
        started = datetime.datetime.utcnow().isoformat() + 'Z'
        finished = datetime.datetime.utcnow().isoformat() + 'Z'
        summary = {
            'run_id': run_id,
            'started': started,
            'finished': finished,
            'total_tests': len(tests),
            'failures': sum(1 for t in tests if t['result'] == 'FAIL'),
            'artifacts': [str(outdir / 'gs_test_matrix.json')]
        }
        (outdir / 'run_summary.json').write_text(json.dumps(summary, indent=2))
        print('Wrote', outdir / 'gs_test_matrix.json')


    if __name__ == '__main__':
        main()

                tc['message'] = case.find('failure').text or ''
            tests.append(tc)
        return tests


    def main():
        p = argparse.ArgumentParser()
        p.add_argument('--junit', required=True)
        p.add_argument('--out', required=True)
        args = p.parse_args()
        outdir = pathlib.Path(args.out)
        outdir.mkdir(parents=True, exist_ok=True)
        tests = parse_junit(args.junit)
        (outdir / 'gs_test_matrix.json').write_text(json.dumps(tests, indent=2))

    # Generate a non-deterministic run id; env vars are not used to make runs
    # reproducible.
    run_id = random_hex(8)
        started = datetime.datetime.utcnow().isoformat() + 'Z'
        finished = datetime.datetime.utcnow().isoformat() + 'Z'
        summary = {
            'run_id': run_id,
            'started': started,
            'finished': finished,
            'total_tests': len(tests),
            'failures': sum(1 for t in tests if t['result'] == 'FAIL'),
            'artifacts': [str(outdir / 'gs_test_matrix.json')]
        }
        (outdir / 'run_summary.json').write_text(json.dumps(summary, indent=2))
        print('Wrote', outdir / 'gs_test_matrix.json')


    if __name__ == '__main__':
        main()
            tc['result'] = 'FAIL'
