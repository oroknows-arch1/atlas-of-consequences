# AOC-002 gap-to-contract review

**Review date:** 19 November 2026  
**Compared:** rendered canonical AOC-001 (`public/adaptive/index.html`) and rendered AOC-002 (`public/review/aoc-002/index.html`)  
**Authority:** `ATLAS-BUILD-LOCK.md`, the 25 September AOC-001 reconciliation and active manifest, Atlas constitution, reader grammar, AOC-001 reader invariants and edition graph  
**Decision:** AOC-002 is an unpublished production candidate. It is not at AOC-001 publication parity.

## Observed production difference

AOC-001 opens with the approved factual report film, retains the film as the live reader background, carries an approved soundtrack/handoff, has a separately approved 25-second STORY / FICTION promo, uses real/source-traceable factual media, and has a complete distribution candidate.

AOC-002 opens with a 15-second, 1920×1080 synthetic regional reconstruction. Its 19 declared still paths resolve to only nine distinct PNG binaries: three Discovery scenes repeat one image, three Commercial scenes repeat one image, three Environmental scenes repeat one image, both Infrastructure scenes repeat one image, both Community scenes repeat one image, and both Work scenes repeat one image. The opening master and WHAT'S REAL image are also identical; the CONSEQUENCES and STORY binaries are identical. No exact Aku-01 documentary image, report video, distinct story promo, or distribution pack exists.

The rendered pixels are attractive in isolation but establish a generated landscape/people montage, not the article-specific factual authority or moving factual-to-human visual grammar of AOC-001. On a desktop Chrome load before this pass, the unmuted WebM was autoplay-blocked and displayed `Tap to play`; the synthetic/documentary boundary was not visibly present on the opening frame.

## Gap-to-contract matrix

| Contract area | AOC-001 canonical | AOC-002 observed | Classification | Correction / authority |
|---|---|---|---|---|
| Core sequence and truth labels | WHAT'S REAL, STORY, CONSEQUENCES, PLACE, SOURCES with visible boundaries | All five surfaces exist; routes carry FACT/UNCERTAIN and reconstruction labels | **Already compliant** | Retain. |
| Reader-selected perspective paths | Six deliberate, non-auto-chained entries with return/deep-link behaviour | Six paths; route endings, back/reload and source anchors exist | **Already compliant** | Retain. |
| Full-viewport scene grammar | Image-led, full-screen scenes rather than article cards | Full-viewport scenes at desktop and phone sizes | **Already compliant** | Retain. |
| Opening autoplay and controls | Muted-policy-compatible factual film; skip control at midpoint | Unmuted WebM was blocked; skip sat near top | **No-cost offline fix** | Keep the retained WebM permanently muted per owner decision; place skip at midpoint. Implemented in this pass. |
| Opening fact/synthetic boundary | Factual film; identity and evidence role are legible | Photoreal regional reconstruction looked documentary; boundary existed only in metadata | **No-cost offline fix** | Add persistent visible `REGIONAL RECONSTRUCTION · NOT DOCUMENTARY FOOTAGE` during film. Implemented in this pass. |
| Opening content | Approved article-specific factual report with sourced real imagery | Generic generated Imo landscape/people sequence; not Aku-01, Seplat, a wellhead or a named host community | **Needs new rights-cleared documentary media and owner approval** | Source/licence article/company, supported OML 53/Imo infrastructure and human/place imagery; edit a factual report; human editorial/style gate. |
| Opening orientation | AOC-001 active truth uses factual-only report, not the retired hybrid requirement | Reconstruction mixes regional and human synthetic imagery without factual-report authority | **Needs documentary media; hybrid not required for this unpublished candidate** | Follow the reconciled factual-only reader opening. Do not spend on a hybrid unless the owner changes the active architecture. |
| Opening persistence / scrub handoff | Same factual video holds its final frame and remains scroll-scrub background | Video hands off to an identical retained still; routes use scene stills | **Needs factual film first; no-cost code change alone would misrepresent parity** | Do not promote the current synthetic clip into the canonical factual-memory role. Revisit only after factual-media approval. |
| 9:16 report/social slot | Approved report exists; vertical derivatives are expected where useful | Only 16:9 1920×1080 opening | **Needs new edit/media; owner authorization before spend** | Produce a mobile-first report/derivative after documentary acquisition. The locked language is primarily 9:16, but the approved AOC-001 test also contains accepted 16:9 assets; aspect ratio alone is not parity. |
| STORY / FICTION promo | Separate approved 25-second cinematic promo with native audio and continuity references | One still repeated as CONSEQUENCES and STORY background; no moving promo | **Needs new media and owner authorization** | Story promo is a distribution asset, not required in the automatic reader opening. It is not required merely to review this unpublished candidate, but is required for AOC-001-equivalent media/distribution completeness. |
| Story narrative | Sustained fictional family/labour lens with explicit boundary | Thirteen-paragraph Adaeze/Chinedu/Nneka narrative with explicit fiction boundary | **Already compliant at candidate level** | Retain; local/cultural human review remains a publication gate. |
| Story simulation | Perspective-based living simulation of documented systems | Fixed prose narrative plus six factual/analytical routes; no persistent or replayable character state | **Genuine production gap; owner/product authority needed** | Do not invent a simulation through more prose. Define whether AOC-002 opts into the world-state/simulation layer before implementation. |
| Visual variation | Richer approved factual, place, character and explanatory set | 19 paths but nine distinct PNGs; repeated imagery inside routes | **Needs new source-cleared or explicitly authorized generated media** | Reuse is honest but below premium parity. Do not pad with generic stills. |
| Place and landscape | Calama/Antofagasta grounded through real place evidence and source limits | Imo/OML 53 resolution is honest; exact wellhead and host communities unresolved | **Already compliant boundary; documentary depth blocked** | Retain geographic stop. New evidence may narrow place; imagery cannot substitute for evidence. |
| Authentic photography | Real/source-traceable factual assets with rights register | All retained AOC-002 visuals are generated reconstructions | **Needs rights-cleared documentary imagery** | Create an asset register containing creator/source, licence, permitted uses, credit, edits and file hash before integration. |
| Sound | Approved AOC-001 bed with natural fade | AOC-002 synthetic ambience was not wanted | **No-cost offline fix** | Soundtrack playback removed from the AOC-002 reader by owner decision; retained source binary remains preserved and permanently muted. |
| Evidence and fiction separation | Persistent, reviewed, regression-protected | Strong text labels and source limitations; opening visual boundary was missing | **Compliant after no-cost fix** | Keep labels visible on every generated factual-context scene. |
| Sources and provenance | Inspectable source register plus media asset registers and rights | Nine institutional/editorial sources; generated-media receipts and hashes exist; no documentary rights register | **Already compliant for retained generated assets; blocked for new documentary media** | Preserve receipts. Add per-asset rights records before any real-world media enters the build. |
| OROK | Explicitly optional downstream for AOC-001 | No AOC-002 companion | **Not required for unpublished candidate** | Do not create unless AOC-002 explicitly opts in. |
| Distribution | Verified AOC-001 master-derived candidate; external execution separately gated | No AOC-002 signal/distribution package | **Not required for unpublished candidate; required before parity/release claim** | Build only after master/media approval. No outreach, scheduling or publication without explicit authority. |
| Publication/deployment | Release gate remains a distinct human act | Local noindex review only; publication authority false | **Already compliant** | Keep local. No deploy, publish or merge. |

## Coherent correction scope

### Completed now, without media generation or spend

1. Made the retained AOC-002 opening autoplay-compatible by starting it muted.
2. Removed soundtrack playback from the AOC-002 reader by keeping the retained opening permanently muted.
3. Moved the opening skip control to the canonical midpoint zone.
4. Added a visible opening-film boundary identifying the footage as a regional reconstruction, not documentary footage.
5. Preserved all binaries, receipts, AOC-001 files, factory code and paid assets.

### Next production package, blocked before spend

Treat this as one media acquisition and edit package, not a series of reader tweaks:

1. Resolve the factual visual brief at supported geography: Seplat/article identity; wider OML 53/Imo infrastructure only where accurately captioned; Imo/Owerri place and human context; no invented wellhead or host community.
2. Source rights-cleared real photography/footage and record licence, attribution, permitted platforms/territories/term, transformations and hash.
3. Edit one article-specific factual report with contemporary mobile-first cuts, captions, restrained branding and sound. Derive 9:16 output where the chosen distribution surface requires it.
4. Human-review the factual film for evidence, rights and style before replacing the opening.
5. Separately decide whether to authorize a cinematic STORY / FICTION promo and continuity set. Do not bundle fiction frames into the factual report.
6. After approved media exists, reconnect and verify exact final-frame handoff, persistent background/scrub behaviour, phone crops and the complete reader.
7. Only after master approval, decide whether AOC-002 needs OROK and build distribution derivatives. Neither is a prerequisite for reviewing this local candidate.

## Paid-operation stop

No purchase or generation is authorized by this review. Before any paid action, the owner needs a concrete acquisition sheet listing the exact missing shot, proposed source/provider, licence terms, cost/credits, factual role, fallback and why retained assets cannot satisfy it. The minimum likely paid categories are documentary licences/acquisition and, only if separately authorized, fiction-promo generation/editing. Credit quantities cannot be stated honestly until a provider, duration, model and shot list are selected.
