#!/usr/bin/env bash
# Uninstall the mri-code module from a target project. Never touches .mri_code/docs/
# (documents produced by the agent while working — always preserved).
#   ./uninstall.sh [target] [--yes]
#   default target: current directory. Prompts for confirmation unless --yes/-y is given.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required (https://www.python.org)."; exit 1; }
PYTHONPATH="$here${PYTHONPATH:+:$PYTHONPATH}" exec python3 -m mri_code_installer.main uninstall "$@"
