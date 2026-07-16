---
name: mri-code-scaffold-react
description: Use when initializing/scaffolding a React project structure (Vite + React + TypeScript strict + Vitest + Testing Library + Biome, feature-based layout) from .mri_code/templates/react, once the spec and plan are ready and before writing feature code. Respects .mri_code/constitution.md.
disable-model-invocation: true
---

# mri-code-scaffold-react — scaffold a React project (Vite + TypeScript + Vitest + Biome)

> ┌─ mri devtools ─┐

Generate the structure of a React single-page app from `.mri_code/templates/react/`, respecting
`.mri_code/constitution.md`. To be used **after** the spec and plan, **before** writing feature code.

> **Why no hexagonal variant?** Hexagonal architecture protects a rich, long-lived domain from the
> framework — a backend problem. In a frontend the server usually owns the domain, and the real
> complexity is server-vs-client state, caching and rendering, which ports and adapters do nothing
> for. This template keeps hexagonal's *payoff* (pure logic, injected dependencies) without its
> ceremony: `model/` is pure TypeScript, hooks are the seam, components are views. If a genuinely
> rich client-side domain appears (offline sync, an editor, a scheduling engine), `model/` is already
> the domain layer and promoting it is mechanical.

## Before starting
1. **Read `.mri_code/constitution.md`**: apply its stack and conventions. If they differ from the template,
   the constitution wins — adapt the generated files accordingly.
2. **Fill in the constitution's Stack section** — see *Seal the stack* below. Do it **before**
   scaffolding, so the rest of the run reads a constitution that matches what you are generating.
3. Determine two names (derive them from the spec, otherwise ask the user):
   - `PROJECT_NAME`: npm package name — **lowercase**, may contain dashes, e.g. `todo-ui`.
   - `PROJECT_DESCRIPTION`: one sentence.

## Procedure
The project is generated **at the repo root** (the app lives in the same repository as the toolbox).
Do **not** overwrite any existing file: if a target file already exists (e.g. `README.md`,
`.gitignore`), keep the existing one and flag it to the user.

> ⚠️ **Never rewrite tokens across the repo root.** The substitution must happen in an **isolated
> staging copy** — otherwise it rewrites the shared template source (`.mri_code/templates/`), the
> skills that document these tokens (`.claude/skills/`, `.agents/skills/`), and your own files, poisoning
> every future scaffold. Render in staging, then copy the finished project in without overwriting.

```bash
# From the repo root. Adapt the 2 variables.
PROJECT_NAME="todo-ui"                         # lowercase, dashes ok
PROJECT_DESCRIPTION="Small todo UI."           # avoid the '/' character (regex delimiter)

SRC=".mri_code/templates/react"

# 1) Render the template in an ISOLATED staging dir. Substitution can only ever touch this copy.
STAGE="$(mktemp -d)"
cp -r "$SRC/." "$STAGE/"                       # includes hidden files

# 2) Substitute the tokens — scoped to "$STAGE" only, never the repo root.
#    `find -exec perl -pi` on purpose: `sed -i` needs an argument on BSD/macOS but not on GNU, and
#    `grep -Z` means "NUL-separated" on GNU/BSD but "fuzzy match" under ugrep. This form is portable.
find "$STAGE" -type f -exec perl -pi \
  -e "s/__PROJECT_DESCRIPTION__/$PROJECT_DESCRIPTION/g; s/__PROJECT_NAME__/$PROJECT_NAME/g" {} +

# 3) Copy the rendered project into the repo WITHOUT overwriting existing files (-n)
cp -rn "$STAGE/." .
rm -rf "$STAGE"
```

## Verification (mandatory before continuing)
```bash
corepack enable                        # once per machine: provides the pnpm version pinned in package.json
pnpm install                           # install dependencies
pnpm lint                              # Biome must report no errors
pnpm typecheck                         # tsc --noEmit must be clean
pnpm test                              # Vitest: 18 tests, all green, in ~1s
pnpm build                             # tsc + vite build must succeed
```
- `pnpm check` runs lint + typecheck + tests in one go (the CI gate).
- If any of them fail, **fix before** moving on to implementation.
- `corepack enable` is not optional: `package.json` pins pnpm via `packageManager`, and pnpm shells out
  to itself to verify deps before running a script. Without the shims on `PATH` every `pnpm <script>`
  dies with `ENOENT: pnpm install`.
- Check that **no** placeholder token remains in the **generated project** — exclude the toolbox dirs,
  whose template/skill sources keep the placeholders on purpose:
  `grep -rn '__P[A-Z_]*__' . --include='*.ts' --include='*.tsx' --include='*.json' --include='*.html' --exclude-dir=.mri_code --exclude-dir=.claude --exclude-dir=.agents --exclude-dir=.git --exclude-dir=node_modules`
  must be empty.

## Seal the stack (constitution)
The constitution ships **stack-agnostic**: its principles hold for any language, and its *Stack*
section is an empty placeholder until a scaffold fills it. Replace everything **between** the two
markers in `.mri_code/constitution.md` with the contents of **`.mri_code/stacks/react.md`**, keeping
the markers themselves:

```markdown
## Stack (non-negotiable)
<!-- mri-code:stack:start -->
… contents of .mri_code/stacks/react.md …
<!-- mri-code:stack:end -->
```

Edit the file in place (do not regenerate it — the user may have amended other sections). If the
block is already filled with this stack, leave it alone; if it is filled with a **different** stack,
stop and ask the user — two stacks in one project is a decision they own, not a merge you perform.
The other sections stay untouched: they are language-agnostic on purpose and already favor a
testable, framework-decoupled core.

> The template pins the current stable majors (React 19, Vite 8, TypeScript 7, Vitest 4, Biome 2).
> Before scaffolding, if a newer stable major exists, bump it and re-run the verification above —
> the template tracks latest stable. Keep `.mri_code/stacks/react.md` in sync when you do.

For the full catalogue of conventions the implementation must follow (state modelling, effects,
data fetching, component boundaries, testing, accessibility), read
**`references/react-best-practices.md`** in this skill.

## Next
Move on to implementation **in TDD** via **/mri-code-implement** (skill `mri-code-tdd` per task), feature by feature,
translating the **spec's acceptance criteria** into tests that fail first (pure unit tests for `model/`,
Testing Library for hooks and components).

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Sonnet (mechanical) — see `.mri_code/models.md`.
