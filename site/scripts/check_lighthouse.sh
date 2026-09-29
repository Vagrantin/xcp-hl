#!/usr/bin/env bash
# Mobile lab checks for the landing page and onboarding guide in each language.
set -euo pipefail
base_url="${1:?Usage: check_lighthouse.sh BASE_URL}"
: "${LIGHTHOUSE_CLI:?Set LIGHTHOUSE_CLI to the pinned Lighthouse CLI entry point}"
mkdir -p browser-evidence
for lang in en fr ja; do
  prefix="${lang}/"
  if [ "$lang" = en ]; then prefix=''; fi
  for page in home start; do
    route="$prefix"
    if [ "$page" = start ]; then route="${prefix}docs/start/"; fi
    node "$LIGHTHOUSE_CLI" "${base_url%/}/${route}" \
      --chrome-flags='--headless --no-sandbox --disable-gpu' \
      --only-categories=performance,accessibility --output=json --quiet \
      --output-path="browser-evidence/lighthouse-${page}-${lang}.json"
  done
done
python3 - <<'PY'
import json
from pathlib import Path
failures = []
for lang in ('en', 'fr', 'ja'):
    for page in ('home', 'start'):
        name = f'{page}-{lang}'
        report = json.loads(Path(f'browser-evidence/lighthouse-{name}.json').read_text())
        for category in ('performance', 'accessibility'):
            score = report['categories'][category]['score']
            print(f'{name}: {category} = {score * 100 if score is not None else "unavailable"}')
            if score is None or score < .95:
                failures.append(f'{name}: {category} below 95')
if failures:
    raise SystemExit('\n'.join(failures))
PY
