#!/usr/bin/env bash
# Publish a vibe-check release: build, validate, commit, push, create the GitHub release for the
# version in SKILL.md, delete older releases, and update your own install.
# The release tag always comes from SKILL.md, so the version check in the skill (Step 0) and
# the GitHub release can never disagree.
#
# Usage:  ./scripts/release.sh            (from anywhere)
# Before: bump `version:` in skills/vibe-check/SKILL.md and add a "## vX.Y.Z (date)" entry to CHANGELOG.md.
set -euo pipefail
cd "$(dirname "$0")/.."

V=$(sed -n 's/^ *version: *"\([0-9][0-9.]*\)".*/\1/p' skills/vibe-check/SKILL.md | head -1)
[ -n "$V" ] || { echo "Couldn't read the version from skills/vibe-check/SKILL.md"; exit 1; }
grep -q "^## v$V " CHANGELOG.md || { echo "CHANGELOG.md has no '## v$V (date)' entry. Add one first."; exit 1; }
command -v gh >/dev/null || { echo "Install the GitHub CLI first: brew install gh"; exit 1; }
if gh release view "v$V" >/dev/null 2>&1; then
  echo "Release v$V already exists. Bump the version in SKILL.md (and CHANGELOG.md) first."; exit 1
fi

echo "== Releasing vibe-check v$V"
python3 scripts/build.py
python3 scripts/validate.py

# never ship a local skill install (npx skills add run inside this repo) or a report
git rm -r -q --cached --ignore-unmatch .agents .claude skills-lock.json .vibe-check >/dev/null 2>&1 || true
git add -A
if git diff --cached --quiet; then echo "(nothing new to commit)"; else git commit -q -m "v$V"; fi
git push -q

NOTES=$(awk -v v="## v$V " 'index($0, v) == 1 {f=1; next} /^## v/ {f=0} f' CHANGELOG.md)
gh release create "v$V" dist/vibe-check.zip --title "vibe-check v$V" --notes "$NOTES

---
**How to update:** run \`npx skills update -g\` (project installs such as Replit: \`npx skills update -p\`), then start a new session in your AI tool. vibe-check only runs on its latest version.
Claude app: download \`vibe-check.zip\` below and upload it again where you added the skill.
Other tools: copy the new file from \`adapters/\` (or \`dist/vibe-check.md\` for paste-in builders)."

# install the new version on this Mac first, so a network blip in the tidy-up below can't leave you on the old one
echo "== Installing v$V for Claude Code on this computer (global)"
npx -y skills add vikneshchandrasekaran21/Vibe-check -g -a claude-code -y >/dev/null || echo "!! Couldn't install here. Run: npx skills update -g"
INSTALLED=$(grep -m1 'version:' ~/.claude/skills/vibe-check/SKILL.md 2>/dev/null | sed 's/.*"\(.*\)".*/\1/')
if [ "$INSTALLED" = "$V" ]; then echo "== Installed: v$INSTALLED at ~/.claude/skills/vibe-check"; else echo "!! Installed copy is v${INSTALLED:-none}, expected v$V. Run: npx skills update -g"; fi

# keep only the newest release page, so "latest" is always this one. Tags stay: older installs read
# their checklists from their own version tag (SKILL.md Step 0a), so a tag must never be deleted.
# Optional tidy-up: a network error here must not fail the release.
set +e
OLD=$(gh release list --json tagName -q '.[].tagName' 2>/dev/null | grep -vx "v$V")
for tag in $OLD; do gh release delete "$tag" --yes >/dev/null 2>&1 || echo "(couldn't delete old release $tag; harmless, try again later)"; done
set -e

echo "== Done: v$V is on GitHub and installed here. Start a new session to use it."
