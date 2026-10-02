#!/usr/bin/env python3
"""Reassemble only from current verified editorial and assets. No provider calls."""
import sys
from pathlib import Path
from production_state import ROOT,read,write,binding,require_current,digest,public_path,reader_hashes,block
from produce_edition import facts
from reader_builder import build_reader

def main(run):
    block(run,'reader_builder','Reader grammar changed; fresh deployment and parity required')
    candidate=read(run/'selected-edition-candidate.json');edition=candidate['candidate_id']
    routes,requirements,story=facts(run,edition)
    qa=read(run/'editorial-qa.json');require_current(run,qa)
    if qa.get('status')!='PASS' or qa['copy_sha256']!=digest(run/'editorial-copy.json'):raise ValueError('current verified copy required')
    receipt=read(run/'asset-persistence-receipt.json');require_current(run,receipt)
    if receipt['status']!='PASS':raise ValueError('verified assets required')
    for a in receipt['assets']:
        if digest(public_path(a['path']))!=a['sha256'] or a['visual_qa'].get('pass') is not True:raise ValueError('asset changed or unverified')
    reader=build_reader(run,edition,candidate,routes,story,receipt['assets'],read(run/'editorial-copy.json'))
    write(run/'production-receipt.json',{**binding(run),'state':'ASSEMBLED','assets_persisted':len(receipt['assets']),'reader':str(reader.relative_to(ROOT)),'reader_hashes':reader_hashes(reader),'defects':[],'next_stage':'rendered_qa','publication_authorized':False})
    print('Reader reassembled; editorial and asset production were not invoked')
if __name__=='__main__':main(Path(sys.argv[1]))
