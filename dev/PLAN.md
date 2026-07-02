# PLAN — Toolbox IA « idée → projet » (repo template open-and-go, basé sur Superpowers)

> Plan de construction. Pré-requis lus : `docs/SEARCH_RESULTS.md` (état de l'art) et
> `docs/DECISIONS.md` (choix & justifications). **La construction est volontairement séparée** :
> à démarrer après revue du plan par l'utilisateur.

## Contexte & objectif

Construire une couche d'amorçage qui transforme une idée vague en projet Python prêt à coder :
**brainstorm → spec précise → plan → scaffold guidant l'agent → implémentation en TDD avec feedback
visuel**, avant contrôle humain. Le livrable est un **repo template GitHub** : `Use this template`,
on ouvre un agent de code dans le dossier, et l'interaction démarre via `AGENTS.md`.

**Principe directeur : ne pas réinventer.** Le moteur méthodologique est **Superpowers** (en
submodule), qui apporte déjà brainstorm socratique, planning, subagent-driven development, TDD imposé,
debugging et code review. Notre travail = une **fine couche** par-dessus (4 ajouts ci-dessous) +
l'orientation **one-shot** via spec précise et `constitution.md`.

## Principe transverse : context management par design (LCM abandonné)

Le **repo est le store lossless** (cf. DECISIONS §7). Pas de LCM.
- **Write** : état durable dans `docs/specs/` (spec, plan, `tasks.md`, journal) — pas dans la compaction.
- **Select** : `AGENTS.md` court (< 150 lignes), `constitution.md` concise, skills à la demande.
- **Isolate** : sous-agents (exploration/implémentation/review en contextes propres).
- **Compress** : hooks + context editing pour purger les vieux résultats d'outils.
- `tasks.md` = mémoire de travail, relue après un `/compact`.

---

## Architecture cible (structure du repo template)

```
toolbox/  (= devient "mon-projet" après "Use this template")
  AGENTS.md                 # bootstrap PORTABLE : oriente le flux (brainstorm→spec→plan→impl) + one-shot
  CLAUDE.md                 # pointe vers AGENTS.md + extras Claude
  superpowers/              # SUBMODULE épinglé (obra/superpowers) — le moteur méthodologique
                            #   activation SÉLECTIVE des skills via AGENTS.md / config
  skills/                   # NOS skills (portables SKILL.md), minimales :
    scaffold-python/        #   applique templates/python-uv selon constitution.md
    meta-prompt/            #   AUTONOME, hors pipeline (optimisation de prompt one-off)
  .claude/                  # ADAPTATEUR Claude
    commands/
      meta-prompt.md        #   wrapper commande -> invoque la skill meta-prompt
    hooks/                  #   SessionStart (accueil) ; Stop -> lint+test (boucle feedback)
    settings.json           #   permissions (denies agressifs, allows minimaux) + skills activées
  .mcp.json                 # Playwright MCP + Chrome DevTools MCP (feedback visuel/runtime)
  templates/
    python-uv/              # scaffold ÉDITABLE : uv + ruff + ty(/mypy) + pytest + pre-commit, src/
  constitution.md           # règles ÉDITABLES respectées par l'agent (stack, qualité, tests, layout)
  docs/
    SEARCH_RESULTS.md        # état de l'art (écrit)
    DECISIONS.md             # choix & justifications (écrit)
    specs/                   # mémoire externe générée par run (spec/plan/tasks/journal)
  README.md                 # mode d'emploi : "Use this template" + init submodule + ouvrir l'agent
```

Ce qu'on **n'écrit pas** (fourni par Superpowers) : brainstorm, planning, subagent-driven dev, TDD,
debugging, code review, git worktrees, skill authoring.
Ce qu'on **écrit** : AGENTS.md + CLAUDE.md, `constitution.md`, `templates/python-uv/`, skill
`scaffold-python`, skill `meta-prompt` + commande, `.mcp.json`, hooks/settings Claude, README.

---

## Lot de travail (ordre suggéré)

### Lot 0 — Squelette + intégration Superpowers
- `git init`, structure de dossiers, `README.md`, `.gitignore`.
- Ajouter **Superpowers en submodule** (version épinglée). **Vérifier la licence** avant vendoring.
- Inspecter ses skills : lesquelles activer, comment il persiste specs/plans sur disque.
- **Vérif** : submodule cloné ; skills Superpowers visibles par Claude Code.

### Lot 1 — Bootstrap « open-and-go » + orientation one-shot
- `AGENTS.md` (< 150 lignes) : rôle d'amorçage, déclenchement du flux, **activation sélective** des
  skills Superpowers, consigne context management (« persiste dans docs/specs, pas de /compact comme
  mémoire »), réglage du curseur one-shot (précision front-loadée puis autonomie).
- `CLAUDE.md` -> AGENTS.md ; hook **SessionStart** (accueil + prochaines étapes).
- **Vérif** : ouvrir Claude Code dans le dossier → accueil + proposition de brainstorm (Superpowers).

### Lot 2 — `constitution.md` éditable
- Modèle de constitution Python (stack uv/ruff/ty, TDD obligatoire, layout src/, conventions, archi).
- **Vérif** : modifier `constitution.md` change les standards que l'agent applique.

### Lot 3 — Scaffold Python + skill `scaffold-python`
- `templates/python-uv/` (uv+ruff+ty/mypy+pytest+pre-commit, layout `src/`).
- `skills/scaffold-python` : applique le template **selon `constitution.md`**.
- **Vérif** : projet généré qui `uv run`/`pytest` à blanc sans erreur ; changer la constitution change
  la structure produite.

### Lot 4 — Feedback visuel/runtime
- `.mcp.json` : Playwright MCP + Chrome DevTools MCP.
- `.claude/hooks` : **Stop → lint + tests** (signal de la boucle, en complément du TDD Superpowers).
- **Vérif** : sur un mini-projet web, l'agent pilote/inspecte le navigateur via MCP ; le hook bloque
  si tests/lint échouent.

### Lot 5 — Skill `meta-prompt` autonome + commande
- `skills/meta-prompt/SKILL.md` (portable) + `.claude/commands/meta-prompt.md` (wrapper).
- **Vérif** : `/meta-prompt` invoque la skill et renvoie un prompt optimisé, **hors** du flux principal.

### Lot 6 — Portabilité & doc
- Vérifier le cœur (AGENTS.md + nos skills + `.mcp.json` + Superpowers) dans un second agent (Codex).
- `README.md` : « Use this template », init submodule, ouverture de l'agent, usage one-shot.
- **Vérif** : ouvrir Codex dans le dossier lit AGENTS.md + skills ; flux de base fonctionne.

---

## Validation end-to-end (cas réel)

Partir d'une **idée vague jouet** (ex. « une petite API de todo ») et dérouler tout le pipeline via
Superpowers + notre couche : brainstorm → spec (+ critères) → plan → scaffold Python (selon
constitution) → TDD (rouge→vert) → review + feedback navigateur. **Succès** : projet Python qui
démarre, passe lint + tests, avec spec/plan/journal dans `docs/specs/`, le tout déclenché en ouvrant
simplement l'agent dans le dossier.

## Hors périmètre (plus tard)
- Adaptateurs Codex/ZCode dédiés (commandes/hooks spécifiques).
- Orchestration multi-agents coût/qualité (Claude = cerveau, GLM/Codex = bras) + worktrees parallèles.
- Distribution en plugin/pack installable pour propager les mises à jour aux projets existants.
- Skill `refine-prompt` enrichie / couche LCM — seulement si un besoin réel émerge à l'usage.
