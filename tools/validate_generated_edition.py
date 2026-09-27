#!/usr/bin/env python3
import json, sys
from pathlib import Path

ALLOWED={"KNOWN","UNCERTAIN","CONTESTED","UNKNOWN","UNAVAILABLE","FICTION_EDITORIAL"}
PROVIDERS={"CHATGPT_IMAGES","RUNWAY","SPECIALIST","DETERMINISTIC","SOURCED_MEDIA","NONE","PENDING"}

def fail(msgs):
    print("AUTOMATED EDITION INVARIANTS: FAIL")
    for m in msgs: print(f"- {m}")
    return 1

def main(path):
    p=Path(path); data=json.loads(p.read_text(encoding="utf-8")); errors=[]
    if data.get("schema_version")!="1.0": errors.append("schema_version must be 1.0")
    if not data.get("world_change",{}).get("evidence_refs"): errors.append("world change requires evidence refs")
    perspectives=data.get("perspectives",[])
    accepted=[x for x in perspectives if x.get("status")=="ACCEPTED"]
    if not accepted: errors.append("at least one evidence-backed Perspective must be accepted")
    names=[x.get("name") for x in accepted]
    if len(names)!=len(set(names)): errors.append("accepted Perspective names must be unique")
    for psp in accepted:
        if not psp.get("evidence_nodes"): errors.append(f"{psp.get('id')}: accepted Perspective has no evidence nodes")
        route=psp.get("route",[])
        if not route: errors.append(f"{psp.get('id')}: accepted Perspective has no route")
        for scene in route:
            sid=scene.get("scene_id","<scene>")
            state=scene.get("state")
            if state not in ALLOWED: errors.append(f"{sid}: invalid evidence/editorial state")
            refs=scene.get("evidence_refs",[])
            if state in {"KNOWN","UNCERTAIN","CONTESTED"} and not refs:
                errors.append(f"{sid}: factual/analytical scene requires evidence refs")
            if state=="FICTION_EDITORIAL" and refs:
                errors.append(f"{sid}: fiction/editorial scene must not present evidence refs as proof of invented events")
            visual=scene.get("visual",{})
            if visual.get("required") and not visual.get("truth_boundary"):
                errors.append(f"{sid}: required visual lacks truth boundary")
            if visual.get("provider_decision") not in PROVIDERS:
                errors.append(f"{sid}: invalid provider decision")
            if state in {"UNKNOWN","UNAVAILABLE"} and not scene.get("knowledge_stop"):
                errors.append(f"{sid}: UNKNOWN/UNAVAILABLE must be an explicit knowledge stop")
    reader=data.get("reader",{})
    if reader.get("reader_selects_perspective") is not True: errors.append("reader must choose the active Perspective")
    if reader.get("routes_do_not_auto_chain") is not True: errors.append("completed Perspective must not auto-chain into another")
    if reader.get("universal_baseline") is not True: errors.append("universal readable/navigable baseline required")
    visual_policy=data.get("visual_fulfilment",{})
    if visual_policy.get("provider_availability_cannot_change_editorial_structure") is not True:
        errors.append("provider availability/credit exhaustion must not change evidence, Perspective structure, scene meaning, or factual boundary")
    if visual_policy.get("video_generation_mandatory") is not False:
        errors.append("video generation must remain optional")
    pub=data.get("publication",{})
    if pub.get("human_approval_required") is not True: errors.append("human publication authority must be preserved")
    if pub.get("state")=="APPROVED": errors.append("automated test validator does not authorize publication")
    return fail(errors) if errors else (print(f"AUTOMATED EDITION INVARIANTS: PASS - {len(accepted)} accepted Perspectives") or 0)

if __name__=="__main__":
    if len(sys.argv)!=2:
        print("usage: validate_generated_edition.py <manifest.json>"); raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
