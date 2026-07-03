# Model suggestions per step (not enforced, editable)

> The `mri-*` commands display a model **suggestion** at the end of each step (never imposed). Adapt
> this table to your providers/budget. Principle: **expensive "brain" model** for architecture/reasoning,
> **economical "arm" model** for high-volume code.

| Step / command | Task type | Suggested model | Why |
|---|---|---|---|
| `/mri-brainstorm` | ideation / framing | **Opus** | open-ended reasoning, challenge |
| `/mri-forge` | adversarial pressure-test | **Opus** | multi-persona argumentation |
| `/mri-design` | architecture | **Opus** | multi-file design, trade-offs |
| `/mri-devplan` | planning | **Opus** | task breakdown, interfaces & contracts |
| `/mri-elicit`, `/mri-adversarial-review` | critique / audit | **Opus** | depth of critique |
| `/mri-meta-prompt` | meta-prompting | **Opus** | precise reformulation |
| `/mri-*-research` | web research | **Sonnet** | fast, sourced synthesis |
| `/mri-scaffold-python` | mechanical | **Sonnet** | deterministic, little reasoning |
| `/mri-implement` | high-volume code (TDD) | **Sonnet** | economical, iterative |
| `/mri-debug` | debugging | **Sonnet** | short cycles; Opus for a stubborn cause |
| `/mri-review` | code review | **Sonnet** (or **Opus** if demanding) | critical reading |
| `/mri-finish` | git integration | any | mechanical |

## Providers
- **Opus / Sonnet**: native Claude Code — switch with `/model`.
- Principle: **Opus** for architecture/reasoning steps, **Sonnet** for high-volume code and mechanical
  work. Adjust the table to your own budget and providers.

> Nothing is automatic: these are *suggestions*. Switch models with `/model` if you wish.
