"""Shared identity and freshness checks for repository-owned manufacturing workers."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = (
    'selected-edition-candidate.json', 'selected-edition-gate.json',
    'selected-edition-perspectives.json', 'route_scene_generation.json',
    'causal_boundary_gate.json', 'story_synthesis.json', 'story_plausibility_gate.json',
    'visual_requirements.json', 'image_provider_routing.json',
    'visual-context.json', 'visual-data.json', 'source-register.json',
)

def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))

def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    temporary.replace(path)

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def identity(run):
    edition = read(Path(run) / INPUTS[0])['candidate_id']
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,80}', edition):
        raise ValueError('unsafe edition identifier')
    return edition

def fingerprint(run):
    return hashlib.sha256(json.dumps({n: digest(Path(run)/n) for n in INPUTS}, sort_keys=True).encode()).hexdigest()

def binding(run):
    return {'edition_id': identity(run), 'input_sha256': fingerprint(run)}

def require_current(run, data):
    for key, value in binding(run).items():
        if data.get(key) != value:
            raise ValueError(f'stale or foreign receipt: {key}')

def public_path(value):
    path = (ROOT/'public'/value.lstrip('/')).resolve()
    if not path.is_relative_to((ROOT/'public').resolve()):
        raise ValueError('asset escapes publication root')
    return path

def reader_hashes(reader):
    reader = Path(reader)
    return {str(p.relative_to(ROOT)): digest(p) for p in sorted(reader.parent.iterdir()) if p.is_file()}

def block(run, worker, reason):
    result = {'edition_id': identity(run), 'status': 'BLOCKED',
              'known_required_items': [{'worker': worker, 'reason': str(reason)}],
              'publication_authorized': False}
    write(Path(run)/'publication-candidate-receipt.json', result)
    return result
