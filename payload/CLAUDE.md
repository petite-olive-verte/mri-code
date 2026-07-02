# CLAUDE.md

This project is driven by `AGENTS.md` (portable bootstrap). Read it and apply it.

@AGENTS.md

## Claude Code specifics

- **Skills**: invoke skills via the `Skill` tool (do not read `SKILL.md` files by hand).
  The module's skills are **local and self-contained** in `.claude/skills/mri-*` (prefix `mri-`).
- **Plan mode**: use plan mode for the "Design" step (human validation before implementation).
- **Subagents**: prefer specialized subagents for exploration and isolated implementation (keep the
  main context short). `mri-implement` relies on them (TDD per task).
- **Self-contained**: the `mri` skills are vendored locally in `.claude/skills/` — there is no external
  plugin at runtime.
