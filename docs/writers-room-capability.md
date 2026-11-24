# Atlas Production Studio — Writers’ Room capability

**Status:** Reusable capability staged for future editions; structural validator only. Not yet wired into the canonical production executor. The existing AOC-001 edition, reader, assets, approvals and production graph are unchanged.

## Required for future productions

All new Atlas editions, including the separately cloned AOC-001-derived demonstration repository, must include this capability in story development. It is not optional and must not be bypassed to produce a quick prototype.

The stage begins after evidence/locality groundwork and story architecture; it develops the institution map, independent character lives, scenes, dialogue, and editorial audits. Its output must pass the existing story boundary and owner approval requirements before media generation or release. A demonstration with hypothetical material may proceed through **creative** development with visible hypothetical/fiction disclosures but cannot be promoted as a verified factual publication.

The canonical AOC-001 edition remains a regression reference, not a target for retroactive rewriting. AOC-002, AOC-003 and other existing editions are likewise unchanged.

## Assets
- `atlas/writers-room/contract-v1.json`: stage contracts, workers, hard rules
- `tools/validate_writers_room.py`: standalone offline validator; separates structural PASS from editorial readiness
- `tests/fixtures/writers-room-neutral-test.json`: synthetic, non-incident fixture that is not Atlas edition content
- `tests/test_writers_room_capability.py`: reusable negative tests
- `.github/workflows/validate-writers-room-capability.yml`: no-cost CI check, runs only when requested or via PR

## Integration checklist (not yet done)
1. Inspect production executor and real manufacturing trace; identify the exact story synthesis/editing handoff. Do not insert a conceptual graph node without a working executable and receipt.
2. Add a new-edition Writers’ Room invocation and durable result receipt. Require required independent editorial decisions; do not treat mere structural compliance as publishable quality.
3. Add tests demonstrating that a new edition cannot advance to fiction media when Writers’ Room gates are REVISE/BLOCKED/UNRESOLVED.
4. Preserve distinct truth modes (verified evidence vs supplied hypothetical event vs fiction). No fabricated specific locality, engineering cause, casualties or operator fault.
5. Test with a neutral fixture and an isolated demo clone; use no paid generation before all gates pass.
6. After review, promote the reusable module through a dedicated PR. No automatic merge/deploy; no changes to existing AOC-001 edition assets.

## Source and cleanup boundary
Recovered from `experiment/aoc004-fiction-production-20261123` **only** the generic contract and validator. The AOC-004 scene board, rejected creative work, and its imagery are deliberately **not copied**. Preserve that historical branch until reusable capability parity has been reviewed.

Notion preservation register: https://app.notion.com/p/42263f5ff9368172af32ce823067357a
