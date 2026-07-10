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

Values are written to `.mri_code/config.json` and substituted into the `AGENTS.md`/`CLAUDE.md`
content the installer prints (see "Shared files" below — the target files themselves are never
written automatically). The skills themselves are always in English; only the agent's
communication/document language is configurable.

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

### Shared files: never modified automatically

`AGENTS.md`, `CLAUDE.md`, `.mcp.json` and `.claude/settings.json` may already exist in your
project, or be owned by another tool. The installer **never writes, creates or edits them** —
not even when they're absent. Instead, `install` and `update` print, for each of the 4 files, its
rendered content (placeholders substituted) plus a ready-to-paste prompt of the form
*"Intègre la configuration mri-code suivante dans `<dst>` : crée le fichier s'il n'existe pas,
sinon fusionne sans perturber le contenu existant."* — hand that to your coding agent, or apply it
by hand. `uninstall` prints the equivalent removal reminder. You stay in full control of these
files; the installer needs no LLM of its own to do this.

## What gets installed (copy only — no symlink)
```
my-project/
  .claude/  skills/ · hooks/            ← real files (copied, deterministic)
  .mri_code/                            ← config.json · constitution.md · models.md · templates/ · docs/<project>/
  .agents/skills/                       ← portable mirror (Codex)
```
`AGENTS.md`, `CLAUDE.md`, `.mcp.json` and `.claude/settings.json` are **not** part of this list —
see "Shared files" above: the installer only ever prints what they should contain. Your project
root stays **clean**: only your code + dotfiles. The install deposits **only the installation**,
not the whole repo (no `dev/`, no `.git`).

## Usage
When you open an agent, the welcome message lists the commands. Start with **`/mri-code-brainstorm`**, resume
with **`/mri-code-resume`**. The full flow and optional commands are described in `AGENTS.md`.

## Develop the module
Sources in `payload/`; internal docs in `dev/` (`MERGE_DESIGN.md`, `DECISIONS.md`, `BUILD_PLAN.md` —
in French, partly describing an earlier architecture). The installer itself is a single
self-contained module, `mri_code_installer/main.py`: no vendored engine, no external spec — the
deployment rules are inlined as plain Python constants and functions. Dogfood: `./install.sh .`
(self-install into this repo; generated artifacts are gitignored).

## License
MIT — see `LICENSE`.
