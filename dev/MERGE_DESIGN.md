# Conception — Fusion BMAD × Superpowers (module « mri »)

> **Statut : design FIGÉ, prêt à implémenter (étape 3+).** Consolide toutes les décisions prises en
> conversation. Source d'exploration : clone BMAD v6 (`/tmp/bmad-probe`) + submodule Superpowers local.

## 1. Constat BMAD v6 (corrigé vs recherche web)

- Skills d'analyse **légers** : `SKILL.md` + `assets/` (templates, CSV) + `references/` (+ parfois script).
- **Runtime partagé fin et détachable** : `_bmad/scripts/{resolve_customization,resolve_config,memlog}.py`,
  chemins **pilotés par config** (`{output_folder}`, `{planning_artifacts}`) — pas de chemins en dur.
- **Contenu portable (MIT)** : `brain-methods.csv` (108 techniques), cadres de mode
  (`references/mode-{facilitator,partner,autonomous}.md`), `converge.md`/`finalize.md`, templates.
- Rôles : brainstorm BMAD sort un **journal** (`.memlog.md`), pas un brief ; le **brief** est un skill
  séparé (`bmad-product-brief`) ; `bmad-forge-idea` sort `forged-idea.md`.

**Stratégie : lever le contenu, jeter la plomberie.** Recâbler sur `.mri_devtools/docs/<projet>/`, zéro
dépendance `uv`/`_bmad`/`memlog`.

## 2. Sélection finale des skills (préfixe `mri-` sur skills ET commandes)

Légende : **Reimpl.** = réécrire un `SKILL.md` léger en levant le contenu BMAD ; **Extract** = copier
le `SKILL.md` Superpowers et l'adapter (chemins/namespace/ledger).

### Cœur du flux
| Skill mri | Origine | Type | Sortie |
|---|---|---|---|
| `mri-brainstorm` | BMAD brainstorming (base = notre `brainstorm-facilitation`, enrichie) | Reimpl. | `.mri_devtools/docs/<projet>/brief.md` |
| `mri-design` | Superpowers `brainstorming` (le **pont**) | Extract+adapt | `.mri_devtools/docs/<projet>/spec.md` (design technique) |
| `mri-devplan` | Superpowers `writing-plans` | Extract+adapt | `plan.md` (cases à cocher intégrées) |
| `mri-scaffold-python` | maison (existant) | — | structure projet |
| `mri-implement` | Superpowers `subagent-driven-development` (+ TDD sous-skill) | Extract+adapt | commits, cases de `plan.md` cochées |
| `mri-review` | Superpowers `requesting-code-review` | Extract+adapt | revue (règle collision `/review`) |
| `mri-finish` | Superpowers `finishing-a-development-branch` | Extract+adapt | merge/PR/cleanup |

### Challenge (facultatifs, suggérés dans la loop)
| Skill mri | Origine | Rôle |
|---|---|---|
| `mri-forge` | BMAD `bmad-forge-idea` | pressure-test d'**une idée** (panel de 5 personas) → HARDENED/CLARIFIED/KILLED |
| `mri-elicit` | BMAD `bmad-advanced-elicitation` | approfondir/critiquer **la dernière sortie** (socratique, pre-mortem, red-team) |
| `mri-adversarial-review` | BMAD `bmad-review-adversarial-general` | **audit cynique d'un document** (brief/spec/plan) → rapport de findings |

### On-demand (hors flux, suggérés au bon moment)
| Skill mri | Origine | Note |
|---|---|---|
| `mri-market-research` | BMAD | web-heavy (WebSearch/MCP) ; suggéré **après forge** |
| `mri-domain-research` | BMAD | idem |
| `mri-technical-research` | BMAD | idem |
| `mri-document-project` | BMAD `bmad-document-project` | **brownfield** (repo existant) → contexte ; optionnel |
| `mri-meta-prompt` | maison (existant) | autonome |
| `mri-debug` | Superpowers `systematic-debugging` | boucle d'implémentation |

### Abandonnés
`brainstorming-light` (forge rend brainstorm déjà léger) · `correct-course` (couplé au modèle
epics/stories non adopté) · `investigate` (n'existe pas en v6 ; couvert par `mri-debug`) ·
`generate-project-context` (chevauche `constitution.md`).

## 3. Graphe de suggestions (flux + facultatifs avec entrées/sorties)

Légende : `─▶` défaut · `⟶(fac.)` appel facultatif · `↩` retour au flux · `⟲` boucle sur place · `⤴` recommence

```
 démarrage ─▶ welcome
                ├─ progress.md existe ? ─▶ /mri-resume ─▶ (re-entre à l'étape ~ ou suivante)
                └─ sinon
                      └─ repo existant ? ⟶(fac.) /mri-document-project ↩▶ /mri-brainstorm
                                 ▼
                        /mri-brainstorm → brief.md
                                 │   ⟲(fac.) /mri-elicit ↩
                                 │   ⟲(fac.) /mri-adversarial-review (brief) ↩ (révise ou continue)
                                 ├──────────────────────────▶ (saut de forge) /mri-design
                                 ▼ ─▶ suggère par défaut
                        /mri-forge  (durcir l'idée)
                                 │   ⤴ si KILLED ─────────────▶ /mri-brainstorm
                                 │ si HARDENED / CLARIFIED :
                                 │     ⟶(fac.) /mri-market-research    ┐
                                 │     ⟶(fac.) /mri-domain-research    ├─ ↩▶ /mri-design
                                 │     ⟶(fac.) /mri-technical-research ┘
                                 ▼
                        /mri-design  brief.md → spec.md
                                 │   ⟲(fac.) /mri-adversarial-review (spec) ↩
                                 │   ⟲(fac.) /mri-elicit ↩
                                 ▼
                        /mri-devplan  spec.md → plan.md + tasks.md
                                 │   ⟲(fac.) /mri-adversarial-review (plan) ↩
                                 ▼
                        /mri-scaffold-python   (nouveau projet)
                                 ▼
                        /mri-implement  (TDD + MCP)
                                 │   ⟲ /mri-debug (sur échec) ↩
                                 │   ⟲(fac.) /mri-elicit ↩
                                 ▼
                        /mri-review ─▶ /mri-finish

 Hors flux : /mri-meta-prompt
```

Règles clés : recherches **uniquement après forge-succès** (jamais sur idée rejetée) ;
`brainstorm ──▶ design` **saute forge** si l'idée est déjà solide ; chaque facultatif **revient** au flux.

## 4. Contrat de handoff + conventions

```
mri-brainstorm → .mri_devtools/docs/<projet>/brief.md   (vision, utilisateurs, périmètre, contraintes, idées)
mri-design     → .mri_devtools/docs/<projet>/spec.md    (design technique : archi, composants, flux, erreurs, tests)
mri-devplan    → .mri_devtools/docs/<projet>/plan.md   (cases à cocher intégrées)
mri-implement  → commits + cases de plan.md cochées
```
- **Une convention de dossier** : `.mri_devtools/docs/<projet>/` (on réécrit les chemins Superpowers en dur).
- **Ledgers, 2 niveaux complémentaires** : `progress.md` = phases (dans `docs/<projet>/`) ;
  `state/sdd/task-ledger.md` = tâches fines *dans* implement.

## 5. État de pipeline `progress.md` + `/mri-resume`

- **`.mri_devtools/docs/<projet>/progress.md`** : miroir du graphe avec statut par étape (`[x]` fait, `[~]` en
  cours, `[ ]` à faire) + section « appels facultatifs » (audit) + « prochaine étape ».
- **Chaque skill met à jour `progress.md`** : au début (`~`), à la fin (`x` + pointe la suivante).
  Instruction gravée dans chaque `SKILL.md`.
- **`/mri-resume`** : lit `progress.md`, rapporte l'état, **re-entre à l'étape `~` ou à la prochaine
  `[ ]`** (recharge les artefacts). Si phase = implement → délègue à `tasks.md`. Pas de `progress.md`
  → suggère `/mri-brainstorm`.
- **`welcome.sh` simplifié** : `progress.md` présent → « Reprends → /mri-resume » ; sinon → `/mri-brainstorm`
  (fin de l'ancien grep heuristique + de l'embranchement direct vers implement).

Schéma type :
```markdown
# Parcours — <projet>   (MAJ: <date> · dernière étape: /mri-design)
## Étapes
- [x] brainstorm → brief.md
- [x] forge → HARDENED
- [~] design → spec.md (en cours)
- [ ] devplan / scaffold / implement / review / finish
## Appels facultatifs
- market-research (après forge) → market-notes.md
## Prochaine étape
/mri-design (finir spec.md) → puis /mri-devplan
```

## 6. Personas de `mri-forge` (panel FIXE, une persona par angle)

Pas de découverte dynamique (le gadget `resolve_personas.py` est jeté). Panel hardcodé :

| Persona | Angle attaqué |
|---|---|
| Investisseur sceptique / pragmatique | valeur, « qui paie ? », « pourquoi ça échoue ? » |
| Utilisateur novice | confusion, hypothèses implicites, friction UX |
| Attaquant / red-team | abus, sécurité, cas limites malveillants |
| Mainteneur surchargé | coût de complexité, dette technique, faisabilité |
| Expert du domaine | « ce n'est pas comme ça que marche ce domaine » |

## 7. Strip du runtime BMAD
Jeter : `resolve_customization.py`, `resolve_config.py`, `memlog.py`, `brain.py`, `customize.toml`,
variables `{output_folder}`/`{planning_artifacts}`, tout `_bmad/`, les keepsakes HTML.
Garder comme **données** : `brain-methods.csv` (lu à la demande, jamais déballé en entier), cadres de mode.

## 8. Installation (étape 7 — cible, pas ce repo de dev)

- **Dossier caché `.mri_devtools/`** = LE MODULE (sources des skills, templates, `constitution.md`,
  `brain-methods.csv`, cadres de mode, docs). Source de vérité.
- **Couche fine imposée par Claude Code** (non cachable) : `.claude/commands/mri-*.md` (à plat),
  `.claude/skills/mri-*/`, hooks dans `.claude/settings.json`, `AGENTS.md`/`CLAUDE.md`/`.mcp.json` à la racine.
  → l'installeur génère ces pointeurs (symlink/copie) vers `.mri_devtools/`.
- **Modèle** : module vendorisé + câblage généré par un **installeur** (`.mri_devtools/scripts/install.sh`
  ou `npx`). Pas de marketplace/plugin (quirks évités).
- **Dev vs cible** : on construit/teste **maintenant dans `.claude/`** ; le packaging `.mri_devtools/`
  + installeur = étape 7.

## 9. Attribution
Superpowers (obra, MIT) — moteur d'exécution. BMAD-METHOD (BMad Code LLC, MIT ; « BMad™ » marque) —
front d'analyse. Conserver les notices ; ne pas utiliser la marque « BMad » dans les noms exposés (d'où `mri-`).
