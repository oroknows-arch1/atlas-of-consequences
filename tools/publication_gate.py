#!/usr/bin/env python3
"""Only current, complete, deployed and independently inspected work can be a candidate."""
import hashlib
import json
import sys
from pathlib import Path
from urllib.request import urlopen
from production_state import ROOT, digest, public_path, read, require_current, write
from produce_edition import facts

def evaluate(run, fetch=urlopen):
    errors=[]
    def check(worker, function):
        try: return function()
        except Exception as error: errors.append({'worker':worker,'reason':str(error)})
    edition=read(run/'selected-edition-candidate.json')['candidate_id']
    check('editorial_inputs',lambda: facts(run,edition))
    receipts={}
    for name in ('production-receipt','asset-persistence-receipt','editorial-qa',
                 'deployment-receipt','source-qa','rendered-qa','visual-review','benchmark-parity'):
        def load(name=name):
            data=read(run/(name+'.json'))
            require_current(run,data)
            if name=='production-receipt':
                if data.get('state')!='ASSEMBLED' or data.get('defects')!=[]: raise ValueError('production incomplete')
            elif data.get('status')!='PASS': raise ValueError('gate did not PASS')
            if data.get('errors') or data.get('defects'): raise ValueError('known defects remain')
            receipts[name]=data
        check(name,load)
    production=receipts.get('production-receipt',{})
    assets=receipts.get('asset-persistence-receipt',{}).get('assets',[])
    def verify_assets():
        required={v['scene_id'] for v in read(run/'visual_requirements.json')['output']['requirements'] if v['required']}
        ids=[a['scene_id'] for a in assets]
        if set(ids)!=required or len(ids)!=len(set(ids)): raise ValueError('required asset coverage mismatch')
        for asset in assets:
            if not asset.get('provenance') or not asset.get('provider') or asset.get('visual_qa',{}).get('pass') is not True:
                raise ValueError('asset lacks independent QA or provenance')
            path=public_path(asset['path'])
            if digest(path)!=asset['sha256'] or path.stat().st_size!=asset['bytes']:
                raise ValueError('asset hash/size mismatch: '+asset['scene_id'])
    check('asset_persistence',verify_assets)
    hashes=production.get('reader_hashes',{})
    def verify_reader():
        if not hashes or not production.get('reader'): raise ValueError('reader output missing')
        for name, expected in hashes.items():
            path=(ROOT/name).resolve()
            if not path.is_relative_to((ROOT/'public/review').resolve()) or digest(path)!=expected:
                raise ValueError('reader changed since assembly')
        reader=(ROOT/production['reader']).read_text()
        if any(a['path'] not in reader for a in assets): raise ValueError('reader asset reference missing')
        editorial=receipts.get('editorial-qa',{})
        if editorial.get('copy_sha256')!=digest(run/'editorial-copy.json'): raise ValueError('unverified editorial copy')
    check('reader_builder',verify_reader)
    deploy=receipts.get('deployment-receipt',{})
    for name in ('deployment-receipt','rendered-qa','visual-review','benchmark-parity'):
        def freshness(name=name):
            data=receipts.get(name,{})
            if not hashes or data.get('reader_hashes')!=hashes: raise ValueError('different reader build was checked')
            if not deploy.get('deploy_id') or data.get('deploy_id')!=deploy['deploy_id']: raise ValueError('different deployment was checked')
        check(name,freshness)
    def verify_rendered():
        rendered=receipts.get('rendered-qa',{})
        if rendered.get('url')!=deploy.get('url'): raise ValueError('QA URL differs from deployment')
        if not rendered.get('observations') or not rendered.get('screenshots'): raise ValueError('rendered evidence missing')
        for shot in rendered['screenshots']:
            if digest(run/shot['path'])!=shot['sha256']: raise ValueError('screenshot changed after QA')
        for name in ('visual-review','benchmark-parity'):
            if receipts.get(name,{}).get('screenshots')!=rendered['screenshots']: raise ValueError('visual verdict references different screenshots')
    check('rendered_qa',verify_rendered)
    def deployed_bytes():
        if deploy.get('branch')!='test/automated-edition-1' or deploy.get('deployment_result')!='live' or not deploy.get('commit'):
            raise ValueError('wrong review deployment')
        targets=[(a['path'],a['sha256']) for a in assets]+[('/'+p.removeprefix('public/'),h) for p,h in hashes.items()]
        for path, expected in targets:
            with fetch(deploy['base_url'].rstrip('/')+path,timeout=25) as response:
                if hashlib.sha256(response.read()).hexdigest()!=expected: raise ValueError('deployed bytes differ: '+path)
    if not errors: check('deployment',deployed_bytes)
    result={'edition_id':edition,'status':'BLOCKED' if errors else 'PUBLICATION_CANDIDATE',
            'known_required_items':errors,'publication_authorized':False}
    if not errors: result['review_url']=deploy['url']
    write(run/'publication-candidate-receipt.json',result)
    return result

def main(run):
    try: result=evaluate(run)
    except Exception as error:
        result={'status':'BLOCKED','known_required_items':[{'worker':'publication_gate','reason':str(error)}],'publication_authorized':False}
        write(run/'publication-candidate-receipt.json',result)
    print(json.dumps(result,indent=2))
    return result['status']!='PUBLICATION_CANDIDATE'

if __name__=='__main__': sys.exit(main(Path(sys.argv[1])))
