# AOC001-REPORT-VIDEO — Production Record

**Edition:** AOC-001 — *AI's Physical Hunger*  
**Role:** factual/news-report clip  
**Current candidate:** v0.4  
**Status:** TECHNICAL QA PASS / INTERNAL EDITORIAL QA PASS / AWAITING HUMAN REVIEW  
**Authority:** `ATLAS-BUILD-LOCK.md`

## Purpose

Produce the factual moving-media half of AOC-001. The report must work independently as `WHAT'S REAL` and later supply selected verified moments to the hybrid opening trailer.

This asset is factual. It contains no fictional people, invented documentary scenes or AI-generated footage presented as reality.

## v0.4 editorial sequence

1. **Anthropic / San Francisco** — rights-cleared Anthropic identity over real San Francisco city context.
2. **500 Howard Street** — real building/address context; the photograph is explicitly labelled as a 2020 Slack-era image while Anthropic's current occupancy is separately verified with 2026 evidence.
3. **Western Downs / Dalby** — real regional context for the Reuters article; the proposed project site is explicitly not shown.
4. **Data-centre infrastructure** — real licensed generic moving footage, clearly labelled as generic and not the Western Downs facility.
5. **Electricity / grid** — real licensed generic moving footage, clearly labelled as context.
6. **Chilean copper transport** — real Chilean copper material/logistics imagery.
7. **Chuquicamata** — real mine image used as northern-Chile copper context.
8. **Chilean miners** — real Codelco Andina miners, explicitly labelled to their true 2007 context and not represented as Chuquicamata workers.
9. **Calama community** — real residential context captioned `HOMES. STREETS. ROUTINES.`; no photographed household is claimed to be a mining family.
10. **Causal boundary** — `CONNECTION, NOT CAUSATION.` and an explicit statement that no direct Anthropic–Chuquicamata supply chain is claimed.

## Article and evidence anchor

- Reuters, *Anthropic signs first Australia data centre agreement*, 16 September 2026.
- Western Downs Digital Park / Zerra DC project source.
- IEA physical-infrastructure / grid / material evidence → **SR-03 / SR-04**.
- Antofagasta / Chile copper-system context → **SR-05 / SR-06**.
- Chuquicamata operation / location → **SR-07 / SR-08**.
- Calama / mining work-home context remains bounded by the publication source register.

Full asset-level provenance, rights and use boundaries:

`content/AOC-001/sources/report-video-v0.4-asset-register.md`

## Technical QA — v0.4

- Duration: **30.000 s**
- Frame: **720 × 1280** vertical
- Video: **H.264**
- Frame rate: **30 fps**
- Audio: **AAC stereo, 48 kHz**
- Encoded size: **4,329,043 bytes**
- Review contact sheet and ten timed review frames generated from the finished encode.
- GitHub Actions render/publish run: **PASS**.

## Internal editorial/style QA — v0.4

**PASS as a candidate for human review.**

Verified against the Build Lock:
- named company/article world appears before the consequence chain;
- recognisable Anthropic identity is present without reusing Reuters imagery;
- San Francisco / headquarters context is distinguishable from data-centre context;
- Western Downs regional imagery is not presented as the project site;
- generic data-centre and grid footage is visibly labelled as generic;
- Chilean copper, mine, worker and Calama community material retains its actual context;
- no real miner, household or community member is claimed to be personally affected by Anthropic;
- no fictional Atlas family appears in the factual report;
- `Connection is allowed. Causation requires evidence.` is preserved on screen;
- source labels are readable at mobile review size;
- the result is materially more article-specific than v0.2/v0.3.

## Candidate output

`public/assets/aoc001-report-video-candidate-v0.4.mp4`

Supporting QA files:
- `public/assets/aoc001-report-video-candidate-v0.4-review.jpg`
- `public/assets/aoc001-report-video-candidate-v0.4-probe.txt`
- `public/assets/aoc001-report-video-candidate-v0.4-credits.txt`

## Approval boundary

v0.4 is **not production-approved yet**. It remains a candidate until the user reviews the actual video and approves the factual clarity, pacing, mobile readability and overall newsroom-style production standard.

If approved, the next production outcome is `AOC001-STORY-PROMO`. If rejected, only the specific review failures should be revised; do not reopen settled factual architecture without evidence.