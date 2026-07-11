# Installation

`mri-code` is **source-first**: the installable content lives in `payload/`, and the
installer at the repo root copies it into a target project. Nothing is symlinked — the
target gets plain, deterministic files.

## Recommended: one command

```bash
cd my-project
uvx --from git+https://github.com/MatioRIGARD/mri-code.git mri-code
```

[`uv`](https://docs.astral.sh/uv/) fetches the installer and runs it against the current
directory. Pin a version, or pass configuration up front:

```bash
# pin a released version
uvx --from git+https://github.com/MatioRIGARD/mri-code.git@v0.1.0 mri-code

# configure non-interactively
uvx --from git+https://github.com/MatioRIGARD/mri-code.git mri-code \
    --lang English --doc-lang English --user Alice
```

> Installing from a **private** fork? Swap `git+https` for `git+ssh://git@github.com/...`
> so `uv` authenticates with your SSH key instead of prompting for a token.

## Alternative: clone + script (plain Python 3, no uv)

```bash
git clone https://github.com/MatioRIGARD/mri-code.git
./mri-code/install.sh my-project --lang English --user Alice
```

## Configuration

Asked interactively when omitted, or passed as flags:

| Flag | Meaning | Default |
|---|---|---|
| `--lang` | language the agent speaks to you | `English` |
| `--doc-lang` | language of generated documents (brief/spec/plan…) | = `--lang` |
| `--user` | how the agent addresses you | (unset) |

Values are written to `.mri_code/config.json` and read at the start of each session. The
skills themselves are always in English; only the agent's communication and document
language are configurable.

## Update & uninstall

Same single-command pattern, via subcommands:

```bash
cd my-project

# update — re-deploys in place, reusing the target's existing config
uvx --from git+https://github.com/MatioRIGARD/mri-code.git mri-code update
# or from a local clone:  ./mri-code/update.sh my-project

# uninstall — removes everything the install/update deposited (asks to confirm)
uvx --from git+https://github.com/MatioRIGARD/mri-code.git mri-code uninstall
# or:  ./mri-code/uninstall.sh my-project [--yes]
```

`update` keeps `--lang` / `--doc-lang` / `--user` from `.mri_code/config.json` unless you
pass new values, and removes any file that existed in the previous version but not the new
one. `.mri_code/docs/` — the brief/spec/plan the agent produces — is **never** touched by
either command, whatever flags you pass.

## What gets installed

```
my-project/
  .claude/  skills/ · hooks/            ← real files (copied, deterministic)
  .mri_code/                            ← config.json · constitution.md · models.md · templates/ · docs/<project>/
  .agents/skills/                       ← portable mirror (for Codex)
```

The install deposits **only the installation**, not the whole repo — no `dev/`, no `.git`.
Your project root stays clean: your code plus these dotfiles.

## Shared files: handled non-destructively

`AGENTS.md`, `CLAUDE.md`, `.mcp.json` and `.claude/settings.json` may already exist in your
project, or be owned by another tool. The installer handles them **without ever clobbering
your content**, so mri-code drops cleanly into an existing repo:

- **`AGENTS.md`, `CLAUDE.md`, `.claude/settings.json` → written only if absent.** If the file
  already exists it is **left untouched** (a one-line note is printed so you can fold in the
  mri-code section by hand if you want the full command-driven pipeline).
- **`.mcp.json` → deep-merged.** The two servers (`playwright`, `chrome-devtools`) are added
  only when missing; a server another tool already registered under the same name is never
  overwritten. Re-running is a no-op.

The manifest records exactly what the installer created, so `uninstall` reverses **only** that:
a shared doc is deleted only if it is still byte-for-byte what was written (an edited one is
kept), and only the installer's own MCP servers are stripped from `.mcp.json`. No LLM needed —
the rules are plain Python.

For how these pieces are produced and deployed, see **[architecture.md](architecture.md)**.
