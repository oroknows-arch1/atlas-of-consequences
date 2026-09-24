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


def starts(value, prefix):
    return isinstance(value, str) and value.startswith(prefix)


errors = []

skills_doc = load("atlas/registry/skills.json")
workers_doc = load("atlas/registry/workers.json")
authority_doc = load("atlas/registry/authority.json")
graph = load("atlas/graphs/edition-production.json")
edition = load("atlas/editions/AOC-001.json")

skill_ids = {s["id"] for s in skills_doc["skills"]}
worker_ids = {w["id"] for w in workers_doc["workers"]}
node_ids = {n["id"] for n in graph["nodes"]}
nodes = {n["id"]: n for n in graph["nodes"]}

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

# Active opening architecture.
# The human-approved AOC-001 path is factual report film -> final-frame handoff -> reader.
# The earlier hybrid factual+fiction opening is retained only as historical evidence and
# must never be an active reader dependency again.
reader_node = nodes.get("reader_build", {})
reader_requires = set(reader_node.get("requires", []))
if "factual_media_human_gate" not in reader_requires:
    errors.append("reader_build must require factual_media_human_gate")
if "hybrid_human_gate" in reader_requires:
    errors.append("reader_build must not depend on retired hybrid_human_gate")
if reader_node.get("opening_contract") != "approved factual report film -> final-frame handoff -> reader":
    errors.append("reader_build opening contract does not match approved factual-opening architecture")

for retired_id in ("hybrid_opening", "hybrid_human_gate"):
    retired_node = nodes.get(retired_id, {})
    if retired_node.get("lifecycle") != "retired" or retired_node.get("active") is not False:
        errors.append(f"{retired_id} must remain explicitly retired and non-blocking")

# AOC-001 state consistency. Validate outputs and gates without re-imposing a retired route.
visual_gate = node_state.get("visual_character_human_gate")
fiction_gate = node_state.get("fiction_media_human_gate")
factual_gate = node_state.get("factual_media_human_gate")
foreground = edition.get("foreground_next")
fiction_state = node_state.get("fiction_media")
reader_state = node_state.get("reader_build")
publication_state = node_state.get("publication_qa")
distribution_state = node_state.get("distribution_pack")
release_state = node_state.get("release_human_gate")

if visual_gate == "approved":
    if node_state.get("visual_character_bible") != "satisfied_by_approved_reference_set":
        errors.append("approved visual gate requires approved visual-character reference state")
    if fiction_state not in {"ready", "candidate_approved"}:
        errors.append("approved visual gate must unlock or preserve fiction_media progress")

if approved(fiction_gate) and fiction_state != "candidate_approved":
    errors.append("approved fiction-media gate requires candidate_approved fiction_media state")

reader_complete_states = {"candidate_approved", "complete_master_integrated"}
distribution_complete_states = {"candidate_approved", "candidate_v0.1_assembled"}

if reader_state in reader_complete_states:
    if not approved(factual_gate):
        errors.append("completed reader requires approved factual_media_human_gate")
    if node_state.get("story_boundary_gate") != "satisfied_by_existing_artifact":
        errors.append("completed reader requires satisfied story boundary gate")
    if node_state.get("source_register") != "satisfied_by_existing_artifact":
        errors.append("completed reader requires satisfied source register")

if foreground == "publication_qa":
    if reader_state not in reader_complete_states:
        errors.append("publication_qa foreground requires completed reader_build")
    if distribution_state not in distribution_complete_states:
        errors.append("publication_qa foreground requires assembled distribution_pack")
    if publication_state not in {"ready", "rerun_pending_after_remediation"} and not starts(publication_state, "failed_") and not starts(publication_state, "passed_"):
        errors.append("publication_qa foreground has an unrecognised publication_qa state")

if starts(publication_state, "failed_") or publication_state == "rerun_pending_after_remediation":
    if release_state != "blocked":
        errors.append("non-passed publication QA must keep release human gate blocked")

if release_state != "blocked" and not starts(publication_state, "passed_"):
    errors.append("release human gate cannot advance before publication QA passes")

# Historical hybrid state is allowed only when explicitly marked historical/retired.
if node_state.get("hybrid_opening") not in {"retired_as_active_requirement", "historical_only", "candidate_approved"}:
    errors.append("hybrid_opening state must remain historical or retired")
if node_state.get("hybrid_human_gate") not in {"historical_approval_only", "retired", "approved_2026-09-24"}:
    errors.append("hybrid_human_gate state must remain historical or retired")

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
print(f"- active opening: {reader_node.get('opening_contract')}")
print(f"- foreground next: {edition['foreground_next']}")
