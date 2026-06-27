# CLAUDE.md

Ce projet est piloté par `AGENTS.md` (bootstrap portable). Lis-le et applique-le.

@AGENTS.md

## Spécificités Claude Code

- **Skills** : invoque les skills via l'outil `Skill` (ne lis pas les `SKILL.md` à la main).
  Skills Superpowers = namespace `superpowers:*` (ex. `superpowers:brainstorming`).
- **Plan mode** : utilise le plan mode pour l'étape « Plan » (validation humaine avant implémentation).
- **Sous-agents** : préfère des sous-agents spécialisés pour l'exploration et l'implémentation isolée
  (garde le contexte principal court).
- **Setup** : si les skills `superpowers:*` sont absentes, lance `./scripts/setup.sh` (une fois),
  puis `/reload-plugins` — ou relance avec `claude --plugin-dir ./superpowers`.
