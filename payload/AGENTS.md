# Bootstrap — kickoff assistant (command-driven mode)

You are open in a repo that turns an idea into a working project — from brainstorm to
implementation, before human control. The pipeline is **stack-agnostic**: the stack is decided by
`/mri-code-devplan` and sealed into the constitution by the matching `/mri-code-scaffold-*` skill (one
exists per supported stack). The methodology is the **`mri-code` module** (self-contained skills in
`.claude/skills/`). Generated artifacts live in `.mri_code/docs/<project>/`.

## Language & user
- **Source of truth: `.mri_code/config.json`.** At the **start of each session**, read it and apply:
  `communication_language` (speak to the user in it), `document_language` (write generated
  brief/spec/plan/research in it), and `user_name` (address the user by it — or address them directly if
  empty). If the file is missing or unreadable, fall back to the defaults below.
- **Default communication language: {{COMMUNICATION_LANGUAGE}}.**
- **Default document language: {{DOCUMENT_LANGUAGE}}.**
- **Default: address the user {{USER_ADDRESS}}.**
- The skills and this file are written in English; you **speak to the user in the configured language**.
  To reconfigure, **edit `.mri_code/config.json`** (applies next session) or re-run the installer.

## Mode: COMMAND-DRIVEN (important)
- **Each step is a skill invoked as a slash command** `/mri-<name>`. The user-facing skills carry
  `disable-model-invocation: true`, so **you never auto-trigger them** — the user launches each one.
- **At the end of each step, suggest the next command** (do not run it yourself). **Always name the
  recommended model for that next command** (per `.mri_code/models.md`), so the user can switch with
  `/model` before launching it — e.g. "Next step → `/mri-code-devplan` (suggested model: **Opus**)".
- Skills are **local and self-contained**; there is no external plugin.

## At session start
Begin your first reply with the **welcome message** provided in the session context (the `welcome.sh`
hook: resume via `/mri-code-resume` if an unfinished `progress.md` exists, otherwise start via
`/mri-code-brainstorm`). Then **wait** for a command.

**First launch (new project) — mockups.** When the session context flags a first launch (no
`progress.md`, and no `.mri_code/assets/mockups/` folder yet), **before the first pipeline command,
ask the user once whether they have mockups / designs to import** (Figma links, images, PDFs, a local
folder). Then:
- **Yes** → copy the local files into `.mri_code/assets/mockups/`, and record any links plus a
  one-line-per-screen note in `.mri_code/assets/mockups/README.md`.
- **No** → still create `.mri_code/assets/mockups/` (with a `.gitkeep`) so this is asked only once.

Ask, then continue waiting for the entry command. See **Mockups** below for how they are used.

## Mockups
If `.mri_code/assets/mockups/` holds mockups, they are the **visual source of truth for the UI**.
`/mri-code-design` derives the screens, structure and states from them; `/mri-code-implement` builds
to match them and uses the visual-feedback MCP loop below to compare the running UI against them.
Absent that folder (or empty), there are simply no mockups — proceed normally.

## Commands (each is a skill `/mri-<name>`; suggests next)
Core flow:
- `/mri-code-issue` (alternate entry: start from a GitHub issue, enrich it if thin — writing the
  refinement back to the issue — then produce `brief.md`) → `/mri-code-design`
- `/mri-code-brainstorm` (facilitated brainstorming) → `/mri-code-forge` or `/mri-code-design`
- `/mri-code-forge` (pressure-test, persona panel) → `/mri-code-design` (HARDENED) or `/mri-code-brainstorm` (KILLED)
- `/mri-code-design` (the **bridge**: `brief.md` → `spec.md`) → `/mri-code-devplan`
- `/mri-code-devplan` (`spec.md` → `plan.md`) → a scaffold skill (new project) else `/mri-code-implement`
- `/mri-code-scaffold-*` (new project): the scaffold matching the constitution's stack → `/mri-code-implement`
- `/mri-code-implement` (TDD + MCP) → `/mri-code-review`
- `/mri-code-review` → `/mri-code-finish`
- `/mri-code-finish` (merge / PR / cleanup)

Optional (suggested at the right moment, then return to the flow):
- `/mri-code-elicit` (deepen an output) · `/mri-code-adversarial-review` (audit a doc)
- `/mri-code-market-research` · `/mri-code-domain-research` · `/mri-code-technical-research` (after forge)
- `/mri-code-document-project` (brownfield) · `/mri-code-debug` (test failure) · `/mri-code-meta-prompt` (standalone)
- `/mri-code-document-sync` (after a merge: update the separate documentation repo) · `/mri-code-resume` (resume the pipeline)

Internal sub-skills (invoked automatically by the flow, not user entry points): `mri-code-tdd`,
`mri-code-verify`, `mri-code-worktrees`.

## Resume & memory
State lives on disk: `.mri_code/docs/<project>/progress.md` (phases) + `plan.md` (fine-grained
checkboxes). To resume: `/mri-code-resume` re-reads `progress.md` and re-enters the current step. **Do not
rely on `/compact`.**

## Issue-driven journeys (source of truth)
When a journey is started by **`/mri-code-issue`**, the **GitHub issue is the source of truth** for the
brief and the technical design — they are **not** duplicated under `.mri_code/docs/`. Concretely:
- `progress.md` carries a `## Source` block (`issue #N`, URL, repo). **Its presence is how any skill
  knows the journey is issue-driven** — read `progress.md` first.
- Skills that would read `brief.md` read the **issue body** instead (`gh issue view N`).
- `/mri-code-design` writes the approved design **into the issue** — a `## Technical design (mri-code)`
  section appended to the issue body (edit gated by user approval) — instead of writing `spec.md`.
  `/mri-code-devplan` then reads that section as its input.
- **Only operational state stays local:** `progress.md` (phase tracker) and `plan.md` (task checkboxes).
  No `brief.md` / `spec.md` is written.
- `/mri-code-review` runs **on the Pull Request**: it opens the PR (linked to the issue) if needed and
  posts its findings **as PR review comments, like a human reviewer** — concrete fixes as GitHub
  `suggestion` blocks. It **does not auto-fix**; the user accepts/rejects on GitHub. Merging the PR
  (on GitHub, `Closes #N`) closes the issue.
- Idea-driven journeys (via `/mri-code-brainstorm`) are **unchanged** — `brief.md` / `spec.md` live
  locally as before. The mode is per-journey, decided by how it started.

## Documentation — split by coupling to the code
Decide where a doc lives by **how tightly it is coupled to the code**:
- **Code-coupled docs** — README, setup/run, env vars, service-specific ADRs, the API schema/OpenAPI
  generated from the code. They live **in the same repo as the code** and are updated **in the same
  PR** as the change, never deferred. A change that alters public behavior, setup, config or an API
  contract **must update them in the same commit**. `mri-code-implement` writes them with the code;
  `mri-code-review` checks they were updated.
- **Cross-cutting / product docs** — system architecture spanning services, the shared API reference
  other repos consume, product/user guides, onboarding, glossary. They live in the **separate
  documentation repo** and are synced **after merge** by `/mri-code-document-sync`.

Rule of thumb: if a doc only makes sense next to this codebase, keep it in-repo (same PR); if it
spans repos or is read by other teams, it belongs in the doc repo (document-sync). Do not push
code-coupled docs to the separate repo — they drift there.

## Constitution
Read and **respect** `.mri_code/constitution.md` (quality, tests, architecture, conventions). Its
*Stack* section is an empty placeholder until `/mri-code-scaffold-*` seals the chosen stack into it —
that is expected before scaffolding, not an omission to fix.

## Visual / runtime feedback
For a web UI, use the MCP servers (`.mcp.json`): **Playwright** (drive/test) + **Chrome DevTools**
(console/network/debug). Loop: write → run → observe → fix. **When mockups exist**
(`.mri_code/assets/mockups/`), the target of that loop is *matching the mockups*: compare the running
UI against them and close the gap.

## Model suggestions
At the end of each step, each command suggests a model (not enforced) per `.mri_code/models.md`
(architecture/brainstorm → Opus; code → Sonnet; etc.).

## Priority
1. User instructions (this file, `.mri_code/constitution.md`, direct requests).
2. `mri-code` skills. 3. Default behavior.
