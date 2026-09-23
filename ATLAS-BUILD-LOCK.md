# Atlas of Consequences — Build Lock

**Purpose:** Prevent implementation drift. This is the highest-authority product contract for Atlas build behaviour. Implementation files, workflows, assets, manifests and hosted output must conform to this file. If another file conflicts with this lock, this lock wins until the conflict is explicitly resolved.

## Source-of-truth order
1. **ATLAS-BUILD-LOCK.md** — approved product behaviour and current production truth.
2. **content/AOC-001/edition-manifest-v0.1.yaml** — edition slots and production requirements; must conform to this lock.
3. **Master edition + source register** — content/evidence truth.
4. **Code, workflows, generated assets and hosted builds** — implementation only; they do not redefine the product.

Implementation detail must never silently replace an approved experience.

## Locked product behaviour

### Core edition structure
`WHAT'S REAL → STORY → CONSEQUENCES → PLACE → SOURCES`

Fact and fiction must remain visibly distinguishable throughout.

### Constitutional rule
**Facts can change the fiction. Fiction must never quietly become fact.**

Real-world evidence may alter fictional world state, characters or consequences. Fiction must never be fed back upstream as evidence.

## AOC-001 media architecture — LOCKED

AOC-001 has **three distinct video assets with different jobs**.

### 1. AOC001-REPORT-VIDEO — factual/news-report clip
- Real-world, evidence-led moving footage and/or clearly explanatory factual media.
- Covers the real chain: AI/data-centre infrastructure → electricity/grid → copper/material system → Calama/Chuquicamata place connection.
- Must preserve provenance, publication rights and factual limitations.
- Must be independently usable as the `WHAT'S REAL` report clip.
- Must never use generated footage as if it were documentary evidence of a real facility, mine, worker or place.

### 2. AOC001-STORY-PROMO — cinematic fiction teaser
- Moving fictional material drawn from the approved story world: Daniela, Mauricio, Tomás, Emilia and Elena.
- Must be visibly identified as `STORY / FICTION`.
- Must be independently usable as the story promotional clip.
- Real identifiable people must never be portrayed as the fictional family.
- Fiction must not be cut or styled so that it can be mistaken for witness/reportage footage.

### 3. AOC001-OPEN-01 — hybrid edition trailer
- The edition opens **straight into this video**.
- Target length: approximately **10–15 seconds**.
- This asset is an **editorial blend of selected moments from AOC001-REPORT-VIDEO and AOC001-STORY-PROMO**.
- Production relationship is locked as:

`AOC001-REPORT-VIDEO + AOC001-STORY-PROMO → AOC001-OPEN-01`

- It introduces the whole edition before conventional navigation appears.
- The five-beat arc remains useful as editorial sequencing:

`data centre → grid / energy → copper / mining → Calama / Chuquicamata → fictional human / family moment`

- **That five-beat arc is not a licence to manufacture the opening from five still images.** It describes the narrative movement of the hybrid trailer.
- Stills may be used as posters, references, keyframes or reduced-motion fallbacks, but they do not substitute for the approved moving report and story footage.
- The transition from factual material into fictional material must remain legible; the fictional human beat must not look like reportage.

## Video-to-site transition — LOCKED
- AOC001-OPEN-01 begins immediately when the edition loads, subject to normal browser autoplay rules.
- It plays forward automatically once.
- It reaches and settles on its **exact final frame**.
- That final frame is the hand-off from autoplay to reader control; it is not a permanent frozen background.
- From that point onward, the **same hybrid opening video** remains behind the edition and becomes scroll-controlled.
- Scrolling forward scrubs the same timeline; reversing scroll reverses the visual progression.
- The reader moves through `WHAT'S REAL → STORY → CONSEQUENCES → PLACE → SOURCES` while the opening timeline moves to editorially selected moments.
- Reduced-motion fallback may use approved static keyframes.
- Do not replace this with a slideshow, crossfading standalone website backgrounds, a looping montage, or a separate post-opening background unless explicitly approved.

## Production approach
- Atlas is a publishing system, not merely a story generator.
- The Atlas website is the permanent/source-of-truth publication home.
- Social channels are distribution/discovery surfaces derived from the verified master edition.
- Build production assets, not duplicate mockups.
- "One action" means one meaningful production outcome, with immediate verification before moving on.

## Drift-control protocol — MANDATORY
Before any Atlas implementation change:
1. Read this file first.
2. State the single production outcome being attempted.
3. Check the change against every relevant locked rule here.
4. If the proposed implementation changes a locked behaviour, **stop and surface the conflict** instead of reinterpreting it.
5. After the change, verify the actual artifact/output against this file.
6. Report `DONE / FAILED / NEXT` before beginning another production outcome.

No additional visual direction, scrolling refinements, deployment work or decorative asset generation should be treated as progress on the opening until the required source video assets exist.

## Current production truth — 23 September 2026
### Content
- AOC-001: **AI's Physical Hunger**.
- Master content, story and core fact/fiction structure are locked.

### Required video assets
- `AOC001-REPORT-VIDEO`: **NOT YET PRODUCED as the approved moving factual/news-report clip**.
- `AOC001-STORY-PROMO`: **NOT YET PRODUCED as the approved moving cinematic fiction teaser**.
- `AOC001-OPEN-01`: **NOT YET PRODUCED as the approved hybrid of those two clips**.

### Existing prototype artifact
- `public/assets/aoc001-opening.mp4` exists in the repository.
- It was assembled from still-image source assets with simulated camera movement.
- **Status: PROTOTYPE / NON-PRODUCTION / DOES NOT SATISFY AOC001-OPEN-01.**
- Its existence must not be reported as completion of the approved opening trailer.
- The existing scroll/video-control code may be reusable later, but it is not evidence that the opening media is complete.

## Recovery sequence
Do not continue adding graphics around the missing core media. Recover in this order:

1. Produce and verify `AOC001-REPORT-VIDEO`.
2. Produce and verify `AOC001-STORY-PROMO`.
3. Edit selected moments from those two verified clips into `AOC001-OPEN-01`.
4. Replace the prototype opening MP4 with the verified hybrid trailer.
5. Reconnect/verify autoplay → exact final frame → scroll hand-off.
6. Only then continue reader polish, section imagery and distribution derivatives.

## Next single production outcome
**Produce `AOC001-REPORT-VIDEO` as a real moving factual/news-report clip.**

Until that passes review, do not spend the foreground action on more opening graphics, scroll polish, alternative deployment paths, or a replacement hybrid trailer.