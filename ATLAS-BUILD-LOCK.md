# Atlas of Consequences — Build Lock

**Purpose:** Prevent implementation drift. This is the highest-authority product contract for Atlas build behaviour. Implementation files, workflows, assets, manifests and hosted output must conform to this file. If another file conflicts with this lock, this lock wins until the conflict is explicitly resolved.

## Source-of-truth order
1. **ATLAS-BUILD-LOCK.md** — approved product behaviour, approved production style and current production truth.
2. **content/AOC-001/edition-manifest-v0.1.yaml** — edition slots and production requirements; must conform to this lock.
3. **Master edition + source register** — content/evidence truth.
4. **Code, workflows, generated assets and hosted builds** — implementation only; they do not redefine the product.

Implementation detail must never silently replace an approved experience or approved visual language.

## Locked product behaviour

### Core edition structure
`WHAT'S REAL → STORY → CONSEQUENCES → PLACE → SOURCES`

Fact and fiction must remain visibly distinguishable throughout.

### Constitutional rule
**Facts can change the fiction. Fiction must never quietly become fact.**

Real-world evidence may alter fictional world state, characters or consequences. Fiction must never be fed back upstream as evidence.

# AOC-001 VIDEO PRODUCTION STYLE — LOCKED

The user-supplied reference clips reviewed on 23 September 2026 establish the production language for AOC-001 video. They are **style references only**, not publication assets and not permission to copy another outlet's branding, graphics package, presenters or proprietary footage.

The desired overall standard is **current, premium vertical editorial media**. Atlas video must feel like a professionally produced 2026 short-form publication, not an AI slideshow, template explainer or dated broadcast package.

## Global visual language — applies to all three video assets
- Mobile-first vertical composition, primarily **9:16**.
- Full-frame moving imagery should dominate. Avoid shrinking the main footage into a small central window over a blurred duplicate background unless a specific shot genuinely requires it.
- Real camera movement, real environmental movement and purposeful cinematic/generated movement are preferred over fake zooms on still images.
- Editing should feel intentional and contemporary: clean cuts, motivated transitions, controlled pacing and strong visual continuity.
- Typography must be modern, restrained and editorial. Use fewer words on screen at once.
- Captions/lower-thirds should support the footage rather than becoming the footage.
- Motion graphics should be minimal, polished and functional.
- Sound design, ambience, music and/or narration should be treated as part of the edit, not an afterthought.
- Atlas branding should be present but restrained. The piece should feel like journalism/storytelling first, branding second.
- No visual treatment may blur the boundary between sourced reality and fiction.

## Explicit anti-drift / anti-style rules
Do **not** produce Atlas video that looks like:
- an AI-generated slideshow;
- a PowerPoint-style sequence of title cards;
- a 1990s/early-2000s TV graphics package;
- an amateur corporate explainer;
- large blocks of static text covering most of the screen;
- five still images with pan/zoom presented as if that were a finished film;
- generic stock-footage montage with no editorial relationship to the claims;
- excessive boxes, gradients, drop shadows, bevels, ticker-style decoration or ornamental motion graphics;
- synthetic "news" footage masquerading as documentary evidence;
- a copied version of the reference outlet's brand identity.

If an output begins to resemble any of the above, it fails the style gate even if the facts, codec and dimensions are technically correct.

# AOC-001 media architecture — LOCKED

AOC-001 has **three distinct video assets with different jobs and different visual languages**.

## 1. AOC001-REPORT-VIDEO — factual/news-report clip

### Editorial job
- A concise vertical factual report derived from the sourced `WHAT'S REAL` material.
- Covers the real chain: AI/data-centre infrastructure → electricity/grid → copper/material system → Calama/Chuquicamata place connection.
- Must preserve provenance, publication rights and factual limitations.
- Must be independently usable as the edition's factual/report video.
- Must never use generated footage as if it were documentary evidence of a real facility, mine, worker, witness or place.

### Locked style
Use the **first user reference clip** as the production-language benchmark:
- modern short-form editorial/news documentary;
- confident, quick but readable pacing;
- premium real-world footage filling the frame;
- occasional presenter/interview/witness material where appropriate and rights-cleared;
- clean contemporary subtitles/captions;
- restrained lower-thirds and source labels;
- visual evidence leads, graphics support;
- strong opening hook rather than a long branded title card;
- narration/interview audio, natural sound and music may carry continuity across cuts.

The report should feel comparable in production discipline to a credible contemporary digital newsroom/social documentary short, while remaining recognisably Atlas.

### Report-video style gate
A report candidate does not pass merely because it contains the correct facts. It must also:
- feel like one coherent piece of editorial video rather than five assembled panels;
- make the factual chain understandable without overloading the screen with prose;
- use real footage where real footage is claimed;
- preserve source/rights traceability;
- look credible enough that the viewer focuses on the story, not on the production method.

## 2. AOC001-STORY-PROMO — cinematic fiction teaser

### Editorial job
- A moving fictional teaser drawn from the approved story world: Daniela, Mauricio, Tomás, Emilia and Elena.
- Must be visibly identified as `STORY / FICTION` at the transition or opening in a way that cannot reasonably be missed.
- Must be independently usable as the story promotional clip.
- Real identifiable people must never be portrayed as the fictional family.
- Fiction must not be cut or styled so that it can be mistaken for witness/reportage footage.

### Locked style
Use the **second user reference clip** as the production-language benchmark:
- cinematic, human and emotionally led;
- character and environment over explanatory text;
- naturalistic movement and performance;
- strong sense of place, light, texture and atmosphere;
- restrained dialogue/text fragments rather than exposition;
- film-trailer/editorial-promo pacing rather than a news package;
- music, room tone, environmental sound and pauses may carry emotional weight;
- visual continuity should make the fictional family feel like people living inside a real world, not generated illustrations placed beside facts.

The story promo should feel closer to a polished dramatic teaser or prestige short-form campaign film than to an explainer.

### Story-promo style gate
A story promo fails if:
- it looks like stock people acting out a concept;
- generated shots visibly change character identity, age, clothing or location without narrative reason;
- it relies on text cards to explain the emotional stakes;
- it resembles reportage closely enough to confuse fiction with witness footage;
- it feels like disconnected AI clips instead of one cinematic world.

## 3. AOC001-OPEN-01 — hybrid edition trailer

### Editorial job
- The edition opens **straight into this video**.
- Target length is now **approximately 20–30 seconds**.
- This is an **editorial blend of selected moments from the verified report video and verified story promo**.
- Production relationship is locked as:

`AOC001-REPORT-VIDEO + AOC001-STORY-PROMO → AOC001-OPEN-01`

- It introduces both halves of the Atlas proposition: **the real change and the human consequence**.
- It must feel like a single deliberately edited trailer, not two videos pasted together.

### Locked hybrid style
The hybrid opening should begin in the visual authority of the factual report and gradually hand emotional gravity to the fictional story.

Indicative editorial movement:

`data centre / AI infrastructure → grid / energy → copper / extraction → Calama / Chuquicamata → explicit FACT-to-FICTION transition → fictional family / human consequence`

This remains an editorial arc, **not a five-shot recipe**. The final cut may use more shots, shorter inserts, sound bridges, match cuts, narration fragments, interview fragments, ambient sound and cinematic story moments as required.

The transition from fact to fiction is a signature Atlas moment and must be legible. It may be achieved through a clear `STORY / FICTION` mark, audio shift, edit transition, colour/texture change or another approved device, but it cannot rely on the audience guessing.

### Hybrid-opening quality target
- first seconds: immediate real-world hook;
- middle: accelerate the consequence chain without turning into an infographic;
- transition: visibly cross from sourced reality into fiction;
- final seconds: land on a strong human/story image that can function as the website hand-off frame;
- overall: premium, contemporary, cinematic-editorial and emotionally coherent.

Stills may be used as posters, references, keyframes, archival inserts or reduced-motion fallbacks, but they do not substitute for the approved moving report and story source videos.

# Video-to-site transition — LOCKED
- `AOC001-OPEN-01` begins immediately when the edition loads, subject to normal browser autoplay rules.
- It plays forward automatically once.
- It reaches and settles on its **exact final frame**.
- That final frame is the hand-off from autoplay to reader control; it is not a permanent frozen background.
- From that point onward, the **same hybrid opening video** remains behind the edition and becomes scroll-controlled.
- Scrolling forward scrubs the same timeline; reversing scroll reverses the visual progression.
- The reader moves through `WHAT'S REAL → STORY → CONSEQUENCES → PLACE → SOURCES` while the opening timeline moves to editorially selected moments.
- Reduced-motion fallback may use approved static keyframes.
- Do not replace this with a slideshow, crossfading standalone website backgrounds, a looping montage, or a separate post-opening background unless explicitly approved.

# Production approach
- Atlas is a publishing system, not merely a story generator.
- The Atlas website is the permanent/source-of-truth publication home.
- Social channels are distribution/discovery surfaces derived from the verified master edition.
- Build production assets, not duplicate mockups.
- "One action" means one meaningful production outcome, with immediate verification before moving on.
- **Technical completion is not production approval.** A rendered MP4 can still fail the editorial/style gate.

# Drift-control protocol — MANDATORY
Before any Atlas implementation or production change:
1. Read this file first.
2. State the single production outcome being attempted.
3. Check the change against every relevant locked rule here, including the video style rules.
4. If the proposed implementation changes a locked behaviour or style direction, **stop and surface the conflict** instead of reinterpreting it.
5. After the change, verify the actual artifact/output against this file.
6. For video, verification must include both **technical QA** and **editorial/style QA**.
7. Report `DONE / FAILED / NEXT` before beginning another production outcome.

No additional scrolling refinements, deployment work or decorative asset generation should be treated as progress on the opening until the required source video assets pass their production style gates.

# Current production truth — 23 September 2026

## Content
- AOC-001: **AI's Physical Hunger**.
- Master content, story and core fact/fiction structure are locked.

## Reference direction
- User supplied two reference clips on 23 September 2026.
- **Reference 1:** approved direction for the factual/report production language.
- **Reference 2:** approved direction for the cinematic story-promo production language.
- They are references for standard, pacing and language only; Atlas must not copy third-party branding or protected creative assets.

## Required video assets
- `AOC001-REPORT-VIDEO`: **v0.2 REBUILT / TECHNICAL QA PASSED / AWAITING HUMAN STYLE APPROVAL**.
  - Current candidate: `public/assets/aoc001-report-video-candidate-v0.2.mp4`
  - Technical verification: 22.2 seconds, 720×1280, 30 fps, H.264 video, stereo AAC audio at 48 kHz.
  - Presentation changes from v0.1: full-frame moving footage, faster editorial cuts, restrained caption/subtitle treatment, restrained Atlas branding, source labels, and a low CC0 atmospheric sound bed.
  - The approved factual chain is unchanged.
  - Real moving footage remains generic where generic; it is not relabelled as a specific AI facility or Chilean grid asset.
  - Real Calama and Chuquicamata place imagery is retained for the location hand-off.
  - Visual QA contact sheet: `public/assets/aoc001-report-video-candidate-v0.2-review.jpg`.
  - Technical probe record: `public/assets/aoc001-report-video-candidate-v0.2-probe.txt`.
  - **Do not promote v0.2 to production-approved status until the user watches it and explicitly approves the style.**
- `AOC001-REPORT-VIDEO v0.1`: retained as **STRUCTURAL PROTOTYPE / NOT PRODUCTION-QUALITY**.
- `AOC001-STORY-PROMO`: **NOT YET PRODUCED to the locked cinematic reference standard**.
- `AOC001-OPEN-01`: **NOT YET PRODUCED as the approved 20–30 second hybrid of the verified report and story clips**.

## Existing opening prototype artifact
- `public/assets/aoc001-opening.mp4` exists in the repository.
- It was assembled from still-image source assets with simulated camera movement.
- **Status: PROTOTYPE / NON-PRODUCTION / DOES NOT SATISFY AOC001-OPEN-01.**
- Its existence must not be reported as completion of the approved opening trailer.
- The existing scroll/video-control code may be reusable later, but it is not evidence that the opening media is complete.

# Recovery / production sequence — LOCKED
1. Human-review and either approve or revise `AOC001-REPORT-VIDEO v0.2` against the first-reference modern editorial/news standard.
2. Only after report approval, produce and verify `AOC001-STORY-PROMO` to the second-reference cinematic human-story standard.
3. Edit selected moments from those two verified clips into the **20–30 second** `AOC001-OPEN-01` hybrid trailer.
4. Human-review and approve the hybrid trailer.
5. Replace the old prototype opening MP4 with the verified hybrid trailer.
6. Reconnect/verify autoplay → exact final frame → scroll hand-off.
7. Only then continue reader polish, section imagery and distribution derivatives.

# Next single production outcome
**Human visual/style review of `AOC001-REPORT-VIDEO v0.2`.**

Do not begin the story promo, hybrid opening or further website polish until v0.2 is explicitly approved or specific revisions are requested.
