#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
priority=json.loads((root/"content/AOC-001/distribution/signal-priority-v0.1.json").read_text())
routing=json.loads((root/"content/AOC-001/distribution/relevance-routing-v0.1.json").read_text())
advance={d["signal_id"] for d in priority["decisions"] if d["outcome"]=="ADVANCE"}
routed={r["signal_id"] for r in routing["routes"]}
assert len(advance)==8
assert routed <= advance, "non-ADVANCE signal reached relevance routing"
assert routed == advance, "an ADVANCE signal has no relevance route"
assert all(r["route_status"] in {"ROUTE","HOLD","REJECT"} for r in routing["routes"])
assert all(r["audience"] and r["relevance_reason"] and r["relevance_basis"] for r in routing["routes"])
banned=("instagram","reddit","tiktok","linkedin","youtube","facebook","x.com","twitter")
for r in routing["routes"]:
    blob=json.dumps(r).lower()
    assert not any(x in blob for x in banned), "platform selection leaked into relevance stage"
print("Relevance Routing proof PASS", {"advance_signals":len(advance),"routes":len(routing["routes"])})
