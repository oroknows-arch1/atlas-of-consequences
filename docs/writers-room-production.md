# Atlas Writers' Room — Core Production Contract v1.0

**State: review-only implementation on an isolated branch.** This is a reusable **machine-readable development and QA layer**, not a claim that a language model can autonomously achieve professional literary quality or that production dispatch has been wired. Do not alter the Atlas Constitution, Build Lock, canonical editions or owner publication authority.

## Why this exists

Atlas must do more than turn an incident report into sensible dialogue. It must build **independent lives in the same connected world**. The reader can enter through different people, learn something another viewpoint could not show, and return to the documented incident with a fuller understanding—without fiction becoming testimony.

The institutional ensemble technique is informed by prestige dramatic craft (including *The Wire*): systems exist through conflicting work, home, business and community incentives. **Do not copy characters, scenes, signature dialogue, storylines or any living creator's distinctive voice.** Atlas writes original fiction rooted in the actual researched locality.

## Contract and evidence flow

`evidence_graph + local_context_pack → world_bible → institution_map → character_bible → scene_board → fiction_scenes → dialogue_edit → continuity/locality/originality/evidence audits → adversarial editorial decision → story plausibility gate → visual/story production`.

The implementation artifacts are:

- `atlas/writers-room/contract-v1.json` — responsibilities and required gate handoffs.
- `tools/validate_writers_room.py` — dependency-free structural, boundary, locality-level and character/scene validation, **not** subjective artistic grading.
- `tests/fixtures/aoc004-writers-room-v1.json` — machine-readable AOC-004 fictional scene board with **REVISE** statuses; not approved content.
- `tests/test_writers_room.py` — regression tests for evidence and development invariants.

The existing Atlas production graph has **not** been silently rerouted. A later integration patch must explicitly connect this layer after `story_synthesis` and before `story_plausibility_gate` and update the manufacturing trace and actual executor, or this remains a tested subsystem rather than an operating autonomous factory.

## Roles: one job, one decision

| Worker / editorial seat | Specific responsibility | Reject if |
| --- | --- | --- |
| World researcher / locality researcher | Differentiate the researchable region from the unidentified precise locality, sources and date range | Broad Niger Delta fact asserted as specific to an unknown host community |
| Institutional story editor / story architect | Map control, incentives, dependence, decisions and information asymmetry | A villain explains the entire system, or each perspective repeats the same facts |
| Character director | Build each person's independent work, private wants, contradictions, relationships and agency | People exist only to illustrate corporate roles or represent a culture |
| Scene writer | Dramatise **goal → resistance → choice → cost/change** | Scene is only dialogue explaining a technical concept |
| Dialogue editor / narrative editor | Create original subtext, silence, humour, status shifts and distinct voices | Every character talks like the same careful analyst |
| Continuity auditor / character director | Track who knows what when, object handoffs, private commitments and causal sequence | Reader can learn a fact from an unavailable source or fictional clue leaks to a later real-world claim |
| Locality reviewer | Test actual regional diversity, professional competence, work and household credibility | Generic village, poverty, religion, accent, ethnicity, oil-spill or ungrounded local practice inserted |
| Originality reviewer / boundary auditor | Reject borrowed expressive elements, distinguish dramatic technique from imitation | Recognisable scenes, borrowed catchphrases, strongly imitated dialogue or real-person likeness |
| Adversarial editor / narrative editor | Name concrete defects and return only failing work for repair | A numerical score or self-congratulation substitutes for an observed effect |
| Human reviewer | Approve finished quality and publication separately | Worker self-approval, unresolved safety, provenance or required asset gates |

## Programmatic versus human checks

**Automatic and fail-closed for a manifest:** unique character/scene ids, minimum cast, separate release classifications, explicit supplied source identity, visible fiction label, scene's stated goal/resistance/choice/cost, reference integrity, cross-perspective revelation, all cast represented, explicit locality scope, independent editorial statuses.

**Human editorial judgement still required:** Is Nengi genuinely individual? Does Boma have a believable independent business? Is Jian an ordinary person rather than a nationality shorthand? Does a reader revise their opinion after a route? Does dialogue carry subtext? Does the place feel authentic to knowledgeable local readers? No threshold algorithm can honestly determine these.

The executable returns STRUCTURE PASS/FAIL separately from EDITORIAL PASS/NOT READY. An unresolved gate never becomes PASS simply because data is syntactically valid.

## Locality grounding for AOC-004

The incident account supports only **Eastern Niger Delta, Nigeria**, onshore operations, a civil contractor and an incoming drilling contractor. It does **not** establish an exact state, village, host community, religion, ethnicity, language, neighbourhood, climate on the date, economic activity of any actual worker/family, or local supplier loss.

*Evidence-backed contextual anchors—comparative, not event verification:*

- Nigeria's Nigerian Content Development and Monitoring Board (NCDMB) describes local operators, contractors, skills and employment participation; its 2026 community-content workshop stresses local manpower, vendors and cross-sector linkages. https://www.ncdmb.gov.ng/ncdmb-intensifies-drive-for-community-inclusion-in-oil-and-gas-sector-through-community-content-guideline-workshop/
- NCDMB describes a **variety** of community-vendor services, from logistics/cleaning to procurement and minor works. https://ncdmb.gov.ng/ncdmb-nlng-team-up-for-integration-of-host-communities-in-oil-and-gas-value-chain/
- Ethnographic research from **particular** Niger Delta communities demonstrates that livelihoods differ and that farming/fishing adaptation is complex. It cannot justify showing pollution or subsistence hardship at the AOC-004 unidentified site. https://www.cambridge.org/core/journals/africa/article/maladaptation-to-environmental-pollution-oil-and-the-livelihood-dysfunction-trap-in-nigerias-niger-delta/E43579FB12A9183D6A5A64868F38E4C9

Therefore AOC-004's character routes may portray technically competent Nigerian professionals, professional Chinese rig workers, varied service businesses and family life **as fiction**. They may not assert that the actual community comprised a particular livelihood, visual stereotype or ethnic group. Before rendering a specific place, obtain local witnesses, reporting or a verified visual/locality pack and rights/accuracy checks.

## Institutional ensemble rules

1. **The institution is not a character.** Individuals are neither faceless company representatives nor allegories for corruption, greed, resilience or poverty.
2. **Four different truths can coexist:** the civil supervisor knows what her team built; operator engineer sees contractual/engineering interfaces; driller experiences operating conditions; entrepreneur sees uncertain prospective demand. None can assert a verified technical cause.
3. **Every perspective carries a private life:** relationships, obligations, aspirations and human contradictions not reducible to the incident.
4. **A scene earns its place** if a character acts under pressure and the choice changes an immediate relationship or condition.
5. **Perspective switches must reveal new information**, not replay the same exposition in another accent or title.
6. **Systems are traced through concrete connections** (a schedule, order, handover, call, missed promise), not speeches on organisational theory.
7. **No single villain:** even an error in the source incident must not be retroactively assigned to a fictional person without explicit hypothetical labelling.
8. **No borrowed prestige dialogue:** learn scene mechanics; author wholly original expressions.
9. **One story's fiction never upgrades another story's evidence:** causal edges remain as supplied/unknown.
10. **Authenticity is not decoration:** place, economic differences, professional skills and ordinary life determine plot plausibility; no staged mud-floor workshops or blanket regional stereotypes.

## AOC-004 narrative direction

A first 12-scene map exists. Develop four original characters: Nengi (civil supervisor), Daniel (operator coordinator), Jian (drilling specialist) and Boma (business operator). Their connecting theme is **the date on several people's calendars**, not a fabricated technical defect or ignored warning.

Avoid a mechanistic story in which each character takes exactly one responsible action and explains a safety lesson. Instead, layer professional dignity, family obligations, friendship, delegation and trust. The reported pad failure arrives midway through a life already in motion. Its physical cause remains unknown in the supplied account.

### Example scene gate

> AOC004-S05 / Nengi: goal—clarify the limits of her civil completion; resistance—Daniel's broader readiness question feels personally dismissive; choice—she asserts her remit without accusing him; cost—an awkward unresolved relationship; reveal to Daniel—“completed work” and “ready for drilling” are different questions. **FICTION / NOT TESTIMONY.**

The scene must not imply she discovered an actual missing load table before the unidentified event. Any such allegation would be a boundary defect, even in a compelling dramatization.

## How to run

```bash
python tools/validate_writers_room.py tests/fixtures/aoc004-writers-room-v1.json --json
python -m unittest tests/test_writers_room.py
```

The manifest currently keeps **all independent editorial gates at REVISE**. A structural pass proves only that the candidate carries the information needed for review. It does **not** mean the prose has been written, reviewed or adopted.

## Required next integration and release steps

- Complete original dialogue/scene rewrite under the dramatic contract; evidence-check all local specificity before visualizing it.
- Get a local/regional authenticity review and an oilfield specialist's plausibility pass, without giving either fictional decisions the status of incident findings.
- Wire writers-room outputs into the canonical story graph and manufacturing trace with explicit migration tests; do not silently change AOC-001 or AOC-002 behaviours.
- Make the AOC-004 experimental reader fiction-first while retaining a separate incident evidence inspector and clear demonstration disclosure.
- Run browser/phone tests of the exact updated branch. Release/publication still needs human approval; experimental docs do not bypass it.
