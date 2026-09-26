#!/usr/bin/env python3
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
cap=json.loads((r/"content/AOC-001/distribution/execution-gateway-capability-v0.1.json").read_text())
state=json.loads((r/"content/AOC-001/distribution/live-test-state-v0.1.json").read_text())
assert cap["status"]=="NOT_CONFIGURED"
assert cap["provider"]=="UNBOUND"
assert cap["capability_available"] is False
assert cap["credential_present"] is False
assert cap["sender_identity_verified"] is False
assert cap["repository_secret_storage_allowed"] is False
assert state["execution"]["state"]=="BLOCKED_NOT_EXECUTED"
assert state["external_effect"] is False
print("Execution Gateway PASS: provider-neutral, secrets external, send blocked")
