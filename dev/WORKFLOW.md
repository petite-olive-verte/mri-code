# Workflow — utiliser le module `mri` (piloté par commandes)

> Flux actuel du module `mri`. Sources canoniques : `MERGE_DESIGN.md` (graphe complet + facultatifs),
> `README.md`, `payload/AGENTS.md`. Ce doc est le résumé du déroulé.

## Principe

Piloté par **slash commands**, pas en pilote automatique. Les skills d'entrée portent
`disable-model-invocation: true` → **l'agent n'en déclenche aucune seul**. Un seul automatisme : le
**message d'accueil** (`welcome.sh`, SessionStart) qui suggère par quoi démarrer. À la fin de chaque
étape, l'agent **suggère la commande suivante + le modèle** conseillé — tu gardes la main.

Skills **auto-portantes** dans `.claude/skills/mri-*` (pas de plugin, pas de submodule). Le mode
command-driven est fixé dans `AGENTS.md`.

## Les commandes

| Commande | Invoque | Suggère ensuite |
|---|---|---|
| `/mri-brainstorm` | skill `mri-brainstorm` (facilitation) | `/mri-forge` ou `/mri-design` |
| `/mri-forge` | skill `mri-forge` (pressure-test, personas) | `/mri-design` (HARDENED) / `/mri-brainstorm` (KILLED) |
| `/mri-design` | skill `mri-design` (pont `brief.md`→`spec.md`, **plan mode**) | `/mri-devplan` |
| `/mri-devplan` | skill `mri-devplan` (`spec.md`→`plan.md`, **plan mode**) | `/mri-scaffold-python` ou `/mri-implement` |
| `/mri-scaffold-python` | skill `mri-scaffold-python` | `/mri-implement` |
| `/mri-implement` | skill `mri-implement` (TDD + sous-agents + MCP) | `/mri-review` |
| `/mri-review` | skill `mri-review` | `/mri-finish` |
| `/mri-finish` | skill `mri-finish` | — (fin) |
| facultatifs | `/mri-elicit` · `/mri-adversarial-review` · `/mri-*-research` · `/mri-document-project` · `/mri-debug` · `/mri-meta-prompt` · `/mri-resume` | (retour au flux) |

## Démarrer un projet (exemple : app de todo)

### 0. Installation (une fois)
```bash
# Installe le module dans un projet cible (copie, pas de symlink) :
npx git+ssh://git@github.com/MatioRIGARD/mri-devtools.git -- <cible> --lang French --user Ton-Nom
# ou, en local : node bin/install.mjs <cible> --lang French --user Ton-Nom
cd <cible> && claude          # ouvre l'agent DANS la cible
```

### 1. Lancement → message d'accueil (le seul automatisme)
Le hook `welcome.sh` affiche le logo + les commandes. Aucun travail en cours → il suggère
`/mri-brainstorm`. L'agent attend ta commande ; il ne lance rien d'autre seul.

### 2. `/mri-brainstorm <ton idée>` → (option `/mri-forge`)
Facilitation (une question à la fois, challenge). Écrit `.mri_devtools/docs/<projet>/brief.md`.
→ suggère `/mri-forge` (durcir) ou `/mri-design`.

### 3. `/mri-design`
Le **pont** analyse→exécution : lit `brief.md`, pose les questions **techniques**, propose 2-3
approches. **Entre en plan mode** ; à l'approbation (`ExitPlanMode`) écrit
`.mri_devtools/docs/<projet>/spec.md`. → suggère `/mri-devplan`.

### 4. `/mri-devplan`
**Entre en plan mode** ; produit un plan **contrat** (fichiers + interfaces/signatures + code de test +
intention — **pas** le code complet). À l'approbation, écrit `.mri_devtools/docs/<projet>/plan.md` (cases
à cocher). → suggère `/mri-scaffold-python` (nouveau projet) ou `/mri-implement`.

### 5. `/mri-scaffold-python`
Lit `.mri_devtools/constitution.md`, rend `.mri_devtools/templates/python-uv/` **en staging isolé**,
substitue les jetons, copie sans écraser, puis vérifie `uv sync` + `pytest` + `ruff` (verts).
→ suggère `/mri-implement`.

### 6. `/mri-implement`
Déroule le plan **en TDD** (rouge → code → vert → refactor), un **sous-agent par tâche** + review :
- hook `format.sh` : auto-format à chaque écriture ;
- hook `lint-test.sh` : résumé `ruff/pytest` à chaque arrêt (boucle de feedback) ;
- coche `- [x]` dans `plan.md` ; ledger d'exécution `.mri_devtools/state/sdd/task-ledger.md`.
→ suggère `/mri-review`.

### 7. `/mri-review` → `/mri-finish`
Review du diff vs spec/plan (corrections, `/mri-debug` si besoin), puis merge / PR / cleanup.

## Reprendre après une pause

À la réouverture, `welcome.sh` détecte un `.mri_devtools/docs/*/progress.md` avec des étapes non
terminées (`- [ ]` / `- [~]`) et suggère `/mri-resume`, qui **relit `progress.md`** (suivi de **phases**)
et ré-entre à l'étape courante. Deux niveaux d'état : `progress.md` = phases ; `task-ledger.md` = tâches
dans l'étape implement.

## Variante web — feedback visuel

Si l'app a une UI, pendant `/mri-implement`/`/mri-design` l'agent utilise les **MCP** : **Playwright**
(piloter la page) + **Chrome DevTools** (console/réseau). Boucle écrire → exécuter → **observer** →
corriger. (Approuver les MCP au démarrage de session.)

## Ce que tu vois à la racine de la cible

```
<cible>/
  README?  AGENTS.md  CLAUDE.md  .mcp.json     ← bootstrap agent
  src/  tests/  pyproject.toml                 ← TON projet (après scaffold)
  .mri_devtools/docs/<projet>/                 ← brief / spec / plan / progress (mémoire)
  .mri_devtools/  .claude/  .agents/           ← toolchain (config, skills, hooks — cachée)
```
Seul ton projet est visible ; la tuyauterie est dans `.mri_devtools/` et les dotfiles.
