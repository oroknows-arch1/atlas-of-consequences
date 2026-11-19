# AOC-002 — Owner review evidence

**Edition:** AOC-002 — *What the Well Changes*  
**Production date:** 19 November 2026  
**State:** Local owner-review candidate; not deployed, published, approved or merged  
**Reader:** `public/review/aoc-002/index.html`

## Open the local owner review

Double-click `content/AOC-002/Open AOC-002.command`. The launcher starts the
required local server only when it is not already running, then opens
<http://127.0.0.1:4174/review/aoc-002/index.html> in the default browser. If the
server cannot start or the reader is missing, the launcher displays a plain-
language error. The opening starts silently and **Skip opening** remains
available.

Do not open `index.html` directly with a `file://` URL, and do not serve the
repository root. The edition intentionally uses site-root asset URLs such as
`/assets/aoc-002/d1-s1.png`; those resolve to `public/assets/aoc-002/` only when
`public/` is the server root. Direct-file opening resolves them against the Mac
filesystem root, while repository-root serving returns 404 for them. Both modes
produce the reported text-only / no-images result even though the media files
are intact.

## Editorial proposition

Seplat Energy's 9M 2026 results report an oil-and-gas discovery at Aku-01 in onshore Imo State. The company's preliminary internal mid-case estimates are 157 Bcf of gas in place and 19 MMbbls of oil in place. It describes Aku-01 as a potential future production well that may be tied back to existing infrastructure.

The edition does **not** convert those statements into proved reserves, current production, revenue, a final development decision, an exact wellhead, a named host community or a guaranteed local benefit.

## Evidence resolution

- **Verified fact:** Aku-01 found oil and gas; preliminary in-place estimates and a potential future tie-back were reported by Seplat.
- **Verified regional context:** OML 53 is an onshore Imo State block with producing fields and existing oil/gas infrastructure.
- **Verified system context:** ANOH has substantial processing and network-injection capacity; Nigerian law and regulation govern host-community trusts, environmental review, flaring and venting; Nigerian content rules create training and capability pathways.
- **Inference / conditional:** existing infrastructure may affect development timing and economics; a discovery can change expectations before it changes production.
- **Unknown:** exact wellhead, official Aku-01 host communities, final development configuration, recoverable reserves, capital budget, start-up date, job count, trust allocation and environmental performance.
- **Fiction:** Adaeze, Chinedu, Nneka, their Owerri household, workshop, dialogue and decisions. They are not host-community residents, workers, witnesses or reported cases.

## Reader structure

The reader reuses the canonical AOC-001 adaptive architecture and preserves reader-selected, non-auto-chained routes:

1. The Discovery
2. The Route to Market
3. The Commercial Question
4. Community and Authority
5. Work and Capability
6. Land, Air and Unknowns

It also includes WHAT'S REAL, STORY / FICTION, CONSEQUENCES, PLACE and inspectable SOURCES surfaces.

## Visual treatment

The owner-rejected deterministic media has been replaced by a cinematic 16:9 visual set: Imo regional landscape, geoscience, wider-block infrastructure, commercial analysis, community process, skills/work, environmental baseline work, Owerri place context and the fictional Adaeze/Nneka household. Generated people and scenes are explicitly labelled reconstructions, not documentary evidence, Aku-01 footage, an exact wellhead or a named host community.

A 15-second local opening film now hands off to the Edition Map using the inherited adaptive-reader controls. STORY uses the fictional household frame; routes retain the completed evidence, boundaries and navigation. The opening film and CSS-referenced story image are both included in the declared, hash-verified asset set.

The AOC-002 reader plays the retained opening permanently muted. Synthetic
soundtrack playback was removed by owner decision; the source media binary was
preserved unchanged.

## AOC-001 parity repair

The final offline parity pass found one AOC-002 defect that could be repaired without changing the factory or generating media: `Before Anything Flows` was a six-paragraph synopsis rather than a sustained human narrative comparable to AOC-001.

The AOC-002 production input now carries a thirteen-paragraph story. It keeps Adaeze, Chinedu and Nneka inside the same fictional Owerri household/workshop frame while giving their choices a complete dramatic progression: announcement, rumour, verification, household cost, work terms, disagreement, bounded action and an ending. No factual claim, source, character status, host-community boundary or Aku-01 development claim was expanded. The unverified training message is explicitly fictional and is not attributed to an operator, regulator or real programme.

The reader was rebuilt from that corrected production input. It was not hand-edited, and all twenty previously verified media assets—including the opening film—were reused unchanged.

The approved six-shot STORY batch is now integrated. The built-in `gpt-image-2` path used the existing included Codex allowance; the verified incremental cash ceiling and actual charge were **USD $0.00**, with no API key, purchased API credit, stock licence or external paid generator. The first generated pass was rejected before integration because it repeated the anchor table and motor-bench compositions. The accepted second pass preserves Adaeze, Nneka and Chinedu while varying bedroom, workshop entrance, parts aisle, kitchen, side-office and veranda settings, as well as camera height, distance and blocking. STORY now uses six unique 16:9 binaries as six labelled full-screen beats. The visual character lock and complete mapping are recorded in `AOC002-VISUAL-CHARACTER-BIBLE-v0.1.md` and `AOC002-SCENE-VISUAL-COVERAGE-v0.1.md`.

## Remaining AOC-001 parity limits

The production-level comparison is recorded in
`content/AOC-002/AOC001-AOC002-GAP-TO-CONTRACT.md`. It supersedes any implication
in this file that valid paths, hashes or technical gates establish experiential
or publication parity.

- AOC-001's factual opening is a source-verified editorial report film. AOC-002's opening is a clearly labelled regional reconstruction made from the existing generated material; it cannot become documentary Aku-01 coverage offline.
- The exact Aku-01 wellhead and officially determined host communities remain unresolved in the cited evidence. AOC-002 therefore stays at Imo State / wider OML 53 resolution and cannot honestly match AOC-001's more precise place grounding.
- Nine scene paths still reuse their route's existing cinematic frame. Purpose-specific crops now reduce visual repetition without pretending to create new evidence, but the underlying unique-image count remains below AOC-001's richer scene-specific benchmark.
- STORY now exposes two existing, character-consistent fictional frames—household and workshop—across three narrative beats. This is a material continuity improvement, but it remains below AOC-001's approved reference set and moving story-promo treatment.
- No AOC-002 OROK companion or distribution package exists in this owner-review build. The inherited reader factory used here has no AOC-002 companion/distribution surface. This is recorded as a factory/product-completion gap; the canonical factory remains unchanged.

These limits do not invalidate the local owner-review reader, but they block a truthful claim of complete publication parity with AOC-001. Publication authority remains false.

## Honest missing-assets report

- No verified documentary photograph or footage of Aku-01's exact wellhead was available or used.
- No official source in the edition identifies an Aku-01 host community; none is named or depicted as such.
- The infrastructure frame is a regional reconstruction of wider-system context, not a photograph of Aku-01 or a confirmed tie-back route.
- The people in the community, workshop, analysis, environmental and household frames are fictional reconstructions, not witnesses, employees or reported cases.
- This integration run incurred **USD $0.00 incremental cash spend** and consumed only the existing included Codex allowance. No API credit, stock licence purchase, deployment, publication or merge occurred.

## Verification

- Python regression suite: **61/61 PASS**
- Atlas graph validation: **PASS** — 38 skills, 33 workers, 38 nodes
- Manufacturing-trace validation: **PASS**
- AOC-001 canonical paths: **unchanged**
- Early Chromium gate: **PASS** — 11 screenshots
- Assembly: **PASS** — 20 assets, 18 rendered beats
- Full Chromium gate: **PASS** — 79 screenshots, all routes at 390×844, 320×740 and 1440×900
- JavaScript syntax: **PASS**
- AOC-002 build-script syntax: **PASS**
- Publication authority: **false**

## Primary and institutional sources

- Seplat Energy, 9M 2026 Financial Results: <https://www.seplatenergy.com/media/xt4h2glj/seplat-energy-report-9m-2026-final-291026.pdf>
- Seplat Energy, OML 53 operations: <https://www.seplatenergy.com/our-company/our-operations/upstream/oml-53/>
- ANOH Gas Processing Company, 2026 network entry agreement: <https://anohgas.com/agpc-signs-network-entry-agreement-with-ngic-unlocking-250-mmscf-d-gas-injection-into-nigerias-national-gas-transportation-network/>
- Nigeria National Bureau of Statistics, Annual Labour Force Survey: <https://nigerianstat.gov.ng/pdfuploads/Annual_Nigerian_Labour_Force_Survey_Report.pdf>
- Nigerian Content Development and Monitoring Board, Human Capacity Development: <https://ncdmb.gov.ng/human-capacity-development/>
- NUPRC, Host Communities Development Regulations 2022: <https://www.nuprc.gov.ng/wp-content/uploads/2022/07/Nigeria-Upstream-Petroleum-Host-Communities-Development-Regulations-2022.pdf>
- Petroleum Industry Act 2021: <https://br2025.nuprc.gov.ng/media/ggwk4wxe/petroleum-industry-act-2021.pdf>
- NUPRC, health, safety and environmental oversight: <https://nuprc.gov.ng/health-safety>
- NUPRC, Gas Flaring and Venting Regulations 2022: <https://www.nuprc.gov.ng/wp-content/uploads/2022/12/Gas-Flaring-and-Venting-Regulations-2022-D.pdf>

## Owner decision

Review the local reader's editorial framing, fictional voice and visual system. Approval here would be approval to continue or revise the review candidate only. Deployment, publication and merge remain separate explicit decisions.
