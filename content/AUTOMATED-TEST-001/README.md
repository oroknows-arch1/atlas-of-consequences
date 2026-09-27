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

## Production pipeline

`tools/produce_edition.py` consumes the selected candidate and its matching gated routes, STORY, visual requirements, locality context and source register. It calls repository-owned image generator and independent visual verifier commands, retries failed contextual assets up to three times, creates source-labelled explanatory graphics, validates and hashes binaries, and assembles a reader from the edition's actual Perspectives. It emits `BLOCKED` and scene-level defects when a required binary cannot be fulfilled. A prompt, URL, gradient, or partial HTML page cannot pass.

The provider adapters are `tools/image_provider_openai.py` and `tools/visual_verifier_openai.py`. They require `OPENAI_API_KEY`; set `ATLAS_IMAGE_COMMAND='python3 tools/image_provider_openai.py'` and `ATLAS_VISUAL_QA_COMMAND='python3 tools/visual_verifier_openai.py'`. Production is not dependent on Runway or generated video. The adapters are replaceable executable commands obeying the JSON input/output contract in `tools/produce_edition.py`.

`tools/deploy_review.py` pins the pushed test branch commit to the existing Render review service using `RENDER_API_KEY`. `tools/rendered_qa.cjs` checks the actual deployed phone and desktop pages and saves screenshots. `tools/review_rendered.py` independently evaluates these alongside an AOC-001 benchmark screenshot. `tools/publication_gate.py` verifies all receipts, local asset hashes and deployed asset hashes before it can emit `PUBLICATION_CANDIDATE`; official publication still requires human approval.

The repository workflow `.github/workflows/atlas-edition-production.yml` is the unattended entry point. It needs GitHub Actions secrets `ATLAS_OPENAI_API_KEY` and `ATLAS_RENDER_API_KEY`. It runs only on `test/automated-edition-1`, writes generated binaries and the reader to that branch, deploys the review service, runs rendered QA and stores receipts/screenshots. No production/main deploy is in the workflow. A missing secret or failed gate blocks it.

**Current AET1 status:** `BLOCKED`. The present Work environment lacks an image API credential and Render API credential. Three explanatory graphics can be built locally; seven contextual stills and deployed rendered QA cannot be completed here. The old `public/review/heat/` HTML remains an editorial review artifact, not a publication candidate.
