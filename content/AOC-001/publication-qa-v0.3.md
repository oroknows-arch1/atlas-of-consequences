# AOC-001 — Publication QA v0.3

**Edition:** AOC-001 — *AI's Physical Hunger*  
**QA date:** 2026-09-25  
**QA scope:** final publication rerun after repair of the Atlas orchestration contract and explicit resolution of OROK companion release scope.  
**Verdict:** **PASS — READY FOR HUMAN RELEASE APPROVAL**

AOC-001 now passes the Atlas publication gate. This QA does **not** publish the edition and does **not** substitute for the release human gate.

No new Runway generation was required. **Runway credits used by this QA: 0.**

## What was rechecked

### 1. Reader and publication-content regression

Publication QA v0.2 had already passed the completed reader, locked Master Edition, fact/fiction boundary, consequence certainty treatment, PLACE treatment, SR-01 through SR-16 evidence surface, reduced-motion implementation, factual-media provenance and Distribution Candidate v0.1.

A commit comparison from the v0.2 QA record (`8dd126d5239da0d5e21d2ade8180c35f48786579`) to the final pre-gate state (`d193d5b669a85af6ccdbdc8b07fae50d3289350b`) shows no changes to:

- `public/index.html`;
- `public/reader-publication-treatments.css`;
- `public/reader-publication-treatments.js`;
- `content/AOC-001/master-edition-v0.1.md`;
- `content/AOC-001/sources/publication-source-register-v0.1.md`;
- `content/AOC-001/distribution/distribution-candidate-v0.1.md`;
- approved factual or fictional media assets.

Changes since v0.2 are confined to the production graph, validator, edition/manifest state and OROK scope records. Therefore the publication-content passes established by v0.2 have not been invalidated.

### 2. Atlas orchestration contract

**PASS.**

The active production graph now encodes the approved reader route:

`factual_media_human_gate + story_boundary_gate + source_register -> reader_build`

The historical hybrid-opening nodes remain explicitly retired and non-blocking. The validator now checks the approved factual-film → final-frame handoff → reader architecture rather than requiring the rejected hybrid route.

GitHub Actions **Validate Atlas worker graph run #49** completed successfully on commit `d193d5b669a85af6ccdbdc8b07fae50d3289350b`.

### 3. OROK companion scope

**PASS / NON-BLOCKING.**

Human authority resolved the scope on 2026-09-25:

- AOC-001 does not require an OROK companion for release;
- OROK is optional downstream enrichment;
- absence of an OROK companion does not fail an Atlas edition unless a future edition explicitly opts into one before production;
- no OROK content is required merely to prove this prototype pipeline.

Decision record: `content/AOC-001/orok/AOC001-OROK-SCOPE-DECISION.md`.

### 4. Fact / fiction and causal boundaries

**PASS — unchanged from v0.2.**

The reader and distribution package continue to preserve the constitutional rule:

**Facts can change the fiction. Fiction must never quietly become fact.**

The prohibited shortcut remains prohibited:

**AI boom → mine expands → Mauricio gets promoted.**

The story promo remains a separate **STORY / FICTION** derivative and is not reintroduced into the automatic factual reader opening.

### 5. Distribution package

**PASS — unchanged from v0.2.**

Distribution Candidate v0.1 still contains the separate factual and fictional branches, captions, carousel/still copy, poster bindings, source anchors, causal limitations and permanent Atlas destination.

No new paid/generated media is required for this release gate.

### 6. Deployment/runtime note

The reader/publication files themselves have not changed since the production reader state audited in v0.2. The final structural repairs affect repository orchestration and release-state records, not runtime reader code or media.

This QA environment could not independently reopen the Render workspace control plane without a workspace selection, so it does not claim a new Render control-plane check for the final state. This is **not a publication-content blocker** because the deployable reader bytes are unchanged from the already-audited live reader. The release human gate may perform a final phone spot-check before publication if desired.

## Final gate table

| Gate | Result |
|---|---|
| Complete locked Master Edition in reader | **PASS** |
| Approved factual opening → reader architecture | **PASS** |
| Reader visual/interaction treatment preserved | **PASS** |
| Reduced-motion and fail-open implementation | **PASS** |
| Fact / fiction separation | **PASS** |
| Consequence certainty / prohibited shortcut | **PASS** |
| PLACE and cultural sourcing boundaries | **PASS** |
| SR-01 through SR-16 evidence inspection | **PASS** |
| Factual media provenance / rights record | **PASS** |
| Distribution package completeness | **PASS** |
| Distribution claim discipline | **PASS** |
| Permanent Atlas return path | **PASS** |
| Atlas graph / validator contract | **PASS** |
| OROK release scope | **PASS / OPTIONAL** |
| New media generation required | **NO** |
| Runway credits required | **0** |

## Final QA decision

**AOC-001 PASSES PUBLICATION QA.**

There is no remaining structural publication blocker identified by this test.

The edition may advance to the **release human gate**. Publication itself remains blocked until that human approval is explicitly given.

## Next foreground action

**AOC001-RELEASE-HUMAN-GATE** — review the final release candidate and explicitly approve or reject publication.

Do not regenerate media, rewrite the locked story, redesign the approved reader, or publish automatically as part of this QA result.
