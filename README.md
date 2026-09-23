# Atlas of Consequences

Global storytelling and publishing system exploring the human consequences of consequential real-world change.

## Operating model

Atlas uses a **worker → skills → authority → graph** architecture.

- Product truth: `ATLAS-BUILD-LOCK.md`
- Constitution: `docs/atlas-constitution.md`
- Operating model: `ATLAS-OPERATING-MODEL.md`
- Worker registry: `atlas/registry/workers.json`
- Skill registry: `atlas/registry/skills.json`
- Authority model: `atlas/registry/authority.json`
- Edition graph: `atlas/graphs/edition-production.json`
- Live regression edition: `atlas/editions/AOC-001.json`
- Contract validator: `python3 tools/validate_atlas_graph.py`

Prompts, scripts, model choice and workflows are implementation details beneath those contracts.

AOC-001 remains the live test case. Existing verified research, story, source registers and media work are preserved and bound into the graph rather than regenerated.
