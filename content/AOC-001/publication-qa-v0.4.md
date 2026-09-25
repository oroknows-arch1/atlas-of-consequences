# AOC-001 — Publication QA v0.4

**Edition:** AOC-001 — *AI's Physical Hunger*  
**QA date:** 2026-09-25  
**QA scope:** full end-to-end rerun after human approval of the reader v0.2 opening handoff, Edition Map, WHAT'S REAL causal flow, STORY perspective entry, CONSEQUENCES treatment, PLACE treatment and SOURCES treatment.  
**Audited reader commit:** `625cb606d9db0bd0eae11d98fc8ab3be1a427b3c`  
**Verdict:** **FAIL — LIVE PUBLICATION CONTENT PASSES; RELEASE STATE / REGRESSION CONTRACT REQUIRES RECONCILIATION**

The complete live reader passes the publication-content and human visual-review gates reached in this cycle. It is not yet clean to advance to release approval because the active repository state does not fully describe the approved reader and one approved reader treatment is not yet protected by the regression contract.

No new media generation was required. **Runway credits used by this QA: 0.**

## Evidence audited

- `public/index.html`
- `public/reader-publication-treatments.css`
- `public/reader-publication-treatments.js`
- `atlas/contracts/aoc001-reader-invariants.json`
- `tools/validate_reader_invariants.py`
- `atlas/editions/AOC-001.json`
- `content/AOC-001/edition-manifest-v0.1.yaml`
- `content/AOC-001/reader-architecture-v0.2.md`
- `content/AOC-001/master-edition-v0.1.md`
- `content/AOC-001/sources/publication-source-register-v0.1.md`
- `content/AOC-001/sources/report-video-v0.4-asset-register.md`
- `content/AOC-001/distribution/distribution-candidate-v0.1.md`
- approved factual-film, story-promo, soundtrack and visual-character approval records
- GitHub Actions Validate Atlas worker graph run #68
- Render production service `atlas-of-consequences`
- human mobile review completed section-by-section in the current approval cycle

## Deployment / source parity

**PASS.**

Render production `atlas-of-consequences` is on branch `main`, auto-deploy is enabled, and commit `625cb606d9db0bd0eae11d98fc8ab3be1a427b3c` is live.

A comparison from Publication QA v0.3 commit `92f8afdca6a26ba7063c8d1a2b5274e2ac96e890` to the audited reader commit shows changes only to reader/runtime treatment, reader architecture/state, the new invariant contract/validator and workflow wiring. The locked Master Edition, publication source register, Distribution Candidate v0.1 and approved media/provenance records did not change.

## Gate results

| Gate | Result | QA finding |
|---|---|---|
| Production deployment parity | **PASS** | Current `main` reader commit is live on Render. |
| Opening factual film | **PASS** | Factual film remains the only automatic opening. Story promo is not auto-appended. |
| Opening soundtrack handoff | **PASS** | Human-approved 2.2-second closing fade is present and regression-protected. |
| Final-frame → reader handoff | **PASS** | Final film frame holds behind the Edition Map and remains the live scrub background until scrolling begins. |
| Scroll-scrub behaviour | **PASS** | Same factual film remains the reader background and scroll position controls frame progression. |
| Edition Map | **PASS — HUMAN REVIEW** | Post-film orientation screen was reviewed on phone and approved. |
| WHAT'S REAL causal flow | **PASS** | Approved `AI/data-centres → electricity/grid → materials/copper → northern Chile → Calama/Chuquicamata` treatment is present and regression-protected. |
| Complete locked Master Edition | **PASS** | Master Edition content remains integrated; master file is unchanged since the prior passing content audit. |
| Fact / fiction separation | **PASS** | STORY — FICTION disclosure remains explicit and the fictional family is not presented as evidence. |
| STORY perspective entry | **PASS — CURRENT READER / HUMAN REVIEW** | Current reader contains the approved family/labour current lens plus operator/supplier, buyer/customer and investor/market framework classes. **Regression protection is incomplete; see B2.** |
| CONSEQUENCES certainty model | **PASS** | Documented global → documented place → fictional human layers and prohibited shortcut remain visible and protected. |
| PLACE treatment | **PASS** | Calama/Antofagasta/Chuquicamata grounding, city-beyond-extraction framing and cultural/fact-fiction boundaries remain visible and protected. |
| SOURCES inspection | **PASS** | SR-01 through SR-16 remain inspectable; each card states what the source supports and its limitation; evidence/fiction boundary remains explicit and protected. |
| Evidence / causal discipline | **PASS** | No direct AI → mine expansion → fictional promotion claim is asserted. |
| Factual media provenance / rights | **PASS — CARRIED FORWARD** | Approval/provenance records are unchanged from the prior passing audit. |
| Distribution candidate | **PASS — CARRIED FORWARD** | Candidate v0.1 is unchanged; factual and fictional branches remain separate and return to the permanent Atlas destination. |
| Atlas graph / worker validation | **PASS** | GitHub Actions run #68 passed the worker/skills/authority/graph/AOC-001 binding step. |
| Human-approved reader invariant validation | **PASS, WITH GAP** | Run #68 passed the encoded invariants. The approved STORY perspective panel is not currently encoded; see B2. |
| OROK release scope | **PASS / OPTIONAL** | Prior human scope decision remains unchanged and non-blocking. |
| New media required | **NO** | No additional video/media generation is required for this QA. |

## Release blockers

### B1 — Active manifest and edition state have drifted behind the approved reader

The live reader is current, but repository authority records still describe the state that existed before this completed review cycle.

`content/AOC-001/edition-manifest-v0.1.yaml` still records, among other stale items:

- edition status as `publication QA v0.3 passed / release human approval ready`;
- Publication QA v0.3 as the active QA authority;
- the retired reduced-motion behaviour in which the video is hidden, a static frame is substituted and the reader is entered immediately;
- reader/content integration statuses as `QA v0.3 pass`;
- production pipeline P6/P8/P9 as already QA-passed / release-ready;
- next foreground action as the release human gate.

That directly conflicts with the current human-approved runtime contract, which requires reduced motion **not** to skip the factual opening or hide the reader video, and with this new QA cycle.

`atlas/editions/AOC-001.json` is also stale: it still says the v0.2 reader is awaiting human visual review, records the older release-review QA failure and keeps `foreground_next` at `reader_build`, despite the completed section-by-section approvals and this QA rerun.

Because the manifest is defined as the active production contract, this is a release blocker rather than harmless historical text.

### B2 — Approved STORY perspective panel is not protected by the reader invariant contract

The current reader correctly contains and the human review approved the STORY entry/perspective panel:

- current: Family + labour;
- framework: Operator + supplier;
- framework: Buyer + customer;
- framework: Investor + market.

However `atlas/contracts/aoc001-reader-invariants.json` v1.5 does not encode this approved STORY treatment, and `tools/validate_reader_invariants.py` does not check the `story-lens` panel or its four perspective classes.

The runtime is correct today, but a future reader change could silently remove or alter this approved treatment while CI remained green. Given the explicit anti-regression rule established for this reader, that gap must be closed before release readiness is declared.

## Warning — soundtrack hosting durability

The approved soundtrack is still loaded from `https://atlas-aoc001-media-bridge.onrender.com/soundtrack.mp3`. The bridge service is present and not suspended, and soundtrack failure does not prevent the factual reader from opening. This remains a **non-blocking durability warning**, but a permanent Atlas-owned asset path would be preferable before the system is treated as fully self-contained.

## QA disposition

- `reader_build`: **PASS — HUMAN APPROVED**
- `publication content`: **PASS**
- `distribution candidate`: **PASS — unchanged**
- `deployment parity`: **PASS**
- `publication_qa`: **FAIL / BLOCKED BY B1 + B2**
- `release_human_gate`: **BLOCKED**
- `publish`: **BLOCKED**

## Next single action

**Reconcile the AOC-001 active state and regression contract to the already-approved reader v0.2.**

That cleanup should, without changing the reader/content/media:

1. update `edition-manifest-v0.1.yaml` to the current reduced-motion behaviour, completed human review and Publication QA v0.4 state;
2. update `atlas/editions/AOC-001.json` to the completed reader review/current QA state;
3. add the approved STORY perspective panel/classes to `aoc001-reader-invariants.json` and `validate_reader_invariants.py`;
4. rerun CI and then rerun Publication QA.

Do **not** rewrite the story, regenerate media, change factual claims, alter the approved reader appearance, reintroduce the Story promo into the automatic opening, or publish as part of this remediation.
