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
cp "$source_root/docs/_data/releases.yml" "$source_root/docs/_data/xoa_releases.yml" "$source_root/site/data/"
python3 "$source_root/site/scripts/check_translation_parity.py"
python3 "$source_root/site/scripts/check_xoa_manual.py"
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
