#!/usr/bin/env python3
"""Reusable motion-job preparation and verified import; never treats stills as film.

Prepare only reuses an existing image. Generation is an authorized provider node.
Import requires independent visual QA and verifies its binding to the actual MP4.
"""
import argparse,json,subprocess
from pathlib import Path
from production_state import ROOT,read,write,binding,require_current,digest,public_path

def prepare(run):
    assets=read(run/'asset-persistence-receipt.json');require_current(run,assets)
    source=next(a for a in assets['assets'] if a['provider']!='ATLAS_DETERMINISTIC_GRAPHIC')
    if digest(public_path(source['path']))!=source['sha256']:raise ValueError('opening source asset changed')
    candidate=read(run/'selected-edition-candidate.json')
    job={**binding(run),'kind':'motion_video','required':True,'source_path':source['path'],'source_sha256':source['sha256'],
         'source_scene_id':source['scene_id'],'duration_seconds':10,'aspect_ratio':'9:16',
         'prompt':f"Animate this existing Atlas contextual illustration as a restrained cinematic opening for {candidate['working_title']}, set in {candidate['geographic_core']}. Preserve the established place, composition, people and natural warm-neutral grade. Very slow forward camera drift, subtle natural environmental motion and ordinary unhurried movements; continuity throughout, no cuts, no invented disaster or dramatic event, no added people, lettering, logos or narration. This is explicitly an AI-generated contextual film, not documentary footage. Retain the factual boundary: {source['truth_boundary']}",
         'publication_label':'AI-generated contextual film · not documentary evidence',
         'provider':'Runway','status':'AWAITING_PROVIDER'}
    write(run/'opening-media-job.json',job);return job

def accept(run,file,provenance,qa_file):
    job=read(run/'opening-media-job.json');require_current(run,job)
    qa=read(qa_file);require_current(run,qa)
    if qa.get('status')!='PASS' or qa.get('sha256')!=digest(file) or not qa.get('reviewer') or not qa.get('reason'):raise ValueError('independent motion QA missing or for different binary')
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(file)]))
    video=next(s for s in probe['streams'] if s['codec_type']=='video')
    duration=float(probe['format']['duration'])
    if duration<4 or min(video['width'],video['height'])<600:raise ValueError('motion below publication quality')
    path=ROOT/'public/assets'/job['edition_id'].lower()/'opening.mp4';path.write_bytes(file.read_bytes())
    receipt={**binding(run),'status':'PASS','kind':'motion_video','path':'/'+str(path.relative_to(ROOT/'public')),'sha256':digest(path),'bytes':path.stat().st_size,'source_sha256':job['source_sha256'],'duration':duration,'dimensions':[video['width'],video['height']],'provenance':provenance,'visual_qa':qa}
    write(run/'opening-media.json',receipt);return receipt
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('run',type=Path);parser.add_argument('--import-file',type=Path);parser.add_argument('--provenance');parser.add_argument('--qa',type=Path);args=parser.parse_args()
    print(json.dumps(accept(args.run,args.import_file,args.provenance,args.qa) if args.import_file else prepare(args.run),indent=2))
