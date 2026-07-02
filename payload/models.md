# Model suggestions per step (not enforced, editable)

> The `mri-*` commands display a model **suggestion** at the end of each step (never imposed). Adapt
> this table to your providers/budget. Principle: **expensive "brain" model** for architecture/reasoning,
> **economical "arm" model** for high-volume code.

| Step / command | Task type | Suggested model | Why |
|---|---|---|---|
| `/mri-brainstorm` | ideation / framing | **Opus** | open-ended reasoning, challenge |
| `/mri-forge` | adversarial pressure-test | **Opus** | multi-persona argumentation |
| `/mri-design` | architecture | **Opus** | multi-file design, trade-offs |
| `/mri-devplan` | planning | **Opus** | task breakdown, complete code |
| `/mri-elicit`, `/mri-adversarial-review` | critique / audit | **Opus** | depth of critique |
| `/mri-meta-prompt` | meta-prompting | **Opus** | precise reformulation |
| `/mri-*-research` | web research | **Sonnet** | fast, sourced synthesis |
| `/mri-scaffold-python` | mechanical | **Sonnet / DeepSeek-v4** | deterministic, little reasoning |
| `/mri-implement` | high-volume code (TDD) | **Sonnet / DeepSeek-v4** | economical, iterative |
| `/mri-debug` | debugging | **Sonnet / DeepSeek-v4** | short cycles; Opus for a stubborn cause |
| `/mri-review` | code review | **Sonnet** (or **Opus** if demanding) | critical reading |
| `/mri-finish` | git integration | any | mechanical |

## Providers
- **Opus / Sonnet**: native Claude Code (`/model`).
- **DeepSeek-v4**: excellent cost/efficiency ratio for code — to be added as a provider in Claude
  Code (see the provider config). A good default "arm" when budget matters.

> Nothing is automatic: these are *suggestions*. Switch models with `/model` if you wish.
