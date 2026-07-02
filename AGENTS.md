# Bootstrap — assistant d'amorçage (mode piloté par commandes)

Tu es ouvert dans un repo qui transforme une idée en projet Python — du brainstorm à l'implémentation,
avant contrôle humain. La méthodo est le **module `mri`** (skills auto-portantes dans `.claude/skills/`,
dérivées de BMAD-METHOD et Superpowers, MIT). Les artefacts générés vivent dans `.mri_devtools/docs/<projet>/`.

## Mode : PILOTÉ PAR COMMANDES (important)
- **N'auto-déclenche AUCUNE skill.** Tu attends que l'utilisateur lance une slash command.
- **À la fin de chaque étape, suggère la commande suivante** (ne l'exécute pas toi-même).
- Les skills sont **locales et auto-portantes** ; il n'y a plus de plugin externe à invoquer.

## Au démarrage de session
Commence ta première réponse par le **message d'accueil** fourni dans le contexte de session
(le hook `welcome.sh` : reprendre via `/mri-resume` s'il existe un `progress.md` inachevé, sinon
démarrer via `/mri-brainstorm`). Puis **attends** une commande.

## Les commandes (→ skill invoquée ; suggère ensuite)
Cœur du flux :
- `/mri-brainstorm` → skill `mri-brainstorm` (facilitation style BMAD) → `/mri-forge` ou `/mri-design`
- `/mri-forge` → skill `mri-forge` (pressure-test, panel de personas) → `/mri-design` (HARDENED) ou `/mri-brainstorm` (KILLED)
- `/mri-design` → skill `mri-design` (le **pont** : `brief.md` → `spec.md`) → `/mri-devplan`
- `/mri-devplan` → skill `mri-devplan` (`spec.md` → `plan.md`) → `/mri-scaffold-python` (nouveau) sinon `/mri-implement`
- `/mri-scaffold-python` → skill `mri-scaffold-python` → `/mri-implement`
- `/mri-implement` → skill `mri-implement` (TDD + MCP) → `/mri-review`
- `/mri-review` → skill `mri-review` → `/mri-finish`
- `/mri-finish` → skill `mri-finish` (merge / PR / cleanup)

Facultatifs (suggérés au bon moment, retour au flux ensuite) :
- `/mri-elicit` (approfondir une sortie) · `/mri-adversarial-review` (auditer un doc)
- `/mri-market-research` · `/mri-domain-research` · `/mri-technical-research` (après forge)
- `/mri-document-project` (brownfield) · `/mri-debug` (échec de test) · `/mri-meta-prompt` (autonome)
- `/mri-resume` (reprendre le pipeline)

## Reprise & mémoire
L'état vit sur disque : `.mri_devtools/docs/<projet>/progress.md` (phases) + `plan.md` (cases fines).
Pour reprendre : `/mri-resume` relit `progress.md` et re-entre à l'étape courante. **Ne te repose pas
sur `/compact`.**

## Constitution
Lis et **respecte** `.toolbox/constitution.md` (stack, qualité, tests, archi, conventions).

## Feedback visuel / runtime
Pour une UI web, utilise les MCP (`.mcp.json`) : **Playwright** (piloter/tester) + **Chrome DevTools**
(console/réseau/déboguer). Boucle : écrire → exécuter → observer → corriger.

## Suggestions de modèle
En fin d'étape, chaque commande suggère un modèle (non forcé) selon `.toolbox/models.md`
(archi/brainstorm → Opus ; code → Sonnet/DeepSeek ; etc.).

## Priorité
1. Instructions utilisateur (ce fichier, `.toolbox/constitution.md`, demandes directes).
2. Skills `mri`. 3. Comportement par défaut.
