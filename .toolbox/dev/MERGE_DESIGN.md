# Conception — Fusion BMAD × Superpowers (module « mri »)

> Livrable de l'étape 2 du plan. **Certaines décisions sont OUVERTES (à valider au checkpoint)** —
> marquées ⏳. Ne pas les traiter comme figées tant que non validées.
> Source d'exploration : clone BMAD v6 dans `/tmp/bmad-probe` + submodule Superpowers local.

## 1. Constat corrigé sur BMAD v6 (vs recherche web initiale)

- Les skills d'analyse sont **légers** : `SKILL.md` + `assets/` (templates, CSV) + `references/` + parfois
  un script. Ex. `bmad-product-brief` = `SKILL.md` + `assets/brief-template.md` + `customize.toml`.
- **Runtime partagé, fin et détachable** : `_bmad/scripts/{resolve_customization,resolve_config,memlog}.py`.
  Chemins **pilotés par config** (`{output_folder}`, `{planning_artifacts}`, `{project_name}`) via
  `config.yaml` + `customize.toml` — **pas de chemins en dur**.
- **Le contenu est portable** (MIT) : `brain-methods.csv` (108 techniques : category, technique_name,
  description, detail, provenance, good_for, audience), les 3 cadres de mode
  (`references/mode-{facilitator,partner,autonomous}.md`), `converge.md`/`finalize.md`, et les templates.
- **Rôles** : le brainstorm BMAD produit un **journal** (`.memlog.md`), PAS un brief. Le **brief** est un
  skill distinct (`bmad-product-brief` → `brief.md`). `bmad-forge-idea` produit `forged-idea.md`
  (pressure-test), qui « peut nourrir bmad-spec/prd/prfaq ».

**Stratégie** : **lever le contenu, jeter la plomberie**, recâbler les chemins sur `docs/specs/<projet>/`.
Zéro dépendance `uv`/`_bmad`/`memlog`.

## 2. Sélection des skills

Légende : **Reimpl.** = réécrire un `SKILL.md` léger en levant le contenu BMAD ; **Extract** = copier le
`SKILL.md` Superpowers et l'adapter (chemins/namespace/ledger).

### Front — analyse (BMAD, Reimpl.)
| Skill mri | Source BMAD | Contenu levé | Sortie |
|---|---|---|---|
| `mri-brainstorm` | `core-skills/bmad-brainstorming` | `brain-methods.csv` (108 tech.) + 3 cadres de mode + converge/finalize ; base = notre `brainstorm-facilitation` | `docs/specs/<projet>/brief.md` (ou `intent.md`) |
| `mri-forge` ⏳ | `core-skills/bmad-forge-idea` | interrogatoire par personas (pressure-test), verdict HARDENED/KILLED/CLARIFIED | notes de challenge repliées dans `brief.md` |
| `mri-prfaq` ⏳ (optionnel) | `1-analysis/bmad-prfaq` | press-release + FAQ Working-Backwards | section de challenge (optionnelle) |
| recherche ⏳ (optionnel, différé) | `1-analysis/research/*` | market/domain/technical | notes de recherche |

### Pont — design technique (Superpowers, Extract+adapt)
| Skill mri | Source | Adaptation |
|---|---|---|
| `mri-design` | `superpowers/skills/brainstorming` | **entrée = `brief.md`** (le prend comme acquis, ne re-explore pas le produit) ; **sortie = `docs/specs/<projet>/spec.md`** (design : archi/composants/flux/erreurs/tests) |

### Back — exécution (Superpowers, Extract+adapt)
| Skill mri | Source | Adaptation |
|---|---|---|
| `mri-devplan` | `writing-plans` | entrée `spec.md` → sortie `plan.md` + `tasks.md` (cases) |
| `mri-implement` | `subagent-driven-development` | ledger → `tasks.md` ; TDD ; boucle MCP |
| (sous-skill) | `test-driven-development` | inchangé (fondation) |
| `mri-review` | `requesting-code-review` | règle la collision `/review` native |
| `mri-debug` | `systematic-debugging` | — |
| `mri-finish` | `finishing-a-development-branch` | — |

### Conservés (déjà maison)
`mri-scaffold-python`, `mri-meta-prompt`, `mri-brainstorming-light` (⏳ délègue à `superpowers:brainstorming`
OU version allégée de `mri-brainstorm` — à trancher).

## 3. Contrat de handoff (le cœur anti-friction)

```
mri-brainstorm  →  docs/specs/<projet>/brief.md   (vision, utilisateurs, périmètre, contraintes, idées retenues)
mri-design      →  docs/specs/<projet>/spec.md    (design technique : archi, composants, flux, erreurs, tests)
mri-devplan     →  docs/specs/<projet>/plan.md + tasks.md  (tâches ordonnées, cases, code complet)
mri-implement   →  commits + tasks.md coché  (ledger de reprise UNIQUE = tasks.md)
```

- **Une seule convention de dossier** : `docs/specs/<projet>/`. On réécrit les chemins en dur de
  Superpowers (`docs/superpowers/specs|plans/`) et on ignore les variables de config BMAD.
- **Ledger unique** : `tasks.md` (cases) — on abandonne `.superpowers/sdd/progress.md` et `.memlog.md`.

## 4. Ce qu'on strippe de BMAD
- `resolve_customization.py`, `resolve_config.py`, `memlog.py`, `brain.py`, `customize.toml`,
  les variables `{output_folder}`/`{planning_artifacts}`, tout `_bmad/`.
- Le catalogue `brain-methods.csv` est **conservé comme donnée** (l'agent le lit directement ; pas de script).

## 5. Décisions ouvertes (checkpoint) ⏳
1. **Périmètre du front** : minimal (`mri-brainstorm` + brief) · **+ `mri-forge`** (challenge) · full (+prfaq +recherche) ?
2. **Enrichir `mri-brainstorm`** avec le vrai `brain-methods.csv` (108) + 3 cadres de mode, ou garder notre catalogue curé (28) ?
3. **`mri-brainstorming-light`** : déléguer à `superpowers:brainstorming` (réintroduit la collision) ou version allégée maison ?
4. Confirmer : **strip total du runtime BMAD** + recâblage `docs/specs/<projet>/` (pas de `uv`/`_bmad`).
