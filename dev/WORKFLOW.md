# Workflow — utiliser le module `mri-code` (piloté par commandes)

> Flux actuel du module `mri-code`. Sources canoniques : `MERGE_DESIGN.md` (graphe complet + facultatifs),
> `README.md`, `payload/AGENTS.md`. Ce doc est le résumé du déroulé.

## Principe

Piloté par **slash commands**, pas en pilote automatique. Les skills d'entrée portent
`disable-model-invocation: true` → **l'agent n'en déclenche aucune seul**. Un seul automatisme : le
**message d'accueil** (`welcome.sh`, SessionStart) qui suggère par quoi démarrer. À la fin de chaque
étape, l'agent **suggère la commande suivante + le modèle** conseillé — tu gardes la main.

Skills **auto-portantes** dans `.claude/skills/mri-code-*` (pas de plugin, pas de submodule). Le mode
command-driven est fixé dans `AGENTS.md`.

## Les commandes

| Commande | Invoque | Suggère ensuite |
|---|---|---|
| `/mri-code-brainstorm` | skill `mri-code-brainstorm` (facilitation) | `/mri-code-forge` ou `/mri-code-design` |
| `/mri-code-forge` | skill `mri-code-forge` (pressure-test, personas) | `/mri-code-design` (HARDENED) / `/mri-code-brainstorm` (KILLED) |
| `/mri-code-design` | skill `mri-code-design` (pont `brief.md`→`spec.md`, **plan mode**) | `/mri-code-devplan` |
| `/mri-code-devplan` | skill `mri-code-devplan` (`spec.md`→`plan.md`, **plan mode**) | `/mri-code-scaffold-python` ou `/mri-code-implement` |
| `/mri-code-scaffold-python` | skill `mri-code-scaffold-python` | `/mri-code-implement` |
| `/mri-code-implement` | skill `mri-code-implement` (TDD + sous-agents + MCP) | `/mri-code-review` |
| `/mri-code-review` | skill `mri-code-review` | `/mri-code-finish` |
| `/mri-code-finish` | skill `mri-code-finish` | — (fin) |
| facultatifs | `/mri-code-elicit` · `/mri-code-adversarial-review` · `/mri-code-*-research` · `/mri-code-document-project` · `/mri-code-debug` · `/mri-code-meta-prompt` · `/mri-code-resume` | (retour au flux) |

## Démarrer un projet (exemple : app de todo)

### 0. Installation (une fois)
```bash
# Installe le module dans un projet cible (copie, pas de symlink) :
uvx --from git+ssh://git@github.com/MatioRIGARD/mri-code.git mri-code <cible> --lang French --user Ton-Nom
# ou, en local : ./install.sh <cible> --lang French --user Ton-Nom
cd <cible> && claude          # ouvre l'agent DANS la cible
```

### 1. Lancement → message d'accueil (le seul automatisme)
Le hook `welcome.sh` affiche le logo + les commandes. Aucun travail en cours → il suggère
`/mri-code-brainstorm`. L'agent attend ta commande ; il ne lance rien d'autre seul.

### 2. `/mri-code-brainstorm <ton idée>` → (option `/mri-code-forge`)
Facilitation (une question à la fois, challenge). Écrit `.mri_code/docs/<projet>/brief.md`.
→ suggère `/mri-code-forge` (durcir) ou `/mri-code-design`.

### 3. `/mri-code-design`
Le **pont** analyse→exécution : lit `brief.md`, pose les questions **techniques**, propose 2-3
approches. **Entre en plan mode** ; à l'approbation (`ExitPlanMode`) écrit
`.mri_code/docs/<projet>/spec.md`. → suggère `/mri-code-devplan`.

### 4. `/mri-code-devplan`
**Entre en plan mode** ; produit un plan **contrat** (fichiers + interfaces/signatures + code de test +
intention — **pas** le code complet). À l'approbation, écrit `.mri_code/docs/<projet>/plan.md` (cases
à cocher). → suggère `/mri-code-scaffold-python` (nouveau projet) ou `/mri-code-implement`.

### 5. `/mri-code-scaffold-python`
Lit `.mri_code/constitution.md`, rend `.mri_code/templates/python-uv/` **en staging isolé**,
substitue les jetons, copie sans écraser, puis vérifie `uv sync` + `pytest` + `ruff` (verts).
→ suggère `/mri-code-implement`.

### 6. `/mri-code-implement`
Déroule le plan **en TDD** (rouge → code → vert → refactor), un **sous-agent par tâche** + review :
- hook `format.sh` : auto-format à chaque écriture ;
- hook `lint-test.sh` : résumé `ruff/pytest` à chaque arrêt (boucle de feedback) ;
- coche `- [x]` dans `plan.md` ; ledger d'exécution `.mri_code/state/sdd/task-ledger.md`.
→ suggère `/mri-code-review`.

### 7. `/mri-code-review` → `/mri-code-finish`
Review du diff vs spec/plan (corrections, `/mri-code-debug` si besoin), puis merge / PR / cleanup.

## Reprendre après une pause

À la réouverture, `welcome.sh` détecte un `.mri_code/docs/*/progress.md` avec des étapes non
terminées (`- [ ]` / `- [~]`) et suggère `/mri-code-resume`, qui **relit `progress.md`** (suivi de **phases**)
et ré-entre à l'étape courante. Deux niveaux d'état : `progress.md` = phases ; `task-ledger.md` = tâches
dans l'étape implement.

## Variante web — feedback visuel

Si l'app a une UI, pendant `/mri-code-implement`/`/mri-code-design` l'agent utilise les **MCP** : **Playwright**
(piloter la page) + **Chrome DevTools** (console/réseau). Boucle écrire → exécuter → **observer** →
corriger. (Approuver les MCP au démarrage de session.)

## Ce que tu vois à la racine de la cible

```
<cible>/
  README?  AGENTS.md  CLAUDE.md  .mcp.json     ← bootstrap agent
  src/  tests/  pyproject.toml                 ← TON projet (après scaffold)
  .mri_code/docs/<projet>/                 ← brief / spec / plan / progress (mémoire)
  .mri_code/  .claude/  .agents/           ← toolchain (config, skills, hooks — cachée)
```
Seul ton projet est visible ; la tuyauterie est dans `.mri_code/` et les dotfiles.
