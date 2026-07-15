#!/usr/bin/env bash
# PostToolUse(Write|Edit): auto-format + lint-fix of the edited file.
# Non-blocking. Dispatches on the project type: Python (pyproject.toml) or
# Symfony/PHP (composer.json). Does nothing until one of them exists.
# Edit/remove freely (it's your project).
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

f=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null || true)
[ -n "$f" ] || exit 0

case "$f" in
  *.py)
    [ -f pyproject.toml ] || exit 0
    command -v uv >/dev/null 2>&1 || exit 0
    uv run ruff check --fix "$f" >/dev/null 2>&1 || true
    uv run ruff format "$f" >/dev/null 2>&1 || true
    ;;
  *.php)
    [ -f composer.json ] || exit 0
    [ -x vendor/bin/php-cs-fixer ] || exit 0
    vendor/bin/php-cs-fixer fix "$f" >/dev/null 2>&1 || true
    ;;
esac
exit 0
