# CLAUDE.md

Ce projet est piloté par `AGENTS.md` (bootstrap portable). Lis-le et applique-le.

@AGENTS.md

## Spécificités Claude Code

- **Skills** : invoque les skills via l'outil `Skill` (ne lis pas les `SKILL.md` à la main).
  Les skills du module sont **locales et auto-portantes** dans `.claude/skills/mri-*` (préfixe `mri-`).
- **Plan mode** : utilise le plan mode pour l'étape « Design » (validation humaine avant implémentation).
- **Sous-agents** : préfère des sous-agents spécialisés pour l'exploration et l'implémentation isolée
  (garde le contexte principal court). `mri-implement` s'appuie dessus (TDD par tâche).
- **Superpowers** : le submodule `.toolbox/superpowers` est la **source d'extraction** du module `mri`
  (plugin désactivé dans `settings.json`) ; il n'est plus invoqué au runtime.
