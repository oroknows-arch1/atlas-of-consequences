#!/usr/bin/env python3
"""Validate Atlas worker/skill/authority/graph contracts and the AOC-001 live binding."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def load(rel):
    with (ROOT / rel).open("r", encoding="utf-8") as f:
        return json.load(f)


def approved(value):
    return isinstance(value, str) and value.startswith("approved")


errors = []

skills_doc = load("atlas/registry/skills.json")
workers_doc = load("atlas/registry/workers.json")
authority_doc = load("atlas/registry/authority.json")
graph = load("atlas/graphs/edition-production.json")
edition = load("atlas/editions/AOC-001.json")

skill_ids = {s["id"] for s in skills_doc["skills"]}
worker_ids = {w["id"] for w in workers_doc["workers"]}
node_ids = {n["id"] for n in graph["nodes"]}

if len(skill_ids) != len(skills_doc["skills"]):
    errors.append("duplicate skill id")
if len(worker_ids) != len(workers_doc["workers"]):
    errors.append("duplicate worker id")
if len(node_ids) != len(graph["nodes"]):
    errors.append("duplicate graph node id")

for worker in workers_doc["workers"]:
    missing = sorted(set(worker.get("skills", [])) - skill_ids)
    if missing:
        errors.append(f"worker {worker['id']} references missing skills: {missing}")
    if not worker.get("write_scope"):
        errors.append(f"worker {worker['id']} has no write_scope")
    if not worker.get("may_not"):
        errors.append(f"worker {worker['id']} has no explicit prohibitions")

for node in graph["nodes"]:
    if node.get("type") == "human_gate":
        if "condition" not in node:
            errors.append(f"human gate {node['id']} has no condition")
    else:
        worker = node.get("worker")
        if worker not in worker_ids:
            errors.append(f"node {node['id']} references missing worker {worker!r}")
    for dep in node.get("requires", []):
        if dep not in node_ids:
            errors.append(f"node {node['id']} requires missing node {dep}")

if graph.get("orchestrator") != "atlas_orchestrator":
    errors.append("graph orchestrator must be atlas_orchestrator")

for boundary in authority_doc.get("immutable_boundaries", []):
    if not boundary.strip():
        errors.append("blank immutable boundary")

if edition.get("graph") != "atlas/graphs/edition-production.json":
    errors.append("AOC-001 is not bound to the production graph")

node_state = edition.get("node_state", {})
for node_id in node_state:
    if node_id not in node_ids:
        errors.append(f"AOC-001 state references unknown node {node_id}")

for rel in edition.get("authority_sources", []):
    if not (ROOT / rel).exists():
        errors.append(f"AOC-001 authority source missing: {rel}")

for name, rel in edition.get("artifact_bindings", {}).items():
    if not (ROOT / rel).exists():
        errors.append(f"AOC-001 artifact binding missing: {name} -> {rel}")

required_boundaries = {
    "Facts can change the fiction. Fiction must never quietly become fact.",
    "Connection may be shown. Causation requires evidence."
}
present = set(authority_doc.get("immutable_boundaries", []))
for item in required_boundaries:
    if item not in present:
        errors.append(f"required Atlas boundary missing: {item}")

# Derive AOC-001 foreground from the live human-gate state.
visual_gate = node_state.get("visual_character_human_gate")
fiction_gate = node_state.get("fiction_media_human_gate")
factual_gate = node_state.get("factual_media_human_gate")
hybrid_gate = node_state.get("hybrid_human_gate")
foreground = edition.get("foreground_next")
fiction_state = node_state.get("fiction_media")
reader_state = node_state.get("reader_build")
publication_state = node_state.get("publication_qa")

if visual_gate == "approved":
    if node_state.get("visual_character_bible") != "satisfied_by_approved_reference_set":
        errors.append("approved visual gate requires approved visual-character reference state")
    if fiction_state not in {"ready", "candidate_approved"}:
        errors.append("approved visual gate must unlock or preserve fiction_media progress")

    if approved(fiction_gate):
        if fiction_state != "candidate_approved":
            errors.append("approved fiction-media gate requires candidate_approved fiction_media state")

        if approved(factual_gate):
            if approved(hybrid_gate) and reader_state == "candidate_approved":
                if foreground != "publication_qa":
                    errors.append("approved reader state requires publication_qa as AOC-001 foreground")
                if publication_state != "ready":
                    errors.append("approved reader state requires publication_qa to be ready")
            else:
                if foreground != "hybrid_opening":
                    errors.append("approved factual media with pending opening gate requires hybrid_opening as AOC-001 foreground")
        else:
            if foreground != "factual_media":
                errors.append("approved fiction-media gate with pending factual gate requires factual_media as AOC-001 foreground")
    else:
        if fiction_state != "ready":
            errors.append("unapproved fiction-media gate requires fiction_media to remain ready")
        if foreground != "fiction_media":
            errors.append("approved visual gate with pending fiction gate requires fiction_media as AOC-001 foreground")
else:
    if foreground != "visual_character_bible":
        errors.append("unapproved visual gate requires visual_character_bible as AOC-001 foreground")

if errors:
    print("ATLAS GRAPH VALIDATION: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("ATLAS GRAPH VALIDATION: PASS")
print(f"- skills: {len(skill_ids)}")
print(f"- workers: {len(worker_ids)}")
print(f"- graph nodes: {len(node_ids)}")
print(f"- live edition: {edition['edition_id']}")
print(f"- foreground next: {edition['foreground_next']}")
