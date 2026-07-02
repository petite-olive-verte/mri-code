---
description: Reprend le pipeline mri là où il s'est arrêté (lit progress.md) → re-entre à l'étape courante
---

Reprends le travail en cours sur ce projet.

## Comportement
1. Cherche le fichier d'état : `.mri_devtools/docs/*/progress.md` (le plus récemment modifié si plusieurs).
   - **Absent** → aucun travail en cours : suggère `/mri-brainstorm` (nouveau projet) et arrête-toi.
2. **Lis `progress.md`** : rapporte l'état à l'utilisateur (étapes faites `[x]`, en cours `[~]`, à faire `[ ]`, + appels facultatifs).
3. **Re-entre** à l'étape **`[~]` en cours** (ou, à défaut, la première **`[ ]`** après la dernière `[x]`) :
   recharge les artefacts déjà sur disque (`brief.md`, `spec.md`, `plan.md`…) et **invoque la skill
   correspondante** pour continuer. Si l'étape est `implement`, délègue le détail fin aux cases du
   `plan.md` (et à `.mri_devtools/state/sdd/` si présent).
4. Confirme la reprise en une phrase avant de continuer.

## Schéma de `progress.md` (canonique — toute skill le lit/écrit ainsi)
`.mri_devtools/docs/<projet>/progress.md` :
```markdown
# Parcours — <projet>   (MAJ: <date> · dernière étape: /mri-<x>)

## Étapes
- [x] brainstorm → brief.md
- [x] forge → HARDENED
- [~] design → spec.md (en cours)
- [ ] devplan
- [ ] scaffold
- [ ] implement
- [ ] review
- [ ] finish

## Appels facultatifs
- market-research (après forge) → research-market.md
- adversarial-review (brief) → 3 findings corrigés

## Prochaine étape
/mri-design (finir spec.md) → puis /mri-devplan
```

Marqueurs : `[x]` fait · `[~]` en cours · `[ ]` à faire. Les skills mettent à jour ce fichier au début
(`[~]`) et à la fin (`[x]` + « Prochaine étape ») de chaque phase.

$ARGUMENTS
