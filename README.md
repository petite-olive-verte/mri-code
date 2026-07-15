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

**Turn an idea into a shipped Python or PHP/Symfony project, one command at a time.**

`mri-code` drops a set of self-contained skills into your project so a coding agent can
walk the whole path — from a fuzzy idea to reviewed, tested code — as a sequence of slash
commands *you* drive. You stay in the loop at every step; the agent brings the method.

<p align="center">
  <img src="docs/diagrams/pipeline.svg" alt="mri-code pipeline: brainstorm → forge → design → devplan → scaffold → implement → review → finish" width="340">
</p>

<p align="center"><sub>The core flow. <a href="docs/skills.md">Click here</a> to watch the full flow with all the skills.</sub></p>

## Quickstart

```bash
cd my-project
uvx --from git+https://github.com/MatioRIGARD/mri-code.git mri-code
```

That copies the skills into `my-project/`. Open a coding agent, then start with
**`/mri-code-brainstorm`** — each step suggests the next one. Resume anytime with
**`/mri-code-resume`**.

> Flags, versions, `update` / `uninstall`, and the no-`uv` path → **[docs/installation.md](docs/installation.md)**.

## What you get

- **A command-driven pipeline** — `brainstorm → forge → design → devplan → scaffold → implement → review → finish`, plus on-demand research, audit, and debug skills. You launch each step and keep control.
- **Work that survives the session** — brief, spec, plan and progress are written to `.mri_code/docs/<project>/`, so you can stop and `/mri-code-resume` later.
- **Quality baked in** — TDD-per-task, a review gate, and MCP visual feedback (Playwright + Chrome DevTools) for web UIs.
- **Your repo stays clean** — skills are copied as plain files; shared files like `AGENTS.md` / `CLAUDE.md` are written *only if absent* (an existing one is never touched), and `.mcp.json` is deep-merged — so mri-code drops cleanly into an existing project without clobbering what you own.

See the full catalogue and how the skills fit together → **[docs/skills.md](docs/skills.md)**.

## Documentation

- **[Installation](docs/installation.md)** — every install option, configuration, update & uninstall.
- **[Skills](docs/skills.md)** — the full skill map and what each one does.
- **[Architecture](docs/architecture.md)** — how the module is built and deployed.

## License

[MIT](LICENSE) — © 2026 Mathieu RIGARD.
