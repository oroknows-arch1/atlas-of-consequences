#!/usr/bin/env python3
"""Bounded repair routing. Routine failures return to their production owner."""
import json
import subprocess
import sys
from pathlib import Path
from production_state import ROOT, binding, block, read, write

def command(*args): return subprocess.run(args,cwd=ROOT).returncode

def persist(run_dir, message):
    paths=['public/assets','public/review',str(run_dir)]
    if command('git','add','--',*paths): return False
    if subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode==0: return True
    return not(command('git','commit','-m',message) or command('git','push','origin','HEAD:test/automated-edition-1'))

def repair(run_dir, defects):
    owners={d.get('worker') for d in defects}
    if owners <= {'reader_treatment'}:
        return not command(sys.executable,'tools/repair_reader.py',str(run_dir))
    if owners & {'visual_factory','asset_persistence','editorial_factory','reader_builder'}:
        if 'editorial_factory' in owners:
            (run_dir/'editorial-qa.json').unlink(missing_ok=True)
        if 'visual_factory' in owners:
            path=run_dir/'asset-persistence-receipt.json'
            receipt=read(path)
            ids={d.get('scene_id') for d in defects if d.get('worker')=='visual_factory'}
            receipt['assets']=[a for a in receipt['assets'] if a['scene_id'] not in ids and None not in ids]
            write(path,receipt)
        return not command(sys.executable,'tools/produce_edition.py',str(run_dir))
    if owners <= {'source_registrar'}:
        return not command(sys.executable,'tools/source_qa.py',str(run_dir))
    return False

def main(directory):
    run_dir=Path(directory)
    history=[]
    for attempt in range(1,4):
        block(run_dir,'production_orchestrator',f'Review/repair attempt {attempt} in progress')
        # Never reuse a prior deployment or visual verdict after a failed command.
        for name in ('deployment-receipt','rendered-qa','visual-review','benchmark-parity'):
            (run_dir/(name+'.json')).unlink(missing_ok=True)
        if command(sys.executable,'tools/deploy_review.py',str(run_dir)):
            history.append({'attempt':attempt,'worker':'deployment_worker','result':'BLOCKED'})
            write(run_dir/'repair-receipt.json',{'history':history})
            continue
        deploy=read(run_dir/'deployment-receipt.json')
        command('node','tools/rendered_qa.cjs',deploy['url'],str(run_dir/'rendered-qa.json'),str(run_dir/'screenshots'))
        if not (run_dir/'rendered-qa.json').exists():
            block(run_dir,'rendered_qa','Browser did not produce a receipt'); return 1
        dom=read(run_dir/'rendered-qa.json')
        dom.update(binding(run_dir),reader_hashes=deploy['reader_hashes'],deploy_id=deploy['deploy_id'])
        write(run_dir/'rendered-qa.json',dom)
        vision_result=command(sys.executable,'tools/review_rendered.py',str(run_dir))
        if not (run_dir/'visual-review.json').exists():
            block(run_dir,'rendered_qa','Independent visual review did not return a verdict'); return 1
        visual=read(run_dir/'visual-review.json')
        defects=list(visual.get('defects',[]))
        for error in dom.get('errors',[]):
            owner='asset_persistence' if 'missing image' in error else 'reader_treatment' if 'overflow' in error else 'reader_builder'
            defects.append({'worker':owner,'reason':error})
        if vision_result and not defects:
            defects.append({'worker':'editorial_factory','reason':read(run_dir/'benchmark-parity.json').get('reason','benchmark parity failed')})
        history.append({'attempt':attempt,'defects':defects})
        write(run_dir/'repair-receipt.json',{'history':history})
        if not defects and not vision_result:
            return command(sys.executable,'tools/publication_gate.py',str(run_dir))
        if attempt==3 or not repair(run_dir,defects):
            block(run_dir,'repair_orchestrator',json.dumps(defects)); return 1
        if not persist(run_dir,f'Repair Atlas production attempt {attempt}'): return 1
    block(run_dir,'deployment_worker','Deployment retries exhausted')
    return 1

if __name__=='__main__':sys.exit(main(sys.argv[1]))
