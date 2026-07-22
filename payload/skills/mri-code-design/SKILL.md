---
name: mri-code-design
description: >-
  Turns the brief from /mri-code-brainstorm into a technical design (spec.md). This is the analysis→execution
  BRIDGE of the mri pipeline: it takes the product intent as given and focuses on architecture.
  Invoked by /mri-code-design.
disable-model-invocation: true
---

# mri-code-design — from brief to technical design (the bridge)

> ┌─ mri devtools ─┐

Turns the **product brief** (`.mri_code/docs/<project>/brief.md`, produced by `/mri-code-brainstorm`,
optionally hardened by `/mri-code-forge`) into a validated **technical design**, ready for planning.

**Role:** take the product intent **as given** (the what/why is already settled in the brief — do not
re-litigate it). Focus on the **technical how**: architecture, components, data flow, error handling,
tests. Output: `.mri_code/docs/<project>/spec.md`.

> **Source of truth — read `progress.md` first.** If it has a `## Source` block, this journey is
> **issue-driven** (started by `/mri-code-issue`): the brief lives in the **GitHub issue**, not in
> `brief.md`. Read it with `gh issue view <N>`, and on approval write the design **into the issue** —
> append a `## Technical design (mri-code)` section to the body via `gh issue edit <N> --body-file`
> (an **outward-facing write: get user approval first**) — instead of writing `spec.md`. Everything
> else below is identical. See `AGENTS.md` → *Issue-driven journeys*.

Communicate in the configured language and write the document in the configured document language
(see `AGENTS.md`).

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, or scaffold anything until you have presented a
design and the user has approved it.
</HARD-GATE>

**Enter plan mode.** Run this whole step in native Claude Code plan mode (call the plan-mode tool
yourself — the user does not toggle it). Plan mode is read-only, so the HARD-GATE above is enforced
structurally: you *cannot* write the spec or any code until you exit. Discuss the approaches and the
design sections with the user inside plan mode; then present the final design via ExitPlanMode — **that
approval is the gate.** On approval, exit and write `spec.md` (checklist step 5). If plan mode is
unavailable (non-interactive run), present the design inline and get explicit approval before writing.

## Checklist (create one task per item, in order)
1. **Read the brief** `.mri_code/docs/<project>/brief.md` — **or the GitHub issue** (`gh issue view <N>`)
   if `progress.md` has a `## Source` block (+ project context: files, docs, recent commits). **If
   `.mri_code/assets/mockups/` holds mockups**, study them: they are the visual source of truth —
   derive the screens, structure and UI states from them, and reflect them in the design.
2. **Ask technical clarifying questions** — one at a time: fill the **design gaps** (do not re-explore the
   product). Technical constraints, dependencies, invariants, measurable success criteria.
3. **Propose 2-3 technical approaches** — trade-offs + your recommendation first.
4. **Present the design** in sections scaled to their complexity; get approval after each section.
   Cover: architecture, components, data flow, error handling, tests.
5. **Write the design** — **only after approval** (ExitPlanMode, or inline if plan mode was
   unavailable). Idea-driven: to `.mri_code/docs/<project>/spec.md` and commit. **Issue-driven:**
   append a `## Technical design (mri-code)` section to the **issue body** (`gh issue edit <N>`),
   after showing the exact new body and getting approval; write no `spec.md`.
6. **Spec self-review** — placeholders/TODO, internal contradictions, scope, ambiguity → fix inline.
7. **User review** — ask the user to review the spec before proceeding.
8. **Transition** — **suggest** the next command **`/mri-code-devplan`** (name the suggested model per
   `.mri_code/models.md`); do not launch it yourself. That is the only step suggested next.

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
> "Design written to `<path>` (or **into issue #N**). Please review it and tell me if you want any
> changes before we write the implementation plan."
Wait for the response. Changes requested → apply + re-run the self-review. Only proceed once approved.

## Visual feedback (web UI)
For a web UI, use the MCP servers (`.mcp.json`): **Playwright** to drive/test, **Chrome DevTools** for
console/network. There is no separate visual companion — the MCP loop covers write → run → observe → fix.

## Principles
One question at a time · YAGNI ruthlessly · explore 2-3 approaches · incremental validation · stay flexible.

## Tracking (progress.md)
- Start: mark `design` `[~]` in `.mri_code/docs/<project>/progress.md`.
- End: `design` `[x] → spec.md` (idea-driven) or `[x] → design in issue #N` (issue-driven), then:
  "**Next step → `/mri-code-devplan`**".

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Opus (architecture) — see `.mri_code/models.md`.
