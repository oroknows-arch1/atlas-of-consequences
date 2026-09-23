# Atlas of Consequences — Build Lock

**Purpose:** Prevent implementation drift. This file records approved product behaviour that must be checked before any Atlas build change.

## Locked product behaviour

### Opening experience
- The edition opens **straight into a video clip**.
- The opening clip begins immediately when the edition loads.
- The opening visual sequence is:
  `data centre → grid / energy → copper / mining → Calama / Chuquicamata → fictional human / family moment`
- The real-world beats use sourced material with provenance and usable publication rights.
- The human/family beat is generated fiction and must remain visibly within the STORY / FICTION boundary.
- The opening is **not** a slideshow or a sequence of independent website backgrounds.
- The sourced/generated assets are production inputs used to create the opening video.

### Video-to-site transition
- The opening video plays through once.
- The clip must settle on its **exact final frame**.
- That exact final frame remains visible after motion stops.
- The final frame becomes the continuing visual background of the edition.
- The reader then moves into the Atlas website over that same visual world.
- Do not replace this behaviour with crossfading standalone images, a looping slideshow, or a separate post-video background unless explicitly approved.

### Edition structure
The core reader structure remains:

`WHAT'S REAL → STORY → CONSEQUENCES → PLACE → SOURCES`

Fact and fiction must remain visibly distinguishable throughout.

### Constitutional rule
**Facts can change the fiction. Fiction must never quietly become fact.**

Real-world evidence may alter fictional world state, characters or consequences. Fiction must never be fed back upstream as evidence.

### Production approach
- Atlas is a publishing system, not merely a story generator.
- The Atlas website is the permanent/source-of-truth publication home.
- Social channels are distribution/discovery surfaces derived from the master edition.
- Production assets should go directly into the real edition where practical; avoid duplicate mockup rounds that do not improve the decision.
- Batch tightly related work where possible. "One action" means one meaningful production outcome, not one microscopic sub-step.

## Drift-control rule
Before implementing any Atlas change:
1. Read this file.
2. Check the proposed change against every relevant locked behaviour above.
3. If implementation would alter a locked behaviour, **stop and surface the conflict instead of silently reinterpreting the experience**.
4. After implementation, verify the result against this file, not merely whether the code runs.

**Implementation detail must never silently replace an approved experience.**

## Current build state — 23 September 2026
- AOC-001 is the current prototype edition: **AI's Physical Hunger**.
- Five opening production assets have been identified and rights/provenance recorded.
- The current hosted reader incorrectly wires those assets as crossfading website images.
- That wiring is **not the approved final behaviour**.
- The approved correction is to use those assets as source material for the opening video, then preserve the video's exact final frame as the edition background.

## Next meaningful build outcome
Correct AOC-001 so the hosted edition follows the locked opening experience:

`video starts immediately → video plays through → exact final frame holds → that same frame continues behind the reader experience`

Do not create another separate slideshow or mockup interpretation of the five source assets.