---
name: mri-technical-research
description: >-
  Recherche technique : faisabilité, options d'architecture, bibliothèques, patterns d'intégration.
  Réimplémenté de BMAD-METHOD (bmad-technical-research, MIT). On-demand, suggéré après /mri-forge.
  Invoquée par /mri-technical-research.
---

# mri-technical-research — recherche technique

**But** : évaluer la faisabilité et les options techniques (avant de figer le design).
**⛔ Prérequis** : recherche web (WebSearch/MCP) ; sinon abandonne et préviens.

## Déroulé
1. **Cadrer** : la question technique (faisabilité, choix de techno/lib, intégration, perf).
2. **Rechercher** (web, sources citées) : options d'architecture et trade-offs, bibliothèques/outils
   candidats (maturité, licence, communauté), patterns d'intégration, risques/limites connus, benchmarks.
3. **Synthétiser** : comparatif des options + recommandation argumentée.
4. **Écrire** `.mri_devtools/docs/<projet>/research-technical.md` (findings + sources).

## Suivi
Facultatif : logue l'appel dans `progress.md`. Reviens au flux (typiquement `/mri-design`).
