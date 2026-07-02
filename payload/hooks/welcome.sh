#!/usr/bin/env bash
# SessionStart: welcome message (the only automation of command-driven mode).
# Suggests resuming (/mri-resume) if a progress.md has unfinished steps, otherwise starting a new
# idea (/mri-brainstorm). The agent replies to the user in the configured language (see AGENTS.md);
# this scaffold message is neutral English.
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

# Detect work in progress: a progress.md with at least one "- [ ]" (todo) or "- [~]" (in progress) step.
inprogress=$(grep -l '^- \[[ ~]\]' .mri_devtools/docs/*/progress.md 2>/dev/null | head -1 || true)
if [ -n "$inprogress" ]; then
  feat=$(basename "$(dirname "$inprogress")")
  resume="Work in progress detected: ${feat}. To resume → /mri-resume"
else
  resume="No work in progress → to start an idea: /mri-brainstorm"
fi

msg=" ███╗   ███╗██████╗ ██╗
 ████╗ ████║██╔══██╗██║
 ██╔████╔██║██████╔╝██║
 ██║╚██╔╝██║██╔══██╗██║
 ██║ ╚═╝ ██║██║  ██║██║
 ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝
   devtools · idea → shipped

Command-driven mode (I wait for your commands, I auto-trigger nothing).
Flow: /mri-brainstorm → /mri-forge → /mri-design → /mri-devplan → /mri-scaffold-python → /mri-implement → /mri-review → /mri-finish
Optional: /mri-elicit · /mri-adversarial-review · /mri-market-research · /mri-domain-research · /mri-technical-research · /mri-document-project · /mri-debug · /mri-meta-prompt · /mri-resume
${resume}"

esc() { python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))'; }
ctx=$(printf '%s' "$msg" | esc)
printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' "$ctx"
exit 0
