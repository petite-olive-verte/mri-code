#!/usr/bin/env bash
# PostToolUse(Write|Edit): auto-format + lint-fix of the edited Python file.
# Non-blocking. Does nothing until a Python project (pyproject.toml) exists.
# Edit/remove freely (it's your project).
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
[ -f pyproject.toml ] || exit 0
command -v uv >/dev/null 2>&1 || exit 0

f=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null || true)
case "$f" in
  *.py)
    uv run ruff check --fix "$f" >/dev/null 2>&1 || true
    uv run ruff format "$f" >/dev/null 2>&1 || true
    ;;
esac
exit 0
