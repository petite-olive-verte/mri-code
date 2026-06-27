# État du projet — reprise de session

> **À lire en premier par une nouvelle instance qui REPREND LE DÉVELOPPEMENT de la toolbox**
> (≠ `AGENTS.md`, qui s'adresse à l'utilisateur d'un projet *généré* à partir du template).
> Dernière mise à jour : 2026-06-28.

## Ce qu'est ce projet

Un **repo template GitHub piloté par commandes** : *Use this template*, on ouvre un agent dans le
dossier, un **message d'accueil** présente les commandes, et l'utilisateur pilote le flux
(idée → spec → plan → scaffold → implémentation TDD → review), avant contrôle humain. Orienté one-shot.

Moteur : [Superpowers](https://github.com/obra/superpowers) (MIT, **submodule** dans
`.toolbox/superpowers`). Notre couche : amorçage command-driven, feedback MCP, scaffold Python
éditable, constitution, meta-prompt. **Décisions fermes : on garde le submodule ; mode command-driven.**

## Statut : BUILD + A1 + A2 FAITS

Tout est construit et committé sur `main` (working tree propre). Commits clés :

```
c27405d A1: mode piloté par commandes (command-driven)
228b8c9 A2: ranger toute la toolchain dans .toolbox/
fc0cc6f docs: WORKFLOW.md + maj PROJECT_STATE
c69d8e0 Activation self-contained de Superpowers
b1f5caf..b8d4b93  Lots 0-6 (build initial)
```

### Vérifié ✅
- Scaffold Python d'essai : `uv sync` + `pytest` (100% cov) + `ruff` verts ; aucun jeton résiduel.
- Hooks `format.sh`/`lint-test.sh` : no-op sans `pyproject.toml`, PASS dans un projet, non-bloquants.
- `welcome.sh` (SessionStart) : produit un JSON `additionalContext` valide, détecte un plan inachevé
  (`docs/specs/*/tasks.md` avec `- [ ]`) → suggère `/implement`, sinon `/brainstorm`.
- A2 : submodule déplacé (`git mv`), `.gitmodules`/settings/skill/setup à jour, marketplace.json présent.

### Pas encore testé en live (session interactive requise)
- **Mode command-driven en vrai** : que l'agent N'auto-déclenche PAS et attende les commandes
  (override du bootstrap Superpowers via AGENTS.md — à confirmer ; sinon durcir, ex. ne pas charger
  son hook).
- **Flux E2E** via les commandes `/brainstorm → /plan → /scaffold → /implement → /review`.
- **MCP** Playwright / Chrome DevTools : nécessite un redémarrage + approbation du `.mcp.json`.
- **Activation self-contained** : sur un clone neuf, le prompt de confiance installe Superpowers
  depuis `extraKnownMarketplaces` (relatif). (En local, état réinstallable via `--plugin-dir` ou
  `claude plugin install superpowers@superpowers-dev --scope project`.)

## Carte des fichiers (après A2)

| Chemin | Rôle |
|---|---|
| `AGENTS.md` | Bootstrap **command-driven** (n'auto-déclenche rien, liste les commandes, override Superpowers) |
| `CLAUDE.md` | Importe `@AGENTS.md` + spécificités Claude |
| `.claude/settings.json` | Permissions, hooks (SessionStart/PostToolUse/Stop), `extraKnownMarketplaces` (relatif) + `enabledPlugins` |
| `.claude/skills/{scaffold-python,meta-prompt}/` | Nos skills (canoniques) |
| `.claude/commands/` | 8 commandes : brainstorm, plan, scaffold, implement, review, finish, debug, meta-prompt |
| `.claude/hooks/` | `welcome.sh` (accueil), `format.sh` (auto-format), `lint-test.sh` (lint+test) |
| `.agents/skills/` | Miroir portable des skills (Codex) |
| `.mcp.json` | Playwright MCP + Chrome DevTools MCP |
| `.toolbox/superpowers/` | Submodule (moteur) |
| `.toolbox/constitution.md` | Règles de projet éditables, respectées par l'agent |
| `.toolbox/templates/python-uv/` | Scaffold (uv+ruff+pytest+mypy, src/), jetons `__PROJECT_NAME__`/`__PACKAGE_NAME__` |
| `.toolbox/scripts/setup.sh` | Init submodule + guidage |
| `.toolbox/dev/` | Méta-docs : SEARCH_RESULTS, DECISIONS, PLAN, WORKFLOW, PROJECT_STATE |
| `docs/specs/` | Mémoire des runs (spec/plan/tasks générés) — vide pour l'instant |

## Pour reprendre
1. Lis ce fichier, puis `.toolbox/dev/DECISIONS.md` (le pourquoi) et `.toolbox/dev/WORKFLOW.md` (le flux).
2. `git status` / `git log`.
3. Si Superpowers inactif : `git submodule update --init` puis `/reload-plugins`
   (ou `claude --plugin-dir ./.toolbox/superpowers`).

## Prochaines étapes possibles
- **Test E2E live** (voir ci-dessous) — dans une **copie** du repo pour garder le template propre.
- Adaptateurs Codex/ZCode dédiés ; orchestration multi-agents (Claude cerveau / GLM bras) ;
  distribution en plugin installable ; skill `refine-prompt` si besoin réel.

## Plan de test (E2E)
> Dans une **copie** du repo (`cp -r` ou clone), pour ne pas transformer le template en projet.
1. Ouvre Claude Code ; le message d'accueil doit s'afficher (commandes + `/brainstorm`).
2. `/brainstorm une petite CLI todo en python` → questions, puis `docs/specs/<projet>/spec.md`.
   Vérifie que l'agent **n'a pas** auto-déclenché de skill avant la commande.
3. `/plan` → `plan.md` + `tasks.md` (cases) validés en plan mode.
4. `/scaffold` → `src/`/`tests/`/`pyproject.toml` selon `.toolbox/constitution.md` ; `uv run pytest` vert.
5. `/implement` → TDD, cases cochées au fur et à mesure ; hooks actifs.
6. `/review` → `/finish`. (Web : redémarrer + approuver MCP pour le feedback visuel.)
