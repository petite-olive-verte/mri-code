---
name: mri-code-scaffold-symfony-hexagonal-apiplatform
description: Use when initializing/scaffolding a Symfony project with a hexagonal (ports & adapters) architecture whose REST API is served by API Platform 4 — layered Domain / Application / Infrastructure, API resources as Infrastructure DTOs bridged to the domain by State providers/processors, Doctrine XML mapping keeping the domain pure — from .mri_code/templates/symfony-hexagonal-apiplatform, once the spec and plan are ready and before writing feature code. For a hexagonal Symfony with plain controllers (no API Platform) use mri-code-scaffold-symfony-hexagonal instead. Respects .mri_code/constitution.md.
disable-model-invocation: true
---

# mri-code-scaffold-symfony-hexagonal-apiplatform — scaffold a hexagonal Symfony + API Platform project

> ┌─ mri devtools ─┐

Generate a **ports-and-adapters** Symfony project whose HTTP layer is **API Platform 4**, from
`.mri_code/templates/symfony-hexagonal-apiplatform/`, respecting `.mri_code/constitution.md`. To be
used **after** the spec and plan, **before** writing feature code.

Same stack, tooling and layered layout as **/mri-code-scaffold-symfony-hexagonal** (pure Domain /
Application / Infrastructure, Doctrine XML mapping, PHPStan max, PHP-CS-Fixer, PHPUnit). The
difference is the **HTTP layer**: instead of thin controllers, the API is exposed with **API
Platform**, kept clean for hexagonal:

- **Resources are Infrastructure DTOs** — `#[ApiResource]` on classes in
  `src/Infrastructure/ApiPlatform/Resource/`. The **domain model is never decorated**.
- **State adapters bridge to the core** — `src/Infrastructure/ApiPlatform/State/`: a **Processor**
  (write: turns the resource into a command, dispatches it on the bus) and a **Provider** (read:
  loads through a domain repository port and maps to the resource).

**Read `references/hexagonal-rules.md` in `mri-code-scaffold-symfony-hexagonal`** first — the layer
rules are identical; only the HTTP adapter differs (API Platform resource + state, not a controller).

## Before starting
Follow the **same "Before starting" steps** as `mri-code-scaffold-symfony`, with **one difference**:
the stack fragment to seal into the constitution is **`.mri_code/stacks/symfony-hexagonal-apiplatform.md`**.
See *Seal the stack* in `mri-code-scaffold-symfony`. Then determine `PROJECT_NAME` (lowercase, dashes
ok) and `PROJECT_DESCRIPTION` (one sentence).

## Procedure
Identical to `mri-code-scaffold-symfony`, rendering from the **`symfony-hexagonal-apiplatform`**
template. The same safety rule applies: **substitute tokens only inside an isolated staging copy,
never at the repo root.**

```bash
PROJECT_NAME="todo-api"
PROJECT_DESCRIPTION="Small todo API."          # avoid the '/' character (sed delimiter)

SRC=".mri_code/templates/symfony-hexagonal-apiplatform"
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
A complete vertical slice: `POST /api/tasks` → `TaskResource` → `CreateTaskProcessor` → `CreateTask`
command → handler → domain `Task` → Doctrine adapter; `GET /api/tasks/{id}` → `TaskProvider` →
repository port → resource. Layout:

```
src/
  Domain/          Model/ ValueObject/ Repository/ (ports) Exception/       — pure PHP
  Application/     Command/ Query/ Handler/ Port/                            — use cases
  Infrastructure/  ApiPlatform/{Resource(#[ApiResource] DTOs), State(Processor/Provider)}
                   Doctrine/{Mapping(XML),Repository,Type}/ Symfony/(Kernel) — adapters + glue
```
API Platform is pointed at `src/Infrastructure/ApiPlatform/Resource` via `config/packages/api_platform.yaml`.

## Verification (mandatory before continuing)
```bash
composer install
composer test                          # unit (no kernel) + functional (WebTestCase) must pass
composer stan                          # PHPStan level max — clean
composer cs:check                      # PHP-CS-Fixer — no changes needed
```
- Fix any failure before implementing. Check no placeholder token remains in the generated project
  (see `mri-code-scaffold-symfony` for the exact `grep`).
- **Remove Flex's flat-layout cruft.** `composer install` runs recipes that create `src/Controller/`,
  `src/Entity/`, `src/Repository/` **and `src/ApiResource/`** (empty) — the flat layout, which
  contradicts the hexagonal structure (API resources live in `Infrastructure/ApiPlatform/Resource`).
  Delete them: `git rm -r src/Controller src/Entity src/Repository src/ApiResource` (or `rm -rf`
  before the first commit).
- **Persisting the create flow needs a migration.** The shipped `TaskApiTest` only checks the
  validation boundary (no DB). To make `POST`/`GET` persist, generate the initial migration once the
  stack is up: `php bin/console doctrine:migrations:diff` then `doctrine:migrations:migrate`.

## Next
Implement **in TDD** via **/mri-code-implement**: unit-test the domain and use cases without booting
the kernel; cover the API Platform state adapters with `WebTestCase`. New API endpoints = a
`Resource` DTO + a `Provider`/`Processor`, never `#[ApiResource]` on the domain model.

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Sonnet (mechanical) — see `.mri_code/models.md`.
