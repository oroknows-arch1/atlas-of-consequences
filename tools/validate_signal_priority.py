#!/usr/bin/env python3
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
lib=json.loads((root/"content/AOC-001/distribution/signal-library-v0.1.json").read_text())
reg=json.loads((root/"content/AOC-001/distribution/signal-priority-v0.1.json").read_text())
signals={s["signal_id"]:s for s in lib["signals"]}
assert len(reg["decisions"])==len(signals)==17
assert set(d["signal_id"] for d in reg["decisions"])==set(signals)
assert set(d["outcome"] for d in reg["decisions"])<= {"ADVANCE","HOLD","STOP"}
for d in reg["decisions"]:
    s=signals[d["signal_id"]]
    assert d["signal_statement"]==s["signal_statement"]
    assert d["classification"]==s["classification"]
    assert d["evidence_refs"]==s["evidence_refs"]
    assert d["source_provenance"]==s["provenance"]
    if s["classification"]=="factual":
        assert s["evidence_refs"], f'{s["signal_id"]}: factual signal lacks evidence'
    if s["classification"]=="fictional":
        assert not s["evidence_refs"], f'{s["signal_id"]}: fiction acquired evidence'
    if d["eligibility"]!="PASS":
        assert d["outcome"]!="ADVANCE"
counts={k:sum(d["outcome"]==k for d in reg["decisions"]) for k in ("ADVANCE","HOLD","STOP")}
assert counts==reg["counts"]
print("Signal Priority proof PASS", counts)
