# Automated Edition Test #1 — implementation map

Baseline inspected: main @ 99aac2b898cf751df9573abb6e5d43ba2e3a1a8b

## KEEP
- Constitution and fact/fiction rule: `docs/atlas-constitution.md`.
- Existing worker/skill/authority registries as the governance base.
- Evidence research, verification, locality research, consequence mapping, source registration and boundary-audit worker roles.
- Distribution contracts and downstream signal/distribution graph concepts.
- AOC-001 reader and its invariant validator as a read-only regression benchmark.
- Human release authority.

## WRAP
- `atlas/graphs/edition-production.json`: preserve it; Automated Edition Test #1 uses an edition-neutral generation graph in front of/alongside it rather than mutating AOC-001 assumptions.
- Reader assembly: wrap the approved presentation language in a data-driven edition manifest. Do not bind new editions to AOC-001 IDs, six Perspectives, fixed scene counts, Chile, video, or its route sequence.
- Signal extraction: retain the downstream contract, but future extraction must consume the generated edition manifest/source graph rather than AOC-001 hard-coded text rules.
- Existing evidence/locality/consequence workers: require structured outputs with stable IDs and provenance.

## REPLACE
- Nothing in AOC-001.
- For new editions only, replace hard-coded AOC-001 signal extraction and reader bindings with generic manifest-driven equivalents once the test reaches those nodes.

## DELETE
- Nothing from the benchmark.
- No production artifact is deleted for Test #1.

## MISSING
1. Edition-neutral world-change input contract.
2. Traceable evidence-graph contract with explicit KNOWN / UNCERTAIN / CONTESTED / UNKNOWN / UNAVAILABLE / FICTION_EDITORIAL states.
3. Perspective derivation output contract with evidence-backed accept/reject reasons.
4. Route/scene contract with per-scene meaning, evidence refs, causal bounds and knowledge-stop states.
5. Visual-requirement contract and provider-routing decision record.
6. Edition-neutral generated manifest consumed by reader assembly.
7. Deterministic invariant validator for provenance, causal boundaries, reader agency, route separation, visual truth and publication hold.
8. Test-run state/receipt so failures remain visible instead of being silently repaired.

## Minimum machinery for the first run
Implement only:
`world change -> evidence graph -> geography -> Perspective candidates/selection -> routes/scenes -> visual requirements/provider decisions -> generated edition manifest -> deterministic invariant validation -> review candidate -> HUMAN PUBLICATION GATE`.

Image generation/persistence is invoked only after scene requirements exist. Distribution remains downstream and blocked until the reviewable edition passes QA. AOC-001 remains untouched.
