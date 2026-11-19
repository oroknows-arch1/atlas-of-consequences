#!/usr/bin/env python3
"""Record a human visual verdict against the saved rendered QA evidence.

This command deliberately requires an explicit verdict file. It never infers a
PASS from DOM checks or from the presence of screenshots.
"""
import hashlib
import json
import sys
from pathlib import Path

from production_state import binding, read, require_current, write


def main(run, verdict_path):
    verdict = read(verdict_path)
    if verdict.get('status') not in ('PASS', 'BLOCKED') or verdict.get('benchmark_parity') not in ('PASS', 'BLOCKED'):
        raise ValueError('explicit visual and parity verdicts required')
    if not verdict.get('reviewer') or not verdict.get('method') or not verdict.get('observations'):
        raise ValueError('review provenance and observations required')
    defects = verdict.get('defects')
    if not isinstance(defects, list) or (verdict['status'] == 'PASS' and defects):
        raise ValueError('visual verdict conflicts with defects')
    rendered = read(run/'rendered-qa.json')
    deploy = read(run/'deployment-receipt.json')
    contract = read(run/'reader-contract-qa.json')
    require_current(run, rendered)
    require_current(run, contract)
    if rendered['status'] != 'PASS' or contract['status'] != 'PASS':
        raise ValueError('browser and reader contract checks must pass')
    if contract['reader_hashes'] != deploy['reader_hashes'] or contract['deploy_id'] != deploy['deploy_id']:
        raise ValueError('reader contract refers to another build or deployment')
    shots = rendered['screenshots']
    if len(shots) < 100 or not any(s['path'].startswith('screenshots/benchmark-') for s in shots):
        raise ValueError('full candidate and benchmark captures required')
    for shot in shots:
        path = run/shot['path']
        if hashlib.sha256(path.read_bytes()).hexdigest() != shot['sha256']:
            raise ValueError('screenshot changed: '+shot['path'])
    common = {**binding(run), 'reader_hashes':deploy['reader_hashes'],
              'deploy_id':deploy['deploy_id'], 'screenshots':shots,
              'reviewer':verdict['reviewer'], 'method':verdict['method']}
    write(run/'visual-review.json', {**common, 'status':verdict['status'],
          'defects':defects, 'observations':verdict['observations']})
    write(run/'benchmark-parity.json', {**common,
          'status':verdict['benchmark_parity'], 'reason':verdict.get('parity_reason',''),
          'contract_version':contract['version'], 'contract_status':contract['status'],
          'dimensions':verdict.get('parity_dimensions',{})})
    print(json.dumps({'status':verdict['status'], 'benchmark_parity':verdict['benchmark_parity'],
                      'screenshots':len(shots)}))


if __name__ == '__main__':
    main(Path(sys.argv[1]), Path(sys.argv[2]))
