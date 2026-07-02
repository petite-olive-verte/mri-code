---
name: mri-scaffold-python
description: Use when initializing/scaffolding the Python project structure (uv + ruff + pytest + mypy, src/ layout) from .mri_devtools/templates/python-uv, once the spec and plan are ready and before writing feature code. Respects .mri_devtools/constitution.md.
---

# Scaffolding a Python project (uv + ruff + pytest)

Generate the structure of a Python project from `.mri_devtools/templates/python-uv/`, respecting
`.mri_devtools/constitution.md`. To be used **after** the spec and plan, **before** writing feature code.

## Before starting
1. **Read `.mri_devtools/constitution.md`**: apply its stack and conventions. If they differ from the template,
   the constitution wins — adapt the generated files accordingly.
2. Determine two names (derive them from the spec, otherwise ask the user):
   - `PROJECT_NAME`: distribution name (may contain dashes), e.g. `todo-api`.
   - `PACKAGE_NAME`: Python import name, `snake_case`, e.g. `todo_api`.
   - `PROJECT_DESCRIPTION`: one sentence.

## Procedure
The project is generated **at the repo root** (the app lives in the same repository as the toolbox).
Do **not** overwrite any existing file: if a target file already exists (e.g. `README.md`,
`.gitignore`), keep the existing one and flag it to the user.

```bash
# From the repo root. Adapt the 3 variables.
PROJECT_NAME="todo-api"
PACKAGE_NAME="todo_api"
PROJECT_DESCRIPTION="Small todo API."

SRC=".mri_devtools/templates/python-uv"
# Copy the template files without overwriting the existing ones (-n), including hidden files.
cp -rn "$SRC/." . 2>/dev/null || true

# Rename the package
if [ -d "src/__PACKAGE_NAME__" ]; then
  mv "src/__PACKAGE_NAME__" "src/$PACKAGE_NAME"
fi

# Substitute the tokens in ALL project files (excluding .git/.venv)
grep -rlZ '__PACKAGE_NAME__\|__PROJECT_NAME__\|__PROJECT_DESCRIPTION__' . \
  --exclude-dir=.git --exclude-dir=.venv 2>/dev/null | \
  xargs -0 sed -i \
    -e "s/__PROJECT_DESCRIPTION__/$PROJECT_DESCRIPTION/g" \
    -e "s/__PROJECT_NAME__/$PROJECT_NAME/g" \
    -e "s/__PACKAGE_NAME__/$PACKAGE_NAME/g"
```

## Verification (mandatory before continuing)
```bash
uv sync                 # creates the env + installs the dev dependencies
uv run pytest -q        # the smoke test must pass (green)
uv run ruff check .     # clean lint
```
- If `pytest` or `ruff` fail, **fix before** moving on to implementation.
- Check that **no** `__PACKAGE_NAME__` / `__PROJECT_NAME__` token remains:
  `grep -rn '__P[A-Z_]*__' . --include='*.py' --include='*.toml'` must be empty.

## Next
Move on to implementation **in TDD** via **/mri-implement** (skill `mri-tdd` per task), feature by feature,
translating the **spec's acceptance criteria** into tests that fail first.
