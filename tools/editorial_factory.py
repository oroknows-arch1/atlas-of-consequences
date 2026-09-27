#!/usr/bin/env python3
"""Turn accepted scene meanings into sourced publication copy, then independently verify.

Never uses an unrelated candidate's legacy evidence_gate/geography_resolution files.
The selected-candidate evidence bundle is the explicit continuation input.
"""
import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from production_state import binding, block, digest, read, require_current, write

def model_json(instruction, data):
    key = os.environ.get('OPENAI_API_KEY')
    if not key:
        raise RuntimeError('OPENAI_API_KEY unavailable')
    body = {'model': os.environ.get('ATLAS_EDITORIAL_MODEL', 'gpt-4.1'),
            'input': [{'role': 'user', 'content': instruction + '\n' + json.dumps(data)}],
            'text': {'format': {'type': 'json_object'}}}
    request = Request('https://api.openai.com/v1/responses', data=json.dumps(body).encode(),
                      headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    with urlopen(request, timeout=180) as response:
        result = json.load(response)
    return json.loads(''.join(p.get('text', '') for x in result.get('output', []) for p in x.get('content', [])))

def validate_copy(copy, routes, source_ids):
    expected = [s['scene_id'] for r in routes for s in r['scenes']]
    if set(copy.get('scenes', {})) != set(expected):
        raise ValueError('editorial copy must cover exactly the accepted scenes')
    for name in ('opening', 'place', 'consequences'):
        if not copy.get(name):
            raise ValueError(f'missing publication section: {name}')
    blocks = [copy[n] for n in ('opening', 'place', 'consequences')] + list(copy['scenes'].values())
    for item in blocks:
        if not item.get('heading') or not item.get('paragraphs'):
            raise ValueError('publication section missing readable copy')
        for paragraph in item['paragraphs']:
            if not isinstance(paragraph.get('text'), str) or not paragraph['text'].strip():
                raise ValueError('empty editorial paragraph')
            if not paragraph.get('evidence_refs') or set(paragraph['evidence_refs']) - source_ids:
                raise ValueError('unregistered paragraph evidence')
            if paragraph.get('state') not in ('FACT', 'UNCERTAIN', 'INTERPRETATION'):
                raise ValueError('missing paragraph truth boundary')

def produce(run, routes):
    target, receipt = run/'editorial-copy.json', run/'editorial-qa.json'
    if target.exists() and receipt.exists():
        previous = read(receipt)
        try:
            require_current(run, previous)
            if previous['status'] == 'PASS' and previous['copy_sha256'] == digest(target):
                validate_copy(read(target), routes, {x['id'] for x in read(run/'source-register.json')})
                return read(target)
        except (KeyError, ValueError):
            pass
    bundle = {name: read(run/(name+'.json')) for name in
              ('selected-edition-candidate', 'selected-edition-gate', 'selected-edition-perspectives',
               'causal_boundary_gate', 'source-register', 'visual-context', 'visual-data')}
    instructions = '''Write publication copy from this accepted evidence bundle, using no outside claims.
Return JSON: {"opening":{"heading":str,"paragraphs":[{"text":str,"state":"FACT|UNCERTAIN|INTERPRETATION","evidence_refs":[source_id]}]},
"place":same,"consequences":same,"scenes":{scene_id:same}}.
Opening must explain the change, place, who is affected and causal limits in substantial readable prose.
PLACE must be geographically grounded at the supported resolution. CONSEQUENCES must separate observed
effects from uncertainty and interpretation. Each accepted scene must have developed prose, not an outline.
Preserve every Perspective, scene meaning and knowledge stop. Do not turn internal instructions into prose.
Facts must stay within supplied direct evidence, population, period and scope. Do not invent measurements,
local detail, personal testimony or stronger causality. Explicitly explain unresolved questions.
Do not rewrite the approved STORY or copy any AOC-001 structure. No fixed scene or Perspective counts.'''
    feedback = []
    for attempt in range(1, 4):
        copy = model_json(instructions, {'evidence': bundle, 'repair_feedback': feedback})
        validate_copy(copy, routes, {x['id'] for x in bundle['source-register']})
        verdict = model_json('''Independently verify publication prose against only the supplied accepted
evidence. Return JSON {"status":"PASS|BLOCKED","defects":[str]}.
Block unsupported facts, mismatched source attribution, changed Perspective/scene meaning, disguised
uncertainty, instructions displayed as article text, thin/outline-only copy, incomplete opening/place/
consequences, or exaggerated causality. Every paragraph source must support the actual assertion.
You did not write this text. Return PASS only with zero defects.''', {'evidence': bundle, 'copy': copy})
        feedback = verdict.get('defects', ['invalid verifier response'])
        write(target, copy)
        write(receipt, {**binding(run), 'status': 'PASS' if verdict.get('status') == 'PASS' and feedback == [] else 'BLOCKED',
                        'defects': feedback, 'copy_sha256': digest(target), 'attempt': attempt,
                        'verifier': os.environ.get('ATLAS_EDITORIAL_MODEL', 'gpt-4.1')})
        if read(receipt)['status'] == 'PASS':
            return copy
    raise RuntimeError('editorial verification exhausted repairs: ' + json.dumps(feedback))

if __name__ == '__main__':
    run = Path(sys.argv[1])
    try:
        produce(run, read(run/'causal_boundary_gate.json')['output']['routes'])
    except Exception as error:
        block(run, 'editorial_factory', error)
        raise
