# AOC-002 — story architecture and footage-deferred handoff

Date: 24 November 2026. **All six perspective scripts drafted; NOT story-locked, built or tested.**

## Scope
Client's unverified hypothetical drilling-pad failure in Eastern Niger Delta. Not Seplat Aku-01. No reuse of discarded AOC-004 content. Footage acquisition intentionally deferred at owner's direction; continue nonvisual production.

## Six scene files
1. scene-01-civil-supervisor-script-2026-11-24.md — handover and evidence
2. scene-02-rig-crew-script-2026-11-24.md — observation and stop-work
3. scene-03-wellsite-engineer-script-2026-11-24.md — engineering and restart
4. scene-04-logistics-script-2026-11-24.md — contract and livelihood
5. scene-05-resident-script-2026-11-24.md — information and safeguards
6. scene-06-liaison-script-2026-11-24.md — multilingual communication and escalation

Each perspective has three choices with conditional outcomes (18 total) and a handoff to another perspective. The branches are learning paths, not claims about what actually occurred.

## Reader state contract (for implementation)
- `intro: unseen|skipped|completed`; intro is optional until media exists.
- `perspective: civil|crew|engineer|logistics|resident|liaison`.
- `choices: { [perspective]: 'A'|'B'|'C' }`; changes must be reversible.
- `section: real|story|consequences|place|sources`.
- Always show `HYPOTHETICAL RECONSTRUCTION` in fictional scenes and `REGIONAL CONTEXT — NOT INCIDENT SITE` for geography.
- Source panel must distinguish client account, externally verified context and unresolved facts.
- Show six-perspective navigation, no dead-end branch, preserve mobile-first full-viewport scene pacing, skip intro, no soundtrack.

## Next nonvisual production gate
Convert scene scripts to structured reader data and wire a working AOC-001-quality interactive reader; validate all 18 choices, back-navigation, fact/fiction boundaries and phone viewport. Do not substitute a static text page for the reader. Film assets remain separate and can be attached later. No approval to merge or deploy.
