#!/usr/bin/env bash
# Build/validate an HTTP-served documentation bundle. Product RPM/ISO builds stay in CI.
set -euo pipefail
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 BASE_URL OUTPUT_DIRECTORY" >&2
  exit 2
fi
base_url="$1"
output_dir="$(realpath -m "$2")"
case "$base_url" in
  http://*/|https://*/) ;;
  *) echo 'BASE_URL must be an http(s) URL ending in /' >&2; exit 2 ;;
esac
if [ -e "$output_dir" ]; then
  echo "Output already exists: $output_dir (choose a new directory)" >&2
  exit 2
fi
source_root="$(cd "$(dirname "$0")/../.." && pwd)"
build_tmp="$(mktemp -d)"
trap 'rm -rf "$build_tmp"' EXIT
mkdir -p "$source_root/site/data"
# Keep the release publisher contract at docs/_data/. Do not relocate these files.
# Publishers write release rows to main (#265); RELEASE_DATA_REF=local uses this checkout.
release_ref="${RELEASE_DATA_REF:-main}"
for data_file in releases.yml xoa_releases.yml; do
  if [ "$release_ref" != local ] && curl -fsSL --retry 3 -o "$build_tmp/$data_file" \
      "https://raw.githubusercontent.com/Vagrantin/xcp-hl/$release_ref/docs/_data/$data_file"; then
    cp "$build_tmp/$data_file" "$source_root/site/data/$data_file"
    echo "Release data: $data_file from xcp-hl@$release_ref"
  else
    [ "$release_ref" = local ] || echo "WARNING: could not fetch $data_file from $release_ref; using this checkout" >&2
    cp "$source_root/docs/_data/$data_file" "$source_root/site/data/$data_file"
  fi
done
# Changelog data is published on main by the release agents. Until the first
# publisher lands, the checked-in empty list renders only the curated archive.
if [ "$release_ref" != local ] && curl -fsSL --retry 3 -o "$build_tmp/changelog.json" \
    "https://raw.githubusercontent.com/Vagrantin/xcp-hl/$release_ref/docs/_data/changelog.json"; then
  cp "$build_tmp/changelog.json" "$source_root/site/data/changelog.json"
  echo "Release data: changelog.json from xcp-hl@$release_ref"
else
  [ "$release_ref" = local ] || echo "WARNING: could not fetch changelog.json from $release_ref; using this checkout" >&2
  cp "$source_root/docs/_data/changelog.json" "$source_root/site/data/changelog.json"
fi
python3 "$source_root/site/scripts/check_changelog.py" "$source_root/site/data/changelog.json"
# Current ISO is GitHub's "Latest" release, which never is a pre-release candidate (#265).
rm -f "$source_root/site/data/latest_release.yml"
latest_tag="$(curl -fsSL --retry 3 ${GITHUB_TOKEN:+-H "Authorization: Bearer $GITHUB_TOKEN"} \
  https://api.github.com/repos/Vagrantin/xcp-ng-ce-iso/releases/latest 2>/dev/null \
  | python3 -c 'import json, sys; print(json.load(sys.stdin)["tag_name"])' 2>/dev/null || true)"
if [[ "$latest_tag" =~ ^v[0-9]+\.[0-9]+-ce[0-9]+$ ]]; then
  printf 'iso_version: "%s"\n' "$latest_tag" > "$source_root/site/data/latest_release.yml"
  echo "Latest stable ISO: $latest_tag"
else
  echo "WARNING: GitHub latest ISO release unavailable; showing the newest release-matrix row" >&2
fi
python3 "$source_root/site/scripts/check_translation_parity.py"
manual_flags=()
case "${XOA_PUBLICATION_MODE:-preview}" in
  preview) ;;
  reviewed) manual_flags+=(--require-reviewed) ;;
  *) echo 'XOA_PUBLICATION_MODE must be preview or reviewed' >&2; exit 2 ;;
esac
python3 "$source_root/site/scripts/check_xoa_manual.py" "${manual_flags[@]}" \
  --report "$source_root/site/data/xoa_manual_review_report.json"
# Production bundles must not contain intentionally untranslated preview stubs.
if grep -R -n -E '\{\{< *translation-pending' "$source_root/site/content"; then
  echo 'Untranslated page blocks the documentation bundle' >&2
  exit 1
fi
hugo --source "$source_root/site" --destination "$build_tmp/public" \
  --baseURL "$base_url" --gc --minify --printPathWarnings 2>&1 | tee "$build_tmp/hugo.log"
if grep -q 'Duplicate target paths' "$build_tmp/hugo.log"; then
  echo 'Duplicate URLs block the documentation bundle' >&2
  exit 1
fi
# The production assembler publishes this same public key at the site root.
# Include it before link validation so a docs-only bundle also has the target.
cp "$source_root/xcp-ng-ce-public.asc" "$build_tmp/public/xcp-ng-ce-public.asc"
python3 "$source_root/site/scripts/check_switcher.py" "$build_tmp/public"
python3 "$source_root/site/scripts/check_site.py" "$build_tmp/public"
python3 "$source_root/site/scripts/check_legacy_urls.py" "$build_tmp/public"
mkdir -p "$(dirname "$output_dir")"
mv "$build_tmp/public" "$output_dir"
printf 'Documentation built for %s in %s\n' "$base_url" "$output_dir"
