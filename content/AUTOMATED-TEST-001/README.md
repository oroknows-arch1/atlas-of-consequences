# Automated Edition Test #1 — executable hand-off

This directory is the input/output boundary for the first genuine automated run.

The deterministic runner is `tools/run_automated_edition.py`. It deliberately does **not** pretend to perform research or creative reasoning. Model/research/verification workers must write explicit stage receipts here; the runner then checks dependency completion, assembles the edition-neutral manifest, runs deterministic invariants and emits a run receipt.

Required pre-assembly files, in graph order:

`world_change_intake.json`, `evidence_graph.json`, `evidence_gate.json`, `geography_resolution.json`, `perspective_candidates.json`, `perspective_gate.json`, `route_scene_generation.json`, `causal_boundary_gate.json`, `visual_requirements.json`, `image_provider_routing.json`.

Every stage file has:
- `stage`: exact graph node id
- `status`: `PASS`
- `produced_by`: worker/model/verifier identity
- `output`: the stage payload

The runner currently consumes the approved/gated outputs from world-change intake, evidence graph, geography, Perspective gate, causal-boundary gate and image-provider routing. Intermediate receipts remain mandatory so failures cannot be hidden.

Run:

`python3 tools/run_automated_edition.py content/AUTOMATED-TEST-001`

Success creates `generated-edition.json` and `run-receipt.json`. It does not publish.

## Visual resilience

Provider availability or credit exhaustion may change HOW a visual requirement is fulfilled; it must never change evidence, Perspective structure, scene meaning or factual boundary. Video generation is optional. Runway is an exception provider, never a completion dependency.

## Publication boundary

A passing runner receipt permits the test to proceed to asset generation/QA and reviewable reader assembly. It never authorizes publication or distribution. Explicit human publication approval remains required.
