#!/usr/bin/env python3
"""One independent visual verdict on the deployed inherited reader."""
import base64
import json
import os
import sys
from pathlib import Path
from urllib.request import Request,urlopen
from production_state import binding,read,write,require_current,digest

def main(run):
    live=read(run/'live-reader-gate.json');require_current(run,live)
    if live['status']!='PASS' or live['defects']:raise ValueError('live rendered gate did not pass')
    deploy=read(run/'deployment-receipt.json');require_current(run,deploy)
    if live['deploy_id']!=deploy['deploy_id'] or live['reader_hashes']!=deploy['reader_hashes']:
        raise ValueError('visual screenshots belong to a different deployment')
    key=os.environ.get('OPENAI_API_KEY')
    if not key:raise RuntimeError('OPENAI_API_KEY unavailable for independent visual review')
    pictures=[]
    for shot in live['screenshots']:
        path=run/shot['path']
        if digest(path)!=shot['sha256']:raise ValueError('rendered screenshot changed: '+shot['path'])
        pictures.append({'type':'input_text','text':shot['path']})
        pictures.append({'type':'input_image','image_url':'data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode()})
    schema={'type':'object','properties':{
        'status':{'type':'string','enum':['PASS','BLOCKED']},
        'defects':{'type':'array','items':{'type':'string'}},
        'reason':{'type':'string'}},
        'required':['status','defects','reason'],'additionalProperties':False}
    prompt=('Independently inspect every attached screenshot of the Atlasoquence AET1 test reader. '
            'The images come from the actual deployed site, across phone and desktop opening, Perspective '
            'menu, first factual scene and PLACE. The reader inherits the approved AOC-001 adaptive CSS. '
            'Judge whether the opening lets imagery dominate, the title and prose remain readable, the '
            'vertical Perspective choices remain image-led and complete, scenes have restrained serif '
            'type over visible images, the geographic treatment feels continuous, labels separate fact '
            'from contextual illustration, and mobile composition has no clipped text or dead image. '
            'Do not block merely because a scene is clearly labelled AI contextual art. '
            'Return BLOCKED with concrete screenshot-specific defects when a material issue is visible. '
            'Do not infer source accuracy or unseen routes from screenshots; those are separately checked. '
            'Return PASS only with zero visual defects.')
    body={'model':os.environ.get('ATLAS_VISION_MODEL','gpt-4.1'),
          'input':[{'role':'user','content':[{'type':'input_text','text':prompt}]+pictures}],
          'max_output_tokens':1600,
          'text':{'format':{'type':'json_schema','name':'atlas_visual_verdict',
                            'strict':True,'schema':schema}}}
    req=Request('https://api.openai.com/v1/responses',data=json.dumps(body).encode(),
                headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    with urlopen(req,timeout=180) as response: result=json.load(response)
    if result.get('status')!='completed':raise RuntimeError('independent visual response incomplete')
    verdict=json.loads(''.join(p.get('text','') for x in result.get('output',[]) for p in x.get('content',[])))
    if verdict['status']=='PASS' and verdict['defects']:raise ValueError('contradictory visual verdict')
    receipt={**binding(run),'reader_hashes':deploy['reader_hashes'],'deploy_id':deploy['deploy_id'],
             'screenshots':live['screenshots'],'status':verdict['status'],
             'defects':verdict['defects'],'reason':verdict['reason'],
             'publication_authorized':False}
    write(run/'visual-review.json',receipt)
    print(json.dumps({'status':receipt['status'],'defects':receipt['defects'],
                      'screenshots':len(receipt['screenshots'])},indent=2))
    return receipt['status']!='PASS'

if __name__=='__main__':sys.exit(main(Path(sys.argv[1]).resolve()))
