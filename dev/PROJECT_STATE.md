# État du projet — reprise de session

> **À lire en premier par une nouvelle instance qui REPREND LE DÉVELOPPEMENT du module.**
> Dernière mise à jour : 2026-07-03.
> ⚠️ Ce fichier contient de l'HISTORIQUE (sections « ancien état », carte pré-reorg…). La réalité
> actuelle est décrite dans le bloc « Statut » ci-dessous + `dev/MERGE_DESIGN.md` + `dev/BUILD_PLAN.md`.

## Ce qu'est ce projet (actuel)

**`mri-devtools`** : un **repo source-first distribuable** (pas un template). Contenu installable dans
`payload/`, installeur `bin/install.mjs`/`install.sh` (+ `package.json`) qui **copie** le module dans un
projet cible (`.claude/` = vrais fichiers, `.mri_devtools/` = config+constitution+models+templates+docs).
Installation : `npx git+ssh://git@github.com/MatioRIGARD/mri-devtools.git` (privé/SSH) ou clone+`install.sh`,
avec config `--lang`/`--doc-lang`/`--user`. **Payload entièrement en anglais** ; langue de l'agent
configurable. Le **submodule Superpowers a été retiré** (skills déjà extraites ; attribution dans `LICENSE`).
Méthodo = module `mri` (fusion BMAD analyse × Superpowers exécution). Voir Décisions 9-12.

## Statut : MODULE « mri » CONSTRUIT (fusion BMAD × Superpowers) — reste l'E2E live

> **MàJ 2026-07-02.** Source de vérité : **`dev/MERGE_DESIGN.md`** + **`dev/BUILD_PLAN.md`**. Le module
> `mri` est construit (Lots 0-8) PUIS le repo a été **réorganisé en source-first distribuable** :
> contenu installable dans **`payload/`**, méta-docs dans **`dev/`** (submodule → `dev/superpowers`),
> **installeur** `bin/install.mjs` (+ `install.sh`, `package.json`). Installation :
> **`npx git+ssh://git@github.com/MatioRIGARD/dev-toolbox.git`** (privé/SSH) ou `git clone`+`./install.sh`.
> Reste : **E2E live** (interactif) + **push du repo distant** (par l'utilisateur).

Le module `mri` remplace l'ancien flux : 19 skills `payload/skills/mri-*` (front BMAD réimplémenté +
back Superpowers extrait/adapté), 17 commandes `payload/commands/mri-*.md`, reprise via `progress.md`
+ `/mri-resume`, suggestions de modèle (`payload/models.md`), installeur `bin/install.mjs`
→ `.mri_devtools/`. Plugin Superpowers **désactivé** (skills auto-portantes). Voir Décisions 11 & 12.

Commits clés du build mri : `30cf002` (lot 0) → `db901e1` (lot 7). Historique antérieur (A1/A2/build
initial) conservé plus bas.

> **MàJ 2026-07-03 (fait autorité sur les points ci-dessous).**
> - **Plus de dossier `payload/commands/`** : les **skills SONT les slash commands** `/mri-*`. Les 17
>   skills d'entrée portent `disable-model-invocation: true` (mode command-driven strict) ; seuls
>   `mri-tdd`/`mri-verify`/`mri-worktrees` restent auto-invocables. (20 skills au total.)
> - **Plan mode intégré** : `mri-design` & `mri-devplan` entrent en plan mode natif (`EnterPlanMode`),
>   gate = `ExitPlanMode`. `mri-devplan` produit un plan **contrat** (pas le code complet). Voir Décision 14.
> - **Revue complète faite** (Décision 15) : DeepSeek retiré → Sonnet ; un seul `progress.md` (phases) +
>   ledger `state/sdd/task-ledger.md` (tâches) ; titres H1 maison ; `welcome.sh` robuste sans `python3` ;
>   `find-polluter.sh` + fixtures d'éval supprimés ; `mri-scaffold-python` corrigé (sed en staging isolé).
> - **Reprise** : le pipeline détecte l'état via `.mri_devtools/docs/<project>/progress.md` (plus
>   `docs/specs/*/tasks.md`). Reste toujours : **E2E live** + **push distant** (utilisateur).

### Archive — état antérieur (pré-mri)
```
c27405d A1 command-driven · 228b8c9 A2 .toolbox/ · b1f5caf..b8d4b93 build initial
```

### Vérifié ✅ (⚠️ log HISTORIQUE pré-mri — noms/chemins périmés : `/brainstorm`, `docs/specs/`, `tasks.md`, submodule, marketplace. Réalité actuelle = bloc « MàJ 2026-07-03 » + « Plan de test (E2E) » ci-dessus)
- Scaffold Python d'essai : `uv sync` + `pytest` (100% cov) + `ruff` verts ; aucun jeton résiduel.
- Hooks `format.sh`/`lint-test.sh` : no-op sans `pyproject.toml`, PASS dans un projet, non-bloquants.
- `welcome.sh` (SessionStart) : produit un JSON `additionalContext` valide, détecte un plan inachevé
  (`docs/specs/*/tasks.md` avec `- [ ]`) → suggère `/implement`, sinon `/brainstorm`.
- A2 : submodule déplacé (`git mv`), `.gitmodules`/settings/skill/setup à jour, marketplace.json présent.

### Pas encore testé en live (⚠️ HISTORIQUE pré-mri — remplacé par « Plan de test (E2E) — À JOUR » ci-dessus ; plus de plugin/submodule/marketplace)
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
| `.claude/skills/{brainstorm-facilitation,scaffold-python,meta-prompt}/` | Nos skills (canoniques). `brainstorm-facilitation` = facilitation style BMAD (nom distinct pour ne pas entrer en collision avec `superpowers:brainstorming`) |
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
- **`/brainstorm` pas assez mordant → RÉGLÉ.** Créé une skill maison **`brainstorm-facilitation`**
  (`.claude/skills/brainstorm-facilitation/SKILL.md` + `techniques.md`, miroir `.agents/skills/`), inspirée de
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
  (skills `brainstorm-facilitation`/`meta-prompt`/`scaffold-python` + ce qu'on garde de Superpowers) dans un
  **repo séparé versionné**, l'intégrer ici en module (submodule épinglé ou plugin), version figée.
  Conserver le socle cross-tool (SKILL.md + AGENTS.md) et les attributions MIT.
- Adaptateurs Codex/ZCode dédiés ; orchestration multi-agents (Claude cerveau / GLM bras) ;
  distribution en plugin installable ; skill `refine-prompt` si besoin réel.

## Plan de test (E2E) — À JOUR 2026-07-03
> Dans une **cible jetable** (`node bin/install.mjs /tmp/e2e-test --lang French --user Mathieu`), ouvrir
> Claude Code **dans la cible** (pas dans ce repo). Idée d'exemple : « une petite CLI todo en Python ».
> Ce que l'E2E valide et que le statique ne couvre pas :

1. **Accueil + command-driven** : `welcome.sh` s'affiche (logo + `/mri-brainstorm`) ; l'agent
   **n'auto-déclenche aucune** skill avant ta commande.
2. **config.json lu au démarrage** : l'agent parle en French et t'appelle Mathieu (édite le JSON → effet
   à la session suivante).
3. `/mri-brainstorm` → facilitation (une question à la fois) → `.mri_devtools/docs/<projet>/brief.md`.
   Puis `/mri-forge` (pressure-test) optionnel.
4. `/mri-design` → **⚠️ vérifier qu'il ENTRE en plan mode tout seul** (point non garanti d'ici) ;
   `ExitPlanMode` = gate → `spec.md`. Suggère `/mri-devplan` **+ le modèle**.
5. `/mri-devplan` → plan mode ; `plan.md` = **contrat** (pas 2000 lignes de code). → scaffold/implement.
6. `/mri-scaffold-python` → `uv sync`+`pytest`+`ruff` verts ; **vérifier que les templates
   `.mri_devtools/templates/` ne sont PAS corrompus** (le bug du `sed` corrigé).
7. `/mri-implement` → TDD, cases cochées dans `plan.md`, `state/sdd/task-ledger.md`, hooks actifs.
8. **Reprise** : tuer la session en cours → rouvrir → `welcome.sh` suggère `/mri-resume` (via
   `progress.md`) → ré-entre à la bonne étape.
9. `/mri-review` → `/mri-finish`. (Web : approuver les MCP pour le feedback visuel.)

> Filet si `/mri-design` n'entre pas seul en plan mode : `permissions.defaultMode: "plan"` dans
> `settings.json` (au démarrage de session).
