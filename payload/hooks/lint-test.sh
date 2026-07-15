#!/usr/bin/env bash
# Stop: feedback loop — runs lint + tests and prints a summary (PASS/FAIL).
# Non-blocking (exit 0). Silent until a project exists: Python (pyproject.toml)
# or Symfony/PHP (composer.json).
# If too noisy for your taste, remove the "Stop" section from .claude/settings.json.
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

# --- Python (uv + ruff + pytest) ---------------------------------------------
if [ -f pyproject.toml ] && command -v uv >/dev/null 2>&1; then
  ruff_log=$(mktemp); test_log=$(mktemp)
  ruff_rc=0; test_rc=0
  uv run ruff check . >"$ruff_log" 2>&1 || ruff_rc=$?
  uv run pytest -q >"$test_log" 2>&1 || test_rc=$?

  echo "── Toolbox feedback (lint + tests) ──"
  if [ "$ruff_rc" -eq 0 ]; then echo "ruff   : OK"; else echo "ruff   : FAILED"; tail -15 "$ruff_log"; fi
  if [ "$test_rc" -eq 0 ]; then echo "pytest : OK"; else echo "pytest : FAILED"; tail -20 "$test_log"; fi
  rm -f "$ruff_log" "$test_log"
fi

# --- Symfony / PHP (php-cs-fixer + phpstan + phpunit) -------------------------
if [ -f composer.json ] && [ -d vendor ]; then
  cs_log=$(mktemp); stan_log=$(mktemp); test_log=$(mktemp)
  cs_rc=0; stan_rc=0; test_rc=0
  [ -x vendor/bin/php-cs-fixer ] && { vendor/bin/php-cs-fixer fix --dry-run --diff >"$cs_log" 2>&1 || cs_rc=$?; }
  [ -x vendor/bin/phpstan ]      && { vendor/bin/phpstan analyse --no-progress >"$stan_log" 2>&1 || stan_rc=$?; }
  [ -x vendor/bin/phpunit ]      && { vendor/bin/phpunit >"$test_log" 2>&1 || test_rc=$?; }

  echo "── Toolbox feedback (lint + tests) ──"
  if [ "$cs_rc" -eq 0 ]; then echo "php-cs-fixer : OK"; else echo "php-cs-fixer : FAILED"; tail -15 "$cs_log"; fi
  if [ "$stan_rc" -eq 0 ]; then echo "phpstan      : OK"; else echo "phpstan      : FAILED"; tail -20 "$stan_log"; fi
  if [ "$test_rc" -eq 0 ]; then echo "phpunit      : OK"; else echo "phpunit      : FAILED"; tail -20 "$test_log"; fi
  rm -f "$cs_log" "$stan_log" "$test_log"
fi

exit 0
