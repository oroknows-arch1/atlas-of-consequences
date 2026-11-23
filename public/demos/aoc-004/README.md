# AOC-004 — The Ground Beneath the Rig (Atlas Demonstration)

Status: **isolated experimental reader / review only / not deployed**

This page is a de-identified interactive educational demonstration based on a single supplied incident account. It does not authenticate the incident, identify the contracting parties, establish engineering causation, or assign responsibility.

## Preview

Serve the repository's existing `public/` directory through the normal Atlas static server, then open `/demos/aoc-004/`. This intentionally sits beside, not inside or over, the canonical `/adaptive/` reader. There is no root navigation link, redirect or existing-edition change.

## Reader paths

The user must consciously choose one of five perspectives: operator/engineering, civil contractor, drilling contractor, crew, or community/suppliers. Each provides three bounded text scenes. The source register remains accessible, and decisions and consequences are explicitly illustrative.

## Technical limits

This is a zero-media, single HTML page with no external JS, API, trackers or soundtrack. It is a preview of route structure, not a full cinematic Atlas edition. It is intentionally `noindex`. Opening it does **not** convert `AOC-004` to an approved edition, waive the Atlas constitution or meet the mandatory completed-media/release requirements.

## Verification checklist

- [x] Exact repository tests and manufacturing-trace validation run against this branch (61/61 passed on 23 November 2026).
- [x] Branch reader exercised in Chromium at 390×844 and 1440×900 across all five routes, direct deep links and evidence navigation.
- [x] Automated accessibility audit, keyboard focus transitions, console-error check and horizontal-overflow check passed locally.
- [ ] Hosted preview at `/demos/aoc-004/` tested on phone and desktop.
- [ ] Confidentiality review (the combination of industry, nationality and region could permit indirect identification).
- [ ] Owner approves publication scope and release.
- [ ] If adopted as a full edition, evidence graph and media outputs enter the canonical factory; keep provenance labels intact.

The branch-specific browser regression is `tests/aoc004-demonstration.cjs`. It requires Playwright, Chromium and `@axe-core/playwright`; it does not deploy or publish the reader.

## Sources and source-state

The claim of a particular partial rig sinking, evacuation and rig replacement comes from a **single unidentified account**. External industry documents are comparison/reference material, not corroboration of this incident.

Project planning: [AOC-004 Notion record](https://app.notion.com/p/42163f5ff936813c9190d3b1f6febfb0).

Repository contracts: [Build Lock](../../../../ATLAS-BUILD-LOCK.md), [Constitution](../../../../docs/atlas-constitution.md), [Adaptive Reader Workflow](../../../../ATLASOQUENCE-ADAPTIVE-READER-WORKFLOW.md).
