#!/usr/bin/env bash
# Stop : boucle de feedback — lance lint + tests et affiche un résumé (PASS/FAIL).
# Non-bloquant (exit 0). Silencieux tant qu'aucun projet Python (pyproject.toml) n'existe.
# Si trop bruyant à ton goût, retire la section "Stop" de .claude/settings.json.
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
[ -f pyproject.toml ] || exit 0
command -v uv >/dev/null 2>&1 || exit 0

ruff_log=$(mktemp); test_log=$(mktemp)
ruff_rc=0; test_rc=0
uv run ruff check . >"$ruff_log" 2>&1 || ruff_rc=$?
uv run pytest -q >"$test_log" 2>&1 || test_rc=$?

echo "── Feedback toolbox (lint + tests) ──"
if [ "$ruff_rc" -eq 0 ]; then echo "ruff   : OK"; else echo "ruff   : ÉCHEC"; tail -15 "$ruff_log"; fi
if [ "$test_rc" -eq 0 ]; then echo "pytest : OK"; else echo "pytest : ÉCHEC"; tail -20 "$test_log"; fi

rm -f "$ruff_log" "$test_log"
exit 0
