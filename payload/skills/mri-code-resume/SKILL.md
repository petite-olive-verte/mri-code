---
name: mri-code-resume
description: >-
  Resume the mri pipeline where it stopped: reads progress.md and re-enters the current step.
  Invoked by the user via /mri-code-resume.
disable-model-invocation: true
---

# mri-code-resume — resume the pipeline

> ┌─ mri devtools ─┐

Resume the work in progress on this project.

## Behavior
1. Look for the state file: `.mri_code/docs/*/progress.md` (the most recently modified if several).
   - **Missing** → no work in progress: suggest `/mri-code-brainstorm` (new project) and stop.
2. **Read `progress.md`**: report the state to the user (steps done `[x]`, in progress `[~]`, to do `[ ]`, + optional calls).
3. **Re-enter** the **`[~]` in-progress step** (or, failing that, the first **`[ ]`** after the last `[x]`):
   reload the artifacts already on disk (`brief.md`, `spec.md`, `plan.md`…) and **run the matching
   skill** to continue. If the step is `implement`, delegate the fine-grained detail to the checkboxes in
   `plan.md` and to the **task ledger** `.mri_code/state/sdd/task-ledger.md` if present (tasks marked
   complete there are DONE — do not redo them).

**Two levels of state (don't confuse them):** `docs/<project>/progress.md` tracks **phases**
(brainstorm→finish) — this is what you read here. `state/sdd/task-ledger.md` tracks **tasks** inside the
implement phase (git-ignored scratch, owned by `mri-code-implement`).
4. Confirm the resumption in one sentence before continuing.

## `progress.md` schema (canonical — every skill reads/writes it this way)
`.mri_code/docs/<project>/progress.md`:
```markdown
# Journey — <project>   (updated: <date> · last step: /mri-<x>)

## Steps
- [x] brainstorm → brief.md
- [x] forge → HARDENED
- [~] design → spec.md (in progress)
- [ ] devplan
- [ ] scaffold
- [ ] implement
- [ ] review
- [ ] finish

## Optional calls
- market-research (after forge) → research-market.md
- adversarial-review (brief) → 3 findings fixed

## Next step
/mri-code-design (finish spec.md) → then /mri-code-devplan
```

Markers: `[x]` done · `[~]` in progress · `[ ]` to do. Skills update this file at the start
(`[~]`) and at the end (`[x]` + "Next step") of each phase.

---
**User input:** $ARGUMENTS

💡 **Suggested model:** any — see `.mri_code/models.md`.
