---
name: mri-code-scaffold-python
description: Use when initializing/scaffolding the Python project structure (uv + ruff + pytest + mypy, src/ layout) from .mri_code/templates/python-uv, once the spec and plan are ready and before writing feature code. Respects .mri_code/constitution.md.
disable-model-invocation: true
---

# mri-code-scaffold-python — scaffold a Python project (uv + ruff + pytest)

> ┌─ mri devtools ─┐

Generate the structure of a Python project from `.mri_code/templates/python-uv/`, respecting
`.mri_code/constitution.md`. To be used **after** the spec and plan, **before** writing feature code.

## Before starting
1. **Read `.mri_code/constitution.md`**: apply its stack and conventions. If they differ from the template,
   the constitution wins — adapt the generated files accordingly.
2. Determine two names (derive them from the spec, otherwise ask the user):
   - `PROJECT_NAME`: distribution name (may contain dashes), e.g. `todo-api`.
   - `PACKAGE_NAME`: Python import name, `snake_case`, e.g. `todo_api`.
   - `PROJECT_DESCRIPTION`: one sentence.

## Procedure
The project is generated **at the repo root** (the app lives in the same repository as the toolbox).
Do **not** overwrite any existing file: if a target file already exists (e.g. `README.md`,
`.gitignore`), keep the existing one and flag it to the user.

> ⚠️ **Never run `sed -i` across the repo root.** The token substitution must happen in an **isolated
> staging copy** — otherwise it rewrites the shared template source (`.mri_code/templates/`), the
> skills that document these tokens (`.claude/skills/`, `.agents/skills/`), and your own files, poisoning
> every future scaffold. Render in staging, then copy the finished project in without overwriting.

```bash
# From the repo root. Adapt the 3 variables.
PROJECT_NAME="todo-api"
PACKAGE_NAME="todo_api"
PROJECT_DESCRIPTION="Small todo API."   # avoid the '/' character (sed delimiter)

SRC=".mri_code/templates/python-uv"

# 1) Render the template in an ISOLATED staging dir. Substitution can only ever touch this copy.
STAGE="$(mktemp -d)"
cp -r "$SRC/." "$STAGE/"                       # includes hidden files

# 2) Rename the package placeholder dir INSIDE the stage
if [ -d "$STAGE/src/__PACKAGE_NAME__" ]; then
  mv "$STAGE/src/__PACKAGE_NAME__" "$STAGE/src/$PACKAGE_NAME"
fi

# 3) Substitute the tokens — scoped to "$STAGE" only, never the repo root
grep -rlZ '__PACKAGE_NAME__\|__PROJECT_NAME__\|__PROJECT_DESCRIPTION__' "$STAGE" 2>/dev/null | \
  xargs -0 -r sed -i \
    -e "s/__PROJECT_DESCRIPTION__/$PROJECT_DESCRIPTION/g" \
    -e "s/__PROJECT_NAME__/$PROJECT_NAME/g" \
    -e "s/__PACKAGE_NAME__/$PACKAGE_NAME/g"

# 4) Copy the rendered project into the repo WITHOUT overwriting existing files (-n)
cp -rn "$STAGE/." .
rm -rf "$STAGE"
```

## Verification (mandatory before continuing)
```bash
uv sync                 # creates the env + installs the dev dependencies
uv run pytest -q        # the smoke test must pass (green)
uv run ruff check .     # clean lint
```
- If `pytest` or `ruff` fail, **fix before** moving on to implementation.
- Check that **no** placeholder token remains in the **generated project** — exclude the toolbox dirs,
  whose template/skill sources keep the placeholders on purpose:
  `grep -rn '__P[A-Z_]*__' . --include='*.py' --include='*.toml' --exclude-dir=.mri_code --exclude-dir=.claude --exclude-dir=.agents --exclude-dir=.git --exclude-dir=.venv`
  must be empty.

## Next
Move on to implementation **in TDD** via **/mri-code-implement** (skill `mri-code-tdd` per task), feature by feature,
translating the **spec's acceptance criteria** into tests that fail first.

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Sonnet (mechanical) — see `.mri_code/models.md`.
