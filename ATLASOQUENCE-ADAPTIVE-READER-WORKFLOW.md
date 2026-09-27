# Atlasoquence Adaptive Reader — Workflow Lock v0.1

**Status:** ACTIVE TEST CONTRACT · v0.2  
**Scope:** Atlasoquence reader/workflow experiments beginning with AOC-001  
**Purpose:** Prevent architecture drift while testing the proposed replacement for the legacy linear Atlas reader.

## 1. What we are testing

Atlasoquence is testing whether the existing linear edition reader should be replaced by an adaptive reader.

This is **not** a redesign of one section of the current reader.

The test asks whether an edition should open as an AI-generated/adaptive shell that lets the reader choose a **Perspective** and enter the edition through that route.

AOC-001 is the benchmark edition. **Minerals + Resources** is the first perspective being used to prove or disprove this reader model.

## 2. Legacy reader vs proposed reader

### Legacy reader

The current production reader is a steady vertical edition:

WHAT'S REAL → STORY → CONSEQUENCES → PLACE → SOURCES

It also provides direct section navigation.

This reader remains the control/baseline while the new model is tested.

### Proposed adaptive reader

The proposed reader opens into an edition shell rather than immediately forcing one continuous editorial path.

The shell should:
1. establish the edition identity and central world change;
2. expose a **Perspectives menu** immediately after the edition entrance;
3. when routing context exists, visually highlight the perspective connected to the incoming marketing signal without auto-entering it;
4. let the user choose where to enter;
5. generate/render a coherent reading route for that perspective;
6. preserve access to evidence, place, story and consequences as appropriate to that route;
7. let the reader move between perspectives without pretending each perspective is a separate edition.

The shell may be AI-generated/adaptive, but factual evidence, editorial boundaries and publication governance remain deterministic and inspectable.

## 3. Perspective rule

A **Perspective is an entry route through the edition. It is not a subsection of WHAT'S REAL.**

Therefore:

- Minerals + Resources MUST NOT be inserted into WHAT'S REAL as a gallery, chapter or visual subsection.
- Perspective-specific imagery, narrative sequencing and evidence belong to that perspective route.
- WHAT'S REAL remains the factual substrate of the edition, not a container for perspectives.
- A perspective may draw from WHAT'S REAL, STORY, CONSEQUENCES, PLACE and SOURCES without changing the factual status of any material.
- Multiple perspectives may expose different parts of the same evidence graph.

## 4. AOC-001 benchmark

Edition: **AOC-001 — AI's Physical Hunger**

Core factual chain:

AI/data-centre expansion → electricity/water → grid/infrastructure → copper/material demand → Antofagasta copper economy → mining opportunity/pressure → human consequences.

Boundary:

AI/data-centre growth can be treated as additional pressure inside a much larger copper/electrification system. Atlasoquence must not claim that AI caused an existing mine expansion, a particular job or a fictional household event.

The fictional Daniela/Mauricio household remains STORY. Fiction must never quietly become evidence.

## 5. First test perspective: Minerals + Resources

Minerals + Resources is a **perspective route** through AOC-001.

Its visual system currently has six approved composed assets:

1. data-centre aisle
2. copper cables
3. South America night/orbit
4. Chile/copper orbit
5. Antofagasta coast/Atacama
6. Chuquicamata mine at blue hour

These assets are evidence-linked editorial scenes for the perspective experience. They are not a six-image insert for the legacy reader.

The target is the previously approved V3/reference-board quality and interaction direction.

## 6. Reader experience hypothesis

The working hypothesis is:

**Marketing signal → edition homepage/shell → Perspectives menu → originating perspective highlighted → reader chooses → coherent route through evidence/story/place/consequences → other perspectives / evidence inspection**

The marketing source does **not** bypass the edition entrance or automatically open a perspective. Every reader enters through the edition homepage/shell and encounters the Perspectives menu.

A distributed signal may carry an **edition ID + perspective ID**. The perspective ID may control only the initial visual highlight/focus of the relevant perspective in the menu. It must not automatically navigate the reader, alter evidence, generate different facts or hide the other available perspectives.

The highlight communicates provenance: **this is the perspective connected to what brought you here.** It is not an algorithmic recommendation or instruction.

The reader retains agency to select that highlighted perspective or choose another available perspective. The presence of the other perspectives at arrival is intentional: it immediately reveals that the world change can be understood from more than one position.

The reader should feel like one living edition with multiple legitimate ways into it, not a webpage containing a stack of conventional sections and not a collection of disconnected mini-articles.

The interface must remain mobile-first.

### Edition geographic home rule

The opening film is a temporary introduction, not the persistent reader background. When the film completes or is skipped, it gives way to the edition's geographic Atlas hero.

The geographic hero should locate the edition in the world before the reader chooses a perspective. For AOC-001 this is South America/Chile context. Future editions should use the geography relevant to that edition (for example, an African edition may resolve to its relevant African region).

The stable entrance hierarchy is:

**Atlasoquence → place in the world → edition/world change → Perspectives → chosen route**

Do not carry the opening film forward as a scroll-scrub background in the adaptive reader. Geographic context owns the persistent edition-home state.


### Perspective transition invariant

A Perspective is a reader-chosen route, not one segment in an endlessly scrolling stack.

The standard transition is:

**Perspective → complete route → conscious next choice → next Perspective**

Only the Perspective the reader explicitly selects should be exposed as the active reading route. Reaching its completion state must not allow ordinary continued scrolling to reveal another Perspective. The completion state returns agency to the reader through the Perspectives menu; another route appears only after a conscious selection.

This is an interaction boundary, not merely end-of-route wording. Implementations may keep routes in one document or runtime for efficiency, but inactive Perspectives must remain outside the active reading flow.

## 7. Architecture separation during testing

Do not destroy the legacy reader to run this experiment.

Until the adaptive model is explicitly approved as the replacement:

- keep the existing reader as the control;
- build the adaptive reader as a separately addressable experimental surface;
- reuse canonical AOC-001 content/evidence where possible;
- do not duplicate factual truth into an independent uncontrolled content store;
- do not merge experimental perspective UI into the legacy WHAT'S REAL flow.

A new repository is **not the default**.

Prefer modifying the existing `oroknows-arch1/atlas-of-consequences` repository with a clean experimental route/directory/branch because both readers use the same edition, evidence and assets.

Create a separate repository only if the experiment proves it requires an independently deployable product/runtime, materially different security boundary, or architecture that cannot remain cleanly isolated in the Atlas repository. That decision requires explicit approval.

## 8. Dynamic edition-generation architecture

AOC-001 is the benchmark used to prove the Atlasoquence machinery. It is **not** the fixed template that future editions must imitate.

Atlasoquence editions are generated from the world change and evidence supplied upstream by EMRADAR. The publication system must derive the edition's useful structure from that material rather than force every subject into AOC-001's perspective count, geography, scene sequence or visual set.

The generation chain is:

**EMRADAR world change → evidence graph → geographic context → viable Perspectives → perspective routes → scene meanings → contextual visual assets → evidence/editorial verification → adaptive edition → distribution signals → reader arrival context → reader-chosen route**

### Invariants

These remain stable across editions:

- evidence provenance and source traceability;
- fact/fiction boundaries;
- geographic and cultural integrity;
- human authority over consequential publication decisions;
- reader agency at the Perspectives menu;
- marketing may highlight provenance but must not determine truth or auto-select a route;
- generated presentation may change form but not factual status;
- visual assets must not manufacture documentary evidence;
- route elasticity and the lightest safe execution path;
- Atlasoquence's core orientation: locate the change, establish what is real, follow where it goes, map what follows.

### Edition-generated variables

These are allowed—and expected—to change according to the evidence:

- geographic hero/location;
- number and names of Perspectives;
- perspective ordering;
- scene count and sequence;
- contextual visual assets;
- visual emphasis within the Atlasoquence aesthetic;
- which evidence nodes appear in each route;
- connections between Perspectives;
- distribution signals and the perspective provenance carried back from them.

Six Perspectives are currently appropriate to AOC-001. **Six is not a global requirement.**

### Dynamic visual-asset rule

Edition visuals are part of the information system, not decoration added after writing.

Each scene visual must be derived from:

**scene meaning/evidence → geographic/cultural context → factual boundary → Atlasoquence visual language → composed asset → visual/evidence QA**

A missing visual asset triggers this generation pipeline. It must not trigger arbitrary reuse of the nearest existing image, generic CSS/SVG illustration, unrelated stock imagery or an ungrounded aesthetic substitute.

Generated editorial imagery may communicate systems, atmosphere, geography and consequence, but it must not visually assert that a specific undocumented event, person, facility or causal relationship is factual. Where the distinction could reasonably be misunderstood, the presentation must make the editorial/illustrative status clear.

The visual system should make each edition feel alive and specific to the world change while remaining recognisably Atlasoquence.

### Adaptive conveyance, evidence states and interface lightness

Atlasoquence may adapt how verified information is conveyed without adapting what is true.

The reader may influence route, depth, presentation and supported medium. Every adaptation must resolve back to the same governed edition evidence graph. The reader can influence presentation and route; the reader cannot influence reality.

Material information must be able to retain an explicit state: KNOWN, UNCERTAIN, CONTESTED, UNKNOWN, UNAVAILABLE, or FICTION / EDITORIAL INTERPRETATION. Missing information is not automatically a publication blocker. It can describe where present knowledge ends. UNKNOWN or UNAVAILABLE must never trigger invented completion, synthetic certainty or unsupported visual specificity.

Complexity belongs in the system, not with the reader. Increased adaptive capability must not produce a control-heavy interface or require the reader to understand Atlasoquence architecture.

The interface target is:

**maximum intelligence underneath → minimum cognitive load above**

Use progressive disclosure. At any moment, expose only the choices useful to the reader's current position. Prefer natural actions such as choose a Perspective, continue, go deeper, inspect evidence or explore a connected Perspective over technical modes, settings panels or dense control surfaces.

Unknown or incomplete knowledge should be communicated in ordinary editorial language, such as what is not known yet, rather than exposing internal system terminology unless deeper inspection is requested.

The governed edition must remain separable from today's rendering medium so future displays, spatial interfaces, audio systems, wearables or other peripheral devices can convey the same evidence, provenance and editorial boundaries without rebuilding the truth layer.

#### Device-agnostic delivery invariant

Atlasoquence is device-agnostic and capability-adaptive. No edition may depend on a particular phone brand, operating system, browser vendor, screen shape, input method or proprietary device feature to remain understandable.

The same governed edition must remain usable wherever Atlasoquence can be viewed. Establish a universal readable/navigable baseline first, then progressively enhance it according to capabilities actually available on the viewing device.

Touch, mouse/trackpad, keyboard, assistive technology, reduced-motion preferences, different viewport sizes/orientations and future interaction hardware must not create different factual editions.

Motion, video, audio, hover, haptics, spatial presentation and other richer capabilities are enhancements. If unavailable, unsupported or intentionally disabled, the evidence, meaning, provenance, navigation and reader agency must survive through an appropriate fallback.

Test representative capability classes rather than designing around a single handset.

### Benchmark rule

AOC-001 should be used to answer:

**Does the Atlasoquence generation system reliably turn a verified world change into a coherent, evidence-backed, geographically grounded, visually contextual and navigable edition?**

Success means the machinery can generate a materially different future edition from different EMRADAR evidence while preserving the invariants above.

Do not encode AOC-001's incidental characteristics as permanent product rules.

## 9. Workflow under test

For each edition:

1. Establish the world change.
2. Lock the factual evidence graph.
3. Identify useful perspectives from that graph.
4. Decide which perspectives deserve reader routes.
5. Generate/compose the perspective experience from approved evidence, story and visual assets.
6. Verify factual boundaries and source traceability.
7. Render the adaptive shell and perspective menu.
8. Test the complete phone experience.
9. Compare it with the legacy reader.
10. Keep, revise or reject the new reader architecture based on observed reading quality.

This is a workflow experiment as well as a UI experiment.

## 10. Governance

Existing Atlasoquence rules remain active:

- Facts can change the fiction. Fiction must never quietly become fact.
- Evidence first.
- Human authority remains over consequential publication decisions.
- Generated UI may change presentation, not factual status.
- Source provenance must survive adaptive rendering.
- Route elasticity applies: use the lightest execution path that can safely complete the node.
- Chat is the default working environment.
- Work is used only for operations that strictly cannot be completed in Chat.
- When a Work-only node finishes, return immediately to Chat.
- Do not expand scope simply because a tool or execution environment is available.

## 11. Anti-drift checks

Before changing the reader, answer these questions:

1. Am I modifying the legacy reader or the adaptive-reader experiment?
2. Is this item a perspective, factual evidence, story, consequence, place context or source?
3. Am I accidentally placing a Perspective inside WHAT'S REAL?
4. Does this change preserve the edition as the parent object?
5. Does every incoming marketing route still land at the edition homepage/shell before perspective selection?
6. If an incoming perspective is known, is it highlighted as provenance rather than auto-opened or presented as a recommendation?
7. Are all other available perspectives still visible so the reader can see the wider edition?
8. Does the Perspectives menu remain the reader's choice of entry route?
9. Does generated presentation preserve evidence provenance and fact/fiction boundaries?
10. Am I testing the whole proposed reader model rather than merely decorating the old linear reader?
11. Can this be isolated inside the existing repository?
12. Has the user explicitly approved replacing the legacy reader? If not, keep the control intact.

If any answer indicates drift, stop the implementation and return to this contract.

## 12. Current correction

The deployment that inserted the six Minerals + Resources assets into WHAT'S REAL is a **failed architecture test**, not the target implementation.

Do not continue polishing that insertion.

Next implementation node:

**Restore the legacy reader/control, then create an isolated adaptive-reader test surface for AOC-001 whose opening shell presents Perspectives and whose first working route is Minerals + Resources.**

That test surface is what should be compared against the legacy reader before any replacement decision is made.
