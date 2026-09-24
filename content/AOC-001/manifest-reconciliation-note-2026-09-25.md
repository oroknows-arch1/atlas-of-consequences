# AOC-001 Manifest Reconciliation — 2026-09-25

This record explains the cleanup applied to `edition-manifest-v0.1.yaml` after Publication QA v0.1 identified manifest drift.

The manifest is the active production contract and must describe the current approved edition state. Historical decisions remain preserved in Git history and the edition's approval/QA records; they must not remain as stale active instructions.

## Retired active instructions

The following obsolete instructions were removed or replaced from the active manifest:

- the unproduced 10–15 second hybrid-trailer opening requirement;
- the automatic factual-to-fiction opening sequence;
- the old `ENTER THE REPORT` / `ENTER THE STORY` entry choice;
- `required / not yet produced` status for the approved factual report video;
- `required / not yet produced` status for the approved story promo;
- empty asset-slot states for assets already produced and reviewed;
- pipeline states that still described media acquisition, assembly and mobile web assembly as not started;
- the old next action to begin asset acquisition.

## Current active truth

The manifest now records:

- the approved factual report film as the automatic opening and persistent scroll-scrub visual layer;
- final-frame hold and visible handoff into the reader;
- full-screen reader background at the approved brighter treatment;
- the story promo as an approved separate fiction/distribution asset, never an automatic opening continuation;
- the Atlas signature soundtrack candidate as approved for testing and subordinate to the visuals;
- the approved reader visual/interaction system as locked during remediation;
- Publication QA v0.1 as failed, with release blocked;
- complete Master Edition integration as the next reader-build action;
- distribution candidate, reduced-motion fallback, and release-scope items as current unresolved work.

Historical prototypes and rejected approaches remain inspectable through Git history and the existing approval/QA records, not as active production instructions.
