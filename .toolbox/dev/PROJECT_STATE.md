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
- **Flux E2E** via les commandes `/brainstorm → /devplan → /scaffold → /implement → /review`.
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
| `.claude/skills/{brainstorming,scaffold-python,meta-prompt}/` | Nos skills (canoniques). `brainstorming` = facilitation style BMAD |
| `.claude/commands/` | 8 commandes : brainstorm, plan, scaffold, implement, review, finish, debug, meta-prompt |
| `.claude/hooks/` | `welcome.sh` (accueil), `format.sh` (auto-format), `lint-test.sh` (lint+test) |
| `.agents/skills/` | Miroir portable des skills (Codex) |
| `.mcp.json` | Playwright MCP + Chrome DevTools MCP |
| `.toolbox/superpowers/` | Submodule (moteur) |
| `.toolbox/constitution.md` | Règles de projet éditables, respectées par l'agent |
| `.toolbox/templates/python-uv/` | Scaffold (uv+ruff+pytest+mypy, src/), jetons `__PROJECT_NAME__`/`__PACKAGE_NAME__` |
| `.toolbox/scripts/setup.sh` | Init submodule + guidage |
| `.toolbox/dev/` | Méta-docs : SEARCH_RESULTS, DECISIONS, PLAN, WORKFLOW, PROJECT_STATE |
| `docs/specs/` | Mémoire des runs (spec/plan/tasks générés) — **n'existe pas au départ**, créé à la volée par `/brainstorm` (repo template laissé vide) |

## Pièges techniques (appris à la dure — ne pas re-découvrir)
- **Gestion du marketplace = à la main dans `.claude/settings.json`** (chemin relatif). NE PAS utiliser
  les commandes CLI pour ça : `claude plugin marketplace add <path>` écrit un chemin **absolu** dans
  `~/.claude/settings.json` (perso, non committé) ; `claude plugin marketplace remove` **vide**
  `enabledPlugins`/`extraKnownMarketplaces` du settings **projet**. La source de vérité committée est
  le fichier édité à la main.
- **`extraKnownMarketplaces` (relatif) ne s'enregistre qu'au TRUST interactif** d'une session, pas via
  un appel CLI headless (`marketplace list` ne le montre pas tant que le dossier n'est pas trusté).
  → impossible de valider l'install self-contained en non-interactif ; c'est un test live.
- **`superpowers/CLAUDE.md` = règles de contribution, PAS le bootstrap.** Le vrai bootstrap est la skill
  `using-superpowers`, injectée par le hook SessionStart de Superpowers (qui calcule sa racine depuis
  son propre chemin, pas via `CLAUDE_PLUGIN_ROOT`).
- **Superpowers auto-déclenche agressivement** ; le mode command-driven le neutralise via la priorité
  AGENTS.md (sa propre règle : instructions utilisateur > skills). À confirmer en live ; sinon durcir.
- **Ce repo est à la fois le DEV de la toolbox ET la source du template** → tester le flux ici le
  pollue. Toujours tester dans une **copie**.
- Détails techniques OK : `git mv` du submodule met bien à jour `.gitmodules` ; le cwd du Bash persiste
  (un `cd` composé le décale) → utiliser des chemins absolus.

## Pour reprendre
1. Lis ce fichier, puis `.toolbox/dev/DECISIONS.md` (le pourquoi) et `.toolbox/dev/WORKFLOW.md` (le flux).
2. `git status` / `git log`.
3. Si Superpowers inactif : `git submodule update --init` puis `/reload-plugins`
   (ou `claude --plugin-dir ./.toolbox/superpowers`).

## Retours du 1er test E2E (2026-06-29)
- **`/brainstorm` pas assez mordant → RÉGLÉ.** Créé une skill maison **`brainstorming`**
  (`.claude/skills/brainstorming/SKILL.md` + `techniques.md`, miroir `.agents/skills/`), inspirée de
  BMAD-METHOD (MIT) : posture facilitateur, 3 modes, menu de techniques, divergence une-à-la-fois,
  challenge explicite (assumption listing, pre-mortem, contre-arguments), convergence → spec. La
  commande `/brainstorm` invoque cette skill (plus `superpowers:brainstorming`). Voir Décision 9.
  ⚠️ **Pas encore testé en live** (vérifier que la facilitation se déclenche bien et reste interactive).
- **Collision `/plan`** avec la commande native de Claude Code → notre commande est renommée
  (voir `.claude/commands/`). Penser à propager tout renommage dans AGENTS.md, README, welcome.sh,
  brainstorm.md et les docs.
- **`docs/` retiré du template** pour livrer un repo vraiment vide ; recréé à la volée au 1er run.
- **`ruff check .` ramassait `.toolbox/superpowers/*.py` → RÉGLÉ.** Ajout de
  `extend-exclude = [".toolbox"]` dans `[tool.ruff]` du template `pyproject.toml` (vérifié : ruff
  ignore bien `.toolbox`, voit `src/`). Le hook `lint-test.sh` lance `ruff check .` depuis la racine,
  donc il hérite de cette config une fois le projet scaffoldé.

## Prochaines étapes possibles
- **Test E2E live** (voir ci-dessous) — dans une **copie** du repo pour garder le template propre.
- **Phase 2 — module méthodo curé (Décision 10)** : après l'E2E, extraire les briques retenues
  (skills `brainstorming`/`meta-prompt`/`scaffold-python` + ce qu'on garde de Superpowers) dans un
  **repo séparé versionné**, l'intégrer ici en module (submodule épinglé ou plugin), version figée.
  Conserver le socle cross-tool (SKILL.md + AGENTS.md) et les attributions MIT.
- Adaptateurs Codex/ZCode dédiés ; orchestration multi-agents (Claude cerveau / GLM bras) ;
  distribution en plugin installable ; skill `refine-prompt` si besoin réel.

## Plan de test (E2E)
> Dans une **copie** du repo (`cp -r` ou clone), pour ne pas transformer le template en projet.
1. Ouvre Claude Code ; le message d'accueil doit s'afficher (commandes + `/brainstorm`).
2. `/brainstorm une petite CLI todo en python` → questions, puis `docs/specs/<projet>/spec.md`.
   Vérifie que l'agent **n'a pas** auto-déclenché de skill avant la commande.
3. `/devplan` → `plan.md` + `tasks.md` (cases) validés en plan mode.
4. `/scaffold` → `src/`/`tests/`/`pyproject.toml` selon `.toolbox/constitution.md` ; `uv run pytest` vert.
5. `/implement` → TDD, cases cochées au fur et à mesure ; hooks actifs.
6. `/review` → `/finish`. (Web : redémarrer + approuver MCP pour le feedback visuel.)
