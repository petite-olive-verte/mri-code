---
name: mri-meta-prompt
description: Transforme une demande vague en un prompt précis, structuré et prêt à l'emploi pour un LLM/agent. Outil ponctuel, hors du pipeline idée->code ; invoqué explicitement (commande /meta-prompt).
disable-model-invocation: true
---

# Meta-prompt — vague → précis

Transforme une demande floue en un **prompt précis et structuré**, prêt à coller dans un agent.
Outil **autonome** : à utiliser à la demande, indépendamment du flux brainstorm→spec→implement.

## Procédure
1. **Lever l'ambiguïté d'abord.** Si la demande est sous-spécifiée, pose **1 à 3 questions ciblées**
   (audience, périmètre, format, contraintes). Si l'utilisateur veut aller vite, énonce plutôt des
   **hypothèses explicites** et continue.
2. **Construis le prompt optimisé** avec, selon la pertinence, ces sections :
   - **Rôle** : qui l'agent doit incarner.
   - **Objectif** : le résultat attendu, en une phrase.
   - **Contexte** : infos nécessaires (et seulement elles).
   - **Contraintes / exigences** : ce qui doit / ne doit pas être fait.
   - **Format de sortie** : structure, longueur, langage.
   - **Critères d'acceptation** : comment juger que c'est réussi.
   - **Exemples** (few-shot) uniquement si un format précis doit être imité.
3. **Raisonnement** : pour une tâche complexe, ajoute un déclencheur zero-shot CoT
   (« réfléchis étape par étape avant de répondre ») plutôt que des exemples.
4. **Concision** : coupe tout ce qui n'aide pas la tâche (le bruit dégrade les résultats).

## Sortie
Rends le prompt final **dans un bloc de code** (copiable tel quel). Si tu as posé des questions,
fournis d'abord une version « hypothèses » utilisable immédiatement, puis propose d'affiner.

## Rappels
- Pour construire une **application**, ne passe pas par ici : utilise le flux brainstorm → spec
  (la spec est déjà l'instruction précise). Ce meta-prompt sert aux **prompts ponctuels** hors projet.
