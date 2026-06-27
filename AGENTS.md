# Bootstrap — assistant d'amorçage de projet

Tu es ouvert dans un **repo template** dont le but est de transformer une **idée vague en projet
Python** prêt à coder, puis de laisser l'agent construire l'essentiel **avant un contrôle humain**.
Ce fichier est lu au démarrage par tout agent (Claude Code, Codex, …) et oriente la session.

## Au premier message de l'utilisateur

Si l'utilisateur décrit une idée / un projet à construire : **n'écris pas de code tout de suite**.
Lance d'abord le **brainstorm** (compétence `superpowers:brainstorming`). Le flux est :

1. **Brainstorm** — clarifier l'idée (questions socratiques, hypothèses, pré-mortem).
2. **Spec** — produire une spec précise avec **critères d'acceptation**, persistée dans `docs/specs/<nom>/spec.md`.
3. **Plan** — plan technique + tâches ordonnées (`docs/specs/<nom>/plan.md`, `tasks.md`). Valide en **plan mode**.
4. **Scaffold** — générer le projet Python via la skill `scaffold-python` (selon `constitution.md`).
5. **Implémentation** — en **TDD** (`superpowers:test-driven-development`, red-green-refactor), pilotée
   par sous-agents (`superpowers:subagent-driven-development`).
6. **Review + feedback** — review (`superpowers:requesting-code-review`) + vérification runtime via MCP.

## Orientation one-shot

On **front-load la précision** (brainstorm + spec + `constitution.md`) puis on laisse l'agent
implémenter de façon autonome. Le seul point de contrôle humain obligatoire est la **validation du
plan**. Après « go », déroule l'implémentation sans t'arrêter à chaque étape tant que les tests passent.

## Constitution (règles du projet)

Lis **`constitution.md`** à la racine et **respecte-la** : c'est le règlement non-négociable du projet
(stack, qualité, tests, architecture, conventions de structure/nommage). En cas de conflit avec une
skill, la constitution et l'utilisateur priment.

## Context management (le repo est la mémoire)

- **Persiste tout ce qui compte sur disque** : spec, plan, `tasks.md` (cases à cocher = progression),
  journal de décisions, dans `docs/specs/`. Ne compte **pas** sur `/compact` comme mémoire.
- Après un `/compact` ou une reprise, **relis `tasks.md`** pour savoir où tu en es.
- Délègue l'exploration lourde (lectures, recherches) à des **sous-agents** pour garder le contexte court.

## Feedback visuel / runtime

Pour toute UI web, utilise les MCP déclarés dans `.mcp.json` : **Playwright** (piloter/tester) et
**Chrome DevTools** (console/réseau/déboguer). Boucle : écrire → exécuter → observer → corriger.

## Moteur Superpowers

La méthodologie (brainstorm, planning, TDD, sous-agents, review, debugging) vient du plugin
**Superpowers** (dossier `superpowers/`, submodule). S'il n'est pas actif (les skills `superpowers:*`
n'existent pas), demande à l'utilisateur de lancer **`./scripts/setup.sh`** une fois, ou de relancer
avec `claude --plugin-dir ./superpowers`.

## Priorité des instructions

1. Instructions explicites de l'utilisateur (ce fichier, `constitution.md`, demandes directes).
2. Skills Superpowers.
3. Comportement par défaut.
