#!/usr/bin/env bash
# SessionStart : message d'accueil (le seul automatisme du mode command-driven).
# Suggère de reprendre (/mri-resume) si un progress.md a des étapes non terminées, sinon de démarrer
# une idée (/mri-brainstorm).
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

# Détecte un travail en cours : un progress.md avec au moins une étape "- [ ]" (à faire) ou "- [~]" (en cours).
inprogress=$(grep -l '^- \[[ ~]\]' .mri_devtools/docs/*/progress.md 2>/dev/null | head -1 || true)
if [ -n "$inprogress" ]; then
  feat=$(basename "$(dirname "$inprogress")")
  resume="Travail en cours détecté : ${feat}. Pour reprendre → /mri-resume"
else
  resume="Aucun travail en cours → pour démarrer une idée : /mri-brainstorm"
fi

msg="👋 Toolbox mri prête — mode piloté par commandes (j'attends tes commandes, je n'auto-déclenche rien).
Flux : /mri-brainstorm → /mri-forge → /mri-design → /mri-devplan → /mri-scaffold-python → /mri-implement → /mri-review → /mri-finish
Facultatifs : /mri-elicit · /mri-adversarial-review · /mri-market-research · /mri-domain-research · /mri-technical-research · /mri-document-project · /mri-debug · /mri-meta-prompt · /mri-resume
${resume}"

esc() { python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))'; }
ctx=$(printf '%s' "$msg" | esc)
printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' "$ctx"
exit 0
