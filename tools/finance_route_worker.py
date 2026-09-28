#!/usr/bin/env python3
"""Append one independently checked finance route without rewriting accepted work."""
import json
import sys
from pathlib import Path

from editorial_factory import model_json, object_schema, validate_copy
from market_finance import DOMAIN, MECHANISMS, SIGNALS, plan, validate
from production_state import binding, digest, read, require_current, write

SCENE_ID='MF1'
P=object_schema({'text':{'type':'string'},'state':{'type':'string','enum':['FACT','UNCERTAIN','INTERPRETATION']},
                 'evidence_refs':{'type':'array','items':{'type':'string'}}})
V=object_schema({'required':{'type':'boolean'},'purpose':{'type':'string'},
                 'truth_boundary':{'type':'string'},
                 'visual_type':{'type':'string','enum':['editorial contextual still','deterministic data graphic','NONE']}})
S=object_schema({'mechanism':{'type':'string','enum':sorted(MECHANISMS)},
                 'heading':{'type':'string'},'paragraphs':{'type':'array','items':P},'visual':V})
SCHEMA=object_schema({'name':{'type':'string'},'entry_label':{'type':'string'},
                      'scenes':{'type':'array','items':S}})
VERDICT=object_schema({'status':{'type':'string','enum':['PASS','BLOCKED']},
                       'defects':{'type':'array','items':{'type':'string'}}})


def assemble(run, output, outline):
    if len(output['scenes'])!=len(outline) or len(outline)<2:
        raise ValueError('finance route lost a required economic mechanism')
    if not SIGNALS.search(output['entry_label']) or not output['name'].strip():
        raise ValueError('finance route is not a visible domain entry')
    register={s['id'] for s in read(run/'source-register.json')}
    old_data=read(run/'visual-data.json')
    scenes=[];copy_blocks={};requirements=[];routing=[];graphics={}
    for i,(made,lead) in enumerate(zip(output['scenes'],outline),1):
        if made['mechanism']!=lead['mechanism']:
            raise ValueError('model changed selected finance mechanism or order')
        sid=f'{SCENE_ID}-S{i}'
        refs=set(lead['evidence_refs'])
        if not refs or refs-register:raise ValueError('unregistered finance evidence')
        for para in made['paragraphs']:
            if not para['text'].strip() or not para['evidence_refs'] or set(para['evidence_refs'])-refs:
                raise ValueError('finance copy lacks matching source refs')
        spec=made['visual']
        if not spec['purpose'] or not spec['truth_boundary']:
            raise ValueError('finance visual lacks purpose or truth boundary')
        if spec['visual_type']=='NONE' and spec['required']:
            raise ValueError('required finance visual cannot be NONE')
        if spec['visual_type']=='deterministic data graphic':
            datum=old_data.get(lead['source_scene'])
            if not datum or datum['source_id'] not in refs:
                raise ValueError(f'{sid} ({lead["source_scene"]}) cannot be a deterministic data graphic: '
                                 'no evidenced datum. Choose an editorial contextual still or NONE; '
                                 'only graphic_eligible_source_scenes may use a graphic')
            graphics[sid]=datum
        scenes.append({'scene_id':sid,'meaning':lead['intent'],'state':'UNCERTAIN' if i==len(outline) else 'KNOWN',
                       'evidence_refs':lead['evidence_refs'],'causal_boundary':lead['boundary'],
                       'knowledge_stop':'Future allocation and investability are unproven.' if i==len(outline) else None,
                       'domains':[DOMAIN],'finance_mechanism':lead['mechanism']})
        copy_blocks[sid]={'heading':made['heading'],'paragraphs':made['paragraphs']}
        requirements.append({'scene_id':sid,**spec})
        routing.append({'scene_id':sid,'required':spec['required'],'purpose':spec['purpose'],
                        'truth_boundary':spec['truth_boundary'],
                        'provider_decision':'DETERMINISTIC' if 'deterministic' in spec['visual_type'] else
                                            'CHATGPT_IMAGES' if spec['required'] else 'NONE','asset_path':None})
    route={'perspective_id':SCENE_ID,'perspective':output['name'],'scenes':scenes}
    perspective={'id':SCENE_ID,'name':output['name'],'entry_label':output['entry_label'],
                 'primary_domain':DOMAIN,'status':'ACCEPTED','necessary':True,
                 'evidence_basis':sorted({ref for lead in outline for ref in lead['evidence_refs']}),
                 'purpose':'Follow measured economic exposure, capital response and unresolved financial distribution.'}
    return route,perspective,copy_blocks,requirements,routing,graphics


def main(run):
    existing=run/'finance-route-receipt.json'
    if existing.exists():
        try:
            receipt=read(existing);require_current(run,receipt)
            if receipt['status']=='PASS' and validate(run,read(run/'causal_boundary_gate.json')['output']['routes'])['status']=='PASS':
                return receipt
        except (KeyError,ValueError):pass
    routes=read(run/'causal_boundary_gate.json')['output']['routes']
    if any(x['perspective_id']==SCENE_ID for x in routes):
        raise ValueError('existing finance route is invalid; do not append a duplicate')
    proposal=plan(run,routes);outline=proposal['route_outline']
    if len(outline)<2:raise ValueError('evidence does not support a meaningful finance route')
    # Give the writer only already accepted scene copy, exact source scopes and the
    # proposed evidence leads. It cannot import outside investment claims.
    original=read(run/'editorial-copy.json')
    data=read(run/'visual-data.json')
    graphic_sources=[lead['source_scene'] for lead in outline
                     if lead['source_scene'] in data and data[lead['source_scene']]['source_id'] in lead['evidence_refs']]
    context={'candidate':read(run/'selected-edition-candidate.json'),
             'outline':outline,'source_register':read(run/'source-register.json'),
             'previously_verified_copy':{x['source_scene']:original['scenes'][x['source_scene']] for x in outline},
             'known_financial_gaps':proposal['financial_evidence_missing'],
             'graphic_eligible_source_scenes':graphic_sources}
    instruction='''Create one visible Markets/Finance Perspective from the supplied, previously verified evidence.
Write one scene for each mechanism in outline order. Preserve each lead's exact factual scope and causal
boundary. Explain measured economic exposure, studied cooling payback and unequal ability to invest or
protect; identify unknown company exposure and valuation explicitly. Never name a security, predict price,
recommend buy/hold/sell, or invent investability. The route name is adaptive. Develop readable, sourced
scene prose and visual purposes. Prefer a distinct contextual asset or sourced data graphic for an
image-led beat. A deterministic data graphic is permitted ONLY for source scenes in
graphic_eligible_source_scenes; for every other scene choose an editorial contextual still or NONE.
The visual purpose for a contextual still must describe context, never imply a measured chart.
NONE is permitted only where evidence makes imagery inappropriate. Return JSON schema.'''
    feedback=[]
    for attempt in range(1,4):
        try:
            output=model_json(instruction+'\nRepair feedback: '+json.dumps(feedback),context,SCHEMA)
            route,perspective,blocks,requirements,routing,graphics=assemble(run,output,outline)
        except (ValueError, KeyError, TypeError) as error:
            feedback=[str(error)]
            continue
        verdict=model_json('''Independently check the proposed finance route against ONLY the existing
verified copy and source register. Block unsupported details, fictitious investability, universalized
payback, hidden uncertainty, thin copy, wrong source attribution, or a missing Markets/Finance entry.
Return PASS only with no defects.''',{'context':context,'proposal':output},VERDICT)
        if verdict['status']=='PASS' and verdict['defects']==[]:break
        feedback=verdict['defects'] or ['independent finance verification failed']
    else:raise RuntimeError('finance route verification exhausted: '+json.dumps(feedback))

    selected=read(run/'selected-edition-perspectives.json')
    selected['output']['perspectives'].append(perspective)
    raw=read(run/'route_scene_generation.json');raw['output']['routes'].append(route)
    bounded=read(run/'causal_boundary_gate.json');bounded['output']['routes'].append(route)
    visuals=read(run/'visual_requirements.json');visuals['output']['requirements'].extend(requirements)
    providers=read(run/'image_provider_routing.json');providers['output']['visuals'].extend(routing)
    data=read(run/'visual-data.json');data.update(graphics)
    selection=read(run/'selected-edition-gate.json');selection['output']['markets_finance_domain']='PASS'
    updated=[('selected-edition-perspectives.json',selected),('route_scene_generation.json',raw),
             ('causal_boundary_gate.json',bounded),('visual_requirements.json',visuals),
             ('image_provider_routing.json',providers),('visual-data.json',data),
             ('selected-edition-gate.json',selection)]
    for name,value in updated:write(run/name,value)
    original['scenes'].update(blocks);write(run/'editorial-copy.json',original)
    new_routes=read(run/'causal_boundary_gate.json')['output']['routes']
    validate_copy(original,new_routes,{s['id'] for s in read(run/'source-register.json')})
    validate(run,new_routes)
    write(run/'editorial-qa.json',{**binding(run),'status':'PASS','defects':[],
          'copy_sha256':digest(run/'editorial-copy.json'),'attempt':attempt,
          'verifier':'previous verified copy preserved; new finance route independently model-verified'})
    receipt={**binding(run),'status':'PASS','perspective_id':SCENE_ID,'name':output['name'],
             'mechanisms':[x['mechanism'] for x in outline],'source_scenes':[x['source_scene'] for x in outline],
             'new_scene_ids':[s['scene_id'] for s in route['scenes']],
             'preserved_scene_count':len(original['scenes'])-len(blocks)}
    write(existing,receipt)
    return receipt


if __name__=='__main__':
    print(json.dumps(main(Path(sys.argv[1])),indent=2))
