#!/usr/bin/env python3
"""Deterministic execution shell for Atlasoquence Automated Edition Test #1.

This does not impersonate model/research workers. It consumes their explicit JSON
outputs, verifies dependency order, assembles the generated-edition manifest,
runs invariant validation, and emits a review receipt. Publication is never
authorized here.
"""
import argparse, json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GRAPH=ROOT/"atlas/graphs/automated-edition-generation.json"
VALIDATOR=ROOT/"tools/validate_generated_edition.py"
MODEL_MODES={"MODEL_RESEARCH","MODEL_CREATE","BOUNDED_VERIFY","BOUNDED_DECISION"}
PRE_ASSEMBLY=[
 "world_change_intake","evidence_graph","evidence_gate","geography_resolution",
 "perspective_candidates","perspective_gate","route_scene_generation",
 "causal_boundary_gate","visual_requirements","image_provider_routing"
]

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def dump(p,obj):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("run_dir",help="directory containing stage JSON outputs")
    args=ap.parse_args()
    run=Path(args.run_dir)
    graph=load(GRAPH)
    nodes={n["id"]:n for n in graph["nodes"]}
    errors=[]; stages={}
    for node_id in PRE_ASSEMBLY:
        node=nodes[node_id]
        path=run/f"{node_id}.json"
        if not path.exists():
            errors.append(f"missing explicit stage output: {path.name}")
            continue
        data=load(path); stages[node_id]=data
        if data.get("stage")!=node_id: errors.append(f"{path.name}: stage must be {node_id}")
        if data.get("status")!="PASS": errors.append(f"{path.name}: status must be PASS")
        for dep in node.get("requires",[]):
            if dep in PRE_ASSEMBLY and dep not in stages:
                errors.append(f"{node_id}: dependency {dep} not loaded/passed")
        if node.get("mode") in MODEL_MODES and not data.get("produced_by"):
            errors.append(f"{path.name}: produced_by required; runner will not fabricate model/research work")
    if errors:
        print("AUTOMATED EDITION RUNNER: BLOCKED")
        for e in errors: print(f"- {e}")
        return 1

    world=stages["world_change_intake"]["output"]
    evidence=stages["evidence_graph"]["output"]
    geography=stages["geography_resolution"]["output"]
    perspectives=stages["perspective_gate"]["output"]["perspectives"]
    routes=stages["causal_boundary_gate"]["output"]["routes"]
    visuals=stages["image_provider_routing"]["output"]["visuals"]

    route_by_id={x["perspective_id"]:x["scenes"] for x in routes}
    visual_by_scene={x["scene_id"]:x for x in visuals}
    assembled=[]
    for p in perspectives:
        q=dict(p)
        q["route"]=[]
        for s in route_by_id.get(p["id"],[]):
            scene=dict(s)
            v=visual_by_scene.get(scene["scene_id"],{
                "required":False,"purpose":"No visual required",
                "truth_boundary":"No visual claim","provider_decision":"NONE","asset_path":None
            })
            scene["visual"]=v
            q["route"].append(scene)
        assembled.append(q)

    manifest={
      "schema_version":"1.0",
      "edition_id":world["candidate_id"],
      "world_change":{"statement":world["statement"],"evidence_refs":world["evidence_refs"]},
      "evidence_graph":str((run/"evidence_graph.json").as_posix()),
      "geography":geography["geography"],
      "perspectives":assembled,
      "reader":{"reader_selects_perspective":True,"routes_do_not_auto_chain":True,"universal_baseline":True},
      "visual_fulfilment":{"provider_availability_cannot_change_editorial_structure":True,"video_generation_mandatory":False},
      "publication":{"state":"DRAFT","human_approval_required":True}
    }
    manifest_path=run/"generated-edition.json"; dump(manifest_path,manifest)
    proc=subprocess.run([sys.executable,str(VALIDATOR),str(manifest_path)],capture_output=True,text=True)
    receipt={
      "run_id":run.name,
      "graph_id":graph["graph_id"],
      "manifest":str(manifest_path.as_posix()),
      "invariant_validation":"PASS" if proc.returncode==0 else "FAIL",
      "validator_output":proc.stdout.strip(),
      "publication_authorized":False,
      "next_stage":"asset_generation" if proc.returncode==0 else "HALT",
      "note":"Model/research stages were supplied explicitly; deterministic runner assembled and validated them."
    }
    dump(run/"run-receipt.json",receipt)
    print(proc.stdout.strip())
    print(f"RUN RECEIPT: {run/'run-receipt.json'}")
    return proc.returncode

if __name__=="__main__": raise SystemExit(main())
