# Project constitution

> **The non-negotiable rulebook for this project.** The agent reads it every session and complies with it.
> The spec says *what* to build; this constitution says *what "well done" means here*.
> **Edit this file** to enforce your preferences — it takes precedence over the agent's default habits.

The principles below are **stack-agnostic** and always apply. The *Stack* section is filled in by the
scaffold skill (`/mri-code-scaffold-*`) from `.mri_code/stacks/<stack>.md`, and names the concrete
tools those principles resolve to. Where the two disagree, the *Stack* section wins on tooling; the
principles below win on intent.

## Stack (non-negotiable)
<!-- mri-code:stack:start -->
_Not defined yet._ The stack is a conclusion of `/mri-code-devplan`, not a starting assumption:
brainstorm, spec and plan are written without one. `/mri-code-scaffold-*` replaces this block with
the fragment for the chosen stack.
<!-- mri-code:stack:end -->

## Code quality
- All public code is **typed** (to the extent the language allows); the **linter** and the
  **type checker** declared in *Stack* must pass with **zero errors**.
- Public modules and functions carry a **short doc comment** (short style, no essays).
- Prefer small functions and **composition** over inheritance.
- No hardcoded secrets; configuration via environment variables (`.env`, not committed).
- Never swallow an error: no catch-all handler that hides the failure — handle errors explicitly.

## Tests (TDD mandatory)
- **Red-Green-Refactor**: write a failing test **before** the implementation.
- The human / the spec owns the test's **intent**; the agent owns the **implementation**.
- The **spec's acceptance criteria become tests**.
- Target coverage **≥ 80%**; at least one integration test per public entry point (API/CLI/UI).
- The **test suite** and the **linter** declared in *Stack* must be green before a task is done.

## Architecture
- The **business logic** does not import the web/UI framework or I/O (keep the core testable).
- Dependencies point inward (I/O and frameworks at the edges).
- Source and tests live in the **layout declared in *Stack*** — one layout per project, applied
  consistently.

## Structure & naming
- Tests **mirror** the source tree, one unit under test ↔ one test file, named per the *Stack*
  convention.
- Follow the **idiomatic naming convention of the language** (declared in *Stack*) — never a
  convention imported from another ecosystem.
- Pipeline artifacts (brief, spec, plan, progress) live in `.mri_code/docs/<project>/` (written by
  the `mri-code-*` skills). The project's own documentation lives in `docs/`.

## Workflow
- Small, atomic commits, with an imperative message describing the *why*.
- Never `git push --force`; never commit secrets or dependency/build directories
  (`.venv`, `node_modules`, `vendor`, `dist`).
