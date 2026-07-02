---
description: Spec → implementation plan (skill mri-devplan) → /mri-scaffold-python or /mri-implement
---

Invoke the `mri-devplan` skill: it reads `spec.md` and produces `.mri_devtools/docs/<project>/plan.md`
(ordered tasks with checkboxes, complete code).

$ARGUMENTS

Next step → **`/mri-scaffold-python`** (new project) otherwise **`/mri-implement`**.
Optional: `/mri-adversarial-review` (audit the plan).
💡 Suggested model: **Opus** (planning). See `.mri_devtools/models.md`.
