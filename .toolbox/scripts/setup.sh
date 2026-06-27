#!/usr/bin/env bash
# Setup du template. Le marketplace local + l'activation du plugin Superpowers sont déjà
# déclarés dans .claude/settings.json (self-contained). Ce script ne fait que l'essentiel.
# Idempotent.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

echo "==> Initialisation du submodule Superpowers…"
git submodule update --init --recursive

cat <<'EOF'

OK. Ouvre Claude Code dans ce dossier :
  - au prompt de confiance du dossier, accepte l'installation du plugin Superpowers
    (marketplace local + plugin sont déclarés dans .claude/settings.json) ;
  - puis décris ton idée — le brainstorm démarrera.

Installation non-interactive (si pas de prompt) :
  claude plugin install superpowers@superpowers-dev --scope project
Si les skills 'superpowers:*' n'apparaissent pas : /reload-plugins
Alternative sans installation : claude --plugin-dir ./.toolbox/superpowers
EOF
