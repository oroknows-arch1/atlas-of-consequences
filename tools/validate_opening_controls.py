#!/usr/bin/env python3
"""Fail CI if AOC-001 opening controls regress into lower-third text."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "atlas/contracts/aoc001-reader-invariants.json"
CSS = ROOT / "public/reader-publication-treatments.css"
INDEX = ROOT / "public/index.html"

errors = []
for path in (CONTRACT, CSS, INDEX):
    if not path.exists():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")

if errors:
    print("AOC-001 OPENING CONTROLS: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
css = CSS.read_text(encoding="utf-8")
index = INDEX.read_text(encoding="utf-8")
runtime = contract.get("immutable_runtime_requirements", {})

if runtime.get("opening_controls_must_remain_mid_screen") is not True:
    errors.append("mid-screen opening-controls invariant is not enabled")
if runtime.get("opening_controls_vertical_position") != "50%":
    errors.append("approved opening-controls vertical position must remain 50%")
if runtime.get("opening_controls_must_not_cover_lower_third_text") is not True:
    errors.append("lower-third text clearance invariant is not enabled")

required_css = [
    "#openingControls{top:50%!important;bottom:auto!important;transform:translateY(-50%)!important}",
]
for needle in required_css:
    if needle not in css:
        errors.append("opening controls are no longer fixed at the approved vertical midpoint")

if '<div id="openingControls">' not in index:
    errors.append("opening controls container is missing")
if 'id="soundBtn"' not in index:
    errors.append("Tap for sound control is missing")
if 'id="skipBtn"' not in index:
    errors.append("Skip control is missing")

if errors:
    print("AOC-001 OPENING CONTROLS: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("AOC-001 OPENING CONTROLS: PASS")
print("- Tap for sound and Skip remain at the vertical midpoint")
print("- lower-third factual text remains unobstructed by opening controls")
