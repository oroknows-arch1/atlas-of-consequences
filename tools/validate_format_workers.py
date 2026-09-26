#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
variants=json.loads((root/"content/AOC-001/distribution/variant-factory-v0.1.json").read_text())
reg=json.loads((root/"content/AOC-001/distribution/format-workers-v0.1.json").read_text())
v={x["variant_id"]:x for x in variants["variants"]}
assert reg["format_count"]==len(v)==len(reg["formats"])
assert {f["variant_id"] for f in reg["formats"]}==set(v)
for f in reg["formats"]:
    assert f["route_id"]==v[f["variant_id"]]["route_id"]
    assert f["status"]=="SPEC_ONLY" and f["external_action_allowed"] is False
    assert f["production_brief"] and f["required_labels"]
assert {"translation release","destination contact","outreach","submission","scheduling","publication"} <= set(reg["blocked_scope"])
print("Format Workers proof PASS", {"formats":len(reg["formats"])})
