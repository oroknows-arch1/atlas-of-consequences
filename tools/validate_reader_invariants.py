#!/usr/bin/env python3
"""Fail CI if the human-approved AOC-001 reader invariants regress."""
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

runtime = contract.get("immutable_runtime_requirements", {})
if runtime.get("opening_soundtrack_must_fade_before_reader_handoff") is not True:
    errors.append("approved audio fade invariant is not enabled in contract")
if runtime.get("opening_soundtrack_fade_seconds") != 2.2:
    errors.append("approved opening soundtrack fade must remain 2.2 seconds")
if runtime.get("opening_soundtrack_must_not_hard_cut_at_reader_handoff") is not True:
    errors.append("approved no-hard-cut audio invariant is not enabled in contract")
if runtime.get("whats_real_causal_flow_must_precede_dense_prose") is not True:
    errors.append("approved WHAT'S REAL causal-flow invariant is not enabled in contract")
if runtime.get("whats_real_causal_boundary_must_remain_visible") is not True:
    errors.append("approved WHAT'S REAL causal boundary invariant is not enabled in contract")
if runtime.get("consequences_three_layer_separation_must_remain_visible") is not True:
    errors.append("approved CONSEQUENCES three-layer separation invariant is not enabled in contract")
if runtime.get("consequences_prohibited_shortcut_must_remain_visible") is not True:
    errors.append("approved CONSEQUENCES prohibited-shortcut invariant is not enabled in contract")

required_index = {
    "opening factual film element": '<video id="factFilm"',
    "approved factual film asset": 'assets/aoc001-report-video-candidate-v0.4.mp4',
    "final-frame hold function": 'function holdFinalFrame()',
    "film pauses on held frame": 'fact.pause();targetTime=hold;visualTime=hold;',
    "film end enters reader": "fact.addEventListener('ended',enterReader);",
    "scroll scrub writes video currentTime": 'fact.currentTime=t',
    "Edition Map starts at final-frame progress": '<section id="intro" data-p="1">',
    "approved reader opacity": 'opacity:.82',
    "approved reader brightness": 'filter:brightness(.67) saturate(.9)',
    "approved opening sound volume": 'const OPENING_SOUND_VOLUME=.08;',
    "approved opening sound fade duration": 'const OPENING_SOUND_FADE_SECONDS=2.2;',
    "opening sound fade function": 'function updateOpeningSoundFade()',
    "opening sound fade tracks film time": "fact.addEventListener('timeupdate',updateOpeningSoundFade);",
    "opening sound fades continuously": 'remaining/OPENING_SOUND_FADE_SECONDS',
    "opening sound reaches silence before pause": 'sound.volume=0;sound.pause();sound.volume=OPENING_SOUND_VOLUME;'
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

# The approved soundtrack must fade during the closing seconds of the factual film.
# A pause at handoff is acceptable only after the volume has reached zero.
fade_fn = re.search(r"function updateOpeningSoundFade\(\)\{(?P<body>.*?)\n\}", index, re.S)
if not fade_fn:
    errors.append("missing invariant: opening soundtrack fade function")
else:
    fade_body = fade_fn.group("body")
    if "remaining" not in fade_body or "sound.volume" not in fade_body:
        errors.append("opening soundtrack fade no longer follows remaining film time")

required_css = {
    "video remains visible in reduced motion": '#factFilm{display:block!important}',
    "reduced-motion reader background does not substitute poster": '#world,#world.reader-mode{background:#000!important}',
    "approved WHAT'S REAL causal-flow container": '.signal-flow{',
    "approved WHAT'S REAL causal-flow nodes": '.flow-node{',
    "approved WHAT'S REAL causal boundary": '.flow-boundary{',
    "approved CONSEQUENCES certainty map": '.certainty-map{',
    "approved CONSEQUENCES certainty cards": '.certainty-card{',
    "approved CONSEQUENCES prohibited shortcut treatment": '.prohibited-boundary{'
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
    "top of reader holds final frame": 'if (y <= points[0].top + 1) return points[0].p;',
    "WHAT'S REAL causal-flow heading": 'THE CONNECTION THIS EDITION IS TESTING',
    "WHAT'S REAL causal boundary": 'this is a documented connection chain, not proof that AI caused a specific Antofagasta mine expansion or a particular job.',
    "CONSEQUENCES documented-global label": '01 · DOCUMENTED GLOBAL',
    "CONSEQUENCES documented-place label": '02 · DOCUMENTED PLACE',
    "CONSEQUENCES fictional-human label": '03 · FICTIONAL HUMAN',
    "CONSEQUENCES prohibited-shortcut label": 'PROHIBITED CAUSAL SHORTCUT'
}
for label, needle in required_js.items():
    if needle not in js:
        errors.append(f"missing invariant: {label}")

# Lock the human-approved WHAT'S REAL causal-flow order.
flow_order = runtime.get("whats_real_causal_flow_order", [])
if not isinstance(flow_order, list) or not flow_order:
    errors.append("approved WHAT'S REAL causal-flow order missing from contract")
else:
    last_pos = -1
    for label in flow_order:
        pos = js.find(f"'{label}'")
        if pos == -1:
            errors.append(f"missing approved WHAT'S REAL causal-flow node: {label}")
            continue
        if pos <= last_pos:
            errors.append(f"approved WHAT'S REAL causal-flow order changed near: {label}")
        last_pos = pos

flow_insert = js.find("if (factStrip) factStrip.insertAdjacentElement('beforebegin', flow);")
if flow_insert == -1:
    errors.append("approved WHAT'S REAL causal flow no longer precedes the dense factual cards/prose treatment")

# Lock the human-approved CONSEQUENCES certainty-layer order and prohibited shortcut.
consequence_order = runtime.get("consequences_three_layer_order", [])
if not isinstance(consequence_order, list) or consequence_order != [
    "01 · DOCUMENTED GLOBAL",
    "02 · DOCUMENTED PLACE",
    "03 · FICTIONAL HUMAN"
]:
    errors.append("approved CONSEQUENCES three-layer order changed in contract")
else:
    last_pos = -1
    for label in consequence_order:
        pos = js.find(label)
        if pos == -1:
            errors.append(f"missing approved CONSEQUENCES layer: {label}")
            continue
        if pos <= last_pos:
            errors.append(f"approved CONSEQUENCES layer order changed near: {label}")
        last_pos = pos

shortcut = runtime.get("consequences_prohibited_shortcut")
if shortcut != "AI boom → mine expands → Mauricio gets promoted.":
    errors.append("approved CONSEQUENCES prohibited shortcut changed in contract")
if shortcut and shortcut not in js:
    errors.append("approved CONSEQUENCES prohibited shortcut is no longer detected in reader treatment")
if "p.classList.add('prohibited-boundary')" not in js:
    errors.append("approved CONSEQUENCES prohibited shortcut is no longer visually marked")

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
