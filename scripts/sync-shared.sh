#!/usr/bin/env bash
# Copy the shared reference files into every skill that uses them, or check the copies match.
#   scripts/sync-shared.sh          copy shared/references/* into each skill below
#   scripts/sync-shared.sh --check  exit 1 if any copy is missing or differs (run before every commit)
#
# ground-rules.md goes to every skill in every plugin.
# theme-target.md goes to every skill that can change a theme, save files in a theme's folder or commit to a theme's
# repository. The page-studio sub-skills read ../page-studio/references/theme-target.md, so they need no copy.
set -euo pipefail
cd "$(dirname "$0")/.."

THEME_TARGET_SKILLS=(
  plugins/analytics/skills/analytics-setup
  plugins/analytics/skills/analytics-cleanup
  plugins/brand-capture/skills/brand-capture
  plugins/brand-voice/skills/voice-builder
  plugins/competitor-research/skills/competitor-research
  plugins/page-studio/skills/page-studio
  plugins/shopify-storefront/skills/campaign-launcher
  plugins/shopify-storefront/skills/campaign-page
  plugins/shopify-storefront/skills/theme-editor
  plugins/styles-builder/skills/styles-builder
  plugins/theme-audit/skills/theme-audit
)

mode="${1:-sync}"
fail=0

sync_one() { # <source> <skill dir>
  local src="$1" dest="$2/references/$(basename "$1")"
  if [[ "$mode" == "--check" ]]; then
    if ! cmp -s "$src" "$dest"; then echo "out of sync: $dest"; fail=1; fi
  else
    mkdir -p "$2/references"; cp "$src" "$dest"
  fi
}

for skill in plugins/*/skills/*/; do
  sync_one shared/references/ground-rules.md "${skill%/}"
done
for skill in "${THEME_TARGET_SKILLS[@]}"; do
  sync_one shared/references/theme-target.md "$skill"
done

# Every SKILL.md must carry the Ground rules block.
for f in plugins/*/skills/*/SKILL.md; do
  grep -q 'references/ground-rules.md' "$f" && grep -q '^## Ground rules' "$f" || { echo "no Ground rules block pointing to references/ground-rules.md: $f"; fail=1; }
done

if [[ "$mode" == "--check" ]]; then
  [[ $fail -eq 0 ]] && echo "shared references in sync" || exit 1
else
  echo "synced"; [[ $fail -eq 0 ]] || exit 1
fi
