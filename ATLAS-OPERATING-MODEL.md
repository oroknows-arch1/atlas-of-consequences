# Atlas of Consequences — Worker / Skills / Authority / Graph Operating Model

## Build rule

Atlas is built as a team of specialised workers, not as one large prompt.

**Hire excellent specialised workers, give them excellent tools, establish their authority and boundaries, then orchestrate their work.**

Prompts may still exist inside a worker implementation where a model requires one. They are replaceable implementation detail. A prompt does not define product truth, grant authority, or decide the production sequence.

## Why this changes the build

The old pattern puts research rules, creative direction, production steps and QA judgement into long instructions or workflows. That makes failures hard to locate because one instruction is doing several jobs.

The worker model separates those jobs:

- **Worker** — who is responsible for one job.
- **Skill** — a reusable capability the worker can use.
- **Authority** — what the worker may decide, write, approve or never change.
- **Graph** — which worker receives work next, what evidence must travel with it, and where human approval gates sit.

In practical terms, when something fails we can ask: was the wrong worker selected, was a skill missing, did a worker exceed authority, or did the graph route work incorrectly?

## Authority order

Product truth remains above the worker system.

1. `ATLAS-BUILD-LOCK.md` — locked product behaviour and current production truth.
2. `docs/atlas-constitution.md` — permanent constitutional boundaries.
3. Edition truth — edition manifest, master edition, source registers and explicitly locked edition records.
4. Human approval gates — approve/reject specific candidates and explicitly change locks when desired.
5. Worker contracts and graph — execution authority and routing.
6. Skills, prompts, scripts, workflows and model choice — replaceable implementation detail.

Lower layers cannot silently rewrite higher layers.

## Worker contract

Every worker must have:

- one primary job;
- explicit inputs and outputs;
- named skills;
- a write scope;
- decisions it may make;
- decisions it may not make;
- conditions that require escalation;
- a QA or approval destination.

Workers should be narrow enough that a failure can be assigned to a specific job.

## Creative intensity

Creative workers may expose an `intensity` setting from `0` to `5`.

- `0` — literal, restrained, minimal invention inside allowed fiction.
- `1` — quiet realism.
- `2` — lightly heightened.
- `3` — strong default narrative energy.
- `4` — high tension, richer subplots, stronger turns and contrast.
- `5` — maximum creative pressure that still obeys story truth, locality truth, continuity and publication boundaries.

Intensity changes **how strongly a creative worker explores its permitted space**. It never expands that space. It cannot turn speculation into fact, invent a new factual condition, alter a locked plot fact, or bypass a human gate.

## Graph rules

The graph is a directed workflow of workers and gates.

- A node names a worker and the artifact it is responsible for.
- An edge names the artifact/evidence passed to the next node.
- A gate blocks progress until its condition is satisfied.
- A failed node returns only to the worker responsible for the failure unless evidence shows an upstream defect.
- Independent factual and fictional branches may proceed separately.
- They may not merge until both branches pass their own approval and boundary gates.
- The orchestrator may route, retry and collect work. It has no authority to author facts, fiction or approvals.

## AOC-001 live test

AOC-001 remains the regression case for this operating model.

Existing useful AOC-001 research, master content, source registers, locality work, report-video candidate, story-promo lock and publication rules are preserved as inputs. They are not regenerated merely because the architecture changed.

The graph records earlier completed work as satisfied by existing artifacts. Current production continues from those artifacts.

The obsolete prototype opening workflow is removed from active GitHub Actions because the Build Lock already records that its still-image montage does not satisfy `AOC001-OPEN-01`. Its history remains in Git.

## Non-negotiable Atlas boundaries

- Facts can change the fiction. Fiction must never quietly become fact.
- Evidence establishes the world. Fiction determines what happens within it.
- Connection may be shown. Causation requires evidence.
- Real people are not fictional Atlas characters.
- Fictional visuals must not masquerade as documentary evidence.
- A worker cannot approve its own publication-critical output.
- Human approval remains required at the gates named in the edition graph.
