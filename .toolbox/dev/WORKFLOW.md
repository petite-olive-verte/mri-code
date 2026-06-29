# Workflow — utiliser la toolbox (mode piloté par commandes)

> **Statut : implémenté.** Le mode command-driven (commandes wrapper + message d'accueil) et le
> rangement `.toolbox/` sont en place (améliorations 1 & 2 livrées). Ce document décrit l'expérience
> réelle ; reste à valider en live interactif (commandes / MCP).

## Principe

L'outil est **piloté par slash commands**, pas en pilote automatique. Un **seul automatisme** : un
message d'accueil au lancement de Claude Code, qui présente les commandes et suggère par quoi démarrer.
Ensuite, **à la fin de chaque étape, l'agent suggère la commande suivante** — tu gardes la main.

Le moteur méthodologique est **Superpowers** (skills invoquées explicitement par les commandes). Le
mode command-driven est établi dans `AGENTS.md`, qui **prime sur l'auto-déclenchement** de Superpowers
(sa propre règle : les instructions utilisateur passent avant les skills).

## Les commandes

| Commande | Invoque | Suggère ensuite |
|---|---|---|
| `/brainstorm` | skill `brainstorming` (notre facilitation, style BMAD) | `/devplan` |
| `/devplan` | `superpowers:writing-plans` | `/scaffold` (nouveau projet) sinon `/implement` |
| `/scaffold` | `scaffold-python` (notre skill) | `/implement` |
| `/implement` | `superpowers:subagent-driven-development` (TDD inclus) | `/review` |
| `/review` | `superpowers:requesting-code-review` | `/finish` |
| `/finish` | `superpowers:finishing-a-development-branch` | — |
| `/debug` | `superpowers:systematic-debugging` | (ad hoc) |
| `/meta-prompt` | skill `meta-prompt` (optimiser un prompt ponctuel) | — |

## Démarrer un projet (exemple : app de todo)

### 0. Création (une fois)
```bash
# GitHub : "Use this template" → ton repo, puis :
git clone <ton-repo> && cd <ton-repo>
.toolbox/scripts/setup.sh     # init du submodule Superpowers
claude                        # ouvre l'agent
```

### 1. Lancement → message d'accueil (le seul automatisme)
```
👋 Toolbox prête. Mode piloté par commandes.
Commandes : /brainstorm · /devplan · /scaffold · /implement · /review · /finish · /debug · /meta-prompt
Aucun travail en cours → démarrer une idée :  /brainstorm
```
L'agent attend ta commande ; il ne lance rien d'autre seul.

### 2. `/brainstorm <ton idée>`
Questions socratiques (stockage, commandes, format…), hypothèses et **critères d'acceptation**.
Écrit `docs/specs/<projet>/spec.md`. → suggère `/devplan`.

### 3. `/devplan`
Plan technique + **tâches ordonnées avec cases à cocher** (`docs/specs/<projet>/plan.md`, `tasks.md`).
Validation **en plan mode** (ton point de contrôle). → suggère `/scaffold`.

### 4. `/scaffold`
`scaffold-python` lit `.toolbox/constitution.md`, applique `.toolbox/templates/python-uv/`, substitue
les jetons, puis vérifie `uv sync` + `pytest` + `ruff` (verts). → suggère `/implement`.

### 5. `/implement`
Déroule les tâches **en TDD** (test rouge → code → vert → refactor), une par une :
- hook `format.sh` : auto-format à chaque écriture ;
- hook `lint-test.sh` : résumé `ruff/pytest` à chaque arrêt (boucle de feedback) ;
- coche `- [x]` dans `tasks.md` au fur et à mesure (= mémoire de reprise) ;
- sous-agents pour les tâches indépendantes (contexte isolé).
→ suggère `/review`.

### 6. `/review` → `/finish`
Review du diff vs spec/plan, corrections (`/debug` si besoin), puis merge / PR / cleanup.

## Reprendre après une pause

À la réouverture, le message d'accueil détecte un **plan avec des cases non cochées** et propose :
```
👋 Travail en cours : <projet> (3/5 tâches). Reprendre →  /implement
```
`/implement` relit `tasks.md` et **continue où ça s'était arrêté**. Règle unique, basée sur l'artefact
de plan explicite (pas de détection heuristique de fichiers).

## Variante web — le feedback visuel

Si l'app a une UI, pendant `/implement` l'agent utilise les **MCP** : **Playwright** pour piloter la
page (arbre d'accessibilité) et **Chrome DevTools** pour la console/le réseau. Boucle
écrire → exécuter → **observer** → corriger, sans screenshot manuel. (Nécessite d'approuver les MCP au
démarrage de session.)

## Ce que tu vois à la racine

```
mon-projet/
  README.md  AGENTS.md  CLAUDE.md
  src/  tests/  pyproject.toml        ← TON projet
  docs/specs/<projet>/                ← spec / plan / tasks (mémoire)
  .toolbox/  .claude/  .mcp.json      ← toolchain (rangée / cachée)
```
Seul ton projet est visible ; la tuyauterie est dans `.toolbox/` et les dotfiles.
