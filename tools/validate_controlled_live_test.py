#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
auth=json.loads((root/"content/AOC-001/distribution/live-test-authorization-v0.1.json").read_text())
state=json.loads((root/"content/AOC-001/distribution/live-test-state-v0.1.json").read_text())
gates=json.loads((root/"content/AOC-001/distribution/distribution-gates-v0.1.json").read_text())
assert auth["scope"]["max_external_actions"]==1
assert auth["scope"]["adapter_id"]=="ADP-005"
assert len(auth["not_authorized"])>=5
assert state["execution"]["actions_attempted"]==0
assert state["execution"]["state"]=="BLOCKED_NOT_EXECUTED"
assert state["external_effect"] is False
assert state["receipt"]["state"]=="NOT_CREATED_NO_ATTEMPT"
assert state["performance"]["state"]=="WAITING_FOR_RECEIPT"
assert state["learning"]["state"]=="WAITING_FOR_PERFORMANCE"
assert state["routing_update"]["state"]=="NOT_ELIGIBLE"
assert any(x["adapter_id"]=="ADP-005" and x["risk_permission_gate"]["outcome"]=="HOLD" for x in gates["items"])
print("Controlled live-test harness PASS: authorized=1 executed=0 external_effect=False")
