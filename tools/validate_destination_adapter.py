#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
fm=json.loads((root/"content/AOC-001/distribution/format-workers-v0.1.json").read_text())
reg=json.loads((root/"content/AOC-001/distribution/destination-adapter-v0.1.json").read_text())
formats={x["format_id"]:x for x in fm["formats"]}
assert reg["adapter_count"]==len(formats)==len(reg["adapters"])
assert {a["format_id"] for a in reg["adapters"]}==set(formats)
for a in reg["adapters"]:
    f=formats[a["format_id"]]
    assert a["destination_id"] in {"DST-001","DST-004","DST-007"}
    assert a["status"]=="INTERNAL_ONLY"
    assert a["verified_mechanics"] and a["adapted_package"] and a["human_gate"]
assert {"destination contact","submission","scheduling","publication"} <= set(reg["blocked_scope"])
print("Destination Adapter proof PASS", {"adapters":len(reg["adapters"])})
