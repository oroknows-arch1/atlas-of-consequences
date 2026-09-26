#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
routes=json.loads((root/"content/AOC-001/distribution/route-decision-v0.1.json").read_text())
signals=json.loads((root/"content/AOC-001/distribution/signal-library-v0.1.json").read_text())
reg=json.loads((root/"content/AOC-001/distribution/variant-factory-v0.1.json").read_text())
pursue={d["route_id"]:d for d in routes["decisions"] if d["outcome"]=="PURSUE"}
sig={s["signal_id"]:s for s in signals["signals"]}
assert len(reg["variants"])==len(pursue)
assert {v["route_id"] for v in reg["variants"]}==set(pursue)
for v in reg["variants"]:
    r=pursue[v["route_id"]]
    assert (v["signal_id"],v["destination_id"],v["audience"])==(r["signal_id"],r["destination_id"],r["audience"])
    assert v["classification"]==sig[v["signal_id"]]["classification"]
    assert set(v["evidence_refs"]) <= set(sig[v["signal_id"]]["evidence_refs"])
    assert v["status"]=="INTERNAL_CANDIDATE" and v["external_action_allowed"] is False
    assert v["candidate_expression"] and v["boundary_notes"]
assert {"destination contact","outreach","submission","scheduling","publication"} <= set(reg["blocked_scope"])
print("Variant Factory proof PASS", {"variants":len(reg["variants"])})
