---
name: mri-domain-research
description: >-
  Recherche domaine/industrie : expertise, terminologie, patterns, contraintes réglementaires.
  Réimplémenté de BMAD-METHOD (bmad-domain-research, MIT). On-demand, suggéré après /mri-forge.
  Invoquée par /mri-domain-research.
---

# mri-domain-research — recherche domaine

**But** : acquérir/valider l'expertise d'un domaine peu familier pour éviter les erreurs de conception.
**⛔ Prérequis** : recherche web (WebSearch/MCP) ; sinon abandonne et préviens.

## Déroulé
1. **Cadrer** : le domaine/industrie, ce qu'on doit comprendre/valider.
2. **Rechercher** (web, sources citées) : terminologie et concepts clés, patterns et bonnes pratiques
   du domaine, acteurs/normes, contraintes (réglementaires, métier), pièges classiques.
3. **Synthétiser** : glossaire, règles du domaine, implications pour l'idée/design.
4. **Écrire** `.mri_devtools/docs/<projet>/research-domain.md` (findings + sources).

## Suivi
Facultatif : logue l'appel dans `progress.md`. Reviens au flux (typiquement `/mri-design`).
