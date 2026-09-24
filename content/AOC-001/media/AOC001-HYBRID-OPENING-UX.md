# AOC-001 — Hybrid Opening UX Lock

Status: **APPROVED READER BEHAVIOUR**
Approved by human gate: **2026-09-24**

## Purpose

Define how the approved AOC-001 hybrid opening behaves when a reader reaches the edition page.

## Locked behaviour

1. Arrival at the AOC-001 edition page immediately hands the viewport to the opening experience.
2. There is **no large play button, splash confirmation screen, or separate test wrapper**.
3. The opening begins automatically in a full-viewport presentation.
4. Because mobile browsers may block autoplay with audible sound, the opening starts **muted where required by the browser**.
5. A small, unobtrusive **Tap for sound** control is available while muted. It must not compete with the visual.
6. On the first reader interaction, sound may be enabled and the approved Atlas sonic bed / source audio may continue at the intended restrained mix.
7. The opening sequence remains explicit about the fact/fiction boundary:
   - approved factual material first;
   - explicit **STORY / FICTION** crossing;
   - approved fictional story promo.
8. When the opening finishes, the full Atlas reader is revealed immediately beneath it.
9. The reader remains available if autoplay fails, media cannot load, reduced-motion settings apply, or the user dismisses/skips the opening. Failure of the opening must never block access to the edition.
10. The production implementation should use a properly hosted media asset / reader-owned media flow. It must not depend on a local HTML attachment streaming several unrelated remote assets.

## Mobile-first requirements

- Opening occupies the screen on entry.
- No interaction larger or more visually dominant than the media itself.
- Sound control is small and optional.
- Respect browser autoplay rules rather than fighting them.
- Respect `prefers-reduced-motion` and accessibility controls.
- Reader content must become available without reload when the opening completes or is skipped.

## Atlas principle

The opening is an entrance to the edition, not a gate in front of it.

The visual remains primary. Audio supports it. Fact and fiction remain unmistakably separated.
