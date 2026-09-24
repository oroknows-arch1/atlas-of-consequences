# AOC-001 Reader Experience Approval

**Edition:** AOC-001 — *AI's Physical Hunger*  
**Status:** APPROVED  
**Human gate date:** 2026-09-24  
**Approved live build:** Render deployment from commit `d36549a603f0bdd24e936a53c22fa1ee7a18bc50`

## Approved entry behaviour

- The approved factual film plays immediately on edition entry, muted where browser policy requires.
- A small `Tap for sound` control may enable the film audio and the restrained Atlas soundtrack.
- The fictional story promo does **not** auto-play after the factual film.
- The factual film holds its final frame at the handoff into the reader.
- The film recedes from the opening state into the reader as a persistent full-screen visual layer.
- The edition text comes forward over that layer.
- Reader scroll position scrubs the factual film in the background.
- The reader background is full-bleed and materially brighter than the earlier dark treatment while preserving text legibility.
- `Skip` and media-failure handling must always reveal the reader rather than trap the user.

## Approved visual treatment

The final approved tuning uses the factual film edge-to-edge behind the reader, with the reader-state brightness raised from `0.43` to `0.67` (about 56% brighter than the prior pass), a lighter veil, stronger film presence, and retained text shadows/local UI treatments for readability.

## Boundary decision

The approved story promo remains a valid separate fictional media asset, but it is **not part of the automatic reader opening**. The opening-to-reader experience must not silently reintroduce it later.

## Human decision

After reviewing the live full-screen, scroll-scrub and brightness pass, the user stated: **“That is approved.”**

This approval closes the AOC-001 reader visual/interaction review and advances the edition to publication QA.
