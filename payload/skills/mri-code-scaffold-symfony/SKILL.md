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
2. **Fill in the constitution's Stack section** — see *Seal the stack* below. Do it **before**
   scaffolding, so the rest of the run reads a constitution that matches what you are generating.
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
- **`composer install` runs Symfony Flex recipes**, which generate/refresh `compose.yaml` and
  `compose.override.yaml` (a `database` service from doctrine, a mail catcher from `symfony/mailer`)
  in **marked `###> pkg ###` blocks**. This is the **dev-infra baseline** later steps build on: when
  implementation needs a containerized service, **extend** these Flex blocks (pin versions via the env
  vars they expose, e.g. `POSTGRES_VERSION`) and hand-author only what has **no** recipe (e.g. MinIO) —
  never replace or duplicate a Flex-managed service (see the constitution's *Stack* section).
- Check that **no** placeholder token remains in the **generated project** — exclude the toolbox dirs,
  whose template/skill sources keep the placeholders on purpose:
  `grep -rn '__P[A-Z_]*__' . --include='*.php' --include='*.json' --include='*.yaml' --exclude-dir=.mri_code --exclude-dir=.claude --exclude-dir=.agents --exclude-dir=.git --exclude-dir=vendor`
  must be empty.

## Seal the stack (constitution)
The constitution ships **stack-agnostic**: its principles hold for any language, and its *Stack*
section is an empty placeholder until a scaffold fills it. Replace everything **between** the two
markers in `.mri_code/constitution.md` with the contents of **`.mri_code/stacks/symfony.md`**,
keeping the markers themselves:

```markdown
## Stack (non-negotiable)
<!-- mri-code:stack:start -->
… contents of .mri_code/stacks/symfony.md …
<!-- mri-code:stack:end -->
```

Edit the file in place (do not regenerate it — the user may have amended other sections). If the
block is already filled with this stack, leave it alone; if it is filled with a **different** stack,
stop and ask the user — two stacks in one project is a decision they own, not a merge you perform.
The other sections stay untouched: they are language-agnostic on purpose and already favor a
testable, framework-decoupled core.

> The template pins the current stable series in `composer.json` (`symfony/* 7.4.*`, `php >=8.3`). Before
> scaffolding, if a newer stable Symfony minor exists, bump the `7.4.*` constraints and `extra.symfony.require`
> to it — the template tracks the latest stable Symfony (which currently happens to also be the 7.4 LTS).
> Keep `.mri_code/stacks/symfony.md` in sync when you do.

For the full catalogue of conventions the implementation must follow (enums, DTO mapping, Messenger
buses, Doctrine mapping, error handling), read **`references/php-symfony-best-practices.md`** in this skill.

## Next
Move on to implementation **in TDD** via **/mri-code-implement** (skill `mri-code-tdd` per task), feature by feature,
translating the **spec's acceptance criteria** into tests that fail first (unit tests for the pure logic,
`WebTestCase`/`KernelTestCase` for the framework edges).

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Sonnet (mechanical) — see `.mri_code/models.md`.
