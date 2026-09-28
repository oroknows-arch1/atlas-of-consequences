# Atlas reader grammar extraction — 2026-09-28

Canonical: AOC-001 `/adaptive/`, main commit `99aac2b898cf751df9573abb6e5d43ba2e3a1a8b`. Read-only throughout. This is the current adaptive reader; historical scroll-reversing film in the root reader is not the active adaptive behaviour. Current adaptive film ends or skips into a geographical home background. Do not invent reverse scrubbing as an observed invariant of this version.

## Audit and gap analysis

| Dimension | Canonical implementation | Previously generated reader | Factory rule |
|---|---|---|---|
| Entry | Real muted inline MP4; identity withheld during motion; skip/rejected autoplay states; 0.9s reveal | Permanent publication header; title above image | Cinematic opening with persistent contextual home image, timed reveal and reduced-motion accommodation. Approved film and verified-image sequence are interchangeable production capabilities |
| Hero | Minimum 100svh; absolute cover media; title in lower foreground | Hero override `min-height:0`; figure in normal flow; 65svh maximum image | Edge-to-edge viewport hero; no article masthead |
| Typography | Georgia regular, hero 58–92px/.87, scenes 36–56px/.98; small tracked labels | Bold display titles, inconsistent heading overrides, default system-font body | Shared scale, serif body 17–20px, low-weight heading hierarchy |
| Perspective discovery | Continuous vertical image composition with clickable regions | Plain text links in a grid of cards | Live accessible labels and imagery in vertical strips; route count derived from accepted topology |
| Scenes | Cover image occupies entire minimum viewport; lower text layered above transparent gradient | Desktop side-by-side grid; mobile image-above-text and `contain` override | Full-bleed contextual scenes; diagrams have explicit uncropped explanatory treatment |
| Grade | Brightness .88, contrast 1.04, saturation .96; modest top opacity, stronger lower gradient | Unrelated backgrounds and layout rules; presentation not compared | Stable warm-neutral grade, image remains visible behind bounded text |
| Pacing | One main claim, evidence line, minimum viewport per scene; explicit route end | Long prose blocks and separate figures; no visual beat contract | Sentence-boundary pagination preserving exact content and citations; no truncation |
| Navigation | Deliberate Perspective choice, sticky back navigation, route end; incoming choice highlighted | Hash isolation existed, but choices had no visual identity | Preserve deep links, history and focus; one route active, no auto-chain |
| Boundaries | Scene-specific evidence/interpretation/STORY labels and explicit limits | Labels existed but did not establish composition | Preserve every state, source, uncertainty and fiction boundary; illustration caption remains visible |
| Responsive | 800px desktop inset, 600px phone menu edge, short-screen accommodations; safe areas | Article-style breakpoints | 320×740, 390×844, 1440×900; rendered geometry at all three |
| Motion/accessibility | End/skip reveal; tap-to-play if autoplay rejected; reduced-motion rules | No entry state machine | Actual timed visual progression and reveal required; an approved film plays if present, otherwise verified images move and crossfade in the browser |

The prior visual prompt explicitly said not to require the benchmark's “media structure”. Only the first visual batch received canonical images. Full-page tall screenshots obscured viewport composition. These were insufficient parity definitions, not evidence that the visible divergence was acceptable.

## Invariants

`atlas/contracts/reader-grammar.json` defines the publication grammar. The shared builder, CSS and JS implement it. The browser contract checks computed sizes, image coverage/layering, heading/body hierarchy, prose density, grade/gradient, Perspective topology, real opening progression and skip behaviour. For the film path it checks decoded playback; for the image path it checks verified image coverage and changing rendered transforms. Independent visual review compares candidate and canonical viewport screenshots in every batch.

## Adaptive rules

- Derive Perspective count, names and sequence from the accepted edition routes; never assume six.
- Use each route's verified imagery. An optional scene can reuse its route's contextual image with its illustration caption; missing content is never invented.
- Explanatory graphics remain uncropped. Their factual labels are not treated as photographic subjects.
- Split long existing paragraphs only at sentence boundaries and repeat the original state and citations on each beat. Editorial source text is unchanged.
- Titles, geography, background media and motion content are edition-specific. A route can have more visual beats than source scenes without changing its evidence topology.
- Sources, route-end boundaries and long-form fiction have deliberately different reading surfaces; this does not permit the whole reader to become an article.

## AOC-001-specific content excluded

All Chile/Calama/copper material, names, fiction, source register, six-route IDs, film, orbit imagery and precomposed six-Perspective menu remain canonical content only. The new builder does not reference those assets or strings. The active benchmark's menu has baked-in words; the reusable menu recreates the visual structure with accessible HTML, without reproducing that image or its fixed hotspot percentages.

## Verification and failure handling

The old HTML/CSS/JS is retained only under `tests/fixtures/legacy-reader`. A real browser regression must reject it. Mutations remove image coverage, change typography, add dense copy, darken images or restore a card grid and must fail the same checker. The final gate requires a current reader-contract receipt, timed opening interaction evidence and a hash-bound opening manifest. The manifest references at least two previously verified contextual assets or an independently reviewed film.

Reader-only remediation protects upstream editorial/evidence and all ten image hashes. A static hero with no cinematic transition remains blocked. Runway is an optional provider, not a dependency of the reader grammar. CSS repairs target shared production styles and are rechecked, rather than editing an edition's output alone.
