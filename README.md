# dev-toolbox — le module `mri`

Module **piloté par commandes** qui transforme une idée en projet Python avec un agent de code :
`brainstorm → forge → design → devplan → scaffold → implémentation TDD → review → finish`, avec
feedback visuel (MCP) pour les UI web. Curation auto-portante de
[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) (analyse) et
[Superpowers](https://github.com/obra/superpowers) (exécution) — tous deux MIT.

Ce repo est **source-first** : le contenu installable vit dans `payload/`, l'installeur à la racine le
déploie dans un projet cible.

## Installation dans un projet (repo privé → collaborateurs)

**Une commande (recommandé, non-curl, via SSH) :**
```bash
cd mon-projet
npx git+ssh://git@github.com/MatioRIGARD/dev-toolbox.git          # installe dans le dossier courant
# épingler une version :  npx git+ssh://git@github.com/MatioRIGARD/dev-toolbox.git#v0.1.0
```
> `curl … | bash` **ne marche pas** ici : le repo est privé (le raw exige une auth). `npx` via `git+ssh`
> utilise la **clé SSH** du collaborateur (accès déjà accordé) — aucun token à gérer.

**Alternative sans Node (clone + script) :**
```bash
git clone git@github.com:MatioRIGARD/dev-toolbox.git
./dev-toolbox/install.sh mon-projet        # ou: cd mon-projet && /chemin/dev-toolbox/install.sh
```

**Si Claude ne découvre pas les skills/commandes liées** (symlinks) : relance avec `--copy`
(`npx … -- --copy` ou `./install.sh mon-projet --copy`).

## Ce qui est installé dans la cible
```
mon-projet/
  AGENTS.md  CLAUDE.md  .mcp.json      ← entrées (imposées à la racine par Claude Code)
  .claude/  commands/ (à plat) · skills/ · hooks/ · settings.json   ← câblage (→ .mri_devtools/)
  .mri_devtools/                       ← LE MODULE + docs/<projet>/ (brief/spec/plan/progress générés)
  .agents/skills/                      ← miroir portable (Codex)
```
La racine de ton projet reste **propre** : seuls ton code + les dotfiles.

## Utilisation
À l'ouverture d'un agent, le message d'accueil liste les commandes. Démarre par **`/mri-brainstorm`**,
reprends via **`/mri-resume`**. Le flux complet et les commandes facultatives sont décrits dans
`payload/AGENTS.md` (copié en `AGENTS.md` dans la cible) et `dev/MERGE_DESIGN.md`.

## Développer le module
Sources dans `payload/` ; méta-docs dans `dev/` (`MERGE_DESIGN.md`, `DECISIONS.md`, `BUILD_PLAN.md`).
Dogfood : `./install.sh .` (self-install dans ce repo ; artefacts gitignorés). Le submodule
`dev/superpowers` est la **source d'extraction** (non distribuée).

## Crédits & licence
`LICENSE` (MIT). Dérivé de **Superpowers** (Jesse Vincent, MIT) et **BMAD-METHOD** (BMad Code LLC, MIT ;
« BMad™ » marque déposée — d'où le préfixe neutre `mri-`).
