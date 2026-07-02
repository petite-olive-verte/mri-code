# Plan de tâches — Construction du module « mri » (fusion BMAD × Superpowers)

> Copie versionnée du plan d'exécution (source : plan approuvé en session). Les cases sont le **ledger
> de reprise** : mises à jour après chaque lot. Conception détaillée dans `MERGE_DESIGN.md`.

## Objectif
Pipeline `mri` cohérent — front d'analyse riche/challengeant (réimplémenté de BMAD, MIT) + boucle
d'exécution disciplinée (extraite/adaptée de Superpowers) + feedback MCP — préfixé `mri-`, artefacts
générés sous **`.mri_devtools/docs/<projet>/`**, reprise via `progress.md`, packagé dans
**`.mri_devtools/`** avec un installeur.

## Conventions actées
- Artefacts générés : **`.mri_devtools/docs/<projet>/`** (brief.md, spec.md, plan.md, tasks.md, progress.md, recherche/findings).
- Préfixe **`mri-`** sur skills ET commandes.
- Build/test des sources dans `.claude/` (repo de dev) ; assemblage `.mri_devtools/` au Lot 7.
- Strip total du runtime BMAD ; contenu portable levé comme données (attributions MIT conservées).

## Arborescence cible `.mri_devtools/` (produite par l'installeur)
```
mon-projet/
  src/ tests/ pyproject.toml
  AGENTS.md  CLAUDE.md  .mcp.json            ← wiring racine (généré)
  .claude/ commands/ (à plat) · skills/ · settings.json  ← wiring fin (généré : symlink→.mri_devtools, fallback copie)
  .mri_devtools/
    VERSION  README.md  constitution.md  models.md
    skills/  commands/  hooks/  templates/python-uv/  mcp/servers.json
    scripts/install.sh
    dev/    ← méta-docs (DECISIONS, MERGE_DESIGN, BUILD_PLAN, SEARCH_RESULTS)
    docs/   ← GÉNÉRÉ : docs/<projet>/{brief,spec,plan,tasks,progress}.md
```
Le submodule `superpowers` reste source d'extraction (dev-only), non embarqué.

## Règles d'exécution autonome
- Commit local par lot (pas de push). Vérifier avant de cocher. MAJ des cases après chaque lot.
- Ne pas casser le `.claude/` fonctionnel du repo de dev pendant le build.

---

## Lot 0 — Prépa, plan & conventions
- [x] Committer ce plan en `.toolbox/dev/BUILD_PLAN.md`.
- [x] Re-cloner BMAD si absent (`/tmp/bmad-probe`).
- [x] MAJ `MERGE_DESIGN.md` : convention → `.mri_devtools/docs/<projet>/`.

## Lot 1 — Front d'analyse (réimpl. BMAD, léger)
- [x] `mri-brainstorm` (base `brainstorm-facilitation` + lever brain-methods.csv, mode-*.md, converge/finalize, brief-template) → `brief.md`.
- [x] `mri-forge` (d'après bmad-forge-idea, panel FIXE de 5 personas, verdict) → notes dans `brief.md`.

## Lot 2 — Pont + back (extract + adapt Superpowers)
- [x] `mri-design` (← brainstorming) : REFRAMÉ en pont, entrée `brief.md` → `spec.md`.
- [x] `mri-devplan` (← writing-plans) : `spec.md` → `plan.md` (cases embarquées, modèle Superpowers ; pas de `tasks.md` séparé).
- [x] `mri-tdd` (← test-driven-development).
- [x] `mri-implement` (← subagent-driven-development) : ledger d'exécution `.mri_devtools/state/sdd/`, boucle MCP.
- [x] `mri-review` (← requesting-code-review) ; `mri-debug` (← systematic-debugging) ; `mri-finish` (← finishing-a-development-branch).
- [x] `mri-verify` (← verification-before-completion, bonus : évite une réf pendante) ; `mri-worktrees` (← using-git-worktrees).

## Lot 3 — Challenge & on-demand
- [x] `mri-elicit` (← bmad-advanced-elicitation) ; `mri-adversarial-review` (← bmad-review-adversarial-general).
- [x] `mri-market-research` / `mri-domain-research` / `mri-technical-research`.
- [x] `mri-document-project` (brownfield, optionnel).

## Lot 4 — État de pipeline & reprise
- [x] Schéma `progress.md` (dans la commande `/mri-resume`).
- [x] Instruction MAJ `progress.md` gravée dans les SKILL.md de phase.
- [x] `/mri-resume`.
- [x] Simplifier `welcome.sh` (`.mri_devtools/docs/*/progress.md` → /mri-resume ; sinon /mri-brainstorm) — testé 2 cas.

## Lot 5 — Préfixe `mri-` + commandes + câblage
- [x] Renommer `scaffold-python`→`mri-scaffold-python`, `meta-prompt`→`mri-meta-prompt`.
- [x] Régénérer les 17 commandes `mri-*` (suggestion suivant + facultatifs + ligne modèle). Collision `/review` réglée (→ `/mri-review`).
- [x] MAJ `.agents/skills/*` (19 symlinks), `AGENTS.md`, `CLAUDE.md`, `README.md` ; plugin Superpowers **désactivé** dans `settings.json`.

## Lot 6 — Suggestions de modèle
- [ ] `models.md` éditable + ligne « 💡 modèle » en fin de commande.

## Lot 7 — Packaging `.mri_devtools/` + installeur
- [ ] Créer l'arbo `.mri_devtools/` + déplacer les sources ; `.claude/` = pointeurs.
- [ ] `install.sh` (câble `.claude/` + racine ; commandes à plat).
- [ ] Tester découverte des symlinks (fallback copie) + installeur dans `/tmp/target-proj`.

## Lot 8 — Docs, mémoire & E2E
- [ ] MAJ DECISIONS (amender 9 ; ajouter 11/12), PROJECT_STATE, WORKFLOW, README, mémoire.
- [ ] E2E dans une copie (interactif = checkpoint humain).

## Limites connues
- Qualité interactive (brainstorm/forge/design) validée seulement en live.
- Extraction Superpowers : préserver la logique interne.
- Lot 7 le plus risqué : cible jetable, ne pas restructurer le repo de dev à l'aveugle.
