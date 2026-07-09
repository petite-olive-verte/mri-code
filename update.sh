#!/usr/bin/env bash
# Update an already-installed mri-code module in a target project, in place (COPY — no symlink).
# Reuses the target's existing .mri_code/config.json (lang/doc-lang/user) unless overridden.
#   ./update.sh [target] [--lang <lang>] [--doc-lang <lang>] [--user <name>]
#   default target: current directory.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required (https://www.python.org)."; exit 1; }
PYTHONPATH="$here${PYTHONPATH:+:$PYTHONPATH}" exec python3 -m mri_code_installer.main update "$@"
