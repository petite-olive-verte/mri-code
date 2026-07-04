#!/usr/bin/env bash
# Install the mri-code module into a target project (COPY — no symlink).
#   ./install.sh [target] [--lang <lang>] [--doc-lang <lang>] [--user <name>]
#   default target: current directory. Missing values are prompted (interactive) or defaulted (English).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
command -v node >/dev/null 2>&1 || { echo "Node.js required (https://nodejs.org)."; exit 1; }
exec node "$here/bin/install.mjs" "$@"
