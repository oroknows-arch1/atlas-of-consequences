#!/usr/bin/env python3
"""Fail-closed publication production from gated editorial receipts.

An image provider is an executable command taking a JSON job on stdin and
returning JSON {"path": "/absolute/binary/path", "provider": "...", "provenance": "..."}.
It must itself generate/obtain the image; a prompt or temporary URL is not a result.
An independent visual verifier takes the same job plus `asset_path` on stdin
and returns {"pass": true, "reason": "..."}. Neither command may self-approve.
"""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from PIL import Image, ImageStat
from production_state import binding, block, digest, reader_hashes, require_current
from editorial_factory import produce as produce_copy
from reader_builder import build_reader
from provider_errors import requires_external_action
from provider_routing import request_asset

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_GATES = ("selected-edition-gate", "story_plausibility_gate")

def read(path): return json.loads(path.read_text(encoding="utf8"))
def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n", encoding="utf8")
def escape(s): return html.escape(str(s), quote=True)
def invoke(command, payload):
    result = subprocess.run(command, input=json.dumps(payload), text=True,
                            shell=True, capture_output=True, timeout=180)
    if result.returncode: raise RuntimeError(result.stderr.strip() or "provider exited unsuccessfully")
    return json.loads(result.stdout)

def facts(run, candidate):
    for name in REQUIRED_GATES:
        receipt=read(run/(name+".json"))
        if receipt.get("status")!="PASS": raise RuntimeError(f"{name} did not pass")
        identity=receipt.get("output",{}).get("candidate_id")
        if identity!=candidate: raise RuntimeError(f"{name} lacks verified identity for {candidate}")
    selection=read(run/'selected-edition-gate.json')['output']
    for gate in ('informational_completeness_gate', 'human_emotional_hook_gate',
                 'geographic_grounding_gate', 'causal_boundary_precheck', 'visual_context_viability'):
        if selection.get(gate)!='PASS': raise RuntimeError(f'{gate} did not pass')
    source_list=read(run/'source-register.json')
    source_ids={s['id'] for s in source_list}
    if len(source_ids)!=len(source_list): raise RuntimeError('duplicate source IDs')
    for source in source_list:
        if not all(source.get(k) for k in ('id','title','url','supports','limitation')) or not source['url'].startswith('https://'):
            raise RuntimeError('source register incomplete')
    selected=read(run/'selected-edition-candidate.json')
    if selected.get('human_emotional_hook',{}).get('state')!='PASS': raise RuntimeError('human consequence missing')
    if {s['id'] for s in selected['evidence_basis']}-source_ids: raise RuntimeError('accepted evidence lacks sources')
    names=("route_scene_generation", "causal_boundary_gate", "visual_requirements",
           "image_provider_routing", "story_synthesis", "story_plausibility_gate")
    receipts={n:read(run/(n+".json")) for n in names}
    for n,r in receipts.items():
        if r.get("status")!="PASS" or r.get("output",{}).get("candidate_id")!=candidate:
            raise RuntimeError(f"{n} missing PASS receipt for {candidate}")
    original=receipts["route_scene_generation"]["output"]["routes"]
    bounded=receipts["causal_boundary_gate"]["output"]["routes"]
    accepted_receipt=read(run/"selected-edition-perspectives.json")
    if accepted_receipt.get("status")!="PASS" or accepted_receipt.get("output",{}).get("candidate_id")!=candidate:
        raise RuntimeError("accepted Perspectives receipt missing or belongs to another candidate")
    accepted={p["id"] for p in accepted_receipt["output"]["perspectives"] if p["status"]=="ACCEPTED"}
    if {r["perspective_id"] for r in bounded}!=accepted:
        raise RuntimeError("reader routes do not match evidence-derived accepted Perspectives")
    if [(r["perspective_id"], [s["scene_id"] for s in r["scenes"]]) for r in original] != [(r["perspective_id"], [s["scene_id"] for s in r["scenes"]]) for r in bounded]:
        raise RuntimeError("bounded route topology differs from accepted route topology")
    requirements=receipts["visual_requirements"]["output"]["requirements"]
    scene_ids=[s['scene_id'] for r in bounded for s in r['scenes']]
    if len(scene_ids)!=len(set(scene_ids)): raise RuntimeError('duplicate scene IDs')
    for route in bounded:
        for scene in route['scenes']:
            if not scene.get('evidence_refs') or set(scene['evidence_refs'])-source_ids:
                raise RuntimeError('scene references unregistered evidence')
    if {v['scene_id'] for v in requirements}!=set(scene_ids) or len(requirements)!=len(scene_ids):
        raise RuntimeError('visual requirements must cover every scene exactly once')
    routed=receipts["image_provider_routing"]["output"]["visuals"]
    if {v["scene_id"] for v in routed}!={v["scene_id"] for v in requirements}:
        raise RuntimeError("visual routing and requirements refer to different scenes")
    for v in requirements:
        if v["required"] != next(x for x in routed if x["scene_id"]==v["scene_id"])["required"]:
            raise RuntimeError(f"{v['scene_id']}: requirement changed during routing")
    return bounded, requirements, receipts["story_synthesis"]["output"]

def validate_binary(path, contextual):
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        if min(image.size)<600: raise RuntimeError("image resolution below 600px")
        if contextual:
            gray=image.convert("L").resize((100,100))
            brightness=ImageStat.Stat(gray).mean[0]
            if brightness<48: raise RuntimeError(f"image too dark ({brightness:.1f})")

def make_graphic(path, scene, requirement, source_ids, datum):
    # Source-labelled explanatory image with explicit scope; no invented map data.
    import textwrap
    if not datum or not datum.get("value") or not datum.get("scope") or not datum.get("source_id") in source_ids:
        raise RuntimeError("deterministic graphic lacks verified value, scope or scene source")
    title=datum["caption"]
    lines=textwrap.wrap(title, width=38)
    body="".join(f'<text x="90" y="{440+i*58}" font-size="42" fill="#f3eadb">{escape(line)}</text>' for i,line in enumerate(lines))
    caption=escape("Scope: "+datum["scope"]+" · Source: "+datum["source_id"])
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900"><rect width="1600" height="900" fill="#15252a"/><path d="M80 225 H1520" stroke="#d5874a" stroke-width="5"/><text x="90" y="115" font-family="sans-serif" font-size="27" letter-spacing="5" fill="#ecb98c">ATLASOQUENCE · EXPLANATORY</text><text x="90" y="350" font-family="Georgia,serif" font-size="118" fill="#f3eadb">{escape(datum['value'])}</text><g font-family="Georgia,serif">{body}</g><text x="90" y="820" font-family="sans-serif" font-size="25" fill="#e2dccf">{caption}</text></svg>'''
    # SVG is a persistent image binary, but it must carry actual explanation, not a gradient substitute.
    path.write_bytes(svg.encode("utf8"))

def produce_assets(run, edition, routes, requirements, output):
    generator=os.environ.get("ATLAS_IMAGE_COMMAND")
    verifier=os.environ.get("ATLAS_VISUAL_QA_COMMAND")
    asset_dir=ROOT/"public"/"assets"/edition.lower()
    asset_dir.mkdir(parents=True,exist_ok=True)
    scenes={s["scene_id"]:s for r in routes for s in r["scenes"]}
    context_file=run/"visual-context.json"
    if not context_file.exists():
        return [],[{"worker":"visual_factory","reason":"geographic/cultural visual context receipt missing"}]
    context=read(context_file)
    graphic_data=read(run/"visual-data.json") if (run/"visual-data.json").exists() else {}
    if context.get("candidate_id")!=edition or not context.get("locality_evidence"):
        return [],[{"worker":"visual_factory","reason":"visual context is not evidenced for this edition"}]
    assets=[]; defects=[]
    old_path=run/"asset-persistence-receipt.json"
    previous={}
    if old_path.exists():
        old=read(old_path)
        try:
            require_current(run,old)
            previous={a["scene_id"]:a for a in old.get("assets",[])}
        except ValueError: pass
    for spec in requirements:
        if not spec["required"]: continue
        sid=spec["scene_id"]
        scene=scenes[sid]
        contextual="deterministic" not in spec["visual_type"].lower()
        dest=asset_dir/(sid.lower()+(".png" if contextual else ".svg"))
        job={"edition_id":edition,"scene_id":sid,"meaning":scene["meaning"],
             "evidence_refs":scene["evidence_refs"],"truth_boundary":spec["truth_boundary"],
             "geography":output["geographic_core"],
             "visual_type":spec["visual_type"],"purpose":spec["purpose"],
             "fiction_status":spec.get("fiction_status", "FACT_CONTEXTUAL"), "continuity":context.get("visual_bible",{}),
             "locality_evidence":context["locality_evidence"],
             "style":"grounded editorial documentary, natural daylight, coherent warm-neutral grade; no text, identifiable signage or claimed event"}
        job_hash=hashlib.sha256(json.dumps(job,sort_keys=True).encode()).hexdigest()
        old=previous.get(sid,{})
        if (dest.is_file() and old.get("sha256")==digest(dest)
                and old.get("job_sha256")==job_hash and old.get("visual_qa",{}).get("pass") is True):
            assets.append(old)
            continue
        try:
            if contextual:
                if not generator or not verifier: raise RuntimeError("image generator and independent visual verifier commands are required")
                feedback=""
                for attempt in range(1,4):
                    try:
                        result=request_asset(run,dict(job,attempt=attempt,repair_feedback=feedback),generator,invoke)
                        source=Path(result["path"])
                        if not source.is_file(): raise RuntimeError("provider returned no binary")
                        with Image.open(source) as im:
                            if im.format!="PNG": raise RuntimeError("image provider must return PNG")
                        validate_binary(source,True)
                        check=invoke(verifier,dict(job,asset_path=str(source),provider=result.get("provider")))
                        if check.get("pass") is not True: raise RuntimeError("visual/evidence QA: "+check.get("reason","failed"))
                        shutil.copyfile(source,dest)
                        break
                    except Exception as error:
                        feedback=str(error)
                        if requires_external_action(error) or attempt==3: raise
            else:
                make_graphic(dest,scene,spec,scene["evidence_refs"],graphic_data.get(sid))
                check={"pass":True,"reason":"Verified deterministic value, scope and scene source; rendered review still mandatory"}
                result={"provider":"ATLAS_DETERMINISTIC_GRAPHIC","provenance":"scene meaning and evidence refs"}
            binary=dest.read_bytes()
            if not binary: raise RuntimeError("empty binary")
            assets.append({"scene_id":sid,"path":"/assets/"+edition.lower()+"/"+dest.name,
                           "sha256":hashlib.sha256(binary).hexdigest(),"bytes":len(binary),
                           "provenance":result.get("provenance"),"provider":result.get("provider"),
                           "truth_boundary":spec["truth_boundary"],"status":"PASS",
                           "job_sha256":job_hash,"visual_qa":check,"routing_provenance":result.get("routing_provenance")})
        except Exception as exc:
            defects.append({"worker":"visual_factory" if contextual else "asset_persistence", "scene_id":sid,"reason":str(exc),"external_action_required":requires_external_action(exc)})
    write(run/"asset-persistence-receipt.json",{**binding(run),"status":"PASS" if not defects else "BLOCKED","assets":assets,"defects":defects})
    return assets,defects


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("run_dir",type=Path)
    args=ap.parse_args()
    run=args.run_dir.resolve()
    candidate=read(run/"selected-edition-candidate.json")
    block(run, "production_orchestrator", "Production in progress; previous review verdict invalidated")
    edition=candidate["candidate_id"]
    defects=[]; assets=[]; reader=None
    try:
        routes,requirements,story=facts(run,edition)
        copy=produce_copy(run,routes)
        assets,defects=produce_assets(run,edition,routes,requirements,candidate)
        if not defects: reader=build_reader(run,edition,candidate,routes,story,assets,copy)
    except Exception as exc: defects.append({"worker":"production_orchestrator","reason":str(exc)})
    receipt={**binding(run),"state":"ASSEMBLED" if reader and not defects else "BLOCKED", "assets_persisted":len(assets),
             "reader":str(reader.relative_to(ROOT)) if reader else None,"defects":defects,
             "next_stage":"rendered_qa" if reader else "external_action" if any(d.get("external_action_required") for d in defects) else "repair", "publication_authorized":False, "reader_hashes":reader_hashes(reader) if reader else {}}
    write(run/"production-receipt.json",receipt)
    print(json.dumps(receipt,indent=2))
    return 0 if reader and not defects else 1

if __name__=="__main__": sys.exit(main())
