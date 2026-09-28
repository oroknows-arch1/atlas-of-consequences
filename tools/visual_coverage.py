"""Plan a verified visual for each rendered beat, with explicit gaps."""
import hashlib
from reader_builder import chunks
from production_state import binding, read, write


def beats_for(block):
    return [(p, text) for p in block['paragraphs'] for text in chunks(p['text'])]

def effective_spec(spec, scene):
    """Carry rendered visual demand upstream when a narrative scene was opted out."""
    if spec['required']: return spec
    return {**spec,'required':True,'visual_type':'editorial contextual still',
            'purpose':'Contextualize the evidenced scene: '+scene['meaning'],
            'truth_boundary':scene.get('causal_boundary') or
              'Contextual illustration, not a documentary record or measured claim.'}

def shared_specs(copy):
    for key,sid in (('opening','reality-scene'),('consequences','consequences-scene'),('place','place-scene')):
        block=copy[key]
        yield sid,block,{'required':True,'visual_type':'editorial contextual still',
                         'purpose':'Illustrate the sourced '+key+' passage without staging a documented event.',
                         'truth_boundary':'Contextual illustration only; paragraph evidence and scope govern factual claims.'}


def plan(run, routes, requirements, assets, copy):
    specs = {s['scene_id']: s for s in requirements}
    by_beat = {a.get('beat_id', a['scene_id']): a for a in assets}
    route_plans, gaps = {}, []
    for route in routes:
        previous = None
        for scene in route['scenes']:
            sid = scene['scene_id']; spec = effective_spec(specs[sid],scene)
            for i, (paragraph, text) in enumerate(beats_for(copy['scenes'][sid]), 1):
                beat_id = f'{sid}-B{i}'
                # Legacy verified scene assets cover only the first rendered beat.
                asset = by_beat.get(beat_id) or (by_beat.get(sid) if i == 1 else None)
                visual_intent = {'scene_meaning': scene['meaning'], 'beat_text': text,
                                 'purpose': spec['purpose'], 'evidence_refs': paragraph['evidence_refs'],
                                 'truth_boundary': spec['truth_boundary'],
                                 'visual_type':spec['visual_type']}
                stale=asset and asset.get('beat_id') and asset.get('beat_text_sha256') != hashlib.sha256(text.encode()).hexdigest()
                if spec['required'] and (not asset or stale):
                    gaps.append({'code': 'VISUAL_COVERAGE_GAP', 'perspective': route['perspective_id'],
                                 'scene': sid, 'beat_id': beat_id, 'intent': visual_intent,
                                 'reason': 'This rendered beat has no current distinct verified asset'})
                elif asset and previous == asset['path']:
                    reuse = spec.get('intentional_reuse', {}).get(beat_id)
                    if not reuse or not reuse.get('reason') or not reuse.get('reviewed'):
                        gaps.append({'code': 'VISUAL_COVERAGE_GAP', 'perspective': route['perspective_id'],
                                     'scene': sid, 'beat_id': beat_id, 'intent': visual_intent,
                                     'reason': 'Consecutive image repetition lacks reviewed narrative justification'})
                route_plans[beat_id] = {'perspective': route['perspective_id'], 'scene': sid,
                                        'required': spec['required'], 'intent': visual_intent,
                                        'asset_path': asset['path'] if asset else None,
                                        'asset_sha256': asset['sha256'] if asset else None}
                previous = asset['path'] if asset else None
    for sid,block,spec in shared_specs(copy):
        previous=None
        for i,(paragraph,text) in enumerate(beats_for(block),1):
            beat_id=f'{sid}-B{i}'
            asset=by_beat.get(beat_id)
            intent={'scene_meaning':block['heading'],'beat_text':text,'purpose':spec['purpose'],
                    'evidence_refs':paragraph['evidence_refs'],'truth_boundary':spec['truth_boundary'],
                    'visual_type':spec['visual_type']}
            stale=asset and asset.get('beat_text_sha256')!=hashlib.sha256(text.encode()).hexdigest()
            if not asset or stale or previous==asset['path']:
                gaps.append({'code':'VISUAL_COVERAGE_GAP','perspective':sid.split('-')[0],
                             'scene':sid,'beat_id':beat_id,'intent':intent,
                             'reason':'Shared publication beat lacks a current distinct verified contextual asset'})
            route_plans[beat_id]={'perspective':sid.split('-')[0],'scene':sid,'required':True,
                                  'intent':intent,'asset_path':asset['path'] if asset else None,
                                  'asset_sha256':asset['sha256'] if asset else None}
            previous=asset['path'] if asset else None
    receipt = {**binding(run), 'status': 'PASS' if not gaps else 'BLOCKED',
               'planned_beats': route_plans, 'required_count': sum(b['required'] for b in route_plans.values()),
               'verified_count': sum(bool(b['asset_path']) for b in route_plans.values()),
               'gaps': gaps, 'upstream_feedback': gaps}
    write(run/'visual-coverage.json', receipt)
    return receipt
