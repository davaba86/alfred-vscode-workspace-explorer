#!/usr/bin/env bash
# Computes next semver from Conventional Commits since the last tag, bumps
# src/info.plist's version, rebuilds the .alfredworkflow bundles, commits,
# tags, and creates a GitHub release. Run in CI only (needs push + gh auth).
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

last_tag="$(git describe --tags --abbrev=0 2>/dev/null || echo "")"
range="${last_tag:+${last_tag}..HEAD}"
commits="$(git log ${range:-} --pretty=format:'%s%n%b' --no-merges)"

if [ -z "$commits" ]; then
  echo "No commits since ${last_tag:-repo start}; nothing to release."
  exit 0
fi

bump="none"
if grep -Eq '^[a-zA-Z]+(\([^)]*\))?!:|BREAKING CHANGE:' <<<"$commits"; then
  bump="major"
elif grep -Eq '^feat(\([^)]*\))?:' <<<"$commits"; then
  bump="minor"
elif grep -Eq '^fix(\([^)]*\))?:' <<<"$commits"; then
  bump="patch"
fi

if [ "$bump" = "none" ]; then
  echo "No feat/fix/breaking commits since ${last_tag:-repo start}; nothing to release."
  exit 0
fi

current="${last_tag#v}"
current="${current:-0.0.0}"
IFS='.' read -r major minor patch <<<"$current"

case "$bump" in
  major) major=$((major + 1)); minor=0; patch=0 ;;
  minor) minor=$((minor + 1)); patch=0 ;;
  patch) patch=$((patch + 1)) ;;
esac

new_version="${major}.${minor}.${patch}"
new_tag="v${new_version}"
echo "Bumping ${last_tag:-<none>} -> ${new_tag} (${bump})"

plutil -replace version -string "$new_version" src/info.plist

for bundle in "VSCode Workspace Explorer.alfredworkflow" "vs.alfredworkflow"; do
  rm -f "$bundle"
  (cd src && zip -r -X "../${bundle}" . -x '.DS_Store')
done

git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"
git add src/info.plist "VSCode Workspace Explorer.alfredworkflow" "vs.alfredworkflow"
git commit -m "chore(release): ${new_tag} [skip ci]"
git tag -a "$new_tag" -m "$new_tag"
git push origin HEAD:master
git push origin "$new_tag"

gh release create "$new_tag" \
  "VSCode Workspace Explorer.alfredworkflow" \
  "vs.alfredworkflow" \
  --title "$new_tag" \
  --notes "$(git log ${last_tag:+${last_tag}..}HEAD --pretty=format:'- %s' --no-merges)"
