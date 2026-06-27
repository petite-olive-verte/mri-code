# État du projet — reprise de session

> **À lire en premier par une nouvelle instance qui REPREND LE DÉVELOPPEMENT de la toolbox**
> (≠ `AGENTS.md`, qui s'adresse à l'utilisateur d'un projet *généré* à partir du template).
> Dernière mise à jour : 2026-06-27.

## Ce qu'est ce projet

Un **repo template GitHub « open-and-go »** : on fait *Use this template*, on ouvre un agent de code
dans le dossier, et l'interaction démarre (idée → spec → plan → scaffold → implémentation TDD avec
feedback visuel) avant contrôle humain. Orienté **one-shot** (front-load de la précision).

Le **moteur méthodologique** est [Superpowers](https://github.com/obra/superpowers) (MIT, vendoré en
**submodule** `superpowers/`). Notre couche ajoute : amorçage, feedback MCP, scaffold Python éditable,
constitution, meta-prompt. **Décision ferme : on garde le submodule.**

## Statut : BUILD TERMINÉ

Tout est construit et committé sur `main` (working tree propre). 8 commits :

```
c69d8e0 Activation self-contained de Superpowers (option A)
b1f5caf Lot 6: portabilité (Codex) + README final
43f9a69 Lot 5: skill meta-prompt autonome + commande /meta-prompt
f38a779 Lot 4: feedback visuel/runtime (MCP) + hooks lint/test
f2c3997 Lot 3: scaffold Python (template uv) + skill scaffold-python
55fdb9c Lot 2: constitution.md
76883f1 Lot 1: bootstrap open-and-go + orientation one-shot
b8d4b93 Lot 0: squelette + Superpowers en submodule
```

### Vérifié ✅
- Scaffold Python d'essai : `uv sync` + `pytest` (100% cov) + `ruff` verts ; aucun jeton résiduel.
- Hooks `format.sh`/`lint-test.sh` : silencieux sans `pyproject.toml`, PASS dans un projet, non-bloquants.
- Activation Superpowers : marketplace local déclaré en **chemin relatif** dans `.claude/settings.json`,
  `claude plugin list` → `superpowers@superpowers-dev` **enabled (scope projet)** ; skills `superpowers:*`
  visibles après `/reload-plugins`.

### Pas encore testé en live (nécessite une session interactive / une action humaine)
- **Flux end-to-end complet** (idée → brainstorm → spec → plan → scaffold → TDD).
- **MCP** Playwright / Chrome DevTools : nécessite un **redémarrage** de Claude Code (approbation du
  `.mcp.json` au prompt de confiance) + un projet web pour être exercé.

## Carte des fichiers

| Chemin | Rôle |
|---|---|
| `AGENTS.md` / `CLAUDE.md` | Bootstrap portable (s'adresse à l'utilisateur du template) |
| `superpowers/` | Submodule (moteur Superpowers) |
| `.claude/settings.json` | Permissions, hooks, `extraKnownMarketplaces` (relatif) + `enabledPlugins` |
| `.claude/skills/{scaffold-python,meta-prompt}/` | Nos skills (canoniques) |
| `.claude/commands/meta-prompt.md` | Commande `/meta-prompt` |
| `.claude/hooks/{format.sh,lint-test.sh}` | Auto-format à l'édition / lint+test à l'arrêt |
| `skills/`, `.agents/skills/` | Exports portables (symlinks) des skills (Codex, etc.) |
| `.mcp.json` | Playwright MCP + Chrome DevTools MCP |
| `constitution.md` | Règles de projet éditables, respectées par l'agent |
| `templates/python-uv/` | Scaffold Python (uv+ruff+pytest+mypy, src/), jetons `__PROJECT_NAME__`/`__PACKAGE_NAME__` |
| `scripts/setup.sh` | Init submodule + guidage (ne touche plus aux settings perso) |
| `docs/SEARCH_RESULTS.md` | État de l'art (recherche) |
| `docs/DECISIONS.md` | Les 8 décisions d'archi + justifications |
| `PLAN.md` | Plan de build (lots) |
| `docs/specs/` | Mémoire des runs (spec/plan/tasks générés) — vide pour l'instant |

## Pour reprendre

1. Lis ce fichier, puis `docs/DECISIONS.md` (le pourquoi) et `PLAN.md` (le quoi).
2. `git status` / `git log` pour l'état.
3. Si le plugin n'est pas chargé : `git submodule update --init` puis `/reload-plugins`
   (ou `claude plugin install superpowers@superpowers-dev --scope project`).

## Prochaines étapes possibles (hors périmètre du build initial)
- **Test E2E** sur une idée jouet (voir « Plan de test » ci-dessous) — à faire dans une **copie**
  du repo pour garder le template propre.
- Adaptateurs Codex/ZCode dédiés ; orchestration multi-agents (Claude cerveau / GLM bras) ;
  distribution en plugin installable ; skill `refine-prompt` si besoin réel.

## Plan de test (E2E)
> Faire dans une **copie** du repo (`cp -r` ou un clone), pour ne pas transformer le template en projet.
1. Ouvre Claude Code dans la copie ; `/reload-plugins` doit montrer le plugin + les skills `superpowers:*`.
2. Dis : « Je veux une petite CLI todo en Python ». Attendu : `superpowers:brainstorming` se déclenche
   (pas de code immédiat) → questions → spec.
3. Laisse aller jusqu'au plan (validation en plan mode), puis au scaffold : la skill `scaffold-python`
   doit générer `src/`, `tests/`, `pyproject.toml` (selon `constitution.md`) ; `uv run pytest` vert.
4. Implémentation en TDD (`superpowers:test-driven-development`). Vérifie que les hooks tournent.
5. (Optionnel, projet web) redémarre Claude, approuve les MCP, teste un screenshot / lecture console.
