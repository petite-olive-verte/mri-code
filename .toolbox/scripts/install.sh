#!/usr/bin/env bash
# Installe le module « mri » dans un projet cible :
#   .mri_devtools/  = LE MODULE (skills, commandes, hooks, templates, constitution, models, docs générées)
#   + câblage imposé par Claude Code : .claude/{commands (à plat), skills, hooks, settings.json}
#     et AGENTS.md / CLAUDE.md / .mcp.json à la racine.
#
# Usage : install.sh <dossier-cible> [--copy]
#   défaut : symlinks .claude/{skills,commands} → .mri_devtools/ (pas de duplication)
#   --copy : copie au lieu de lier (si la découverte des symlinks pose problème)
#
# NB : ce repo de dev n'est PAS restructuré ; l'installeur PACKAGE ses sources vers la cible.
set -euo pipefail

SRC="$(cd "$(dirname "$0")/../.." && pwd)"                 # racine du repo module (source)
TARGET="${1:?usage: install.sh <dossier-cible> [--copy]}"
MODE="link"; [ "${2:-}" = "--copy" ] && MODE="copy"
mkdir -p "$TARGET"; TARGET="$(cd "$TARGET" && pwd)"
MRI="$TARGET/.mri_devtools"

echo "==> Installation du module mri dans : $TARGET  (mode: $MODE)"
mkdir -p "$MRI"/{skills,commands,hooks,templates,dev,docs,scripts} \
         "$TARGET/.claude/skills" "$TARGET/.claude/commands" "$TARGET/.claude/hooks" \
         "$TARGET/.agents/skills"

# 1) Sources du module → .mri_devtools/
cp -r "$SRC"/.claude/skills/mri-* "$MRI/skills/"
cp "$SRC"/.claude/commands/mri-*.md "$MRI/commands/"
cp "$SRC"/.claude/hooks/"*.sh" "$MRI/hooks/" 2>/dev/null || cp "$SRC"/.claude/hooks/*.sh "$MRI/hooks/"
cp "$SRC"/.toolbox/constitution.md "$SRC"/.toolbox/models.md "$MRI/"
cp -r "$SRC"/.toolbox/templates/python-uv "$MRI/templates/"
cp "$SRC"/.toolbox/dev/MERGE_DESIGN.md "$SRC"/.toolbox/dev/DECISIONS.md "$SRC"/.toolbox/dev/BUILD_PLAN.md "$MRI/dev/" 2>/dev/null || true
cp "$SRC"/.toolbox/scripts/install.sh "$MRI/scripts/"

# 2) Réécriture des chemins .toolbox/ → .mri_devtools/ dans le contenu copié
grep -rlZ '\.toolbox/' "$MRI" 2>/dev/null | xargs -0 -r sed -i 's#\.toolbox/#.mri_devtools/#g' || true

# 3) Fichiers racine
cp "$SRC"/AGENTS.md "$SRC"/CLAUDE.md "$SRC"/.mcp.json "$TARGET/"
sed -i 's#\.toolbox/#.mri_devtools/#g' "$TARGET/AGENTS.md" "$TARGET/CLAUDE.md"

# 4) settings.json propre (permissions + hooks ; pas de plugin externe)
cat > "$TARGET/.claude/settings.json" <<'JSON'
{
  "permissions": {
    "allow": [
      "Bash(git status:*)","Bash(git diff:*)","Bash(git add:*)","Bash(git commit:*)",
      "Bash(git log:*)","Bash(git branch:*)","Bash(git checkout:*)","Bash(git switch:*)",
      "Bash(uv:*)","Bash(ruff:*)","Bash(pytest:*)","Bash(python:*)","Bash(python3:*)",
      "Bash(pre-commit:*)","Bash(mkdir:*)","Bash(ls:*)","Bash(cat:*)","Bash(rg:*)"
    ],
    "deny": [
      "Bash(sudo:*)","Bash(rm -rf /:*)","Bash(rm -rf ~:*)",
      "Bash(git push --force:*)","Bash(git push -f:*)"
    ]
  },
  "hooks": {
    "SessionStart": [ { "hooks": [ { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/welcome.sh\"" } ] } ],
    "PostToolUse": [ { "matcher": "Write|Edit", "hooks": [ { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh\"" } ] } ],
    "Stop": [ { "hooks": [ { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/lint-test.sh\"" } ] } ]
  }
}
JSON

# 5) Câblage .claude/ (lien ou copie) + hooks (toujours copiés, référencés par chemin)
for d in "$MRI"/skills/mri-*; do n=$(basename "$d")
  if [ "$MODE" = copy ]; then cp -r "$d" "$TARGET/.claude/skills/$n"
  else ln -sfn "../../.mri_devtools/skills/$n" "$TARGET/.claude/skills/$n"; fi
done
for c in "$MRI"/commands/*.md; do n=$(basename "$c")
  if [ "$MODE" = copy ]; then cp "$c" "$TARGET/.claude/commands/$n"
  else ln -sfn "../../.mri_devtools/commands/$n" "$TARGET/.claude/commands/$n"; fi
done
cp "$MRI"/hooks/*.sh "$TARGET/.claude/hooks/"; chmod +x "$TARGET/.claude/hooks/"*.sh
# Miroir portable Codex
for d in "$MRI"/skills/mri-*; do n=$(basename "$d"); ln -sfn "../../.mri_devtools/skills/$n" "$TARGET/.agents/skills/$n"; done

echo "==> OK. Ouvre un agent dans $TARGET (message d'accueil → /mri-brainstorm)."
[ "$MODE" = link ] && echo "    (Si Claude ne découvre pas les skills/commandes symlinkées, relance avec --copy.)"
