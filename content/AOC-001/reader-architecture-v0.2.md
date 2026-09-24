# AOC-001 — Reader Architecture v0.2

**Edition:** AOC-001 — *AI's Physical Hunger*  
**Status:** approved direction / implementation candidate  
**Decision date:** 2026-09-25

## Release-review result

The prior release candidate is not approved for publication. Human review identified two reader problems and one larger story-system opportunity:

1. the first factual block asks the reader to assemble too many connections from prose;
2. after the opening film, the reader needs an immediate title/menu screen explaining the upcoming scroll;
3. STORY should become a perspective-based living simulation of the documented market/consequence system rather than fiction included merely because the format requires a story.

Publication remains blocked until the revised reader is visually reviewed and publication QA is rerun.

## Reader sequence v0.2

The active reader sequence is:

**FACTUAL OPENING FILM → EDITION MAP → WHAT'S REAL → STORY / PERSPECTIVE → CONSEQUENCES → PLACE → SOURCES**

The opening film remains factual-only. The separate STORY / FICTION promo is not inserted into the automatic opening path.

## Edition Map

The first reader screen after the factual film must orient the reader before long-form prose.

It shows what the scroll will do:

1. **WHAT'S REAL** — documented change and physical chain;
2. **STORY** — fictional human lens living inside that real system;
3. **CONSEQUENCES** — separate documented effects, connected implications and fictional exploration;
4. **PLACE** — explain why the chain narrows to a particular location;
5. **SOURCES** — inspect evidence and claim limits.

The section route remains available while reading and should make the reader's current location obvious.

## WHAT'S REAL — visual mechanism first

Before the dense explanatory prose, the reader sees the causal/connection chain visually:

**AI / data-centre growth**  
↓  
**electricity + grid demand**  
↓  
**material demand including copper**  
↓  
**northern Chile / Antofagasta**  
↓  
**Calama / Chuquicamata and the human/commercial system around it**

Each step is tied to evidence. The visual must preserve the boundary:

**Connection may be shown. Causation requires evidence.**

The flow must never be interpreted as proof that AI caused a specific Antofagasta mine expansion or a particular job.

## Story system — perspective architecture

Atlas STORY becomes a **perspective-based living simulation of the documented system**.

A real-world signal can support several fictional lenses built around the same factual spine. The fiction can demonstrate how value, constraints, demand, labour, supply, customers and market formation might be experienced from different positions without becoming evidence that a stock or product will rise.

AOC-001 v0.2 establishes these perspective classes:

- **Inside → out: family + labour** — the existing Daniela/Mauricio household lens;
- **Building the market: operator + supplier** — operations, equipment, contractors, bottlenecks and capacity;
- **Buying from the market: buyer + customer** — downstream need, substitution, availability and price sensitivity;
- **Outside → in: investor + market** — how the same documented signals may be interpreted commercially.

Only the existing family/labour story is currently written. The other lenses are architecture, not invented completed stories.

Future editions may contain one or several story branches depending on what materially improves understanding of the selected market/product/system.

## Investment/commercial boundary

Fiction may illustrate a documented market mechanism from different human or commercial positions. It must never become disguised investment evidence.

The factual/evidence layers are responsible for proving what is happening. Fiction may explore what documented conditions could mean if they strengthen, weaken or propagate through the system.

## Media-generation rule

Until the next edition publishing approval gate:

- **no new video generation is required or authorised for reader architecture work;**
- new media generation, when needed, is limited to **story media**;
- do not regenerate the approved factual opening film merely to support this reader revision;
- do not spend Runway credits on video unless a future explicit approval changes this rule.

## Current implementation target

AOC-001 is the test case for this architecture. The existing locked factual content, source register and approved factual film remain intact while the presentation layer is reorganised around orientation, visual mechanism and perspective clarity.

## Next gate

Human mobile visual review of the revised reader. If approved, rerun Publication QA before returning to the release human gate.
