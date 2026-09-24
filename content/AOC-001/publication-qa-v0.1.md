# AOC-001 — Publication QA v0.1

**Edition:** AOC-001 — *AI's Physical Hunger*  
**QA date:** 2026-09-25  
**QA scope:** complete publication readiness across the approved mobile reader, locked master content, evidence, fact/fiction boundaries, place treatment, source inspection, distribution package and release-state consistency.  
**Verdict:** **FAIL — NOT RELEASE READY**

The approved visual/interaction system is preserved. This failure is about publication completeness and contract drift, not the reader treatment the human gate approved.

## Evidence audited

- `public/index.html`
- approved reader record: `content/AOC-001/media/AOC001-READER-APPROVAL.md`
- locked master: `content/AOC-001/master-edition-v0.1.md`
- source register: `content/AOC-001/sources/publication-source-register-v0.1.md`
- edition manifest: `content/AOC-001/edition-manifest-v0.1.yaml`
- distribution directory: `content/AOC-001/distribution/`
- live edition state: `atlas/editions/AOC-001.json`

## Publication gate results

| Gate | Result | QA finding |
|---|---|---|
| Approved opening / reader visual behaviour | PASS | The approved factual-film → final-frame hold → full-screen scroll-scrub reader treatment remains the accepted visual baseline. Story promo is correctly excluded from automatic opening playback. |
| Reader sequence | PASS | The live shell preserves WHAT'S REAL → STORY → CONSEQUENCES → PLACE → SOURCES. |
| Full master-edition content present in reader | **FAIL** | `public/index.html` contains short summary paragraphs only. It does not publish the locked WHAT'S REAL report, the full Daniela/Mauricio/Tomás/Emilia/Elena story, the complete consequence analysis, the full PLACE material or the full source surface from `master-edition-v0.1.md`. |
| Factual claim visibility / key numbers | **FAIL** | The live WHAT'S REAL surface omits material locked claims and callouts including 415 TWh, ~1.5%, Antofagasta 58%, Chuquicamata ~15 km north of Calama, current operation/workforce context and their limitations. |
| Fact / fiction boundary in long-form reader | **FAIL** | The shell labels STORY / FICTION, but the complete fiction disclosure and full story are not present. Publication QA cannot certify a fast-scrolling reader against material that has not yet been integrated. |
| Consequence certainty model | **FAIL** | The live CONSEQUENCES section is a single summary paragraph. It does not render the three required certainty layers — documented global mechanism, documented place connection, fictional human exploration — and does not surface the prohibited shortcut `AI boom → mine expands → Mauricio gets promoted` as a boundary. |
| PLACE publication treatment | **FAIL** | The live PLACE section is only a short paragraph. It does not yet provide the required map/location treatment, city facts, lived-city context, relocation/heritage context or Indigenous sourcing boundary from the locked edition/manifest. |
| SOURCES inspection surface | **FAIL** | The live page links to the asset register and publication source register but does not provide the required scannable source cards, direct source links, source roles and limitations. The evidence register itself is complete; its reader presentation is not. |
| Evidence / causal discipline | PASS at source-of-truth level | The publication source register explicitly wires material claims and preserves `Connection may be shown. Causation requires evidence.` No direct AI → individual promotion claim is supported. This must survive reader integration. |
| Real-world media provenance | PASS for approved factual film | The approved factual film has a source/rights register and was human-approved. Fiction media remains separately labelled and is not used as evidence. |
| Mobile opening failure safety | PASS in approved source | `Skip` and opening media-error handling reveal the reader. Muted autoplay fallback is present. |
| Reduced-motion / static fallback | **FAIL** | The current code removes transitions for `prefers-reduced-motion`, but still uses the moving/scrubbed video layer. The manifest requires approved static keyframes with normal section transitions. No poster/static fallback is wired to the live video element. |
| Distribution package | **FAIL** | `content/AOC-001/distribution/` contains only its README. Required derivatives — vertical cuts, still/carousel assets, captions, headlines/descriptions, thumbnails/poster frames and links back to the permanent edition — have not been assembled into a candidate package. |
| OROK companion requirement | **FAIL / unresolved contract** | The manifest still marks an OROK companion as required for the complete v0.1 publishing package, but no completed companion package is bound into release state. This must either be produced or the requirement must be explicitly revised by human authority before release. |
| Manifest / live-state congruence | **FAIL** | `edition-manifest-v0.1.yaml` still describes the old required 10–15 second hybrid opening, Report/Story entry buttons, empty required asset slots and earlier pending pipeline states. That no longer matches the human-approved live reader. This drift could cause future workers to rebuild rejected behaviour. |
| Durable production dependency | WARNING | The optional Atlas soundtrack is still referenced through the temporary `atlas-aoc001-media-bridge` service. The silent experience remains complete, so this is not the primary release blocker, but a permanent release should not depend on a temporary bridge for its approved sonic layer. |

## Release blockers

### B1 — Complete locked content is not in the live reader

This is the primary blocker. The current reader proves the interaction and visual language, but it is still a publication skeleton. The locked master edition is the source of truth and must be integrated without rewriting or shortening it into summaries.

**Responsible node:** `reader_build`

### B2 — Required publication treatments are missing

During master integration, the reader must implement:

- key factual number callouts and limitations;
- full fiction disclosure before the story begins;
- full STORY text with scene breaks;
- three-level consequence certainty treatment and prohibited-shortcut boundary;
- PLACE map/location and local-context treatment;
- inspectable SOURCES cards with direct links, roles and limitations;
- reduced-motion/static fallback.

**Responsible node:** `reader_build`

### B3 — Distribution candidate does not exist

The distribution directory defines the rules but does not contain the required package.

**Responsible node:** `distribution_pack`

### B4 — Edition manifest is stale

The production contract must be reconciled to the approved reader so later agents cannot reintroduce the rejected auto-playing story promo, obsolete entry interface or empty/pending states.

**Responsible nodes:** `reader_build` / `atlas_orchestrator`

### B5 — Complete-package OROK requirement unresolved

The manifest still calls this required for complete v0.1. Produce it or explicitly revise that requirement before the release human gate.

## What remains approved

Do **not** reopen these during remediation unless a new defect is discovered:

- full-screen factual opening;
- no automatic story-promo playback;
- final-frame hold into reader;
- full-bleed background;
- reader brightness treatment (`0.67` baseline);
- scroll-driven scrub behaviour;
- Tap for sound / Skip / fail-open access;
- separate approved fictional story promo asset;
- source-of-truth story and evidence boundaries.

## QA disposition

- `publication_qa`: **FAILED / BLOCKED**
- `release_human_gate`: remains **BLOCKED**
- visual reader approval: **PRESERVED**
- next foreground node: **`reader_build`**

## Next single action

Integrate the **complete locked Master Edition v0.1** into the already-approved mobile reader treatment. Do not redesign the approved visual system and do not rewrite the locked story. Once the complete reader exists, the distribution candidate is assembled and the manifest is reconciled, rerun Publication QA before asking for release approval.
