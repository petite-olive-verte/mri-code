# État de l'art — Agents de code IA & workflows (recherche, mi-2026)

> Compilation de recherche pour le projet « toolbox IA pour agents de code ».
> Objectif : cartographier l'état de l'art avant de construire une couche d'amorçage de projets
> (idée vague → spec précise → scaffold guidant l'agent → implémentation largement automatique).

## Sommaire
1. [Agents de code : panorama & quel agent pour quel usage](#1-agents-de-code--panorama--quel-agent-pour-quel-usage)
2. [Retour d'information visuel/runtime (point clé)](#2-retour-dinformation-visuelruntime-point-clé)
3. [Brainstorming / idéation structurée](#3-brainstorming--idéation-structurée)
4. [Planification & Spec-Driven Development](#4-planification--spec-driven-development-sdd)
5. [Meta-prompting & prompting (vague → précis)](#5-meta-prompting--prompting-vague--précis)
6. [Context engineering & one-shot](#6-context-engineering--one-shot)
7. [Loop engineering (boucle agent)](#7-loop-engineering-boucle-agent)
8. [Context management & context rot](#8-context-management--context-rot)
9. [Tests & TDD avec agents](#9-tests--tdd-avec-agents)
10. [Personnalisation des agents (skills, commands, sous-agents, hooks)](#10-personnalisation-des-agents)
11. [Portabilité entre agents (AGENTS.md, SKILL.md, MCP)](#11-portabilité-entre-agents)
12. [Connexion aux serveurs MCP](#12-connexion-aux-serveurs-mcp)
13. [Git workflow & sous-agents en parallèle](#13-git-workflow--sous-agents-en-parallèle)
14. [Template projet Python 2026](#14-template-projet-python-2026)
15. [Frameworks open-source à réutiliser (BMAD, Superpowers)](#15-frameworks-open-source-à-réutiliser-bmad-superpowers)

---

## 1. Agents de code : panorama & quel agent pour quel usage

| Agent | Forces | Faiblesses | Coût | Usage idéal |
|---|---|---|---|---|
| **Claude Code** (Opus 4.8 / Sonnet 4.6) | Meilleur raisonnement multi-fichiers, refactors complexes, intégration Git native ; SWE-bench Pro ~69% (Opus 4.8) | Le plus gros consommateur de tokens | Pro $20 / Max $100 | Planification, archi, refactors, review — tâches « cerveau » |
| **Codex CLI** (GPT-5.5) | #1 Terminal-Bench 2.1 (~83%), ~4× moins de tokens, sandboxing fort | Moins fort en raisonnement multi-fichiers profond | Économe | Exécution autonome en lot, single-file, environnements sensibles |
| **Gemini CLI → Antigravity** | Contexte 1M, gros free tier | Transition produit (cutoff free tier 18/06/2026) | Free tier généreux | Exploration de gros monorepo, tâches rapides/budget |
| **GLM-5.2 (Z.ai)** + harnais (Cline, OpenCode, ZCode, Roo, Crush) | Open-weights, contexte 1M, ~1/6 du coût de GPT-5.5, proche d'Opus en long-horizon | Légèrement sous Opus | GLM Lite $12.6 / Pro $50 / Max $112 | Implémentation en volume à bas coût, BYO-API |
| **Cline / Aider** | OpenAI-compatible, BYO-key, flexible | Moins clé en main | Coût API seul | Boucles locales, contrôle fin, modèle au choix |
| **ZCode** (Zhipu) | GUI multi-agents | Écosystème jeune | — | Orchestration multi-agents en GUI |

**Repères benchmarks (2026)** : Terminal-Bench 2.1 → Codex/GPT-5.5 #1 (83,4%), Claude Code/Opus 4.8 #2
(78,9%), Gemini CLI/Gemini 3.1 Pro (70,7%). SWE-bench Pro → Opus 4.8 #1 (69,2%).
Gain médian de débit de PR mesuré sur 400+ orgs / 14 mois : **+7,76%** (réel mais loin des promesses).

**Stratégie multi-agents coût/qualité** : « cerveau » coûteux (Claude Opus) pour brainstorm, spec,
plan et review ; « bras » bon marché (Codex / GLM via Cline/OpenCode) pour l'implémentation en volume.
Les techniques d'efficience token peuvent réduire le coût de **77 à 91%**. Un harnais open + modèle
open-weight ≈ 1/20 du coût d'un agent fermé type Devin.

Sources :
[deployhq](https://www.deployhq.com/blog/comparing-claude-code-openai-codex-and-google-gemini-cli-which-ai-coding-assistant-is-right-for-your-deployment-workflow),
[codeant](https://www.codeant.ai/blogs/claude-code-cli-vs-codex-cli-vs-gemini-cli-best-ai-cli-tool-for-developers-in-2025),
[firecrawl](https://www.firecrawl.dev/blog/best-ai-coding-agents),
[getdx](https://getdx.com/blog/ai-coding-assistant-pricing/),
[morphllm](https://www.morphllm.com/ai-coding-agent),
[venturebeat (GLM-5.2)](https://venturebeat.com/technology/z-ais-open-weights-glm-5-2-beats-gpt-5-5-on-multiple-long-horizon-coding-benchmarks-for-1-6th-the-cost),
[tembo (15 CLI agents)](https://www.tembo.io/blog/coding-cli-tools-comparison).

---

## 2. Retour d'information visuel/runtime (point clé)

C'est le levier #1 de fiabilité : un agent qui **écrit → exécute → lit le résultat → corrige**.
Les screenshots seuls sont un pis-aller (raisonnement visuel obligatoire, coûteux). Préférer un MCP
navigateur qui renvoie des **données structurées**.

| Outil | Sortie par défaut | Navigateurs | Idéal pour |
|---|---|---|---|
| **Playwright MCP** (Microsoft) | Arbre d'**accessibilité** (rôles, noms, refs) ; screenshots possibles | Chromium / Firefox / WebKit | **Piloter / tester** des parcours UI : fiable, économe en tokens |
| **Chrome DevTools MCP** (Google, 1st-party, ~34k★) | Console (stack traces source-mappées), réseau, perf, screenshots, snapshot DOM | Chromium | **Déboguer** une app web ; permet le **self-healing** (l'agent vérifie et re-corrige) |
| **Puppeteer MCP** | Screenshots only | Chromium | ~15-20% plus rapide sur Chromium pur mais perd en fiabilité/compréhension ; globalement supplanté |

**Verdict** : combo gagnant = **Playwright MCP (piloter) + Chrome DevTools MCP (déboguer)**, branchés
dans une boucle de vérification (tests + observation runtime) déclenchée par des hooks. C'est ce qui
comble le « trou » des approches purement spec (erreurs runtime sinon diagnostiquées à la main).

Sources :
[stevekinney](https://stevekinney.com/writing/driving-vs-debugging-the-browser),
[mcp.directory (DevTools vs Playwright)](https://mcp.directory/blog/chrome-devtools-mcp-vs-playwright-mcp-2026),
[chrome-devtools-mcp (repo)](https://github.com/ChromeDevTools/chrome-devtools-mcp),
[Addy Osmani — Give your AI eyes](https://addyosmani.com/blog/devtools-mcp/),
[dev.to — browser tools for agents](https://dev.to/stevengonsalvez/browser-tools-for-ai-agents-part-1-playwright-puppeteer-and-why-your-agent-picked-playwright-k71).

---

## 3. Brainstorming / idéation structurée

Le combo humain+IA bat l'un ou l'autre seul : l'IA génère le volume et les connexions inter-domaines,
l'humain juge la nouveauté/pertinence. Techniques efficaces :

- **Socratic questioning** : interview multi-tours pour clarifier croyances et hypothèses (= le cœur
  du « idée vague → précis »).
- **Assumption listing** : lister les hypothèses qui doivent être vraies pour chaque idée + un test
  low-effort qui la valide/tue → transforme le brainstorm en décisions actionnables.
- **Pre-mortem** : anticiper les modes d'échec.
- **SCAMPER**, **reverse brainstorming**, **rolestorming / personas**, **Alternative Worlds**
  (transposer une stratégie d'une industrie à une autre).

Sources :
[jenova.ai](https://www.jenova.ai/en/resources/ai-for-brainstorming-ideas),
[itonics (ideation techniques)](https://www.itonics-innovation.com/blog/powerful-ideation-techniques),
[asana (29 techniques)](https://asana.com/resources/brainstorming-techniques).

---

## 4. Planification & Spec-Driven Development (SDD)

Le SDD est la réponse au « vibe coding ». **GitHub Spec Kit** (v0.11, juin 2026, agent-agnostic, 30+
agents) formalise le flux. Commandes : `/constitution` (principes : qualité, tests, perf) →
`/specify` (le quoi/pourquoi, sans la stack) → `/clarify` (questions pour lever les zones floues) →
`/plan` (stack + archi) → `/tasks` (découpe ordonnée avec dépendances) → `/implement` → `/converge`
(compare le code fini à la spec). Artefacts générés : `.specify/` (constitution, templates, scripts)
et `specs/[feature]/` (`spec.md`, `plan.md`, `tasks.md`, `data-model.md`, `research.md`).

**Bénéfices** : capture d'intention structurée, moins de rework, technologie-agnostique.
**Limites** : exige de la discipline ; surtout greenfield ; **erreurs runtime diagnostiquées à la
main** (← comblé par les MCP de feedback) ; dépendance + CLI à installer. Le **plan mode** de Claude
Code s'inscrit dans la même logique (planifier + valider avant d'implémenter).

Sources :
[GitHub Blog — SDD](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/),
[spec-kit (repo)](https://github.com/github/spec-kit),
[spec-kit docs](https://github.github.com/spec-kit/),
[BCMS — guide SDD 2026](https://thebcms.com/blog/spec-driven-development).

---

## 5. Meta-prompting & prompting (vague → précis)

- **Meta-prompting** : faire concevoir/améliorer le prompt par le modèle avant de répondre ; ajouter
  structure (format, ton, audience, périmètre), demander une auto-revue, reformuler une demande floue
  en spec exécutable. C'est exactement le « idée vague → prompt précis » recherché.
- **Zero-shot vs few-shot** : commencer zero-shot ; passer few-shot pour guider un format/domaine
  précis. ⚠️ Les exemples peuvent **nuire** en raisonnement pur (copie d'étapes erronées).
- **Chain-of-Thought** : zero-shot CoT (« réfléchis étape par étape ») = meilleur ratio
  simplicité/gain ; few-shot CoT pour domaines spécialisés ; Auto-CoT pour générer les exemplaires.

Sources :
[promptingguide — meta prompting](https://www.promptingguide.ai/techniques/meta-prompting),
[prompthub — meta prompting](https://www.prompthub.us/blog/a-complete-guide-to-meta-prompting),
[vellum — zero vs few-shot](https://www.vellum.ai/blog/zero-shot-vs-few-shot-prompting-a-guide-with-examples),
[arxiv 2506.14641 — zero-shot CoT peut battre few-shot](https://arxiv.org/abs/2506.14641).

---

## 6. Context engineering & one-shot

Les agents échouent plus souvent au niveau **contexte** qu'au niveau prompt. Context engineering =
fournir la bonne info + les bons outils, au bon format, au bon moment (= ingénierie de l'état de
l'agent). Pour améliorer le **one-shot**, investir dans le contexte (CLAUDE.md/AGENTS.md ciblé, spec
claire, sous-agents) plus que dans le wording. Étude multi-agents (clarification d'intention + RAG +
sous-agents spécialisés) : **80% de succès vs 40%** pour un single-agent.

Sources :
[deepset — context engineering](https://www.deepset.ai/blog/context-engineering-the-next-frontier-beyond-prompt-engineering),
[firecrawl — context vs prompt](https://www.firecrawl.dev/blog/context-engineering),
[arxiv 2508.08322 — multi-agent code assistants](https://arxiv.org/html/2508.08322v1).

---

## 7. Loop engineering (boucle agent)

Terme popularisé en 2026 (Addy Osmani / Boris Cherny). La boucle qui marche en prod :
**écrire → exécuter → lire le résultat → corriger**, jusqu'à une cible *mesurable* (tests qui passent,
check runtime). Le signal de feedback (tests, exécution, observation navigateur) est « la magie ».
Les agents de code sont l'exemple le plus mature d'agent loop (plan-act-observe-evaluate). À
industrialiser via hooks + MCP de feedback.

Sources :
[explainx — loop engineering Claude Code](https://explainx.ai/blog/loop-engineering-coding-agents-claude-code-guide-2026),
[Towards AI — loop engineering](https://pub.towardsai.net/loop-engineering-for-ai-agents-building-verifiable-self-correcting-coding-workflows-8b32c72184a1),
[arxiv 2506.11442 — ReVeal self-verification](https://arxiv.org/pdf/2506.11442).

---

## 8. Context management & context rot

- **Context rot** : dégradation mesurable des perfs quand l'input s'allonge, *indépendamment* de la
  pertinence (recherche Chroma, confirmée sur Claude/GPT/Gemini/Qwen). **Les grandes fenêtres ne le
  règlent pas** — elles montent le plafond, la dégradation garde la même forme. Certains réduisent
  volontairement la fenêtre de Claude Code à 200k pour de meilleurs résultats.
- **Framework Anthropic (formalisé 09/2025) : Write / Select / Compress / Isolate**
  - *Write* : externaliser l'état → artefacts durables (SPEC.md, PLAN.md, journal de décisions), memory tool.
  - *Select* : ne charger que le pertinent → AGENTS.md < 150 lignes, skills chargées à la demande.
  - *Compress* : `/compact`, **context editing** (`clear_tool_uses_20250919` purge les vieux résultats d'outils).
  - *Isolate* : sous-agents au contexte propre ; seul un résumé revient au coordinateur.
- **Chiffres** : context editing seul **+29%** ; +memory tool **+39%**. Les observations d'outils
  consomment **70-80%** du budget dans une boucle ReAct.
- **⚠️ Piège `/compact`** : peut réduire 132k→2,3k tokens (-98%) et **jeter la compréhension fine**.
  → S'appuyer sur les **artefacts écrits**, pas sur la compaction, comme mémoire de session.
- **Lossless Context Management (LCM)** : approche DAG/SQLite (immutable store + active context ;
  résumés mais originaux préservés et re-récupérables exactement — ex. hermes-lcm, papier LCM 2026).
  Pertinent pour un **assistant** (la conversation EST l'état). Pour un **agent de code**, le **repo
  est déjà le store lossless** (code/spec/plan/tests/git = path-addressable, compaction-stable) →
  LCM généralement superflu (cf. décision retenue dans `DECISIONS.md`).

Sources :
[Anthropic — context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing),
[hermes-lcm](https://github.com/stephenschoettler/hermes-lcm),
[arxiv 2605.04050 — LCM](https://arxiv.org/html/2605.04050v1),
[arxiv 2604.08224 — externalization in LLM agents](https://arxiv.org/pdf/2604.08224),
[Claude Cookbook — memory/compaction/tool clearing](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools),
[Claude Code — context window](https://code.claude.com/docs/en/context-window),
[Chroma / context rot](https://glasp.co/articles/context-rot-rag-long-context-hybrid),
[digitalapplied — reliability playbook](https://www.digitalapplied.com/blog/context-engineering-agent-reliability-playbook-2026).

---

## 9. Tests & TDD avec agents

- Le TDD devient **le** garde-fou : l'agent code plus vite qu'on ne relit → les tests sont la seule
  barrière viable contre les régressions.
- **Qui écrit quoi** : le test définit « correct » *avant* l'implémentation → l'agent ne peut pas
  valider ses propres bugs. Tests écrits *après* par l'IA = il valide ce qu'il a écrit, pas la feature.
- **⚠️ Tests générés par l'IA = faibles** : ~20% de score de mutation (80% des bugs passent — ils
  compilent, passent, et ne valident rien). → L'humain/la spec possède l'**intention** du test ;
  l'agent possède l'**implémentation**.
- **Red-Green-Refactor imposé mécaniquement** (skill/hook) bat le TDD laissé au jugement de l'agent.
  *Superpowers* : 85-95% de couverture (vs 30-50% standard) ; spec-driven : -60% de rollbacks.
- Couches : unit + integration + e2e + UI. Les tests = **signal de la boucle** écrire→exécuter→lire→corriger.

Sources :
[fundesk — TDD avec agents](https://www.fundesk.io/test-driven-development-ai-agents-guide),
[Superpowers framework](https://baeseokjae.github.io/posts/superpowers-framework-ai-coding-2026/),
[htek.dev — tests are everything](https://htek.dev/articles/tests-are-everything-agentic-ai/),
[arxiv 2510.23761 — TDFlow](https://arxiv.org/pdf/2510.23761).

---

## 10. Personnalisation des agents

- **CLAUDE.md / AGENTS.md** = « constitution » du repo, lue à chaque session. À garder **minimale et
  ciblée** (ne pas surcharger le contexte ; < 150 lignes).
- **Slash command** = template de prompt injecté, invoqué par l'utilisateur, simple/pas cher.
- **Skill** (`SKILL.md`) = quand il y a de la logique métier / fichiers d'aide ; chargée à la demande
  (seuls nom+description en RAM au départ → contexte propre). Peut embarquer templates/scripts/exemples.
- **Sous-agent** = acteur autonome, contexte isolé, outils/permissions propres ; les agents
  *spécifiques par feature* battent les agents génériques. Mémoire scopable (`memory: user/project/local`).
- **Hooks** = comportements automatiques déclenchés par le harnais (lint/test on stop, SessionStart, etc.).
- **Permissions** : denies agressifs (sudo, `rm -rf /`, `git push --force`), allows minimaux.

Sources :
[Claude Code — skills](https://code.claude.com/docs/en/skills),
[mcp.directory — best practices](https://mcp.directory/blog/claude-code-best-practices),
[alexop.dev — customization guide](https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/),
[claude.com — skills explained](https://claude.com/blog/skills-explained).

---

## 11. Portabilité entre agents

Bonne nouvelle pour « ne pas dépendre d'un seul outil » : le socle est **déjà portable** via standards ouverts.

| Brique | Portable | Standard / note |
|---|---|---|
| Instructions | ✅ | **AGENTS.md** (OpenAI 08/2025 → Linux Foundation/AAIF ; 28+ outils, 60k+ repos). Codex natif, Cursor, Gemini, Copilot… **Claude Code le lit depuis printemps 2026**. < 150 lignes. AGENTS.md améliore le succès ~+4% et réduit les bugs 35-55%. |
| Skills | ✅ | **SKILL.md** (Anthropic 12/2025, adopté OpenAI/Codex, Cursor, Gemini, 30+ outils ; agentskills.io). Même fichier ; dossier diffère (`.claude/skills/` vs `.agents/skills/`) → symlink. |
| MCP | ✅ | Standard universel (inclut le feedback visuel). |
| Slash commands | ⚠️ | Custom prompts Codex (`~/.codex/prompts`) **dépréciés au profit des Skills** → converger vers Skills. |
| Sous-agents / hooks / permissions | ❌ | Spécifiques Claude → couche « adaptateur » par agent. |

**Conséquence** : cœur portable (AGENTS.md + SKILL.md + MCP) + adaptateurs minces par agent. C'est
exactement ce que fait Spec Kit (génération per-agent depuis une source unique).

Sources :
[codex.danielvaughan — AGENTS.md cross-tool](https://codex.danielvaughan.com/2026/05/27/agent-instruction-files-agents-md-claude-md-cross-tool-portability-codex-cli/),
[morphllm — AGENTS.md guide](https://www.morphllm.com/agents-md-guide),
[OpenAI — Agent Skills (Codex)](https://developers.openai.com/codex/skills),
[VoltAgent — awesome-agent-skills (cross-tool)](https://github.com/VoltAgent/awesome-agent-skills),
[termdock — SKILL.md vs CLAUDE.md vs AGENTS.md](https://www.termdock.com/blog/skill-md-vs-claude-md-vs-agents-md).

---

## 12. Connexion aux serveurs MCP

Trois transports : **stdio** (process local, accès système), **HTTP** (distant, recommandé ;
**SSE déprécié début 2026**). Ajout :
`claude mcp add --transport stdio <nom> -- <cmd>` / `--transport http <url> --header "Authorization:Bearer …"`.
Toutes les options (`--transport`, `--env`, `--scope`, `--header`) avant le nom du serveur ; `--`
sépare le nom de la commande stdio. Scopes : perso (défaut), équipe (`.mcp.json`), managé admin.

Sources :
[Claude Code — MCP docs](https://code.claude.com/docs/en/mcp),
[builder.io — MCP servers](https://www.builder.io/blog/claude-code-mcp-servers),
[systemprompt.io — install MCP 2026](https://systemprompt.io/guides/claude-code-mcp-servers-extensions).

---

## 13. Git workflow & sous-agents en parallèle

**Git worktrees** = meilleur ratio coût/isolation pour paralléliser des agents sur un même repo
(`.git` partagé, répertoires séparés). **Limite** : isole le code mais **pas le runtime**
(ports/DB/services partagés). Pattern : un Coordinateur planifie → décompose en tâches ordonnées →
délègue à des spécialistes en « vagues » dans des worktrees isolés (cf. Cursor « Parallel Agents »,
Augment Intent). Anthropic recommande les worktrees pour le multi-session.

Sources :
[Augment — worktrees parallel agents](https://www.augmentcode.com/guides/git-worktrees-parallel-ai-agent-execution),
[MindStudio — worktrees](https://www.mindstudio.ai/blog/parallel-ai-coding-agents-git-worktrees),
[Upsun — worktrees](https://developer.upsun.com/posts/ai/git-worktrees-for-parallel-ai-coding-agents).

---

## 14. Template projet Python 2026

Stack par défaut : **uv** (remplace pyenv/pip/venv/pip-tools/Poetry) + **Ruff** (lint/format) +
**ty** (type checker Astral, très rapide, encore beta 0.0.x → mypy/pyright en fallback) + **pytest**
(+ pytest-sugar) + **pre-commit**. Layout `src/`, Python 3.12+, `pyproject.toml` = **source unique**
de config. Réfs : `uv init`, template `jlevy/simple-modern-uv`. Perf : uv installe en ~100ms ce que
pip faisait en 30s ; Ruff lint 100k LoC en ~200ms.

Sources :
[KDnuggets — Python setup 2026](https://www.kdnuggets.com/python-project-setup-2026-uv-ruff-ty-polars),
[jlevy/simple-modern-uv](https://github.com/jlevy/simple-modern-uv),
[pydevtools — complete project](https://pydevtools.com/handbook/tutorial/set-up-a-complete-python-project/).

---

## 15. Frameworks open-source à réutiliser (BMAD, Superpowers)

Principe : **ne pas réinventer**. Plusieurs frameworks open-source couvrent déjà tout ou partie du
pipeline « idée → code ». On compose à partir d'eux.

### Superpowers (obra) — retenu comme spine
Plugin / framework de skills composables + méthodologie, **portable** (Claude Code, Cursor, Codex,
Gemini, Copilot CLI, OpenCode…). ~7 skills cœur (jusqu'à ~14 avec sous-skills) :
- **Brainstorm socratique** (questionne avant de coder)
- **Extraction de spec** montrée par bouts validés
- **Planning** en tâches de 2-5 min avec specs de code précises
- **Subagent-driven development** + review en 2 passes (conformité spec, puis qualité)
- **TDD red-green-refactor imposé** (le test échoue avant l'implémentation)
- **Debugging systématique** (4 phases, cause racine avant correctif)
- **Git worktrees** + **skill authoring**

**Empreinte** : les skills se chargent **à la demande** (nom+description au repos, contenu complet au
déclenchement) → faible coût contexte. « Lourdeur » surtout méthodologique (process imposé = le
guidage voulu). **Limites assumées** : debugging d'environnement, récupération de session,
erreurs de spec passant la review → faiblesse **runtime** (comblée par les MCP de feedback).
**Modèle « interaction front-loadée puis exécution autonome »** = aligné avec le one-shot.

### BMAD Method — alternative / source d'idées
Framework agile IA open-source (MIT), **tool-agnostic**, full SDLC via **personas** (Analyst, PM,
Architect…) produisant des **artefacts versionnés** (PRD, architecture) avant le code. 7 étapes :
Brainstorm → PM → Architect → Develop → Review → Test → Commit. Modules : BMM (workflows), BMB
(builder d'agents/workflows), TEA (test architect), BMGD (game dev), **CIS** (Creative Intelligence
Suite = l'outil de brainstorming apprécié). Bonne source d'idées pour le brainstorm et les personas.

### Autres à cherry-pick
Listes **awesome-claude-code** / **awesome-agent-skills** (skills par domaine), **Spec Kit** (squelette
spec→plan→tasks + concept de *constitution*), skills « pitfalls » type Karpathy, UI/UX, etc.

> ⚠️ Compteurs d'étoiles GitHub renvoyés par la recherche peu fiables (probablement gonflés) →
> à vérifier directement sur les repos. Périmètre et existence des frameworks, eux, confirmés.

Sources :
[Superpowers (repo)](https://github.com/obra/superpowers),
[Superpowers — blog auteur](https://blog.fsck.com/2025/10/09/superpowers/),
[builder.io — Superpowers plugin](https://www.builder.io/blog/claude-code-superpowers-plugin),
[BMAD-METHOD (repo org)](https://github.com/bmad-code-org),
[BMad Method](https://www.bmadcode.com/bmad-method/),
[awesome-claude-code](https://github.com/jqueryscript/awesome-claude-code),
[VoltAgent — awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills).
