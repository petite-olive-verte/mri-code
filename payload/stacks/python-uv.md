- **Python 3.12+**.
- **uv** for the environment and dependencies (never `pip`/`poetry`/`venv` by hand).
- **Ruff** for lint **and** format (no separate black/flake8/isort) — `uv run ruff check .`.
- **ty** (Astral) for type checking if available, otherwise **mypy** as a fallback.
- **pytest** (+ `pytest-cov`) for tests — `uv run pytest`.
- **pre-commit** for pre-commit guardrails.
- Centralized config in **`pyproject.toml`** (single source; no setup.cfg/requirements.txt).
- **Layout**: `src/` — code in `src/<package>/`, tests in `tests/`.
- **Naming**: `snake_case` for files/functions/variables, `PascalCase` for classes; one module
  `src/<package>/foo.py` ↔ one test file `tests/test_foo.py`.
