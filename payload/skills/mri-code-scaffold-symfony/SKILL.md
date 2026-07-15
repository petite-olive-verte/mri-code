---
name: mri-code-scaffold-symfony
description: Use when initializing/scaffolding a Symfony project structure (latest stable PHP + Symfony + Composer + PHPStan + PHP-CS-Fixer + PHPUnit + Doctrine) from .mri_code/templates/symfony, once the spec and plan are ready and before writing feature code. For a ports-and-adapters layout use mri-code-scaffold-symfony-hexagonal instead. Respects .mri_code/constitution.md.
disable-model-invocation: true
---

# mri-code-scaffold-symfony — scaffold a Symfony project (latest stable PHP + Composer + PHPUnit)

> ┌─ mri devtools ─┐

Generate the structure of a Symfony project from `.mri_code/templates/symfony/`, respecting
`.mri_code/constitution.md`. To be used **after** the spec and plan, **before** writing feature code.

> Want a **hexagonal / ports-and-adapters** layout (Domain / Application / Infrastructure)? Use
> **/mri-code-scaffold-symfony-hexagonal** instead — it lays down the layered skeleton and the rules
> the implementation must follow.

## Before starting
1. **Read `.mri_code/constitution.md`**: apply its stack and conventions. If they differ from the template,
   the constitution wins — adapt the generated files accordingly.
2. **If the constitution still describes the default Python stack** (it mentions `uv`/`ruff`/`pytest` and
   no PHP), the project is going PHP: **rewrite its "Stack" section** to the Symfony one before scaffolding
   — see *Align the constitution* below. Leave the quality/tests/architecture principles intact (they are
   language-agnostic and already favor a testable, framework-decoupled core).
3. Determine two names (derive them from the spec, otherwise ask the user):
   - `PROJECT_NAME`: Composer package name — **lowercase**, may contain dashes, e.g. `todo-api`
     (becomes `app/todo-api` in `composer.json`).
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
# From the repo root. Adapt the 2 variables.
PROJECT_NAME="todo-api"                        # lowercase, dashes ok
PROJECT_DESCRIPTION="Small todo API."          # avoid the '/' character (sed delimiter)

SRC=".mri_code/templates/symfony"

# 1) Render the template in an ISOLATED staging dir. Substitution can only ever touch this copy.
STAGE="$(mktemp -d)"
cp -r "$SRC/." "$STAGE/"                        # includes hidden files

# 2) Substitute the tokens — scoped to "$STAGE" only, never the repo root
grep -rlZ '__PROJECT_NAME__\|__PROJECT_DESCRIPTION__' "$STAGE" 2>/dev/null | \
  xargs -0 -r sed -i \
    -e "s/__PROJECT_DESCRIPTION__/$PROJECT_DESCRIPTION/g" \
    -e "s/__PROJECT_NAME__/$PROJECT_NAME/g"

# 3) Copy the rendered project into the repo WITHOUT overwriting existing files (-n)
cp -rn "$STAGE/." .
rm -rf "$STAGE"
```

## Verification (mandatory before continuing)
```bash
composer install                       # install deps + build the autoloader
composer test                          # PHPUnit smoke test must pass (green)
composer stan                          # PHPStan (level max) must be clean
composer cs:check                      # PHP-CS-Fixer must report no changes needed
```
- The scripts are defined in `composer.json` (`test` → phpunit, `stan` → phpstan, `cs`/`cs:check` → php-cs-fixer).
- If any of them fail, **fix before** moving on to implementation.
- Check that **no** placeholder token remains in the **generated project** — exclude the toolbox dirs,
  whose template/skill sources keep the placeholders on purpose:
  `grep -rn '__P[A-Z_]*__' . --include='*.php' --include='*.json' --include='*.yaml' --exclude-dir=.mri_code --exclude-dir=.claude --exclude-dir=.agents --exclude-dir=.git --exclude-dir=vendor`
  must be empty.

## Align the constitution (only if it still describes Python)
Replace the **"Stack (non-negotiable)"** section of `.mri_code/constitution.md` with the PHP/Symfony one,
and adjust the two Python-specific lines under *Structure & naming* (the `src/` mirror rule stays; the
`snake_case`/`test_<module>.py` naming becomes PHP/PSR-4 naming). Suggested Stack block:

```markdown
## Stack (non-negotiable)
- **Latest stable PHP** (currently ≥ 8.4, the floor Symfony requires) with `declare(strict_types=1)` in every file.
- **Composer** for dependencies (single source of truth: `composer.json`).
- **Latest stable Symfony**; framework code at the edges, not in the business logic.
- **PHPStan** at **level max** (+ strict-rules, symfony & doctrine extensions) — zero errors.
- **PHP-CS-Fixer** (`@Symfony` + `@PSR12` + strict) for style — no manual formatting debates.
- **PHPUnit** (+ zenstruck/foundry for fixtures) for tests.
- **Doctrine ORM** for persistence; migrations via doctrine-migrations.
- Native **enums** for closed sets of states; **readonly** value objects; constructor injection only.
```

> The template pins the current stable series in `composer.json` (`symfony/* 8.1.*`, `php >=8.4`). Before
> scaffolding, if a newer stable Symfony minor exists, bump the `8.1.*` constraints and `extra.symfony.require`
> to it — the template always tracks the latest stable, it does not target the LTS.

For the full catalogue of conventions the implementation must follow (enums, DTO mapping, Messenger
buses, Doctrine mapping, error handling), read **`references/php-symfony-best-practices.md`** in this skill.

## Next
Move on to implementation **in TDD** via **/mri-code-implement** (skill `mri-code-tdd` per task), feature by feature,
translating the **spec's acceptance criteria** into tests that fail first (unit tests for the pure logic,
`WebTestCase`/`KernelTestCase` for the framework edges).

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Sonnet (mechanical) — see `.mri_code/models.md`.
