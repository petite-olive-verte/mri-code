# Toolbox IA — « idée → projet » (template piloté par commandes)

Repo **template** pour démarrer un projet Python avec un agent de code. Tu fais *Use this template*,
tu ouvres un agent dans le dossier, un **message d'accueil** te présente les commandes, et tu pilotes
le flux pas à pas : `brainstorm → plan → scaffold → implémentation TDD → review → finish`, avec
feedback visuel pour les UI web.

> **Mode piloté par commandes** : l'agent n'auto-déclenche rien ; tu lances une slash command à chaque
> étape, et il te suggère la suivante. Le seul automatisme est le message d'accueil au démarrage.

Moteur méthodologique : [**Superpowers**](https://github.com/obra/superpowers) (MIT, vendoré en
submodule dans `.toolbox/superpowers`). Détails des choix dans `.toolbox/dev/DECISIONS.md` ; le
déroulé complet dans `.toolbox/dev/WORKFLOW.md`.

## Démarrage

```bash
git clone <ton-repo> && cd <ton-repo>
./.toolbox/scripts/setup.sh        # init du submodule Superpowers
claude                             # ouvre l'agent → message d'accueil → /brainstorm
```

Le marketplace local + le plugin sont **déclarés dans `.claude/settings.json`** (chemin relatif
`./.toolbox/superpowers`) : un clone neuf est auto-suffisant — à la confiance du dossier, Claude
propose d'installer Superpowers.
**Fallback fiable (sans install)** : `claude --plugin-dir ./.toolbox/superpowers`.
**Codex** : `git submodule update --init` puis ouvre Codex (lit `AGENTS.md` + `.agents/skills/`).

## Les commandes

| Commande | Rôle | Suggère ensuite |
|---|---|---|
| `/brainstorm <idée>` | clarifier l'idée → spec + critères d'acceptation | `/devplan` |
| `/devplan` | plan technique + `tasks.md` (cases à cocher), validé en plan mode | `/scaffold` ou `/implement` |
| `/scaffold` | structure Python (uv/ruff/pytest/mypy) selon `constitution.md` | `/implement` |
| `/implement` | implémentation **en TDD**, coche les tâches au fur et à mesure | `/review` |
| `/review` | revue vs spec/plan | `/finish` |
| `/finish` | merge / PR / cleanup | — |
| `/debug` | débogage systématique (cause racine d'abord) | — |
| `/meta-prompt <texte>` | optimiser un prompt ponctuel | — |

**Reprise** : la mémoire vit dans `docs/specs/<projet>/` (`tasks.md` avec cases). À la réouverture, le
message d'accueil détecte un plan inachevé et propose `/implement` pour reprendre.

## Structure

```
mon-projet/
  README.md  AGENTS.md  CLAUDE.md      ← entrées (racine)
  src/  tests/  pyproject.toml          ← TON projet
  docs/specs/<projet>/                  ← spec / plan / tasks (mémoire)
  .toolbox/                             ← toolchain (caché, committé)
    superpowers/  templates/python-uv/  constitution.md  scripts/  dev/
  .claude/  .mcp.json  .agents/         ← dotfiles agents (cachés)
```

## Personnaliser

- **`.toolbox/constitution.md`** — tes conventions (stack, structure, tests…). Levier principal.
- **`.toolbox/templates/python-uv/`** — ta structure de projet concrète.
- **`.claude/settings.json`** — permissions et hooks (retire la section `Stop` si le lint+test
  automatique te dérange).

## Notes

- Le feedback visuel via MCP (Playwright + Chrome DevTools) nécessite Node/`npx`.
- Le mode command-driven est établi par `AGENTS.md`, qui prime sur l'auto-déclenchement de Superpowers.

## Crédits

[Superpowers](https://github.com/obra/superpowers) (Jesse Vincent, MIT).
