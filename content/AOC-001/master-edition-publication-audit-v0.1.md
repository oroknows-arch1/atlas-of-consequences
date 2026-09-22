# AOC-001 — Master Edition v0.1 Publication Audit

**Status:** CONDITIONAL PASS — one publication blocker before content lock  
**Audited:** 2026-09-23  
**Scope:** duplication, reader flow, fact/fiction visibility, source completeness and mobile-reading structure.

## Overall verdict

The master edition is structurally ready for publication and the STORY remains locked.

There is **one genuine publication blocker**: the SOURCES section currently names source organisations/documents but does not yet give the reader an inspectable source-by-claim register with direct source links.

That is not a writing problem. It is a publication-evidence problem.

Resolve that single item, then content can be locked and webpage implementation can begin.

## 1. Duplication — PASS WITH LIGHT WEB-PRESENTATION NOTE

The edition repeats the AI → electricity/infrastructure → copper → Antofagasta chain in WHAT'S REAL and CONSEQUENCES.

This repetition is justified because the sections perform different jobs:
- WHAT'S REAL explains the mechanism;
- CONSEQUENCES labels the certainty boundary and explicitly blocks the false AI → Mauricio shortcut.

Do not cut either section from the master.

For the webpage, CONSEQUENCES should be rendered more visually/compactly than WHAT'S REAL so the repetition feels like a map of the argument rather than a second explanation.

No material duplication exists inside STORY.

## 2. Reader flow — PASS

The sequence works:

WHAT'S REAL moves from a familiar AI interaction to physical infrastructure, copper, Chile and Calama.

STORY changes mode clearly and moves from system-scale facts into one fictional household.

CONSEQUENCES returns the reader to analytical mode and explains exactly what was documented versus explored.

PLACE widens the household back into the real city.

SOURCES provides the evidence destination.

The zoom pattern is coherent:

**screen → data centre → grid → copper → Antofagasta → Calama → household → consequence map → city → evidence.**

No reordering is required.

## 3. Fact / fiction visibility — PASS

The transition is sufficiently explicit at content level:
- STORY — FICTION is a dedicated mode heading;
- the fiction boundary names every fictional character;
- Mauricio's opportunity is explicitly identified as fictional;
- CONSEQUENCES separates documented mechanism, documented place connection and fictional human exploration;
- the prohibited causal shortcut is stated directly.

### Web implementation requirement

The webpage must make this distinction visual, not merely textual.

Minimum requirement:
- persistent/obvious mode label when entering STORY;
- visibly different treatment for WHAT'S REAL and STORY;
- fiction disclosure presented before the first story paragraph;
- CONSEQUENCES returns clearly to factual/analytical mode.

A reader scrolling quickly on a phone should not be able to mistake Daniela's household for reportage.

## 4. Source completeness — ONE BLOCKER

The source families are appropriate and the claims in the edition map to the research already assembled:
- IEA for AI/data-centre electricity and infrastructure;
- Cochilco for copper production;
- Codelco for Chuquicamata operational facts;
- INE for census/population;
- UCN for commuting and Calama household context;
- Municipalidad de Calama for civic context;
- heritage/Codelco records for historical Chuquicamata context.

However, the assembled SOURCES section currently functions as a bibliography summary rather than an inspectable evidence register.

Before publication lock, create a source register that gives each material factual claim:
1. claim or claim group;
2. source title;
3. publisher/organisation;
4. publication year/date where available;
5. direct URL;
6. what the source supports;
7. source limitation where relevant.

At minimum, directly trace:
- 415 TWh / ~1.5% global electricity in 2024;
- projected data-centre demand growth and AI's role;
- copper/material requirement statement;
- Antofagasta 58% 2025 production share;
- Chuquicamata ~15 km north of Calama;
- 266 kt 2025 production;
- 3,992 direct employees;
- Calama 166,334 population;
- mining commuting/shift-life claims;
- 2026 Calama household-survey claims;
- Chuquicamata relocation / 10,000+ residents;
- organised worker-transport plausibility;
- El Loa Indigenous-community context.

This register can live behind SOURCES on the website; the narrative itself does not need footnote clutter.

## 5. Mobile-reading structure — PASS FOR CONTENT; REQUIREMENTS LOCKED FOR BUILD

The master is suitable for a mobile-first page, but should not be rendered as one uninterrupted Markdown wall.

### Required mobile hierarchy

Top-level navigation/mode access:
**WHAT'S REAL | STORY | CONSEQUENCES | PLACE | SOURCES**

WHAT'S REAL:
- short paragraphs;
- key-number callouts for 415 TWh, 1.5%, 58%, 15 km;
- simple consequence-chain visual rather than repeating arrow text as prose.

STORY:
- preserve current short paragraphs and scene breaks;
- do not insert fact cards into the fiction;
- maintain STORY — FICTION label;
- avoid visual interruptions that make the family look like case-study evidence.

CONSEQUENCES:
- three clearly separated levels: documented global / documented place / fictional exploration;
- prohibited shortcut visually distinct.

PLACE:
- map/location treatment appropriate;
- city facts separated from story;
- avoid generic desert/mining imagery that reduces Calama to extraction.

SOURCES:
- collapsible or scannable source cards/register;
- direct links;
- show source role/limitation where useful.

## 6. Editorial integrity — PASS

The master preserves the Atlas constitutional rule:

**Facts can change the fiction. Fiction must never quietly become fact.**

The edition also avoids the opposite problem: factual caution has not been allowed to flatten the STORY into a disclaimer.

No further STORY revision is recommended.

## 7. Content lock status

### Locked now
- STORY v0.2;
- reader sequence;
- fact/fiction boundary;
- central causal boundary;
- locality;
- core consequence mechanism;
- master section architecture.

### Not locked yet
- final SOURCES/evidence register.

## Publication gate

**CONDITIONAL PASS.**

Do not return to narrative editing.

Complete one final content task:

**Build the AOC-001 publication source register and wire it to the material claims in Master Edition v0.1.**

Once that is complete and checked, AOC-001 content is publication-locked and the next foreground stage is the actual mobile webpage build.
