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
2. **If the constitution still describes the default Python stack** (it mentions `uv`/`ruff`/`pytest` and
   no TypeScript), the project is going React: **rewrite its "Stack" section** to the React one before
   scaffolding — see *Align the constitution* below. Leave the quality/tests/architecture principles
   intact (they are language-agnostic and already favor a testable, framework-decoupled core).
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

## Align the constitution (only if it still describes Python)
Replace the **"Stack (non-negotiable)"** section of `.mri_code/constitution.md` with the React one, and
adjust the Python-specific lines under *Structure & naming* (the `src/` mirror rule stays; the
`snake_case`/`test_<module>.py` naming becomes the feature-based layout below). Suggested Stack block:

```markdown
## Stack (non-negotiable)
- **Node ≥ 22.12** (the floor Vite 8 requires); **pnpm** via corepack, pinned in `packageManager`.
- **React 19** + **Vite 8** — SPA, no meta-framework unless the spec calls for SSR.
- **TypeScript 7**, `strict` plus `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`,
  `verbatimModuleSyntax` and `erasableSyntaxOnly` — no `any`, no non-null assertions (`!`).
- **Biome** for lint *and* format (one tool, one config) — no manual formatting debates.
- **Vitest** + **Testing Library** for tests; query by accessible role, never by test id.
- Logic lives in pure TypeScript (`model/`), free of React; hooks orchestrate; components render.
- Organise **by feature**, not by technical role. Each feature exposes a public API via `index.ts`.
```

> The template pins the current stable majors (React 19, Vite 8, TypeScript 7, Vitest 4, Biome 2).
> Before scaffolding, if a newer stable major exists, bump it and re-run the verification above —
> the template tracks latest stable.

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
