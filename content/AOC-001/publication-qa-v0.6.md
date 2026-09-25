# AOC-001 — Publication QA v0.6

**Edition:** AOC-001 — *AI's Physical Hunger*  
**QA date:** 2026-09-25  
**QA type:** targeted rerun after post-v0.5 opening-control placement correction  
**Baseline full QA:** `content/AOC-001/publication-qa-v0.5.md`  
**Approved UI correction commit:** `6ff5173e7c6df6e20d2ff162403489cfdd4cdec3`  
**Regression/state verification commit:** `ad01a9c81ac006f29dc3898c55e1c912fe1f485b`  
**Verdict:** **PASS — READY FOR HUMAN RELEASE APPROVAL**

AOC-001 remains publication-clean after moving the opening **Tap for sound** and **Skip** controls away from lower-third factual video text. The human device check confirmed the overlap is fixed. This targeted rerun does not publish the edition and does not replace the release human gate.

## Scope

The only reader presentation change since Publication QA v0.5 is the opening-control placement override in `public/reader-publication-treatments.css`:

- controls remain horizontally separated left/right;
- vertical position is fixed at the midpoint (`top: 50%` with `translateY(-50%)`);
- bottom anchoring is disabled;
- lower-third factual text is no longer covered.

No story text, factual claim, source register, media asset, causal boundary, reader sequence, opening soundtrack behaviour, final-frame handoff, Edition Map, scroll scrub, WHAT'S REAL treatment, STORY perspective treatment, CONSEQUENCES treatment, PLACE treatment, SOURCES treatment or distribution content was changed.

## Regression protection

The approved midpoint control position is now part of the human-approved reader contract:

- `atlas/contracts/aoc001-reader-invariants.json` schema v1.7;
- `tools/validate_opening_controls.py` verifies midpoint placement, both controls and lower-third clearance intent;
- `.github/workflows/validate-atlas-graph.yml` runs this check with the existing graph and reader-invariant checks whenever relevant Atlas/content/public files change.

GitHub Actions run **#79** completed successfully. Its validation job passed all three relevant checks:

1. Atlas worker/skills/authority/graph and AOC-001 binding;
2. human-approved AOC-001 reader invariants;
3. approved opening-control position.

## Gate results

| Gate | Result | Finding |
|---|---|---|
| Human phone check of control placement | **PASS** | User confirmed the overlap issue is fixed. |
| Lower-third factual text clearance | **PASS** | Controls moved from bottom anchoring to vertical midpoint. |
| Tap for sound retained | **PASS** | Control remains present and functional surface is unchanged. |
| Skip retained | **PASS** | Control remains present and functional surface is unchanged. |
| Opening factual film | **PASS — unchanged** | Same approved factual film remains the automatic opening. |
| Soundtrack fade | **PASS — unchanged** | Approved 2.2-second closing fade remains protected. |
| Final-frame → Edition Map handoff | **PASS — unchanged** | No handoff code changed. |
| Scroll-scrub background | **PASS — unchanged** | No scrub code changed. |
| Fact / fiction separation | **PASS — carried forward** | No content or boundary file changed. |
| WHAT'S REAL / STORY / CONSEQUENCES / PLACE / SOURCES | **PASS — carried forward** | No section content/treatment changed. |
| Source register / provenance | **PASS — carried forward** | No evidence or media provenance record changed. |
| Distribution candidate | **PASS — carried forward** | Distribution Candidate v0.1 unchanged. |
| Reader regression protection | **PASS** | Existing invariant suite plus new opening-control check passed in CI run #79. |

## Disposition

- `reader_build`: **PASS — HUMAN APPROVED**
- `opening_controls`: **PASS — HUMAN APPROVED + REGRESSION PROTECTED**
- `publication_qa`: **PASS — v0.6**
- `release_human_gate`: **READY**
- `publish`: **BLOCKED pending explicit human release approval**

## Remaining non-blocking warning

The approved soundtrack is still served from the separate Atlas media-bridge service. Soundtrack failure does not block the factual reader, so this remains non-blocking.

## Next single action

**AOC-001 Release Human Gate:** review the final live candidate and explicitly approve or reject publication. No automatic publication is authorised by this QA pass.
