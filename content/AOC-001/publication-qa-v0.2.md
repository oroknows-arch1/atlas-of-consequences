# AOC-001 — Publication QA v0.2

**Edition:** AOC-001 — *AI's Physical Hunger*  
**QA date:** 2026-09-25  
**QA scope:** full end-to-end rerun across the remediated mobile reader, locked Master Edition, evidence surfaces, approved media, distribution candidate, Render deployment state and Atlas production/validation contracts.  
**Verdict:** **FAIL — PUBLICATION MECHANICS PASS, RELEASE READINESS STILL BLOCKED**

The v0.1 reader-completeness failures have been remediated. The current reader and distribution candidate pass the publication-content gates. Two release blockers remain outside the approved reader design: the Atlas orchestration validator is enforcing a retired hybrid-opening state, and the OROK companion release scope remains unresolved.

## Evidence audited

- `public/index.html`
- `public/reader-publication-treatments.css`
- `public/reader-publication-treatments.js`
- `content/AOC-001/master-edition-v0.1.md`
- `content/AOC-001/sources/publication-source-register-v0.1.md`
- `content/AOC-001/sources/report-video-v0.4-asset-register.md`
- `content/AOC-001/media/AOC001-READER-APPROVAL.md`
- `content/AOC-001/media/AOC001-REPORT-VIDEO-APPROVAL.md`
- `content/AOC-001/media/AOC001-STORY-PROMO-APPROVAL.md`
- `content/AOC-001/distribution/distribution-candidate-v0.1.md`
- `content/AOC-001/edition-manifest-v0.1.yaml`
- `atlas/editions/AOC-001.json`
- `atlas/graphs/edition-production.json`
- `tools/validate_atlas_graph.py`
- GitHub Actions run `36043978963`
- Render service `atlas-of-consequences`

## Live deployment check

Render reports the production static site `atlas-of-consequences` on branch `main`, auto-deploy enabled, with commit `05a6182cc35aa1f20b7348dd3ef79947d316243f` live. This is the same commit containing the integrated reader, distribution candidate and current AOC-001 state.

The QA environment could verify the Render deployment/control-plane state and repository source, but it did not have an independent interactive iPhone browser session. The previously human-approved visual baseline remains the authority for the opening/reader look; this rerun checks that the approved source behaviour was preserved and that the new publication layers do not replace it.

## Publication gate results

| Gate | Result | QA finding |
|---|---|---|
| Production deployment parity | **PASS** | Render production is live from current `main` commit `05a6182c…`. |
| Approved opening / reader visual behaviour | **PASS** | Factual film remains the only automatic opening; muted autoplay fallback, Tap for sound, Skip, final-frame hold, full-screen handoff, `0.67` reader brightness, scroll-scrub and fail-open error handling remain in source. Story promo is not auto-played. |
| Reader sequence | **PASS** | WHAT'S REAL → STORY → CONSEQUENCES → PLACE → SOURCES remains intact. |
| Complete locked Master Edition in reader | **PASS** | The full factual report, locked fiction, consequence analysis, PLACE material and SOURCES surface are now present rather than skeleton summaries. |
| Key factual claims / callouts | **PASS** | Reader text and callouts surface 415 TWh, ~1.5%, 58%, ~15 km, 266 kt and 3,992 with the relevant limitations retained. |
| Fact / fiction boundary | **PASS** | STORY — FICTION is visually explicit; the complete fiction disclosure precedes the story; the fictional household is not presented as testimony or evidence. |
| Consequence certainty model | **PASS** | The three certainty levels are present and the prohibited shortcut `AI boom → mine expands → Mauricio gets promoted` is explicitly separated. |
| PLACE treatment | **PASS** | Full Calama context, real-location treatment, city-not-mine framing, work/home context, relocation/heritage context and Indigenous sourcing boundary are present. |
| SOURCES inspection surface | **PASS** | SR-01 through SR-16 are wired as collapsible source cards with source role, limitation and direct links. |
| Evidence / causal discipline | **PASS** | Distribution and reader claims remain inside the locked source register. No direct AI → specific mine expansion → fictional promotion chain is asserted. |
| Real-world media provenance / rights record | **PASS** | Factual film has an asset register with source context, licensing and use boundaries. Required attribution/ShareAlike obligations remain recorded. |
| Mobile opening failure safety | **PASS** | Skip and video-error handlers reveal the reader; playback failure does not trap the user. |
| Reduced-motion / static fallback | **PASS — implementation** | Reduced-motion CSS hides the video and uses the approved v0.4 review frame; JS pauses/removes autoplay, hides the sound control and enters the reader immediately. A separate human device spot-check of the OS preference remains advisable before release, but the v0.1 implementation defect is fixed. |
| Distribution candidate exists | **PASS** | v0.1 binds the approved factual report film and approved STORY / FICTION promo and includes factual carousel copy, fiction-still treatment, captions, headlines/descriptions and poster/thumbnail bindings. |
| Distribution fact / fiction separation | **PASS** | Factual and fictional branches are explicitly separate and are not stitched into an ambiguous auto-playing asset. |
| Distribution claim discipline | **PASS** | Factual captions and carousel claims map to SR-01/02/03/04/05/07/08 and preserve the causal limitation. |
| Permanent-edition return path | **PASS** | Distribution copy points to `https://atlas-of-consequences.onrender.com/`. |
| Manifest / live-reader congruence | **PASS** | Active manifest reflects factual-film-only opening, complete reader integration, distribution candidate and retired rejected opening behaviours. |
| OROK companion release scope | **FAIL / RELEASE BLOCKER** | OROK remains an unresolved release-scope requirement. It is explicitly carried forward rather than silently dropped, but it must be produced or explicitly removed/re-scoped by human authority before the release gate. |
| Atlas graph / CI contract | **FAIL / RELEASE BLOCKER** | GitHub Actions run `36043978963` fails `tools/validate_atlas_graph.py` because the validator still requires the retired `hybrid_opening` route when factual media is approved. The current edition state correctly marks the old hybrid requirement retired/historical. The test contract is stale and would route Atlas back toward rejected behaviour. |
| Optional soundtrack durability | **WARNING** | The reader still references `atlas-aoc001-media-bridge.onrender.com` for the optional soundtrack. The silent/factual-film experience remains complete, so this does not block the reader, but a permanent release should not depend on a temporary bridge for the sonic layer. |

## Regression findings from QA v0.1

The following v0.1 failures are now closed:

- complete Master Edition missing from reader → **closed**;
- key factual callouts missing → **closed**;
- full fiction disclosure/story missing → **closed**;
- consequence certainty treatment missing → **closed**;
- PLACE treatment missing → **closed**;
- inspectable SR-01–SR-16 source cards missing → **closed**;
- reduced-motion static fallback missing → **closed in implementation**;
- distribution candidate missing → **closed**;
- manifest drift → **closed**.

## Remaining blockers

### B1 — Atlas orchestration validator still encodes the retired opening model

The current GitHub Actions validation run fails with:

> `approved factual media with pending opening gate requires hybrid_opening as AOC-001 foreground`

That assertion is no longer valid. The approved product truth is:

- factual report film only on automatic entry;
- Story promo remains separate;
- no automatic factual → story-promo sequence;
- final factual frame hands into the reader;
- full reader then scroll-scrubs the factual film.

The graph/validator must be reconciled to that truth without changing the approved reader to satisfy the stale validator.

### B2 — OROK companion scope remains unresolved

The current manifest deliberately keeps this visible. Before release human approval, Atlas needs one explicit decision:

- produce the AOC-001 OROK companion package; or
- revise v0.1 release scope so the OROK companion is not required for this prototype release.

No silent omission is permitted.

## Warnings, not blockers

- Reduced-motion fallback is implemented by source inspection, but was not independently exercised in a new device/browser session during this rerun.
- The optional soundtrack remains served through the temporary media bridge.
- Distribution Candidate v0.1 is a release candidate package; platform-specific 9:16 story-promo reframing remains optional and must not be generated merely to satisfy format convention if it damages labels, faces or meaning.

## QA disposition

- `reader_build`: **PASS**
- `distribution_pack`: **PASS**
- `publication_qa`: **FAIL / BLOCKED BY B1 + B2**
- `release_human_gate`: **BLOCKED**
- `publish`: **BLOCKED**
- visual reader approval: **PRESERVED**

## Next single action

Repair the **Atlas orchestration contract / validator drift** so the production graph recognises the already-approved factual-opening-to-reader architecture and the current post-remediation reader/distribution state. Do **not** reintroduce the rejected auto-playing Story promo or redesign the reader. Rerun graph validation after that repair; OROK scope remains the following release-scope decision.
