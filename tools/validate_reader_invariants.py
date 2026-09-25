#!/usr/bin/env python3
"""Fail CI if the human-approved AOC-001 opening-to-reader handoff regresses."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "atlas/contracts/aoc001-reader-invariants.json"
INDEX = ROOT / "public/index.html"
CSS = ROOT / "public/reader-publication-treatments.css"
JS = ROOT / "public/reader-publication-treatments.js"

errors = []

for path in (CONTRACT, INDEX, CSS, JS):
    if not path.exists():
        errors.append(f"missing required reader invariant file: {path.relative_to(ROOT)}")

if errors:
    print("AOC-001 READER INVARIANTS: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
index = INDEX.read_text(encoding="utf-8")
css = CSS.read_text(encoding="utf-8")
js = JS.read_text(encoding="utf-8")

if contract.get("status") != "human_approved":
    errors.append("reader invariant contract is not marked human_approved")

required_index = {
    "opening factual film element": '<video id="factFilm"',
    "approved factual film asset": 'assets/aoc001-report-video-candidate-v0.4.mp4',
    "final-frame hold function": 'function holdFinalFrame()',
    "film pauses on held frame": 'fact.pause();targetTime=hold;visualTime=hold;',
    "film end enters reader": "fact.addEventListener('ended',enterReader);",
    "scroll scrub writes video currentTime": 'fact.currentTime=t',
    "Edition Map starts at final-frame progress": '<section id="intro" data-p="1">',
    "approved reader opacity": 'opacity:.82',
    "approved reader brightness": 'filter:brightness(.67) saturate(.9)'
}
for label, needle in required_index.items():
    if needle not in index:
        errors.append(f"missing invariant: {label}")

# Validate the reader-entry behaviour rather than one exact implementation string.
# Audio handling may evolve, but the final-frame hold must remain the first visual handoff.
enter_reader = re.search(r"function enterReader\(\)\{(?P<body>.*?)\n\}", index, re.S)
if not enter_reader:
    errors.append("missing invariant: enterReader function")
else:
    body = enter_reader.group("body")
    if "holdFinalFrame();" not in body:
        errors.append("missing invariant: reader entry invokes final-frame hold")
    hold_pos = body.find("holdFinalFrame();")
    reader_mode_pos = body.find("world.classList.add('reader-mode')")
    if reader_mode_pos != -1 and hold_pos > reader_mode_pos:
        errors.append("reader invariant order broken: final-frame hold must precede reader-mode transition")

required_css = {
    "video remains visible in reduced motion": '#factFilm{display:block!important}',
    "reduced-motion reader background does not substitute poster": '#world,#world.reader-mode{background:#000!important}'
}
for label, needle in required_css.items():
    if needle not in css:
        errors.append(f"missing invariant: {label}")

forbidden_css = {
    "reduced-motion must not hide reader video": 'body.reader-active #factFilm{display:none',
    "reader must not replace video with static poster": "#world.reader-mode{background:#000 url('assets/aoc001-report-video-candidate-v0.4-review.jpg')"
}
for label, needle in forbidden_css.items():
    if needle in css:
        errors.append(label)

required_js = {
    "reduced motion still attempts opening film": 'const playAttempt = video.play();',
    "top of reader holds final frame": 'if (y <= points[0].top + 1) return points[0].p;'
}
for label, needle in required_js.items():
    if needle not in js:
        errors.append(f"missing invariant: {label}")

forbidden_js = {
    "reduced motion must not auto-enter reader": "if (typeof enterReader === 'function') enterReader();",
    "reduced motion must not pause opening film": 'video.pause();'
}
for label, needle in forbidden_js.items():
    if needle in js:
        errors.append(label)

if 'aoc001-story-promo' in index.lower():
    errors.append("story promo must not be auto-wired into the factual reader opening")

if errors:
    print("AOC-001 READER INVARIANTS: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("AOC-001 READER INVARIANTS: PASS")
for item in contract.get("approved_sequence", []):
    print(f"- {item}")
