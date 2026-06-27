#!/usr/bin/env bash
# Setup unique du template : récupère Superpowers (submodule) et l'active comme plugin Claude Code.
# Idempotent — peut être relancé sans risque.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> 1/2 Initialisation du submodule Superpowers…"
git submodule update --init --recursive

if command -v claude >/dev/null 2>&1; then
  echo "==> 2/2 Marketplace local + installation du plugin Superpowers (scope projet)…"
  claude plugin marketplace add ./superpowers || true
  claude plugin install superpowers@superpowers-dev --scope project || true
  echo
  echo "OK. Ouvre Claude Code dans ce dossier et décris ton idée — le brainstorm démarrera."
  echo "Si les skills 'superpowers:*' n'apparaissent pas, lance /reload-plugins."
else
  echo "!! CLI 'claude' introuvable."
  echo "   Alternative sans installation (open-and-go) :"
  echo "     claude --plugin-dir ./superpowers"
fi
