# Development

For working on the module itself, not for using it in a project.

## Layout

- `payload/` — the deployed content:
  - `skills/mri-code-*/` — one skill per directory, each with a `SKILL.md`.
  - `hooks/` — shell hooks (`welcome.sh`, `format.sh`, `lint-test.sh`).
  - `mcp/servers.json` — MCP server declarations.
  - `templates/<stack>/` — the project skeleton rendered by `mri-code-scaffold-<stack>`.
  - `stacks/<stack>.md` — the constitution's *Stack* fragment for that stack, sealed into
    `.mri_code/constitution.md` by the matching scaffold skill.
  - `constitution.md` — the stack-agnostic core, with an empty *Stack* placeholder.
  - `models.md`, `settings.json`.
- `mri_code_installer/main.py` — the whole installer (see [architecture.md](architecture.md)).
- `dev/` — internal design notes (in French, partly describing an earlier architecture).

## Dogfood

Self-install the module into this repo — generated artifacts are gitignored:

```bash
./install.sh .
```

## Adding a skill

1. Create `payload/skills/mri-code-<name>/SKILL.md`. The directory name must match the
   `name:` in the frontmatter.
2. User-facing skills set `disable-model-invocation: true` so they only run when the user
   invokes `/mri-code-<name>` — internal sub-skills omit it.
3. End the skill by suggesting the next command **and its recommended model** (keep
   `models.md` in sync).
4. Re-run the installer (or `./install.sh .`) to deploy it locally and test.
