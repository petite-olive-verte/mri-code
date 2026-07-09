# Plan de tâches — Construction du module « mri-code » (fusion BMAD × Superpowers)

> **MàJ v0.1.0 (finalisation distribution)** : payload **entièrement en anglais** ; langue de
> l'agent **configurable** à l'install (`--lang`/`--doc-lang`/`--user` → `config.json` + placeholders) ;
> installeur **copy-only** (plus de symlink) ; **submodule Superpowers retiré** ; companion visuel de
> mri-code-design **supprimé** (doublon MCP + branding tiers) ; repo/paquet renommés **`mri-code`**.


> **MàJ layout (v0.1.0)** : après les Lots 0-8, le repo est passé **source-first** — contenu dans
> `payload/`, méta-docs dans `dev/`, installeur `bin/install.mjs`/`install.sh` + `package.json`
> (`npx git+ssh://…` en privé). Les chemins `.claude/`/`.toolbox/` ci-dessous décrivent la **cible
> installée**, pas le repo source. Voir README + `dev/MERGE_DESIGN.md`.

> **MàJ 2026-07-09** : l'installeur est réécrit en **Python** (`mri_code_installer/`) sur un moteur
> générique vendoré depuis **`mri-installer-kit`** (repo séparé) — `bin/*.mjs`+`package.json` (Node)
> supprimés ; distribution à distance `npx git+ssh://…` → `uvx --from git+ssh://… mri-code`. Voir
> Décision 16.


> Copie versionnée du plan d'exécution (source : plan approuvé en session). Les cases sont le **ledger
> de reprise** : mises à jour après chaque lot. Conception détaillée dans `MERGE_DESIGN.md`.

## Objectif
Pipeline `mri-code` cohérent — front d'analyse riche/challengeant (réimplémenté de BMAD, MIT) + boucle
d'exécution disciplinée (extraite/adaptée de Superpowers) + feedback MCP — préfixé `mri-`, artefacts
générés sous **`.mri_code/docs/<projet>/`**, reprise via `progress.md`, packagé dans
**`.mri_code/`** avec un installeur.

## Conventions actées
- Artefacts générés : **`.mri_code/docs/<projet>/`** (brief.md, spec.md, plan.md, tasks.md, progress.md, recherche/findings).
- Préfixe **`mri-`** sur skills ET commandes.
- Build/test des sources dans `.claude/` (repo de dev) ; assemblage `.mri_code/` au Lot 7.
- Strip total du runtime BMAD ; contenu portable levé comme données (attributions MIT conservées).

## Arborescence cible `.mri_code/` (produite par l'installeur)
```
mon-projet/
  src/ tests/ pyproject.toml
  AGENTS.md  CLAUDE.md  .mcp.json            ← wiring racine (généré)
  .claude/ commands/ (à plat) · skills/ · settings.json  ← wiring fin (généré : symlink→.mri_code, fallback copie)
  .mri_code/
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
- [x] MAJ `MERGE_DESIGN.md` : convention → `.mri_code/docs/<projet>/`.

## Lot 1 — Front d'analyse (réimpl. BMAD, léger)
- [x] `mri-code-brainstorm` (base `brainstorm-facilitation` + lever brain-methods.csv, mode-*.md, converge/finalize, brief-template) → `brief.md`.
- [x] `mri-code-forge` (d'après bmad-forge-idea, panel FIXE de 5 personas, verdict) → notes dans `brief.md`.

## Lot 2 — Pont + back (extract + adapt Superpowers)
- [x] `mri-code-design` (← brainstorming) : REFRAMÉ en pont, entrée `brief.md` → `spec.md`.
- [x] `mri-code-devplan` (← writing-plans) : `spec.md` → `plan.md` (cases embarquées, modèle Superpowers ; pas de `tasks.md` séparé).
- [x] `mri-code-tdd` (← test-driven-development).
- [x] `mri-code-implement` (← subagent-driven-development) : ledger d'exécution `.mri_code/state/sdd/`, boucle MCP.
- [x] `mri-code-review` (← requesting-code-review) ; `mri-code-debug` (← systematic-debugging) ; `mri-code-finish` (← finishing-a-development-branch).
- [x] `mri-code-verify` (← verification-before-completion, bonus : évite une réf pendante) ; `mri-code-worktrees` (← using-git-worktrees).

## Lot 3 — Challenge & on-demand
- [x] `mri-code-elicit` (← bmad-advanced-elicitation) ; `mri-code-adversarial-review` (← bmad-review-adversarial-general).
- [x] `mri-code-market-research` / `mri-code-domain-research` / `mri-code-technical-research`.
- [x] `mri-code-document-project` (brownfield, optionnel).

## Lot 4 — État de pipeline & reprise
- [x] Schéma `progress.md` (dans la commande `/mri-code-resume`).
- [x] Instruction MAJ `progress.md` gravée dans les SKILL.md de phase.
- [x] `/mri-code-resume`.
- [x] Simplifier `welcome.sh` (`.mri_code/docs/*/progress.md` → /mri-code-resume ; sinon /mri-code-brainstorm) — testé 2 cas.

## Lot 5 — Préfixe `mri-` + commandes + câblage
- [x] Renommer `scaffold-python`→`mri-code-scaffold-python`, `meta-prompt`→`mri-code-meta-prompt`.
- [x] Régénérer les 17 commandes `mri-code-*` (suggestion suivant + facultatifs + ligne modèle). Collision `/review` réglée (→ `/mri-code-review`).
- [x] MAJ `.agents/skills/*` (19 symlinks), `AGENTS.md`, `CLAUDE.md`, `README.md` ; plugin Superpowers **désactivé** dans `settings.json`.

## Lot 6 — Suggestions de modèle
- [x] `.toolbox/models.md` éditable + ligne « 💡 modèle » en fin de chaque commande (faite au Lot 5).

## Lot 7 — Packaging `.mri_code/` + installeur
- [x] Arbo `.mri_code/` **produite par l'installeur dans la cible** (décision de sûreté : le repo de dev n'est PAS restructuré ; l'installeur package ses sources).
- [x] `.toolbox/scripts/install.sh` : assemble `.mri_code/` + câble `.claude/` (commandes à plat) + racine ; réécrit `.toolbox/`→`.mri_code/` ; settings propre (sans plugin).
- [x] Testé dans `/tmp/target-proj` : symlinks résolvent, 0 résidu `.toolbox/`, `welcome.sh` OK. Défaut symlink, fallback `--copy` (découverte live Claude à confirmer en E2E).

## Lot 8 — Docs, mémoire & E2E
- [x] MAJ DECISIONS (11 fusion / 12 installeur, amende 9), PROJECT_STATE, WORKFLOW, README, mémoire.
- [ ] **E2E dans une copie (interactif = checkpoint humain)** — À FAIRE AVEC L'UTILISATEUR :
      les étapes de facilitation (brainstorm/forge/design) ne se valident qu'en session live.
      Vérif statique + installeur déjà OK ; reste le déroulé réel du pipeline.

## Limites connues
- Qualité interactive (brainstorm/forge/design) validée seulement en live.
- Extraction Superpowers : préserver la logique interne.
- Lot 7 le plus risqué : cible jetable, ne pas restructurer le repo de dev à l'aveugle.
