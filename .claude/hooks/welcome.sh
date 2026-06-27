#!/usr/bin/env bash
# SessionStart : message d'accueil (le seul automatisme du mode command-driven).
# Liste les commandes et suggère de démarrer (/brainstorm) ou de reprendre (/implement)
# si un plan a des cases non cochées dans docs/specs/.
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

# Détecte un travail en cours : un fichier de docs/specs/ avec au moins une case "- [ ]".
inprogress=$(grep -rl '^- \[ \]' docs/specs 2>/dev/null | head -1 || true)
if [ -n "$inprogress" ]; then
  feat=$(basename "$(dirname "$inprogress")")
  resume="Travail en cours détecté : ${feat}. Pour reprendre → /implement"
else
  resume="Aucun travail en cours → pour démarrer une idée : /brainstorm"
fi

msg="👋 Toolbox prête — mode piloté par commandes (j'attends tes commandes, je n'auto-déclenche rien).
Commandes : /brainstorm · /plan · /scaffold · /implement · /review · /finish · /debug · /meta-prompt
${resume}"

esc() { python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))'; }
ctx=$(printf '%s' "$msg" | esc)
printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' "$ctx"
exit 0
