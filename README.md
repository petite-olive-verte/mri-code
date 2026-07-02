# Module `mri` — « idée → projet » (piloté par commandes)

Boîte à outils pour démarrer/faire évoluer un projet Python avec un agent de code. Tu ouvres un agent
dans le dossier, un **message d'accueil** te présente les commandes, et tu pilotes le flux pas à pas :
`brainstorm → forge → design → devplan → scaffold → implémentation TDD → review → finish`, avec
feedback visuel pour les UI web.

> **Mode piloté par commandes** : l'agent n'auto-déclenche rien ; tu lances une slash command à chaque
> étape, et il te suggère la suivante (+ les appels facultatifs pertinents). Le seul automatisme est le
> message d'accueil au démarrage.

Le module `mri` est une **curation auto-portante** dérivée de [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)
(front d'analyse) et [Superpowers](https://github.com/obra/superpowers) (boucle d'exécution) — tous deux
MIT. Détails : `.toolbox/dev/MERGE_DESIGN.md` (conception) et `.toolbox/dev/DECISIONS.md`.

## Démarrage

```bash
git clone <ton-repo> && cd <ton-repo>
claude                             # ouvre l'agent → message d'accueil → /mri-brainstorm
```

Les skills sont **locales** (`.claude/skills/mri-*`) — pas de plugin externe à installer.
**Codex** : ouvre Codex (lit `AGENTS.md` + `.agents/skills/`).

## Les commandes

Cœur du flux :

| Commande | Rôle | Suggère ensuite |
|---|---|---|
| `/mri-brainstorm <idée>` | facilitation → `brief.md` | `/mri-forge` ou `/mri-design` |
| `/mri-forge` | pressure-test (personas) → HARDENED/CLARIFIED/KILLED | `/mri-design` ou `/mri-brainstorm` |
| `/mri-design` | brief → design technique (`spec.md`) | `/mri-devplan` |
| `/mri-devplan` | spec → `plan.md` (tâches + cases) | `/mri-scaffold-python` ou `/mri-implement` |
| `/mri-scaffold-python` | structure Python (uv/ruff/pytest/mypy) | `/mri-implement` |
| `/mri-implement` | implémentation **TDD** + boucle MCP | `/mri-review` |
| `/mri-review` | revue vs spec/plan | `/mri-finish` |
| `/mri-finish` | merge / PR / cleanup | — |

Facultatifs : `/mri-elicit`, `/mri-adversarial-review`, `/mri-market-research`, `/mri-domain-research`,
`/mri-technical-research`, `/mri-document-project`, `/mri-debug`, `/mri-meta-prompt`, `/mri-resume`.

**Reprise** : l'état vit dans `.mri_devtools/docs/<projet>/progress.md`. À la réouverture, le message
d'accueil détecte un pipeline inachevé et propose **`/mri-resume`**.

## Structure

```
mon-projet/
  README.md  AGENTS.md  CLAUDE.md      ← entrées (racine)
  src/  tests/  pyproject.toml          ← TON projet
  .mri_devtools/docs/<projet>/          ← brief / spec / plan / progress (mémoire générée)
  .toolbox/                             ← sources du module (transition ; → .mri_devtools/ au packaging)
    superpowers/  templates/python-uv/  constitution.md  scripts/  dev/
  .claude/  .mcp.json  .agents/         ← câblage agents (commandes à plat, skills, hooks)
```

## Personnaliser

- **`.toolbox/constitution.md`** — tes conventions (stack, structure, tests…). Levier principal.
- **`.toolbox/templates/python-uv/`** — ta structure de projet concrète.
- **`.toolbox/models.md`** — table de suggestions de modèle par étape.
- **`.claude/settings.json`** — permissions et hooks (retire la section `Stop` si le lint+test te gêne).

## Notes

- Le feedback visuel via MCP (Playwright + Chrome DevTools) nécessite Node/`npx`.
- Le mode command-driven est établi par `AGENTS.md`.
- Le plugin Superpowers est **désactivé** (`settings.json`) : le submodule sert de source d'extraction, pas de runtime.

## Crédits

- [Superpowers](https://github.com/obra/superpowers) (Jesse Vincent, MIT) — boucle d'exécution.
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) (BMad Code LLC, MIT ; « BMad™ » marque) — front d'analyse.
