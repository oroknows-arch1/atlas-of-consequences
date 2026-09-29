#!/usr/bin/env python3
"""Build the AOC-001 inherited reader before requesting any new imagery."""
import json
import sys
from pathlib import Path
from production_state import ROOT, read, write, binding, digest
from produce_edition import facts
from reader_builder import build_reader

def main(run):
    candidate=read(run/'selected-edition-candidate.json')
    edition=candidate['candidate_id']
    routes,_,story=facts(run,edition)
    copy=read(run/'editorial-copy.json')
    persisted=read(run/'asset-persistence-receipt.json')
    if persisted['status']!='PASS': raise ValueError('verified asset receipt unavailable')
    page=build_reader(run,edition,candidate,routes,story,persisted['assets'],copy,structural=True)
    inherited=ROOT/'public/adaptive/adaptive.css'
    if digest(page.parent/'adaptive.css')!=digest(inherited):
        raise ValueError('canonical adaptive stylesheet diverged')
    result={**binding(run),'status':'RENDER_PENDING','reader':str(page.relative_to(ROOT)),
            'canonical_css_sha256':digest(inherited),'reader_sha256':digest(page),
            'asset_generation_authorized':False,'publication_authorized':False,
            'note':'Existing verified imagery is reused for structural preview; repeated imagery is not final asset coverage.'}
    write(run/'early-reader-gate.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__': main(Path(sys.argv[1]).resolve())
