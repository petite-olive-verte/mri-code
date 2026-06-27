# Toolbox IA — « idée → projet » (template open-and-go)

Repo **template** pour démarrer un nouveau projet Python avec un agent de code (Claude Code, et
portable vers Codex/autres). Le principe : tu fais `Use this template`, tu **ouvres un agent de code
dans le dossier**, et l'interaction démarre toute seule — brainstorm → spec précise → plan → scaffold
→ implémentation en TDD avec feedback visuel, avant ton contrôle.

> Pensé pour le **one-shot** : on front-load la précision (brainstorm + spec + `constitution.md`),
> puis on laisse l'agent construire l'essentiel de façon autonome.

## Démarrage rapide

```bash
# 1. Créer ton repo depuis ce template (bouton "Use this template" sur GitHub), puis :
git clone <ton-repo> && cd <ton-repo>
git submodule update --init --recursive   # récupère le moteur Superpowers

# 2. Ouvrir un agent de code dans le dossier (ex. Claude Code) :
claude
# -> l'agent lit AGENTS.md et te propose de démarrer le brainstorm.
```

## Ce qu'il y a dans la boîte

| Élément | Rôle |
|---|---|
| `AGENTS.md` / `CLAUDE.md` | Bootstrap portable : oriente le flux idée→code + le one-shot |
| `superpowers/` (submodule) | Le moteur méthodologique (brainstorm, planning, TDD, sous-agents, review) — MIT |
| `constitution.md` | **Tes règles** éditables (stack, qualité, tests, archi) que l'agent respecte |
| `templates/python-uv/` | Scaffold Python éditable (uv + ruff + ty/mypy + pytest + pre-commit) |
| `skills/` | Nos skills : `scaffold-python`, `meta-prompt` (autonome) |
| `.claude/` | Adaptateur Claude : commandes, hooks (SessionStart, lint+test), permissions |
| `.mcp.json` | Feedback visuel/runtime : Playwright MCP + Chrome DevTools MCP |
| `docs/` | `SEARCH_RESULTS.md` (état de l'art), `DECISIONS.md` (choix), `specs/` (mémoire de run) |

## Personnaliser

- Édite **`constitution.md`** pour imposer tes conventions (structure, nommage, stack…).
- Édite **`templates/python-uv/`** pour ta structure de projet concrète.
- Active/désactive les skills Superpowers via `AGENTS.md`.

## Crédits

S'appuie sur [Superpowers](https://github.com/obra/superpowers) (Jesse Vincent, MIT) comme moteur
méthodologique. Voir `docs/DECISIONS.md` pour le détail des choix d'architecture.
