# Bootstrap — assistant d'amorçage (mode piloté par commandes)

Tu es ouvert dans un repo template qui transforme une idée en projet Python — du brainstorm à
l'implémentation, avant contrôle humain. La toolchain est rangée dans `.toolbox/`.

## Mode : PILOTÉ PAR COMMANDES (important)
- **N'auto-déclenche AUCUNE skill.** Tu attends que l'utilisateur lance une slash command.
- Cette consigne **prime sur le bootstrap Superpowers** (`using-superpowers`) : d'après sa propre
  règle, les instructions utilisateur (ce fichier) passent avant les skills. Tu n'invoques donc une
  skill que quand une commande te le demande.
- **À la fin de chaque étape, suggère la commande suivante** (ne l'exécute pas toi-même).

## Au démarrage de session
Commence ta première réponse par le **message d'accueil** fourni dans le contexte de session
(liste des commandes + suggestion de démarrer `/brainstorm` ou de reprendre `/implement` s'il existe
un plan inachevé). Puis **attends** une commande.

## Les commandes (→ skill invoquée ; suggère ensuite)
- `/brainstorm` → `superpowers:brainstorming` → `/plan`
- `/plan` → `superpowers:writing-plans` → `/scaffold` (nouveau projet) sinon `/implement`
- `/scaffold` → skill `scaffold-python` → `/implement`
- `/implement` → `superpowers:subagent-driven-development` (TDD) → `/review`
- `/review` → `superpowers:requesting-code-review` → `/finish`
- `/finish` → `superpowers:finishing-a-development-branch`
- `/debug` → `superpowers:systematic-debugging`
- `/meta-prompt` → skill `meta-prompt` (optimiser un prompt ponctuel)

## Reprise & mémoire
La mémoire du projet vit sur disque dans `docs/specs/<projet>/` (spec, plan, `tasks.md` avec cases).
Pour reprendre : relis `tasks.md` et continue aux tâches non cochées. **Ne te repose pas sur `/compact`.**

## Constitution
Lis et **respecte** `.toolbox/constitution.md` (stack, qualité, tests, archi, conventions).

## Feedback visuel / runtime
Pour une UI web, utilise les MCP (`.mcp.json`) : **Playwright** (piloter/tester) + **Chrome DevTools**
(console/réseau/déboguer). Boucle : écrire → exécuter → observer → corriger.

## Si Superpowers est inactif
Si les skills `superpowers:*` n'existent pas : demande de lancer `./.toolbox/scripts/setup.sh`
(puis `/reload-plugins`), ou de relancer avec `claude --plugin-dir ./.toolbox/superpowers`.

## Priorité
1. Instructions utilisateur (ce fichier, `.toolbox/constitution.md`, demandes directes).
2. Skills Superpowers. 3. Comportement par défaut.
