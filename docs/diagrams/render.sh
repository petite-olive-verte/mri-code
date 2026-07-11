#!/usr/bin/env bash
# Regenerate the diagram SVGs from the .d2 sources.
#
# Requires: d2 (https://d2lang.com). Outputs (committed): pipeline.svg, skills-map.svg
# pipeline.svg uses animated arrows: they flow when the file is opened on its own in a
# browser. GitHub sanitises SVG animation, so it renders there as a static sketch.
set -euo pipefail
cd "$(dirname "$0")"

THEME="${D2_THEME:-4}"   # 4 = Cool Classics; override with D2_THEME=<id>

echo "→ pipeline.svg (animated, sketch)"
d2 --sketch --theme="$THEME" --pad=20 pipeline.d2 pipeline.svg

echo "→ skills-map.svg (sketch)"
d2 --sketch --theme="$THEME" --pad=30 skills-map.d2 skills-map.svg

echo "✓ done"
