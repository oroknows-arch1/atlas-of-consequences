#!/usr/bin/env python3
"""Offline Atlas writers' room contract gate. No API calls or creative-score automation."""
import argparse
import json
from pathlib import Path

SCENE_KEYS = {"id", "pov", "movement", "goal", "resistance", "choice", "cost",
              "reveal_to", "fiction_label", "evidence_boundary", "context_refs"}
CHARACTER_KEYS = {"id", "desire", "contradiction", "relationship", "flaw", "agency"}
MOVEMENTS = {"BEFORE", "DURING", "AFTER"}
STATES = {"PASS", "REVISE", "BLOCKED"}

def validate_room(room):
    errors, warnings = [], []
    if room.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if room.get("release_kind") not in ("DEMONSTRATION", "VERIFIED_EDITION"):
        errors.append("release_kind must be DEMONSTRATION or VERIFIED_EDITION")
    evidence = room.get("evidence", {})
    if evidence.get("incident_state") not in ("SUPPLIED_UNVERIFIED", "VERIFIED"):
        errors.append("incident_state is invalid")
    if room.get("release_kind") == "VERIFIED_EDITION" and evidence.get("incident_state") != "VERIFIED":
        errors.append("verified edition cannot rely on an unverified incident account")
    if not evidence.get("source_id"):
        errors.append("incident evidence needs a source_id")
    if not room.get("world_scope", {}).get("geographic_resolution"):
        errors.append("geographic_resolution is required")
    local = room.get("world_scope", {}).get("locality_specificity", "UNKNOWN")
    if local not in ("REGION_ONLY", "PLACE_VERIFIED"):
        errors.append("locality_specificity must be REGION_ONLY or PLACE_VERIFIED")
    claims = {c.get("id"): c for c in room.get("context_claims", [])}
    if not claims:
        errors.append("context_claims required")
    for claim in room.get("context_claims", []):
        if not claim.get("id") or not claim.get("source_url") or not claim.get("scope"):
            errors.append("context claim must have id/source_url/scope")
        if claim.get("state") not in ("GENERAL_CONTEXT", "PLACE_VERIFIED"):
            errors.append("context claim has invalid state")
        if local == "REGION_ONLY" and claim.get("state") == "PLACE_VERIFIED":
            warnings.append("check place-specific context against unresolved community")
    chars = room.get("characters", [])
    ids = [c.get("id") for c in chars]
    if len(chars) < 2 or len(set(ids)) != len(ids):
        errors.append("characters need at least two distinct ids")
    for c in chars:
        for key in CHARACTER_KEYS:
            if not c.get(key):
                errors.append("character %s missing %s" % (c.get("id"), key))
    scenes = room.get("scenes", [])
    scene_ids = [s.get("id") for s in scenes]
    if len(scenes) < 3 or len(set(scene_ids)) != len(scene_ids):
        errors.append("scenes need at least three unique ids")
    used_povs = set()
    for scene in scenes:
        sid = scene.get("id", "<unknown>")
        for key in SCENE_KEYS:
            if key not in scene or (not scene[key] and key != "reveal_to"):
                errors.append("scene %s missing %s" % (sid, key))
        if scene.get("pov") not in ids:
            errors.append("scene %s references unknown character" % sid)
        else:
            used_povs.add(scene["pov"])
        if scene.get("movement") not in MOVEMENTS:
            errors.append("scene %s has invalid movement" % sid)
        if scene.get("fiction_label") != "STORY / FICTION":
            errors.append("scene %s missing prominent fiction label" % sid)
        if scene.get("evidence_boundary") != "FICTION_NOT_TESTIMONY":
            errors.append("scene %s mixes fiction and incident testimony" % sid)
        for ref in scene.get("context_refs", []):
            if ref not in claims:
                errors.append("scene %s has unknown context ref %s" % (sid, ref))
        for other in scene.get("reveal_to", []):
            if other not in ids or other == scene.get("pov"):
                errors.append("scene %s has invalid cross-perspective reveal" % sid)
        for forbidden in scene.get("prohibited_claims", []):
            if forbidden in ("ACTUAL_CAUSE_ESTABLISHED", "REAL_INJURY_ASSERTED", "REAL_COMPANY_FAULT"):
                errors.append("scene %s asserts unsupported real-world claim" % sid)
    if set(ids) != used_povs:
        errors.append("not every character has a perspective scene")
    if not any(s.get("reveal_to") for s in scenes):
        errors.append("no scenes reveal information across perspectives")
    gates = room.get("review", {})
    if gates.get("writer_is_sole_approver"):
        errors.append("writer cannot self-approve")
    for name in ("dramatic_editor", "locality", "continuity", "originality", "evidence_boundary"):
        status = gates.get(name)
        if status not in STATES:
            errors.append("review gate %s missing/invalid" % name)
    if room.get("release_kind") == "DEMONSTRATION":
        if evidence.get("incident_state") == "SUPPLIED_UNVERIFIED" and not room.get("visible_demo_disclosure"):
            errors.append("unverified demonstration must disclose incident limits")
    if local == "REGION_ONLY" and not room.get("world_scope", {}).get("no_unverified_local_identities"):
        errors.append("region-only setting cannot imply specific unverified identities")
    return errors, warnings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    room = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors, warnings = validate_room(room)
    statuses = room.get("review", {})
    ready = not errors and all(statuses.get(k) == "PASS" for k in (
        "dramatic_editor", "locality", "continuity", "originality", "evidence_boundary"))
    report = {"structure_valid": not errors, "editorially_ready": ready, "errors": errors,
              "warnings": warnings, "remaining_gates": [k for k,v in statuses.items()
                if k != "writer_is_sole_approver" and v != "PASS"]}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("STRUCTURE PASS" if not errors else "STRUCTURE FAIL")
        print("EDITORIAL PASS" if ready else "EDITORIAL NOT READY")
        for error in errors: print("ERROR:", error)
        for warning in warnings: print("WARNING:", warning)
        if report["remaining_gates"]: print("REMAINING:", ", ".join(report["remaining_gates"]))
    raise SystemExit(0 if not errors else 1)

if __name__ == "__main__":
    main()
