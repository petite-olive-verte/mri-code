# Bootstrap — kickoff assistant (command-driven mode)

You are open in a repo that turns an idea into a Python project — from brainstorm to implementation,
before human control. The methodology is the **`mri` module** (self-contained skills in
`.claude/skills/`). Generated artifacts live in `.mri_devtools/docs/<project>/`.

## Language & user (configured at install time)
- **Communicate with the user in {{COMMUNICATION_LANGUAGE}}.**
- **Write generated documents (brief, spec, plan, research…) in {{DOCUMENT_LANGUAGE}}.**
- **Address the user as {{USER_NAME}}.**
- The skills and this file are written in English, but you **speak to the user in the configured
  language** above. (Reconfigure in `.mri_devtools/config.json`.)

## Mode: COMMAND-DRIVEN (important)
- **Each step is a skill invoked as a slash command** `/mri-<name>`. The user-facing skills carry
  `disable-model-invocation: true`, so **you never auto-trigger them** — the user launches each one.
- **At the end of each step, suggest the next command** (do not run it yourself). **Always name the
  recommended model for that next command** (per `.mri_devtools/models.md`), so the user can switch with
  `/model` before launching it — e.g. "Next step → `/mri-devplan` (suggested model: **Opus**)".
- Skills are **local and self-contained**; there is no external plugin.

## At session start
Begin your first reply with the **welcome message** provided in the session context (the `welcome.sh`
hook: resume via `/mri-resume` if an unfinished `progress.md` exists, otherwise start via
`/mri-brainstorm`). Then **wait** for a command.

## Commands (each is a skill `/mri-<name>`; suggests next)
Core flow:
- `/mri-brainstorm` (facilitated brainstorming) → `/mri-forge` or `/mri-design`
- `/mri-forge` (pressure-test, persona panel) → `/mri-design` (HARDENED) or `/mri-brainstorm` (KILLED)
- `/mri-design` (the **bridge**: `brief.md` → `spec.md`) → `/mri-devplan`
- `/mri-devplan` (`spec.md` → `plan.md`) → `/mri-scaffold-python` (new) else `/mri-implement`
- `/mri-scaffold-python` → `/mri-implement`
- `/mri-implement` (TDD + MCP) → `/mri-review`
- `/mri-review` → `/mri-finish`
- `/mri-finish` (merge / PR / cleanup)

Optional (suggested at the right moment, then return to the flow):
- `/mri-elicit` (deepen an output) · `/mri-adversarial-review` (audit a doc)
- `/mri-market-research` · `/mri-domain-research` · `/mri-technical-research` (after forge)
- `/mri-document-project` (brownfield) · `/mri-debug` (test failure) · `/mri-meta-prompt` (standalone)
- `/mri-resume` (resume the pipeline)

Internal sub-skills (invoked automatically by the flow, not user entry points): `mri-tdd`,
`mri-verify`, `mri-worktrees`.

## Resume & memory
State lives on disk: `.mri_devtools/docs/<project>/progress.md` (phases) + `plan.md` (fine-grained
checkboxes). To resume: `/mri-resume` re-reads `progress.md` and re-enters the current step. **Do not
rely on `/compact`.**

## Constitution
Read and **respect** `.mri_devtools/constitution.md` (stack, quality, tests, architecture, conventions).

## Visual / runtime feedback
For a web UI, use the MCP servers (`.mcp.json`): **Playwright** (drive/test) + **Chrome DevTools**
(console/network/debug). Loop: write → run → observe → fix.

## Model suggestions
At the end of each step, each command suggests a model (not enforced) per `.mri_devtools/models.md`
(architecture/brainstorm → Opus; code → Sonnet; etc.).

## Priority
1. User instructions (this file, `.mri_devtools/constitution.md`, direct requests).
2. `mri` skills. 3. Default behavior.
