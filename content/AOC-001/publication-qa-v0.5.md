# AOC-001 — Publication QA v0.5

**Edition:** AOC-001 — *AI's Physical Hunger*  
**QA date:** 2026-09-25  
**QA scope:** full end-to-end rerun after remediation of Publication QA v0.4 blockers B1 (active manifest/edition-state drift) and B2 (missing STORY perspective regression protection).  
**Audited reader baseline:** `625cb606d9db0bd0eae11d98fc8ab3be1a427b3c`  
**Audited remediation state:** `46d9ec65d95179e86efd0bb0c59890260bdab9e3`  
**Verdict:** **PASS — READY FOR HUMAN RELEASE APPROVAL**

AOC-001 passes the publication gate after reconciliation. This QA does **not** publish the edition and does **not** substitute for the release human gate.

No new media generation was required. **Runway credits used by this QA: 0.**

## What was verified

### 1. Reader/content preservation during remediation

**PASS.**

A commit comparison from the fully human-approved reader baseline `625cb606d9db0bd0eae11d98fc8ab3be1a427b3c` to remediation state `46d9ec65d95179e86efd0bb0c59890260bdab9e3` shows changes only to:

- `atlas/contracts/aoc001-reader-invariants.json`;
- `tools/validate_reader_invariants.py`;
- `atlas/editions/AOC-001.json`;
- `content/AOC-001/edition-manifest-v0.1.yaml`;
- `content/AOC-001/publication-qa-v0.4.md`.

No `public/**` reader file changed. The locked Master Edition, factual claims, story text, source register, approved media and Distribution Candidate v0.1 were not altered by remediation.

### 2. Publication QA v0.4 blocker B1 — active state / manifest drift

**PASS — CLOSED.**

The active manifest and edition binding now describe the current human-approved reader v0.2 rather than the superseded pre-review state.

The reconciled state now records:

- completed human mobile review of the opening handoff, Edition Map, WHAT'S REAL, STORY, CONSEQUENCES, PLACE and SOURCES;
- the approved 2.2-second soundtrack fade;
- final-frame hold into the Edition Map and live scroll-scrub background;
- reduced-motion behaviour that does not skip the factual opening, hide the reader video or replace the reader background with the static poster;
- Publication QA v0.4 as the prior failed QA authority while remediation was being verified;
- `publication_qa` as `rerun_pending_after_remediation` and the release human gate blocked during this rerun.

The stale v0.3 release-ready state is no longer the active production truth.

### 3. Publication QA v0.4 blocker B2 — STORY perspective regression protection

**PASS — CLOSED.**

`atlas/contracts/aoc001-reader-invariants.json` schema v1.6 now protects the human-approved STORY perspective entry:

- **CURRENT:** Family + labour;
- **FRAMEWORK:** Operator + supplier;
- **FRAMEWORK:** Buyer + customer;
- **FRAMEWORK:** Investor + market.

The contract also protects the boundary that additional fictional perspectives do not become market or investment evidence.

`tools/validate_reader_invariants.py` now checks:

- STORY perspective panel and grid treatment;
- current/framework state styling hooks;
- the four approved perspective classes and their order;
- the current `Inside → out · family + labour` direction;
- the market-evidence boundary;
- placement of the perspective panel before the fiction boundary.

### 4. Atlas graph + reader invariant CI

**PASS.**

GitHub Actions **Validate Atlas worker graph run #73** completed successfully on commit `46d9ec65d95179e86efd0bb0c59890260bdab9e3`.

Both validation stages passed:

- worker / skills / authority / graph / AOC-001 binding;
- human-approved AOC-001 reader invariants, including the new STORY protections.

### 5. Production deployment parity

**PASS.**

Render production service `atlas-of-consequences` auto-deployed commit `46d9ec65d95179e86efd0bb0c59890260bdab9e3` and reports it **live**.

Because the remediation commit range contains no `public/**` changes, the live reader surface remains the same human-approved reader while its governing state and regression protection have been repaired.

### 6. Reader publication gates

**PASS — carried forward and protected.**

The following were already human-reviewed and remain unchanged through remediation:

- factual film is the only automatic opening;
- opening soundtrack ends with the approved natural 2.2-second fade;
- final factual frame holds behind the Edition Map;
- the same factual film remains the live scroll-scrub background;
- Edition Map is approved;
- WHAT'S REAL causal flow is approved and protected;
- STORY fact/fiction disclosure and perspective entry are approved and protected;
- CONSEQUENCES certainty layers and prohibited shortcut are approved and protected;
- PLACE grounding and cultural/context boundaries are approved and protected;
- SOURCES SR-01 through SR-16, supports/limitations and evidence/fiction boundary are approved and protected.

### 7. Master content, evidence, media and distribution

**PASS — unchanged.**

The locked Master Edition, publication source register, factual-media provenance/rights record, separate STORY / FICTION promo approval, visual-character continuity records and Distribution Candidate v0.1 remain unchanged from the prior passing content audits.

OROK remains optional downstream enrichment and is non-blocking for AOC-001 release.

## Non-blocking warning

The opening soundtrack is still served from the separate `atlas-aoc001-media-bridge.onrender.com` service rather than a permanent Atlas-owned static asset path. The bridge is operational and soundtrack failure does not block reader access. This is a durability improvement for later, not a publication blocker for AOC-001.

## Final gate table

| Gate | Result |
|---|---|
| Human-approved live reader preserved | **PASS** |
| Production deployment parity | **PASS** |
| Opening film / soundtrack / final-frame handoff | **PASS** |
| Scroll-scrub background | **PASS** |
| Edition Map | **PASS** |
| WHAT'S REAL causal flow | **PASS** |
| STORY fact/fiction boundary | **PASS** |
| STORY perspective framework | **PASS** |
| STORY regression protection | **PASS** |
| CONSEQUENCES certainty / causal boundary | **PASS** |
| PLACE / cultural boundaries | **PASS** |
| SR-01 through SR-16 source inspection | **PASS** |
| Master Edition / factual claims unchanged | **PASS** |
| Media provenance / rights | **PASS** |
| Distribution Candidate v0.1 | **PASS** |
| Atlas graph validation | **PASS** |
| Reader invariant validation | **PASS** |
| Active manifest / edition-state congruence | **PASS** |
| OROK scope | **PASS / OPTIONAL** |
| New media generation | **NONE** |

## Final QA decision

**AOC-001 PASSES PUBLICATION QA v0.5.**

No structural publication blocker remains from the v0.4 audit.

The edition may now advance to the **release human gate**. Publication itself remains blocked until explicit human release approval is given.

## Next foreground action

**AOC001-RELEASE-HUMAN-GATE** — review the final AOC-001 release candidate and explicitly approve or reject publication.

Do not regenerate media, rewrite the locked story, alter factual claims, redesign the approved reader or publish automatically as part of this QA result.
