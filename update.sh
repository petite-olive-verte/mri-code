#!/usr/bin/env bash
# Update an already-installed mri-code module in a target project, in place (COPY — no symlink).
# Reuses the target's existing .mri_code/config.json (lang/doc-lang/user) unless overridden.
#   ./update.sh [target] [--lang <lang>] [--doc-lang <lang>] [--user <name>]
#   default target: current directory.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
command -v node >/dev/null 2>&1 || { echo "Node.js required (https://nodejs.org)."; exit 1; }
if [ -d "$here/.git" ]; then
  git -C "$here" pull --ff-only --quiet 2>/dev/null \
    || echo "warning: could not fast-forward $here (local changes or detached HEAD?) — using current checkout" >&2
fi
exec node "$here/bin/update.mjs" "$@"
