---
description: Spec → plan d'implémentation (skill mri-devplan) → /mri-scaffold-python ou /mri-implement
---

Invoque la skill `mri-devplan` : elle lit `spec.md` et produit `.mri_devtools/docs/<projet>/plan.md`
(tâches ordonnées avec cases à cocher, code complet).

$ARGUMENTS

Prochaine étape → **`/mri-scaffold-python`** (nouveau projet) sinon **`/mri-implement`**.
Facultatif : `/mri-adversarial-review` (auditer le plan).
💡 Modèle suggéré : **Opus** (planification). Voir `.mri_devtools/models.md`.
