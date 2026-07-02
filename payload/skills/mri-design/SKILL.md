---
name: mri-design
description: >-
  Convertit le brief produit par /mri-brainstorm en un design technique (spec.md). C'est le PONT
  analyse→exécution du pipeline mri : il prend l'intention produit comme acquise et se concentre sur
  l'architecture. Invoquée par /mri-design. (Adapté de superpowers:brainstorming, MIT.)
---

# mri-design — du brief au design technique (le pont)

Transforme le **product brief** (`.mri_devtools/docs/<projet>/brief.md`, produit par `/mri-brainstorm`,
éventuellement durci par `/mri-forge`) en un **design technique** validé, prêt pour la planification.

**Rôle** : tu prends l'intention produit **comme acquise** (le quoi/pourquoi est déjà tranché dans le
brief — ne le re-litige pas). Tu te concentres sur le **comment technique** : architecture, composants,
flux de données, gestion d'erreurs, tests. Sortie : `.mri_devtools/docs/<projet>/spec.md`.

<HARD-GATE>
N'invoque aucune skill d'implémentation, n'écris aucun code et ne scaffolde rien tant que tu n'as pas
présenté un design et obtenu l'approbation de l'utilisateur.
</HARD-GATE>

## Checklist (crée une tâche par item, dans l'ordre)
1. **Lire le brief** `.mri_devtools/docs/<projet>/brief.md` (+ contexte projet : fichiers, docs, commits récents).
2. **Companion visuel just-in-time** — pas d'emblée. La première fois qu'une question serait plus claire
   montrée que décrite, propose-le (message dédié). Voir `./visual-companion.md`.
3. **Questions de clarification techniques** — une à la fois : combler les **trous de design** (pas
   re-explorer le produit). Contraintes techniques, dépendances, invariants, critères de succès mesurables.
4. **Proposer 2-3 approches** techniques — trade-offs + ta recommandation en tête.
5. **Présenter le design** en sections dimensionnées à leur complexité ; approbation après chaque section.
   Couvre : architecture, composants, flux de données, gestion d'erreurs, tests.
6. **Écrire le design** dans `.mri_devtools/docs/<projet>/spec.md` et committer.
7. **Auto-revue de la spec** — placeholders/TODO, contradictions internes, périmètre, ambiguïtés → corrige inline.
8. **Revue utilisateur** — demande à l'utilisateur de relire la spec avant de continuer.
9. **Transition** — invoque **`mri-devplan`** pour créer le plan d'implémentation. **C'est le seul skill
   invoqué ensuite.**

## Design pour l'isolation et la clarté
Découpe le système en unités à **but unique**, communiquant par **interfaces bien définies**, testables
indépendamment. Pour chaque unité : que fait-elle, comment l'utilise-t-on, de quoi dépend-elle ? Si on
ne peut pas comprendre une unité sans lire ses internes, ou changer ses internes sans casser les
consommateurs, les frontières sont à revoir. Les fichiers qui grossissent = signal qu'ils font trop.

## En codebase existant
Explore la structure avant de proposer. Suis les patterns existants. Inclus les améliorations ciblées
qui servent le but courant ; pas de refactoring non lié.

## Auto-revue de la spec (yeux neufs)
1. **Placeholders** : « TBD », « TODO », sections incomplètes, exigences vagues → corrige.
2. **Cohérence interne** : des sections se contredisent-elles ? l'archi colle-t-elle aux features ?
3. **Périmètre** : assez focalisé pour un seul plan d'implémentation, ou à décomposer ?
4. **Ambiguïté** : une exigence interprétable de deux façons ? Choisis-en une, rends-la explicite.

## Gate de revue utilisateur
> « Spec écrite et committée dans `<chemin>`. Relis-la et dis-moi si tu veux des changements avant qu'on
> écrive le plan d'implémentation. »
Attends la réponse. Changements demandés → applique + re-passe l'auto-revue. Ne continue qu'après approbation.

## Principes
Une question à la fois · YAGNI impitoyable · explore 2-3 approches · validation incrémentale · reste flexible.

## Suivi
- Début : `design` `[~]` dans `.mri_devtools/docs/<projet>/progress.md`.
- Fin : `design` `[x] → spec.md`, puis : « **Prochaine étape → `/mri-devplan`** ».

## Companion visuel
Companion navigateur pour montrer maquettes/diagrammes pendant le design (outil, pas mode). Offre-le
just-in-time (message dédié) uniquement quand une question serait plus claire **montrée** que décrite.
Guide détaillé : `./visual-companion.md`.
