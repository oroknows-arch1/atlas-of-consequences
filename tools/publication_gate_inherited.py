#!/usr/bin/env python3
"""Fail-closed candidate gate for the AOC-001 inherited reader, not publication."""
import json
import sys
from pathlib import Path
from production_state import ROOT,binding,digest,public_path,read,require_current,write
from produce_edition import facts
from editorial_factory import validate_copy
from market_finance import validate as validate_markets
from visual_coverage import plan

def evaluate(run):
    errors=[];proof={}
    for name in ('early-reader-gate','full-reader-gate','production-receipt',
                 'asset-persistence-receipt','editorial-qa','source-qa',
                 'deployment-receipt','live-reader-gate','visual-review'):
        try:
            data=read(run/(name+'.json'));require_current(run,data)
            if name=='production-receipt':
                if data.get('state')!='ASSEMBLED' or data.get('defects'):raise ValueError('reader assembly incomplete')
            elif data.get('status')!='PASS' or data.get('defects') or data.get('errors'):
                raise ValueError('gate did not pass cleanly')
            proof[name]=data
        except Exception as error:errors.append({'worker':name,'reason':str(error)})
    try:
        candidate=read(run/'selected-edition-candidate.json');edition=candidate['candidate_id']
        routes,requirements,_=facts(run,edition)
        validate_markets(run,routes)
        copy=read(run/'editorial-copy.json')
        if proof['editorial-qa']['copy_sha256']!=digest(run/'editorial-copy.json'):
            raise ValueError('editorial copy changed after independent QA')
        validate_copy(copy,routes,{s['id'] for s in read(run/'source-register.json')})
        assets=proof['asset-persistence-receipt']['assets']
        coverage=plan(run,routes,requirements,assets,copy)
        if coverage['status']!='PASS' or coverage['gaps'] or len(assets)!=proof['full-reader-gate']['asset_count']:
            raise ValueError('persisted beat coverage incomplete')
        for asset in assets:
            file=public_path(asset['path'])
            if (not file.is_file() or digest(file)!=asset['sha256'] or
                file.stat().st_size!=asset['bytes'] or asset.get('visual_qa',{}).get('pass') is not True):
                raise ValueError('asset persistence changed: '+asset['path'])
        production=proof['production-receipt'];reader=ROOT/production['reader']
        if production['reader_hashes'].get(production['reader'])!=proof['early-reader-gate']['reader_sha256']:
            raise ValueError('final reader diverged from early approved structure')
        for name,expected in production['reader_hashes'].items():
            if digest(ROOT/name)!=expected:raise ValueError('reader file changed: '+name)
        html=reader.read_text()
        if any(a['path'] not in html for a in assets) or 'STORY / FICTION' not in html:
            raise ValueError('asset connection or fiction boundary missing')
        if html.count('class="purposeful-ending"')!=len(routes):
            raise ValueError('Perspective ending coverage incomplete')
        deployment=proof['deployment-receipt'];live=proof['live-reader-gate'];visual=proof['visual-review']
        if (deployment['branch']!='test/automated-edition-1' or deployment['deployment_result']!='live' or
            deployment['asset_integration_status']!='PASS' or not deployment['commit']):
            raise ValueError('isolated review deployment incomplete')
        for item in (live,visual):
            if item['deploy_id']!=deployment['deploy_id'] or item['reader_hashes']!=production['reader_hashes']:
                raise ValueError('review checked a different reader or deployment')
        if live['url']!=deployment['url'] or visual['screenshots']!=live['screenshots']:
            raise ValueError('independent visual review checked different images')
        for shot in live['screenshots']:
            if digest(run/shot['path'])!=shot['sha256']:
                raise ValueError('review screenshot changed: '+shot['path'])
    except Exception as error:errors.append({'worker':'publication_completeness','reason':str(error)})
    result={**binding(run),'status':'BLOCKED' if errors else 'PUBLICATION_CANDIDATE',
            'known_required_items':errors,'publication_authorized':False}
    if not errors:result['review_url']=proof['deployment-receipt']['url']
    write(run/'publication-candidate-receipt.json',result)
    return result

if __name__=='__main__':
    result=evaluate(Path(sys.argv[1]).resolve())
    print(json.dumps(result,indent=2))
    sys.exit(result['status']!='PUBLICATION_CANDIDATE')
