---
name: mri-code-scaffold-symfony-hexagonal
description: Use when initializing/scaffolding a Symfony project with a hexagonal (ports & adapters) architecture — layered Domain / Application / Infrastructure, Doctrine XML mapping keeping the domain pure — from .mri_code/templates/symfony-hexagonal, once the spec and plan are ready and before writing feature code. For a plain pragmatic Symfony layout use mri-code-scaffold-symfony instead. Respects .mri_code/constitution.md.
disable-model-invocation: true
---

# mri-code-scaffold-symfony-hexagonal — scaffold a hexagonal Symfony project

> ┌─ mri devtools ─┐

Generate a **ports-and-adapters** Symfony project from `.mri_code/templates/symfony-hexagonal/`,
respecting `.mri_code/constitution.md`. To be used **after** the spec and plan, **before** writing
feature code.

Same stack and tooling as **/mri-code-scaffold-symfony** (latest stable PHP + Symfony, Composer,
PHPStan max, PHP-CS-Fixer, PHPUnit, Doctrine) — the difference is the **layout**: a layered
`Domain / Application / Infrastructure` skeleton where the domain has **zero** framework
dependency. Prefer the plain scaffold for small CRUD apps; prefer this one when the business
logic is worth isolating and testing on its own.

## Before starting
Follow the **same "Before starting" and constitution-alignment steps** as `mri-code-scaffold-symfony`
(read the constitution; if it still describes the Python stack, rewrite its *Stack* section to the
Symfony one). Then determine:
- `PROJECT_NAME`: Composer package name — **lowercase**, dashes ok, e.g. `todo-api`.
- `PROJECT_DESCRIPTION`: one sentence.

**Read `references/hexagonal-rules.md` in this skill** before scaffolding and keep it open during
implementation — it is the rulebook the generated structure assumes.

## Procedure
Identical to `mri-code-scaffold-symfony`, but render from the hexagonal template. The same safety
rule applies: **substitute tokens only inside an isolated staging copy, never at the repo root.**

```bash
PROJECT_NAME="todo-api"                         # lowercase, dashes ok
PROJECT_DESCRIPTION="Small todo API."           # avoid the '/' character (sed delimiter)

SRC=".mri_code/templates/symfony-hexagonal"

STAGE="$(mktemp -d)"
cp -r "$SRC/." "$STAGE/"

grep -rlZ '__PROJECT_NAME__\|__PROJECT_DESCRIPTION__' "$STAGE" 2>/dev/null | \
  xargs -0 -r sed -i \
    -e "s/__PROJECT_DESCRIPTION__/$PROJECT_DESCRIPTION/g" \
    -e "s/__PROJECT_NAME__/$PROJECT_NAME/g"

cp -rn "$STAGE/." .
rm -rf "$STAGE"
```

## What you get (the `Task` worked example)
A complete vertical slice you extend or delete: HTTP request DTO → command → handler → domain
model → Doctrine adapter. Layout:

```
src/
  Domain/          Model/ ValueObject/ Repository/ (ports) Exception/   — pure PHP
  Application/     Command/ Query/ Handler/ Port/                        — use cases
  Infrastructure/  Doctrine/{Mapping(XML),Repository,Type}/ Controller/  — adapters
```
Ports are bound to adapters in `config/services.yaml`; the domain model is mapped by **XML** under
`src/Infrastructure/Doctrine/Mapping/` so it carries no ORM attributes.

## Verification (mandatory before continuing)
```bash
composer install
composer test                          # unit (no kernel) + functional (WebTestCase) must pass
composer stan                          # PHPStan level max — clean
composer cs:check                      # PHP-CS-Fixer — no changes needed
```
- Fix any failure before implementing. Check no placeholder token remains in the generated project
  (see `mri-code-scaffold-symfony` for the exact `grep`).

## Next
Implement **in TDD** via **/mri-code-implement** (skill `mri-code-tdd` per task): unit-test the domain
and use cases without booting the kernel; cover the adapters with `KernelTestCase`/`WebTestCase`.
Keep new code inside the right layer — see `references/hexagonal-rules.md`.

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Sonnet (mechanical) — see `.mri_code/models.md`.
