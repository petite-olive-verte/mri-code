# Toolbox IA — « idée → projet » (template open-and-go)

Repo **template** pour démarrer un projet Python avec un agent de code. Le principe : `Use this
template`, tu **ouvres un agent de code dans le dossier**, et l'interaction démarre — brainstorm →
spec précise → plan → scaffold → implémentation en **TDD** avec **feedback visuel**, avant ton contrôle.

> **Orienté one-shot** : on front-load la précision (brainstorm + spec + `constitution.md`), puis on
> laisse l'agent construire l'essentiel de façon autonome. Seul point de contrôle obligatoire : la
> validation du plan.

Le moteur méthodologique est [**Superpowers**](https://github.com/obra/superpowers) (MIT, vendoré en
submodule) ; cette couche ajoute l'amorçage « open-and-go », le **feedback visuel** (MCP), un
**scaffold Python éditable** et une **constitution** de projet. Voir `docs/DECISIONS.md` pour le pourquoi.

## Démarrage

```bash
# 1. Crée ton repo depuis ce template (bouton "Use this template" sur GitHub), puis :
git clone <ton-repo> && cd <ton-repo>

# 2. Setup unique (récupère Superpowers + l'active comme plugin Claude Code) :
./scripts/setup.sh

# 3. Ouvre un agent dans le dossier et décris ton idée :
claude          # le brainstorm démarre (AGENTS.md)
```

**Alternative open-and-go (sans install)** : `claude --plugin-dir ./superpowers`
**Avec Codex** : `git submodule update --init` puis ouvre Codex ; il lit `AGENTS.md` et les skills
(`.agents/skills/`, plus le `.codex-plugin/` de Superpowers).

## Le flux

`brainstorm → spec (critères d'acceptation) → plan (validé en plan mode) → scaffold Python → TDD
(red-green-refactor) → review + feedback navigateur`. Les artefacts sont persistés dans `docs/specs/`
(c'est la mémoire du projet : on ne compte pas sur `/compact`).

## Contenu

| Élément | Rôle |
|---|---|
| `AGENTS.md` / `CLAUDE.md` | Bootstrap portable : oriente le flux + le one-shot |
| `superpowers/` (submodule) | Moteur : brainstorm, planning, TDD, sous-agents, review, debugging — MIT |
| `constitution.md` | **Tes règles** éditables (stack, qualité, tests, archi) que l'agent respecte |
| `templates/python-uv/` | Scaffold Python éditable (uv + ruff + pytest + mypy, layout `src/`) |
| `.claude/skills/` (+ `skills/`, `.agents/skills/`) | Skills `scaffold-python` et `meta-prompt` |
| `.claude/commands/meta-prompt.md` | Commande `/meta-prompt` (optimise un prompt ponctuel) |
| `.claude/hooks/` | `format.sh` (auto-format à l'édition) + `lint-test.sh` (résumé lint+tests à l'arrêt) |
| `.mcp.json` | Feedback visuel/runtime : Playwright MCP + Chrome DevTools MCP |
| `docs/` | `SEARCH_RESULTS.md` (état de l'art), `DECISIONS.md` (choix), `specs/` (mémoire de run) |

## Personnaliser

- **`constitution.md`** — impose tes conventions (structure, nommage, stack…). C'est le levier principal.
- **`templates/python-uv/`** — ta structure de projet concrète.
- **`.claude/settings.json`** — permissions et hooks (retire la section `Stop` si le lint+test
  automatique te dérange).

## Notes

- Le feedback visuel via MCP nécessite Node/`npx` (Playwright/Chrome DevTools sont récupérés à la volée).
- L'auto-déclenchement des skills Superpowers suit son mécanisme officiel (hook SessionStart) ; il
  s'active après `setup.sh` ou via `--plugin-dir`. Test d'acceptation : ouvrir une session et dire
  « Let's make a react todo list » doit lancer le brainstorm.

## Crédits

[Superpowers](https://github.com/obra/superpowers) (Jesse Vincent, MIT).
