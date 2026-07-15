# Skills

Every step of `mri-code` is a **skill** invoked as a slash command `/mri-code-<name>`.
The user-facing skills carry `disable-model-invocation: true`, so the agent never triggers
them on its own — **you launch each one**. At the end of a step the agent suggests the next
command *and the model to run it with* (per `.mri_code/models.md`), so you can switch with
`/model` before launching. The skills are vendored locally in `.claude/skills/`; there is
no external plugin at runtime.

![Full skill map](diagrams/skills-map.svg)

<sub>Core flow (left), on-demand skills (right), internal sub-skills (bottom).</sub>

## Core flow

The happy path from idea to shipped code. Each step reads the previous step's artifact and
writes the next.

| Command | Does | In → out |
|---|---|---|
| `/mri-code-brainstorm` | Facilitated, challenging brainstorming — the agent draws ideas out of you, pushes on assumptions, then converges. | idea → `brief.md` |
| `/mri-code-forge` | Pressure-tests the idea through a fixed multi-persona panel until it hardens, clarifies, or dies cheaply. | `brief.md` → *hardened* / *killed* |
| `/mri-code-design` | The analysis→execution **bridge**: takes product intent as given and designs the architecture. Runs in plan mode. | `brief.md` → `spec.md` |
| `/mri-code-devplan` | Breaks the spec into an ordered plan of independent, checkable tasks. Runs in plan mode. | `spec.md` → `plan.md` |
| `/mri-code-scaffold-*` | Scaffolds the project skeleton from a template, matching the stack in the constitution. New projects only. One skill per supported stack — see [Scaffold skills](#scaffold-skills). | `plan.md` → project skeleton |
| `/mri-code-implement` | Executes the plan task by task with TDD and MCP visual feedback. Drives the internal sub-skills. | `plan.md` → code + tests |
| `/mri-code-review` | Verifies the work meets the spec and plan before integration. | code → review findings |
| `/mri-code-finish` | Completes the work: merge, PR, or cleanup. | reviewed code → integrated |

## On-demand skills

Suggested at the right moment, then you return to the flow.

| Command | Does | When |
|---|---|---|
| `/mri-code-elicit` | Reconsiders and deepens the last output (Socratic, first principles, pre-mortem, red-team…). | any output feels thin |
| `/mri-code-adversarial-review` | Cynical audit of a document (brief, spec, plan, diff) → findings report; looks for what's missing as much as what's wrong. | before trusting a doc |
| `/mri-code-market-research` | Market research (competition, customers, trends) on current web data, with cited sources. | after forge |
| `/mri-code-domain-research` | Domain/industry research: expertise, terminology, patterns, regulatory constraints. | after forge |
| `/mri-code-technical-research` | Technical research: feasibility, architecture options, libraries, integration patterns. | after forge |
| `/mri-code-document-project` | Documents an existing (brownfield) project — structure, stack, conventions, how to run/test — to give the agent context. | ahead of brainstorm, on an existing repo |
| `/mri-code-debug` | Systematic root-cause investigation before proposing fixes. | a bug or failing test |
| `/mri-code-meta-prompt` | Turns a vague request into a precise, ready-to-use prompt. Standalone — outside the pipeline. | anytime |
| `/mri-code-resume` | Re-reads `progress.md` and re-enters the current step. | resuming a session |

## Scaffold skills

One `mri-code-scaffold-*` skill per supported stack, chosen after `devplan` to match the
constitution. New projects only; each renders its template into the repo. More can be added over
time without changing the flow above.

| Skill | Scaffolds |
|---|---|
| `/mri-code-scaffold-python` | A Python project — uv + ruff + pytest + mypy, `src/` layout. |
| `/mri-code-scaffold-symfony` | A Symfony project — latest stable PHP/Symfony, PHPStan max, PHP-CS-Fixer, PHPUnit, Doctrine. |
| `/mri-code-scaffold-symfony-hexagonal` | A Symfony project with a hexagonal (ports & adapters) layout — pure Domain / Application / Infrastructure, Doctrine XML mapping. |

## Internal sub-skills

Invoked automatically by the flow (mainly by `implement`) — not user entry points.

| Skill | Does |
|---|---|
| `mri-code-tdd` | Red → green → refactor discipline for every feature or bugfix. |
| `mri-code-verify` | Runs verification commands and confirms output before any success claim — evidence before assertions. |
| `mri-code-worktrees` | Ensures an isolated workspace (native tools, or a git worktree fallback) before implementation. |

## Where the work lives

Generated artifacts are written to `.mri_code/docs/<project>/`:

- `brief.md`, `spec.md`, `plan.md` — the outputs of brainstorm/design/devplan.
- `progress.md` — the phase tracker `/mri-code-resume` reads to pick the pipeline back up.

State lives on disk, not in the conversation — so a session can end and resume cleanly. How
this is wired into the deployed module is covered in **[architecture.md](architecture.md)**.
