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
npx git+ssh://git@github.com/MatioRIGARD/mri-code.git                       # install into the current dir
# pin a version:  npx git+ssh://git@github.com/MatioRIGARD/mri-code.git#v0.1.0
# with config:    npx git+ssh://git@github.com/MatioRIGARD/mri-code.git -- --lang English --doc-lang English --user Alice
```
> `curl … | bash` does **not** work here: the repo is private (raw needs auth). `npx` over `git+ssh`
> uses the collaborator's **SSH key** (access already granted) — no token to manage.

**Alternative without Node (clone + script):**
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
npx git+ssh://git@github.com/MatioRIGARD/mri-code.git update
# or, from a local clone:
./mri-code/update.sh my-project

# uninstall — removes everything the install/update deposited, asks for confirmation
npx git+ssh://git@github.com/MatioRIGARD/mri-code.git uninstall
# or:
./mri-code/uninstall.sh my-project
# skip the confirmation prompt: add --yes (append flags after `--` in the npx form)
./mri-code/uninstall.sh my-project --yes
```

`update` keeps `--lang`/`--doc-lang`/`--user` from `.mri_code/config.json` unless you pass new
values, and removes any file that existed in the previous version but not in the new one.
`.mri_code/docs/` — the brief/spec/plan/etc. the agent produces while you work — is **never**
touched by either command, no matter what flags are passed.

## What gets installed (copy only — no symlink)
```
my-project/
  AGENTS.md  CLAUDE.md  .mcp.json      ← entries (required at root by Claude Code)
  .claude/  commands/ (flat) · skills/ · hooks/ · settings.json   ← real files (copied)
  .mri_code/                           ← config.json · constitution.md · models.md · templates/ · docs/<project>/
  .agents/skills/                      ← portable mirror (Codex)
```
Your project root stays **clean**: only your code + dotfiles. The install deposits **only the
installation**, not the whole repo (no `dev/`, no `bin/`, no `.git`).

## Usage
When you open an agent, the welcome message lists the commands. Start with **`/mri-code-brainstorm`**, resume
with **`/mri-code-resume`**. The full flow and optional commands are described in `AGENTS.md`.

## Develop the module
Sources in `payload/`; internal docs in `dev/` (`MERGE_DESIGN.md`, `DECISIONS.md`, `BUILD_PLAN.md` —
in French). Dogfood: `./install.sh .` (self-install into this repo; generated artifacts are gitignored).

## License
MIT — see `LICENSE`.
