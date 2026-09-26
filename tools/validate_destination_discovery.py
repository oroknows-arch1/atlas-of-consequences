#!/usr/bin/env python3
import json
from pathlib import Path
from urllib.parse import urlparse
root=Path(__file__).resolve().parents[1]
rel=json.loads((root/"content/AOC-001/distribution/relevance-routing-v0.1.json").read_text())
dst=json.loads((root/"content/AOC-001/distribution/destination-discovery-v0.1.json").read_text())
eligible={r["signal_id"] for r in rel["routes"] if r["route_status"]=="ROUTE"}
assert dst["destinations"], "no destinations"
ids=set()
for d in dst["destinations"]:
    assert d["destination_id"] not in ids
    ids.add(d["destination_id"])
    assert d["state"] in {"CANDIDATE","HOLD","REJECT"}
    assert set(d["matched_signal_ids"]) <= eligible, "destination matched non-routed signal"
    assert d["fit_reason"] and d["discovery_evidence"] and d["access_mode"] and d["permission_risk"]
    u=urlparse(d["url"])
    assert u.scheme=="https" and u.netloc, "destination lacks verifiable HTTPS URL"
    assert any(marker in d["permission_risk"].lower() for marker in ("permission", "approval required", "fit only")) or d["state"]!="CANDIDATE"
blocked=set(dst["blocked_scope"])
assert {"variant generation","publication","outreach"} <= blocked
print("Destination Discovery proof PASS", {"destinations":len(dst["destinations"])})
