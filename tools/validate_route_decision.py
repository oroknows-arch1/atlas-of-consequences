#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
pri=json.loads((root/"content/AOC-001/distribution/signal-priority-v0.1.json").read_text())
rel=json.loads((root/"content/AOC-001/distribution/relevance-routing-v0.1.json").read_text())
dst=json.loads((root/"content/AOC-001/distribution/destination-discovery-v0.1.json").read_text())
reg=json.loads((root/"content/AOC-001/distribution/route-decision-v0.1.json").read_text())
advance={d["signal_id"] for d in pri["decisions"] if d["outcome"]=="ADVANCE"}
route_pairs={(r["signal_id"],r["audience"]) for r in rel["routes"] if r["route_status"]=="ROUTE"}
dest={d["destination_id"]:d for d in dst["destinations"]}
for d in reg["decisions"]:
    assert d["signal_id"] in advance
    assert (d["signal_id"],d["audience"]) in route_pairs
    assert d["destination_id"] in dest
    assert d["signal_id"] in dest[d["destination_id"]]["matched_signal_ids"]
    assert d["audience"] in dest[d["destination_id"]]["matched_audiences"]
    assert d["outcome"] in {"PURSUE","HOLD","REJECT"}
    if d["outcome"]=="PURSUE" and any(x in d["permission_state"].lower() for x in ("approval required","outreach","submission")):
        assert d["human_gate"] is True
counts={k:sum(d["outcome"]==k for d in reg["decisions"]) for k in ("PURSUE","HOLD","REJECT")}
assert counts==reg["counts"]
assert {"variant generation","outreach","submission","publication"} <= set(reg["blocked_scope"])
print("Route Decision proof PASS", counts)
