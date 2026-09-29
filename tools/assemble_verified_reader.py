#!/usr/bin/env python3
"""Advance a passed structural reader using only persisted, independently checked assets."""
import json
import sys
from pathlib import Path
from production_state import ROOT, read, write, binding, require_current, digest, public_path, reader_hashes
from produce_edition import facts
from editorial_factory import validate_copy
from market_finance import validate as validate_markets
from visual_coverage import plan
from reader_builder import build_reader

def main(run):
    early=read(run/'early-reader-gate.json')
    require_current(run,early)
    if early.get('status')!='PASS' or early.get('defects'):
        raise ValueError('early rendered visual gate has not passed')
    candidate=read(run/'selected-edition-candidate.json')
    edition=candidate['candidate_id']
    routes,requirements,story=facts(run,edition)
    validate_markets(run,routes)
    copy=read(run/'editorial-copy.json')
    editorial=read(run/'editorial-qa.json');require_current(run,editorial)
    if editorial.get('status')!='PASS' or editorial.get('copy_sha256')!=digest(run/'editorial-copy.json'):
        raise ValueError('verified editorial copy changed')
    validate_copy(copy,routes,{s['id'] for s in read(run/'source-register.json')})
    persisted=read(run/'asset-persistence-receipt.json');require_current(run,persisted)
    if persisted.get('status')!='PASS': raise ValueError('verified asset receipt is blocked')
    assets=persisted['assets']
    for asset in assets:
        file=public_path(asset['path'])
        if (not file.is_file() or digest(file)!=asset['sha256'] or file.stat().st_size!=asset['bytes']
            or asset.get('visual_qa',{}).get('pass') is not True or not asset.get('provenance')):
            raise ValueError('asset lacks verified persisted bytes: '+asset['path'])
    coverage=plan(run,routes,requirements,assets,copy)
    if coverage['status']!='PASS' or coverage['gaps']:
        raise ValueError('distinct verified beat coverage incomplete: '+str(len(coverage['gaps'])))
    page=build_reader(run,edition,candidate,routes,story,assets,copy,structural=False)
    for obsolete in ('reader.css','reader.js'):
        (page.parent/obsolete).unlink(missing_ok=True)
    html=page.read_text()
    missing=[a['path'] for a in assets if a['path'] not in html]
    if missing: raise ValueError('persisted assets not connected to reader: '+str(missing))
    if digest(page)!=early['reader_sha256']:
        raise ValueError('full asset wiring changed the approved structural reader; rerun early visual gate')
    result={**binding(run),'state':'ASSEMBLED','assets_persisted':len(assets),
            'reader':str(page.relative_to(ROOT)),'defects':[],
            'next_stage':'full_rendered_qa','publication_authorized':False,
            'reader_hashes':reader_hashes(page)}
    write(run/'production-receipt.json',result)
    write(run/'full-reader-gate.json',{**binding(run),'status':'RENDER_PENDING',
          'reader':str(page.relative_to(ROOT)),'reader_sha256':digest(page),
          'asset_count':len(assets),'beat_count':len(coverage['planned_beats']),
          'asset_generation_authorized':False,'publication_authorized':False})
    print(json.dumps({'state':result['state'],'assets':len(assets),
                      'beats':len(coverage['planned_beats']),'reader':result['reader']},indent=2))

if __name__=='__main__':main(Path(sys.argv[1]).resolve())
