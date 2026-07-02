#!/usr/bin/env bash
# Installe le module « mri » dans un projet cible (fin wrapper de bin/install.mjs).
#   ./install.sh [cible] [--copy]     (défaut cible : dossier courant)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
command -v node >/dev/null 2>&1 || { echo "Node.js requis (https://nodejs.org) — sinon copie payload/ à la main."; exit 1; }
exec node "$here/bin/install.mjs" "$@"
