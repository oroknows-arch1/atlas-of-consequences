# Production execution continuation

The runner lives in this repository and executes in GitHub Actions. Work is used to change and verify its code, not as the edition's ongoing production host.

## Accepted input and manufacturing coverage

`tools/production_state.py:INPUTS` defines the selected-candidate continuation bundle. The legacy `evidence_gate.json` and `geography_resolution.json` in the test folder describe an earlier fertilizer candidate. They are deliberately not inputs to heat production. The selected heat candidate, selection gate, accepted Perspectives, bounded routes, STORY, visual requirements, context, data and source register remain authoritative.

The constitutional **MANUFACTURING-TRACE COVERAGE INVARIANT** is represented by `atlas/contracts/manufacturing-trace.json`. Run `python3 tools/validate_manufacturing_trace.py` to detect missing operations or missing executable owners. Coverage PASS means each operation is mapped; it does not claim that an edition has passed execution.

## Execution

Workflow: `.github/workflows/atlas-edition-production.yml`, restricted to `test/automated-edition-1`. It never deploys main or grants publication authority.

1. Validate manufacturing coverage and regression tests.
2. Check all provider credentials and invalidate prior terminal approval.
3. Validate the selected input bundle; generate publication prose from accepted claims and independently verify it. Preserve the approved STORY.
4. Generate required contextual binaries, independently inspect them, and persist hashes, provenance and visual QA. Reuse verified unchanged assets on retry.
5. Assemble opening, reader-selected routes, STORY, CONSEQUENCES, PLACE and inspectable SOURCES.
6. Check source accessibility, commit outputs to the test branch, and deploy to its existing review service.
7. Exercise every view at 320px, 390px and 1440px; check route isolation, selection, reload, Back, source anchors and decoded images. Capture phone/desktop views and benchmark routes.
8. Independently inspect rendered screenshots; return typed defects to the responsible worker. Repair and redeploy up to three times. Exhausted or unsupported repair stays BLOCKED.
9. Require current input fingerprints, reader hashes, deployment identity, screenshot hashes, asset coverage, visual verdicts and actual deployed bytes before emitting PUBLICATION_CANDIDATE with its review URL.

The reader's visible build label does not claim candidate status. The terminal receipt is authoritative. Nothing is officially published by this workflow.

## Capability setup

GitHub repository Actions secrets required by the existing provider adapters:

- `ATLAS_OPENAI_API_KEY`: image generation, editorial generation and independent visual/editorial verification.
- `ATLAS_RENDER_API_KEY`: deployment to the existing review service.

ChatGPT-connected Render access does not make a credential available to GitHub Actions. Never paste credential values into repository files or logs.

Existing review service: `srv-dase6m8jo6nc73bdh1ig`, bound to `test/automated-edition-1`; automatic deployment is off. The deployment worker verifies service repository, branch, requested commit and deployed commit before accepting its receipt.

After configuring credentials, rerun the failed production job from the branch. Normal operations and repair run in the repository workflow.

## Verification limits for this change

Synthetic regression fixtures test failure behavior; they are not publication assets or QA receipts. AOC-001 regression validators pass without changing benchmark files. The live provider/deployment/rendered path remains unproven while runner credentials are unavailable. A local Chromium download also failed, so source/DOM inspection is not presented as rendered proof. The heat edition remains BLOCKED until the real workflow completes.
