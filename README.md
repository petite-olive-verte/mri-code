```
 ███╗   ███╗██████╗ ██╗        ██████╗ ██████╗ ██████╗ ███████╗
 ████╗ ████║██╔══██╗██║       ██╔════╝██╔═══██╗██╔══██╗██╔════╝
 ██╔████╔██║██████╔╝██║ █████ ██║     ██║   ██║██║  ██║█████╗  
 ██║╚██╔╝██║██╔══██╗██║ ╚═══╝ ██║     ██║   ██║██║  ██║██╔══╝  
 ██║ ╚═╝ ██║██║  ██║██║       ╚██████╗╚██████╔╝██████╔╝███████╗
 ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝        ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
                        idea → shipped
```

# mri-code

A **command-driven** module that turns an idea into a Python project with a coding agent:
`brainstorm → forge → design → devplan → scaffold → TDD implementation → review → finish`, with visual
(MCP) feedback for web UIs.

This repo is **source-first**: the installable content lives in `payload/`; the installer at the root
deploys it into a target project.

## Install into a project (private repo → collaborators)

**One command (recommended, no curl, over SSH):**
```bash
cd my-project
uvx --from git+ssh://git@github.com/MatioRIGARD/mri-code.git mri-code                       # install into the current dir
# pin a version:  uvx --from git+ssh://git@github.com/MatioRIGARD/mri-code.git@v0.1.0 mri-code
# with config:    uvx --from git+ssh://git@github.com/MatioRIGARD/mri-code.git mri-code --lang English --doc-lang English --user Alice
```
> `curl … | bash` does **not** work here: the repo is private (raw needs auth). `uvx` over
> `git+ssh` uses the collaborator's **SSH key** (access already granted) — no token to manage.

**Alternative without uv (clone + script, plain Python 3):**
```bash
git clone git@github.com:MatioRIGARD/mri-code.git
./mri-code/install.sh my-project --lang English --user Alice
```

### Configuration (asked interactively, or via flags)
| Flag | Meaning | Default |
|---|---|---|
| `--lang` | language the agent speaks to you | `English` |
| `--doc-lang` | language of generated documents (brief/spec/plan…) | = `--lang` |
| `--user` | how the agent addresses you | (unset) |

Values are written to `.mri_code/config.json` and injected into the target `AGENTS.md`. The skills
themselves are always in English; only the agent's communication/document language is configurable.

## Update / uninstall

Same single-command pattern as the install, via subcommands:

```bash
# update — re-deploys the module in place, reusing the target's existing config
cd my-project
uvx --from git+ssh://git@github.com/MatioRIGARD/mri-code.git mri-code update
# or, from a local clone:
./mri-code/update.sh my-project

# uninstall — removes everything the install/update deposited, asks for confirmation
uvx --from git+ssh://git@github.com/MatioRIGARD/mri-code.git mri-code uninstall
# or:
./mri-code/uninstall.sh my-project
# skip the confirmation prompt:
./mri-code/uninstall.sh my-project --yes
```

`update` keeps `--lang`/`--doc-lang`/`--user` from `.mri_code/config.json` unless you pass new
values, and removes any file that existed in the previous version but not in the new one.
`.mri_code/docs/` — the brief/spec/plan/etc. the agent produces while you work — is **never**
touched by either command, no matter what flags are passed.

### Coexisting with other `mri-*` modules in the same project

`AGENTS.md`, `CLAUDE.md`, `.mcp.json` and `.claude/settings.json` are **shared, not overwritten**:
mri-code contributes its own delimited block/entries into them (via
[mri-installer-kit](https://github.com/MatioRIGARD/mri-installer-kit)) without touching what
another `mri-*` module — or you — put there. Uninstalling mri-code only ever removes mri-code's
own contribution.

## What gets installed (copy only — no symlink)
```
my-project/
  AGENTS.md  CLAUDE.md  .mcp.json      ← entries (required at root by Claude Code), shared-safe
  .claude/  skills/ · hooks/ · settings.json (merged)   ← real files (copied)
  .mri_code/                           ← config.json · constitution.md · models.md · templates/ · docs/<project>/
  .agents/skills/                      ← portable mirror (Codex)
```
Your project root stays **clean**: only your code + dotfiles. The install deposits **only the
installation**, not the whole repo (no `dev/`, no `.git`).

## Usage
When you open an agent, the welcome message lists the commands. Start with **`/mri-code-brainstorm`**, resume
with **`/mri-code-resume`**. The full flow and optional commands are described in `AGENTS.md`.

## Develop the module
Sources in `payload/`; internal docs in `dev/` (`MERGE_DESIGN.md`, `DECISIONS.md`, `BUILD_PLAN.md` —
in French). The installer itself (`mri_code_installer/`) is a thin `Spec` on top of the generic
engine vendored at `.mri-installer-kit/` (from
[mri-installer-kit](https://github.com/MatioRIGARD/mri-installer-kit) — see that repo's README for
the contract). Refresh the vendored copy by rerunning mri-installer-kit's own installer against
this repo: `path/to/mri-installer-kit/install.sh .`. Dogfood: `./install.sh .` (self-install into
this repo; generated artifacts are gitignored).

## License
MIT — see `LICENSE`.
