# Bootstrap — kickoff assistant (command-driven mode)

You are open in a repo that turns an idea into a working project — Python or PHP/Symfony — from
brainstorm to implementation, before human control. The methodology is the **`mri-code` module**
(self-contained skills in `.claude/skills/`). Generated artifacts live in `.mri_code/docs/<project>/`.

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

## Commands (each is a skill `/mri-<name>`; suggests next)
Core flow:
- `/mri-code-brainstorm` (facilitated brainstorming) → `/mri-code-forge` or `/mri-code-design`
- `/mri-code-forge` (pressure-test, persona panel) → `/mri-code-design` (HARDENED) or `/mri-code-brainstorm` (KILLED)
- `/mri-code-design` (the **bridge**: `brief.md` → `spec.md`) → `/mri-code-devplan`
- `/mri-code-devplan` (`spec.md` → `plan.md`) → a scaffold skill (new project) else `/mri-code-implement`
- Scaffold (new project, per the constitution's stack): `/mri-code-scaffold-python` ·
  `/mri-code-scaffold-symfony` · `/mri-code-scaffold-symfony-hexagonal` → `/mri-code-implement`
- `/mri-code-implement` (TDD + MCP) → `/mri-code-review`
- `/mri-code-review` → `/mri-code-finish`
- `/mri-code-finish` (merge / PR / cleanup)

Optional (suggested at the right moment, then return to the flow):
- `/mri-code-elicit` (deepen an output) · `/mri-code-adversarial-review` (audit a doc)
- `/mri-code-market-research` · `/mri-code-domain-research` · `/mri-code-technical-research` (after forge)
- `/mri-code-document-project` (brownfield) · `/mri-code-debug` (test failure) · `/mri-code-meta-prompt` (standalone)
- `/mri-code-resume` (resume the pipeline)

Internal sub-skills (invoked automatically by the flow, not user entry points): `mri-code-tdd`,
`mri-code-verify`, `mri-code-worktrees`.

## Resume & memory
State lives on disk: `.mri_code/docs/<project>/progress.md` (phases) + `plan.md` (fine-grained
checkboxes). To resume: `/mri-code-resume` re-reads `progress.md` and re-enters the current step. **Do not
rely on `/compact`.**

## Constitution
Read and **respect** `.mri_code/constitution.md` (stack, quality, tests, architecture, conventions).

## Visual / runtime feedback
For a web UI, use the MCP servers (`.mcp.json`): **Playwright** (drive/test) + **Chrome DevTools**
(console/network/debug). Loop: write → run → observe → fix.

## Model suggestions
At the end of each step, each command suggests a model (not enforced) per `.mri_code/models.md`
(architecture/brainstorm → Opus; code → Sonnet; etc.).

## Priority
1. User instructions (this file, `.mri_code/constitution.md`, direct requests).
2. `mri-code` skills. 3. Default behavior.
