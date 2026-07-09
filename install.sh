#!/usr/bin/env bash
# Install the mri-code module into a target project (COPY — no symlink).
#   ./install.sh [target] [--lang <lang>] [--doc-lang <lang>] [--user <name>]
#   default target: current directory. Missing values are prompted (interactive) or defaulted (English).
# See also: ./update.sh (update in place), ./uninstall.sh (remove).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required (https://www.python.org)."; exit 1; }
PYTHONPATH="$here${PYTHONPATH:+:$PYTHONPATH}" exec python3 -m mri_code_installer.main "$@"
