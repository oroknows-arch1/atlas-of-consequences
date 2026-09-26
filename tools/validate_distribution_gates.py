#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
ad=json.loads((root/"content/AOC-001/distribution/destination-adapter-v0.1.json").read_text())
reg=json.loads((root/"content/AOC-001/distribution/distribution-gates-v0.1.json").read_text())
ids={a["adapter_id"] for a in ad["adapters"]}
assert reg["item_count"]==len(ids)==len(reg["items"])
assert {x["adapter_id"] for x in reg["items"]}==ids
for x in reg["items"]:
    assert x["evidence_gate"]["outcome"] in {"PASS","HOLD","FAIL"}
    assert x["brand_editorial_gate"]["outcome"] in {"PASS","HOLD","FAIL"}
    assert x["risk_permission_gate"]["outcome"] in {"PASS","HOLD","FAIL"}
    assert x["overall"]=="HOLD" and x["external_action_allowed"] is False
    assert not (x["overall"]=="PASS" and any(x[g]["outcome"]!="PASS" for g in ["evidence_gate","brand_editorial_gate","risk_permission_gate"]))
assert reg["summary"]=={"evidence_pass":6,"brand_editorial_pass":6,"risk_permission_hold":6,"execution_eligible":0}
assert {"destination contact","submission","scheduling","publication"} <= set(reg["blocked_scope"])
print("Distribution gates proof PASS", reg["summary"])
