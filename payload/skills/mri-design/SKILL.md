---
name: mri-design
description: >-
  Turns the brief from /mri-brainstorm into a technical design (spec.md). This is the analysis→execution
  BRIDGE of the mri pipeline: it takes the product intent as given and focuses on architecture.
  Invoked by /mri-design. (Adapted from Superpowers brainstorming, MIT.)
---

# mri-design — from brief to technical design (the bridge)

Turns the **product brief** (`.mri_devtools/docs/<project>/brief.md`, produced by `/mri-brainstorm`,
optionally hardened by `/mri-forge`) into a validated **technical design**, ready for planning.

**Role:** take the product intent **as given** (the what/why is already settled in the brief — do not
re-litigate it). Focus on the **technical how**: architecture, components, data flow, error handling,
tests. Output: `.mri_devtools/docs/<project>/spec.md`.

Communicate in the configured language and write the document in the configured document language
(see `AGENTS.md`).

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, or scaffold anything until you have presented a
design and the user has approved it.
</HARD-GATE>

## Checklist (create one task per item, in order)
1. **Read the brief** `.mri_devtools/docs/<project>/brief.md` (+ project context: files, docs, recent commits).
2. **Ask technical clarifying questions** — one at a time: fill the **design gaps** (do not re-explore the
   product). Technical constraints, dependencies, invariants, measurable success criteria.
3. **Propose 2-3 technical approaches** — trade-offs + your recommendation first.
4. **Present the design** in sections scaled to their complexity; get approval after each section.
   Cover: architecture, components, data flow, error handling, tests.
5. **Write the design** to `.mri_devtools/docs/<project>/spec.md` and commit.
6. **Spec self-review** — placeholders/TODO, internal contradictions, scope, ambiguity → fix inline.
7. **User review** — ask the user to review the spec before proceeding.
8. **Transition** — invoke **`mri-devplan`** to create the implementation plan. **That is the only skill
   invoked next.**

## Design for isolation and clarity
Break the system into units with a **single purpose**, communicating through **well-defined interfaces**,
independently testable. For each unit: what does it do, how is it used, what does it depend on? If a unit
can't be understood without reading its internals, or its internals can't change without breaking
consumers, the boundaries need work. Files that grow large are a signal they do too much.

## In an existing codebase
Explore the structure before proposing. Follow existing patterns. Include targeted improvements that
serve the current goal; no unrelated refactoring.

## Spec self-review (fresh eyes)
1. **Placeholders:** "TBD", "TODO", incomplete sections, vague requirements → fix.
2. **Internal consistency:** do sections contradict each other? does the architecture match the features?
3. **Scope:** focused enough for a single implementation plan, or should it be decomposed?
4. **Ambiguity:** could a requirement be read two ways? Pick one and make it explicit.

## User review gate
> "Spec written and committed to `<path>`. Please review it and tell me if you want any changes before
> we write the implementation plan."
Wait for the response. Changes requested → apply + re-run the self-review. Only proceed once approved.

## Visual feedback (web UI)
For a web UI, use the MCP servers (`.mcp.json`): **Playwright** to drive/test, **Chrome DevTools** for
console/network. There is no separate visual companion — the MCP loop covers write → run → observe → fix.

## Principles
One question at a time · YAGNI ruthlessly · explore 2-3 approaches · incremental validation · stay flexible.

## Tracking (progress.md)
- Start: mark `design` `[~]` in `.mri_devtools/docs/<project>/progress.md`.
- End: `design` `[x] → spec.md`, then: "**Next step → `/mri-devplan`**".
