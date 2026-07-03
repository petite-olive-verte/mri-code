# Décisions d'architecture — options envisagées & justification

> Ce document trace **les choix structurants** faits pendant le brainstorming, les options qui
> étaient sur la table, et **pourquoi** on a tranché ainsi. Il accompagne `SEARCH_RESULTS.md`
> (l'état de l'art) et `PLAN.md` (le plan de construction).

## Contrainte directrice de l'utilisateur

> « Je ne veux pas être dépendant d'un seul outil de code, mais intégrer la toolbox à un outil de
> code, c'est très puissant — donc pas envie d'un truc indépendant. »

Plus : praticité maximale (« j'ouvre un agent dans le dossier et l'interaction démarre »), **structure
de projet éditable**, orientation **one-shot** (idée précise → laisser coder avant contrôle humain),
et **ne pas réinventer** ce que des frameworks open-source font déjà bien.

Découverte clé qui résout la tension « pas verrouillé / mais intégré » : **le socle est déjà portable**
(AGENTS.md + SKILL.md + MCP sont des standards ouverts lus par Claude Code, Codex, Cursor, Gemini,
ZCode/Cline…). On peut être *intégré aux outils* sans être *verrouillé* à un seul.

---

## Décision 1 — Form factor : repo template GitHub « open-and-go »

**Options** : (A) repo template tout-en-un *(choisi)* ; (B) toolbox séparée qui génère un projet
enfant ; (C) plugin Claude Code only ; (D) CLI scaffolder indépendant.

**Choix : A.** `Use this template` → on ouvre un agent dans le dossier → **AGENTS.md** (lu au démarrage
par tout agent) déclenche le flux guidé ; le code de l'app se greffe dans le même repo.
**Pourquoi** : praticité max ; mécanisme « ouvrir = lancer » natif et portable via AGENTS.md (+ hook
SessionStart côté Claude) ; un seul dossier.
**Compromis** : un peu de fichiers méta dans le repo (rangés dans `docs/`) ; « open-and-go » ~95%
(AGENTS.md est du contexte, pas un script auto-déclenché).
**Plus tard** : la distribution par template est un *snapshot* ; pour propager les mises à jour,
on pourra passer à un plugin/pack installable sans changer l'UX.

---

## Décision 2 — Spine : Superpowers en submodule (et non un pipeline maison)

**Contexte** : le framework open-source **Superpowers** (obra) implémente déjà ~80-90% du pipeline
voulu (brainstorm socratique, extraction de spec validée par bouts, planning, subagent-driven
development avec review en 2 passes, **TDD red-green-refactor imposé**, debugging systématique, git
worktrees, skill authoring). Il est lui-même portable (Claude Code, Cursor, Codex, Gemini, Copilot…).

**Options envisagées**
1. **Dépendance plugin** (marketplace) — le plus léger, updates auto, mais étape d'install séparée et
   repo non self-contained.
2. **Submodule épinglé** *(choisi)* — Superpowers embarqué à une version figée dans le repo template ;
   self-contained, voie de mise à jour propre (bump du submodule), pas d'édition de ses internes.
3. **Cherry-pick des skills markdown** — copier seulement les skills voulues ; self-contained, contrôle
   max, mais updates manuelles et **risque de perdre l'expertise des auteurs** si on diverge trop.
4. **Hard fork** — contrôle total mais maintenance lourde et perte d'upstream.

**Choix : 2 (submodule épinglé) + activation sélective des skills.**
**Pourquoi** : (a) on **garde l'expertise des auteurs** intacte (on ne réécrit pas leurs skills —
on n'a pas la prétention de faire mieux) ; (b) self-contained → cohérent avec l'open-and-go ;
(c) mises à jour propres ; (d) les skills se déclenchant **à la demande**, on obtient la *sélectivité*
du cherry-pick (n'activer que ce qu'on câble dans AGENTS.md) **sans** copier ni perdre l'upstream.
**Orientation one-shot** : elle se fait dans **notre couche** (AGENTS.md d'orchestration + spec précise
+ `constitution.md`), pas en modifiant les skills de Superpowers — dont le modèle « interaction
front-loadée pour la précision, puis exécution autonome » colle déjà au one-shot.
**Escape hatch** : cherry-pick (option 3) seulement *si* une skill se bat vraiment contre le flux
one-shot. À vérifier au montage : **licence** de Superpowers (avant de vendorer) et **persistance
disque** de ses specs/plans.
**Spec Kit** n'est plus la base, mais reste une **référence d'idées à voler** : la *constitution*,
l'étape *clarify*, le dossier `specs/` comme mémoire externe.

---

## Décision 3 — Feedback visuel/runtime : Playwright MCP + Chrome DevTools MCP

**Options** : Playwright seul / Chrome DevTools seul / les deux / aucun.

**Choix : les deux.** **Playwright MCP** pour *piloter/tester* l'UI (arbre d'accessibilité,
cross-browser, fiable, économe) ; **Chrome DevTools MCP** pour *déboguer* (console/réseau/perf,
self-healing). **Pourquoi** : ils ferment la boucle écrire→exécuter→lire→corriger côté front, et
comblent la **faiblesse runtime assumée de Superpowers** (debugging d'environnement, erreurs runtime).
**Écarté** : Puppeteer MCP (screenshots only, Chromium only, supplanté).

---

## Décision 4 — Portabilité : Claude-first, cœur déjà portable

**Choix : Claude-first.** Le cœur (AGENTS.md + Skills + MCP) est **déjà portable** → Codex/ZCode
fonctionnent pour la partie portable. L'adaptateur complet (sous-agents, hooks, permissions, commandes)
est livré pour Claude Code en V1 (outil principal), structure prête pour des adaptateurs Codex/ZCode
plus tard. **Pourquoi** : simple, évolutif, conforme au « pas verrouillé ».

---

## Décision 5 — Tests : TDD imposé mécaniquement

**Choix : TDD red-green-refactor imposé** (fourni par la skill TDD de **Superpowers**) ; les **critères
d'acceptation de la spec deviennent les tests** ; les tests sont le **signal** de la boucle (hook
test-on-stop côté Claude). **Pourquoi** : les tests générés par l'IA *après* le code valident ce que
l'agent a écrit (score de mutation ~20%). En imposant le test *avant*, l'humain/la spec possède
l'**intention**, l'agent l'**implémentation** → il ne peut pas valider ses propres bugs.

---

## Décision 6 — Structure de projet : intégrée **et** éditable (+ rôle de `constitution.md`)

**Choix** : ne pas hardcoder une structure « universelle ». Deux leviers :
1. **`templates/python-uv/`** — le scaffold concret (fichiers), édité directement → *ta* structure.
2. **`constitution.md`** — le **règlement intérieur** du projet que l'agent lit et **respecte** :
   principes et standards non-négociables (stack, qualité, tests, architecture, conventions de nommage,
   emplacement des tests). La spec dit *quoi* construire ; la constitution dit *ce que « bien fait »
   veut dire ici*. Petite, durable, fort signal (bon citoyen du context management, pilier *Select*).

**Pourquoi** : l'utilisateur possède à la fois les fichiers (template) *et* les règles (constitution) —
l'inverse d'un générateur rigide. **Lien one-shot** : la constitution **front-load** tous les standards
→ en one-shot, l'agent dérive moins et s'arrête moins pour demander.

---

## Décision 7 — Context management : « le repo est le store lossless » (LCM abandonné)

**Options** : (a) Lossless Context Management (DAG/SQLite type hermes-lcm) ; (b) file-based / repo
comme store *(choisi)*.

**Choix : file-based.** Pour un **agent de code**, la source de vérité n'est pas la conversation mais
le **repo** (code, spec, plan, `tasks.md`, tests, git) — qui est déjà *path-addressable*,
*compaction-stable* et *lossless*. **Pourquoi pas LCM** : il se justifie pour un **assistant** où la
conversation EST l'état ; pour du code, c'est superflu — la nuance importante doit vivre sur disque,
pas dans le chat. Stratégie retenue : externaliser dans `docs/specs/` (spec/plan/tasks/journal) +
**sous-agents** (isolation) + **relecture à la demande** + `tasks.md` comme mémoire de travail
(relue après `/compact`). Porte laissée ouverte pour brancher un LCM plus tard si besoin marathon.

---

## Décision 8 — Meta-prompt : skill autonome + commande (hors cœur)

**Choix** : le meta-prompting **n'est pas** dans le pipeline (la spec + le plan *sont* déjà
l'instruction précise ; Superpowers couvre idée→précis via son brainstorm). On garde quand même une
**skill `meta-prompt` autonome**, invocable explicitement via une **commande `/meta-prompt`**
(skill portable `SKILL.md` + wrapper commande dans l'adaptateur Claude), pour le besoin **ponctuel**
d'optimiser un prompt one-off. **Pourquoi** : usage réel mais limité → composant optionnel découplé,
pas un maillon du flux principal. L'amélioration du one-shot passe surtout par spec + constitution.

---

## Décision 9 — Brainstorming maison (style BMAD) au lieu de `superpowers:brainstorming`

**Choix** : la commande `/brainstorm` invoque désormais **notre skill `brainstorm-facilitation`**
(`.claude/skills/brainstorm-facilitation/`, + miroir `.agents/skills/`), inspirée du workflow de brainstorming
facilité de **BMAD-METHOD** (MIT), au lieu de `superpowers:brainstorming`. Elle apporte ce qui
manquait : posture de **facilitateur** (l'agent fait émerger les idées, ne les génère pas), 3 modes,
menu de techniques (`techniques.md`, catalogue curé), divergence une-technique-à-la-fois, **challenge**
explicite (assumption listing, pre-mortem, contre-arguments), puis **convergence** → spec + critères
d'acceptation. **Pourquoi** : le brainstorm de Superpowers était jugé trop « doux » au 1er test.
**Conçue extraction-ready** (skill autonome) pour la Décision 10.

## Décision 10 — Cap : extraire un **module méthodo curé** dans un repo séparé, version figée

**Choix (validé, à exécuter en phase 2)** : plutôt que de dépendre du submodule Superpowers complet,
**extraire uniquement les briques utiles** (de Superpowers, BMAD, Spec Kit…) dans **un repo séparé
« pack méthodo » versionné**, intégré ici **en module** (submodule épinglé ou plugin/marketplace).
**Se figer sur une version est assumé** : une méthodo ne périme pas, les updates upstream sont du
nice-to-have. **Pourquoi** : légèreté (fini le « trop gros »), cohérence, contrôle du workflow,
réutilisabilité multi-projets. **Nuances** : (1) extraire **après** l'E2E (les tests disent quoi
garder) ; (2) garder le socle cross-tool (SKILL.md + AGENTS.md) et les **licences/attributions MIT**.
**Supersede partiellement** la Décision « submodule Superpowers » : le submodule reste tant que la
phase 2 n'est pas faite, puis sera remplacé par le module curé.

---

## Décision 11 — Le module curé « mri » (exécution de la Décision 10)

**Fait.** Construction du module `mri` (voir `MERGE_DESIGN.md` + `BUILD_PLAN.md`) : **front d'analyse
réimplémenté de BMAD** (mri-brainstorm avec le vrai catalogue 108 techniques + 3 modes, mri-forge à
panel de personas fixe, + elicit/adversarial-review/recherches/document-project) et **back d'exécution
extrait+adapté de Superpowers** (mri-design=pont brief→spec, devplan, implement/tdd, review, debug,
finish, verify, worktrees). **Runtime BMAD strippé** ; namespaces `superpowers:*` → `mri-*` ; chemins
normalisés sur `.mri_devtools/docs/<projet>/`. Préfixe **`mri-`** sur skills ET commandes (règle la
collision `/review` avec le natif). **Plugin Superpowers désactivé** (skills auto-portantes ; supprime
le bootstrap agressif). **Handoff** : `brief.md` (mri-brainstorm) → `spec.md` (mri-design, le pont) →
`plan.md` (mri-devplan) → implémentation. **Amende la Décision 9** : le brainstorming Superpowers
revient dans un rôle *différent* (synthèse de design = mri-design), pas comme front d'idéation.

## Décision 12 — Installation par installeur dans `.mri_devtools/` (pas de template)

**Fait.** Abandon du modèle « repo template ». Un **installeur** (`install.sh <cible> [--copy]`) dépose
le module dans **`.mri_devtools/`** (dossier caché) et génère le câblage imposé par Claude Code :
`.claude/commands/*` **à plat** (bug de découverte des sous-dossiers), `.claude/skills/*`, hooks +
`settings.json`, et `AGENTS.md`/`CLAUDE.md`/`.mcp.json` à la racine. `.claude/` = **pointeurs**
(symlink par défaut, `--copy` en fallback). La racine du projet reste **propre** (projet + dotfiles).
Le repo de dev n'est **pas** restructuré : l'installeur package ses sources vers la cible. `état généré`
(brief/spec/plan/progress) sous `.mri_devtools/docs/<projet>/` ; reprise via `/mri-resume`.

> **MàJ v0.1.0** : la Décision 12 a évolué — repo **source-first** (`payload/` + `dev/`), installeur
> **`bin/install.mjs`** (Node) + `install.sh`, distribution **`npx git+ssh://…mri-devtools.git`** (privé),
> **copy-only** (plus de symlink ; `.claude/` = vrais fichiers), config à l'install
> (`--lang`/`--doc-lang`/`--user`), **submodule Superpowers retiré**.

## Décision 13 — White-label + attribution concentrée dans LICENSE

**Fait (v0.1.0).** Le contenu **distribué** (`payload/`, `README.md`, `package.json`) ne mentionne plus
Superpowers ni BMAD (retrait cosmétique) ; un **logo ASCII maison `mri`** est apposé sur les 19 skills et
au message d'accueil. **L'attribution MIT reste dans `LICENSE`** (obligation légale : conserver la notice
« dans toutes les copies » — satisfaite par un seul fichier). Fuites périmées corrigées au passage
(directive `superpowers:brainstorming`, chemins de marque, commentaire submodule). **Pourquoi** :
produit white-label pour distribution à des clients/amis, tout en restant conforme. `dev/` (interne, FR,
non distribué) garde l'historique honnête des origines.

---

## Décision 14 — `mri-devplan` = plan léger + plan mode natif (au lieu du moteur Superpowers)

**Fait.** Le `plan.md` ne contient plus le **code d'implémentation complet** (héritage Superpowers, pensé
pour des sous-agents amnésiques-transcripteurs) : il porte le **contrat** — fichiers, blocs `Interfaces`
(signatures), **code de test**, intention. Exception gardée : les **surfaces de contrat partagées**
(types, dataclasses, Protocols, signatures publiques dont plusieurs tâches dépendent) sont montrées en
vrai code verbatim. **Pourquoi** : notre implémenteur (`mri-implement`) *raisonne* en TDD ; pré-écrire le
code le duplique, le fait drifter et coûte cher. En plus, `mri-design` et `mri-devplan` **entrent
eux-mêmes en plan mode natif** (`EnterPlanMode`) et utilisent `ExitPlanMode` comme **porte de
validation** — on garde le raisonnement/gate natif (meilleur) plutôt que de le concurrencer. Règle
globale AGENTS.md : à chaque transition, suggérer aussi le **modèle** de la commande suivante.

## Décision 15 — Revue complète (cohérence, robustesse, nettoyage)

**Fait.** Suite aux retours E2E, revue via 3 audits (flux/frontmatter, propreté/chemins, wiring/install).
- **DeepSeek retiré** partout (provider non intégrable simplement) → **Sonnet** ; section Providers révisée.
- **État unifié** : un seul `progress.md` (suivi de **phases**, `docs/<project>/`) ; le ledger d'exécution
  SDD devient `state/sdd/task-ledger.md` (**tâches**). Contradiction `docs/specs/` de la constitution levée.
- **Titres H1** uniformisés au style maison `# mri-<name> — …` ; auto-référence cassée et workflow fantôme
  « Executing Plans » supprimés ; recherches + `adversarial-review` rendus atteignables ; fins de step
  nommées + modèle.
- **Robustesse** : `welcome.sh` échappeur JSON portable (ne casse plus sans `python3`) ; `ty`/`mypy` dans
  les permissions ; prose `config.json` honnête ; scripts de skill re-chmodés à l'install.
- **Nettoyage** : `find-polluter.sh` (script `npm test` inadapté Python) + fixtures d'éval héritées retirés.
- **Bug de stack corrigé plus tôt** : `mri-scaffold-python` faisait un `sed -i` global qui corrompait les
  templates partagés → rendu en staging isolé.
- **Signalé, non traité** (le plan interdit la refonte des skills) : `mri-debug/condition-based-waiting.md`
  (+ `.ts`) et `defense-in-depth.md` utilisent des exemples **TypeScript** dans un toolbox Python.

---

## Synthèse des choix

| Sujet | Décision |
|---|---|
| Form factor | Repo template GitHub « open-and-go » via AGENTS.md (option A) |
| Spine | **Superpowers en submodule épinglé** + activation sélective (pas de pipeline maison) |
| Référence d'idées | Spec Kit (constitution, clarify, dossier specs/) — sans dépendance |
| Feedback visuel | Playwright MCP + Chrome DevTools MCP |
| Portabilité | Claude-first ; cœur AGENTS.md + Skills + MCP déjà portable |
| Tests | TDD imposé (skill Superpowers) ; critères d'acceptation → tests |
| Structure projet | Template éditable + `constitution.md` respectée par l'agent |
| Context management | Repo = store lossless + sous-agents + `tasks.md`/journal — **LCM abandonné** |
| Meta-prompt | Skill autonome + commande `/meta-prompt`, **hors cœur** |
| Brainstorming | Skill **maison** `brainstorm-facilitation` (style BMAD) au lieu de `superpowers:brainstorming` |
| Cap méthodo | Phase 2 : **module curé en repo séparé**, version figée (remplace le submodule complet) |

## Couche à construire au-dessus de Superpowers (récap)
1. Repo template open-and-go (AGENTS.md + hook SessionStart).
2. Feedback visuel/runtime (`.mcp.json` : Playwright + Chrome DevTools).
3. Scaffold Python (`templates/python-uv/`) + `constitution.md` éditable.
4. Skill `meta-prompt` autonome + commande `/meta-prompt`.
