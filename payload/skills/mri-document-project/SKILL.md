---
name: mri-document-project
description: >-
  Documente un projet existant (brownfield) pour donner du contexte à l'agent : structure, stack,
  conventions, points d'entrée, comment lancer/tester. Réimplémenté de BMAD-METHOD
  (bmad-document-project, MIT). On-demand, en amont de /mri-brainstorm sur un repo existant.
---

# mri-document-project — contexte d'un projet existant (brownfield)

**But** : quand on travaille sur un **repo existant** (pas un greenfield), produire un document de
contexte concis que les skills suivantes consommeront, pour éviter les hypothèses fausses.

## Déroulé
1. **Explorer** : structure des dossiers, `README`, fichiers de build/config (`pyproject.toml`,
   `package.json`…), points d'entrée, tests, commits récents. Repère la stack et les conventions réelles.
2. **Cartographier** : modules principaux et leurs responsabilités, flux de données, dépendances
   externes, commandes pour installer/lancer/tester.
3. **Écrire** `.mri_devtools/docs/<projet>/project-context.md` : synthèse **actionnable** (pas un dump) —
   « ce qu'un agent doit savoir avant de toucher ce code ». Signale les zones fragiles/dette repérées.

Ce doc complète `.mri_devtools/constitution.md` (règles voulues) en décrivant l'existant (règles de fait).

## Suivi
Facultatif : logue l'appel dans `progress.md`. Enchaîne ensuite sur `/mri-brainstorm` (l'idée/évolution
à concevoir sur ce projet).
