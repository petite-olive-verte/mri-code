---
name: mri-code-devplan
description: Use when you have a spec or requirements for a multi-step task, before touching code
disable-model-invocation: true
---

# mri-code-devplan — turn a spec into a task plan

> ┌─ mri devtools ─┐

## Overview

Write an implementation plan that is a **map of the work, not the pre-written codebase**. The plan
carries the **contract** of each task — which files to touch, the interfaces/signatures it produces and
consumes, the tests to write, the acceptance criteria, and the order — so that `mri-code-implement` (TDD) can
execute it. **It does not carry the implementation bodies**: the real code is written at implementation
time, once. Give the whole thing as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume the implementer is a skilled developer who knows almost nothing about our problem domain: the plan
must make the **intent, boundaries and contracts** unambiguous, and let them write the code.

**Why not embed the code:** a plan that pre-writes every function body duplicates what `mri-code-implement`
produces, drifts from it immediately, bloats the document, and is expensive to generate. The test code is
the exception — it *defines* the contract precisely, so showing it is useful.

**The one exception beyond tests — shared contract surfaces.** Types, dataclasses, Protocols/interfaces
and public signatures that *multiple tasks depend on* ARE the contract: show them as **real code,
verbatim**, in the task's Interfaces block. Every dependent task must see the identical definition, so
this is the one place fully-written code earns its keep. What stays prose is the implementation *body*
internal to a single task.

**Announce at start:** "I'm using mri-code-devplan to turn the spec into an implementation plan."

**Enter plan mode first.** Begin the step by entering native Claude Code plan mode (call the plan-mode
tool yourself — the user does not toggle it). Plan mode is read-only, so no file is written while you
reason and decompose. Present the task breakdown via ExitPlanMode — **that approval is the step's gate.**
Only after the user approves do you write the plan to disk (see "Execution Handoff"). If plan mode is
unavailable (non-interactive run), fall back to presenting the plan inline and getting explicit approval
before writing.

**Context:** If working in an isolated worktree, it should have been created via the `mri-code-worktrees` skill at execution time.

**Save plans to:** `.mri_code/docs/<project>/plan.md` (written on approval)
- (User preferences for plan location override this default)

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Task Right-Sizing

A task is the smallest unit that carries its own test cycle and is worth a
fresh reviewer's gate. When drawing task boundaries: fold setup,
configuration, scaffolding, and documentation steps into the task whose
deliverable needs them; split only where a reviewer could meaningfully
reject one task while approving its neighbor. Each task ends with an
independently testable deliverable.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use mri-code-implement to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

## Global Constraints

[The spec's project-wide requirements — version floors, dependency limits,
naming and copy rules, platform requirements — one line each, with exact
values copied verbatim from the spec. Every task's requirements implicitly
include this section.]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [what this task uses from earlier tasks — exact signatures]
- Produces: [what later tasks rely on — exact function names, parameter
  and return types. A task's implementer sees only their own task; this
  block is how they learn the names and types neighboring tasks use.]
- Shared contract surfaces (a type/dataclass, a Protocol/interface, a public API
  signature depended on by more than one task) → show them here as **real code, verbatim**.
  Implementation *bodies* stay intent + test (Step 3 below).

- [ ] **Step 1: Write the failing test** — show the test code (it defines the contract)

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Implement `function(input) -> ReturnType`** to make the test pass

Intent: [one line — what the implementation must do]. Constraints: [invariants, edge cases to
handle]. **Do not write the body here** — the implementer writes it in `mri-code-implement`.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## No vague placeholders

The plan carries the *contract*, not the code — but the contract must be **precise**. These are **plan
failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases" — name the *specific* errors
  and edge cases the task must handle instead.
- "Write tests for the above" (without the test code — the test code IS required, it defines the contract)
- An implementation step with no stated intent, signature, or constraints
- References to types, functions, or methods whose signature is defined in no task's **Interfaces** block

## Remember
- Exact file paths always
- Show **test code** (defines the contract); describe implementation by **intent + signature**, not body
- Every produced/consumed type or signature lives in an **Interfaces** block
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits

## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

**2. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.

## Execution Handoff

Once the user **approves** the plan (via ExitPlanMode, or inline if plan mode was unavailable):
1. **Write** the plan to `.mri_code/docs/<project>/plan.md` and seed/update `progress.md`.
2. **Commit** the plan.
3. Hand off to the next step (name the suggested model per `.mri_code/models.md`):
   - New project still needing a skeleton → suggest the scaffold matching the stack in
     `.mri_code/constitution.md` (suggested model: **Sonnet**):
     - Python → "**Next step → `/mri-code-scaffold-python`**";
     - PHP/Symfony → "**Next step → `/mri-code-scaffold-symfony`**" (or
       "**`/mri-code-scaffold-symfony-hexagonal`**" for a ports-and-adapters layout).
   - Otherwise → "**Next step → `/mri-code-implement`** (suggested model: **Sonnet**)".

`mri-code-implement` is the execution skill: a fresh subagent per task + two-stage review, driven by the
plan's checkboxes. Do not execute it yourself — the user launches it.

## Tracking (progress.md)
At the **start** of this step, mark it `[~]` in `.mri_code/docs/<project>/progress.md` (create the
file if missing — schema in the `/mri-code-resume` command). At the **end**, set it to `[x]` and point to
the next step of the pipeline.

---
**User input:** $ARGUMENTS

💡 **Suggested model:** Opus (planning) — see `.mri_code/models.md`.
