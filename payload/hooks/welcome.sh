#!/usr/bin/env bash
# SessionStart: welcome message (the only automation of command-driven mode).
# Suggests resuming (/mri-code-resume) if a progress.md has unfinished steps, otherwise starting a new
# idea (/mri-code-brainstorm). The agent replies to the user in the configured language (see AGENTS.md);
# this scaffold message is neutral English.
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

# Detect work in progress: a progress.md with at least one "- [ ]" (todo) or "- [~]" (in progress) step.
inprogress=$(grep -l '^- \[[ ~]\]' .mri_code/docs/*/progress.md 2>/dev/null | head -1 || true)
if [ -n "$inprogress" ]; then
  feat=$(basename "$(dirname "$inprogress")")
  resume="Work in progress detected: ${feat}. To resume → /mri-code-resume"
else
  resume="No work in progress → to start an idea: /mri-code-brainstorm"
fi

msg=" ███╗   ███╗██████╗ ██╗        ██████╗ ██████╗ ██████╗ ███████╗
 ████╗ ████║██╔══██╗██║       ██╔════╝██╔═══██╗██╔══██╗██╔════╝
 ██╔████╔██║██████╔╝██║ █████ ██║     ██║   ██║██║  ██║█████╗
 ██║╚██╔╝██║██╔══██╗██║ ╚═══╝ ██║     ██║   ██║██║  ██║██╔══╝
 ██║ ╚═╝ ██║██║  ██║██║       ╚██████╗╚██████╔╝██████╔╝███████╗
 ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝        ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
                        idea → shipped

Command-driven mode (I wait for your commands, I auto-trigger nothing).
Flow: /mri-code-brainstorm → /mri-code-forge → /mri-code-design → /mri-code-devplan → /mri-code-scaffold-python → /mri-code-implement → /mri-code-review → /mri-code-finish
Optional: /mri-code-elicit · /mri-code-adversarial-review · /mri-code-market-research · /mri-code-domain-research · /mri-code-technical-research · /mri-code-document-project · /mri-code-debug · /mri-code-meta-prompt · /mri-code-resume
${resume}"

# Portable JSON-string encoder: jq if available, else python3, else a pure-bash fallback
# (the message contains no " or \, so escaping backslash/quote/newline is sufficient).
esc() {
  if command -v jq >/dev/null 2>&1; then
    jq -Rs .
  elif command -v python3 >/dev/null 2>&1; then
    python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))'
  else
    local s; s=$(cat)
    s=${s//\\/\\\\}; s=${s//\"/\\\"}; s=${s//$'\n'/\\n}
    printf '"%s"' "$s"
  fi
}
ctx=$(printf '%s' "$msg" | esc)
printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":%s}}\n' "$ctx"
exit 0
