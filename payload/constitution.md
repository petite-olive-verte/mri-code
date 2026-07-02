# Project constitution

> **The non-negotiable rulebook for this project.** The agent reads it every session and complies with it.
> The spec says *what* to build; this constitution says *what "well done" means here*.
> **Edit this file** to enforce your preferences — it takes precedence over the agent's default habits.

## Stack (non-negotiable)
- **Python 3.12+**.
- **uv** for the environment and dependencies (never `pip`/`poetry`/`venv` by hand).
- **Ruff** for lint **and** format (no separate black/flake8/isort).
- **ty** (Astral) for type checking if available, otherwise **mypy** as a fallback.
- **pytest** (+ `pytest-cov`) for tests.
- **pre-commit** for pre-commit guardrails.
- Centralized config in **`pyproject.toml`** (single source; no setup.cfg/requirements.txt).

## Code quality
- All public code is **typed**; `ruff check` and the type checker must pass (zero errors).
- Docstrings on public modules and functions (short style, no essays).
- Prefer small functions and **composition** over inheritance.
- No hardcoded secrets; configuration via environment variables (`.env`, not committed).
- No bare `except`; handle errors explicitly.

## Tests (TDD mandatory)
- **Red-Green-Refactor**: write a failing test **before** the implementation.
- The human / the spec owns the test's **intent**; the agent owns the **implementation**.
- The **spec's acceptance criteria become tests**.
- Target coverage **≥ 80%**; at least one integration test per public entry point (API/CLI).
- Tests must pass (`pytest`) and lint must be clean before considering a task done.

## Architecture
- **`src/`** layout: code in `src/<package>/`, tests in `tests/`.
- The **business logic** does not import the web framework / I/O (keep the core testable).
- Dependencies point inward (I/O and frameworks at the edges).

## Structure & naming
- `tests/` **mirrors** `src/` (one module ↔ one test file `test_<module>.py`).
- `snake_case` for files/functions/variables, `PascalCase` for classes.
- Documentation and spec artifacts in `docs/` (`docs/specs/<feature>/`).

## Workflow
- Small, atomic commits, with an imperative message describing the *why*.
- Never `git push --force`; never commit secrets or the `.venv` directory.
