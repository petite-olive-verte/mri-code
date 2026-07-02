---
description: Brief → technical design (skill mri-design, the bridge) → /mri-devplan
---

Invoke the `mri-design` skill: it reads `.mri_devtools/docs/<project>/brief.md` (intent taken as
given) and produces the technical design `.mri_devtools/docs/<project>/spec.md`.

$ARGUMENTS

Next step → **`/mri-devplan`**. Optional: `/mri-adversarial-review` (audit the spec), `/mri-elicit`.
💡 Suggested model: **Opus** (architecture). See `.mri_devtools/models.md`.
