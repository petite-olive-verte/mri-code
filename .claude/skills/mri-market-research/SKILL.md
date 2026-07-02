---
name: mri-market-research
description: >-
  Recherche marché (concurrence, clients, tendances) sur données web actuelles avec sources citées.
  Réimplémenté de BMAD-METHOD (bmad-market-research, MIT). On-demand, suggéré après /mri-forge.
  Invoquée par /mri-market-research.
---

# mri-market-research — recherche marché

**But** : produire une recherche marché appuyée sur des données web actuelles et des **sources citées**,
avec un récit clair. **Rôle** : facilitateur de recherche — tu apportes méthodo + recherche web,
l'utilisateur apporte le domaine et la direction.

**⛔ Prérequis** : recherche web disponible (WebSearch/MCP). Sinon, abandonne et préviens.

## Déroulé
1. **Cadrer** : question de recherche, marché/segment visé, concurrents connus, ce qu'on veut décider.
2. **Rechercher** (web) : concurrents (positionnement, prix, forces/faiblesses), clients/segments et
   besoins, tendances, taille/dynamique du marché. Vérifie et **cite chaque source** (URL).
3. **Synthétiser** : mapping concurrentiel, opportunités/risques, implications pour l'idée.
4. **Écrire** `.mri_devtools/docs/<projet>/research-market.md` (findings + sources). Concis, actionnable.

## Suivi
Facultatif : logue l'appel dans `progress.md` (« Appels facultatifs » → `research-market.md`). Reviens
ensuite au flux (typiquement `/mri-design`).
