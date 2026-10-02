#!/usr/bin/env bash
# PR check (xcp-hl#148, jenkins-infra docs/dev-checks.md): repo files, release data, spec and key consistency.
# Local: run from a clean checkout with python3, python3-yaml, rpm (rpmspec) and shellcheck.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> shellcheck"
shellcheck ci/*.sh

echo "==> .repo files: the section contract and the security settings"
python3 - <<'PY'
import configparser, sys
# Section names are read by XCP-ng's updater.py through xoa-hl's patch: renaming one hides its updates.
SECTIONS = ['xcp-hl-base', 'xcp-hl-xolite', 'xcp-hl-xoa-proxy']
WANT = {'enabled': '1', 'gpgcheck': '0', 'repo_gpgcheck': '1', 'skip_if_unavailable': 'True'}
def load(path):
    c = configparser.ConfigParser(interpolation=None)
    c.read(path)
    return c
packaged, bootstrap = load('SOURCES/xcp-hl.repo'), load('pages/xcp-hl.repo')
bad = []
for name, c in (('SOURCES/xcp-hl.repo', packaged), ('pages/xcp-hl.repo', bootstrap)):
    if c.sections() != SECTIONS:
        bad.append(f'{name}: sections {c.sections()}, want {SECTIONS}')
        continue
    for s in SECTIONS:
        for k, v in WANT.items():
            if c[s].get(k) != v:
                bad.append(f'{name} [{s}] {k}={c[s].get(k)}, want {v}')
        if not c[s].get('baseurl', '').startswith('https://'):
            bad.append(f'{name} [{s}] baseurl is not https')
# The bootstrap copy differs from the packaged one only by gpgkey (pages/xcp-hl.repo header).
for s in SECTIONS:
    if s in packaged and s in bootstrap:
        a = {k: v for k, v in packaged[s].items() if k != 'gpgkey'}
        b = {k: v for k, v in bootstrap[s].items() if k != 'gpgkey'}
        if a != b:
            bad.append(f'[{s}] packaged and bootstrap copies differ beyond gpgkey')
print('\n'.join(bad) or 'ok')
sys.exit(1 if bad else 0)
PY

echo "==> release data (docs/_data, written by the release agents) parses, one entry per tag"
python3 - <<'PY'
import re, sys, yaml
bad = []
for path, key, pattern in (('docs/_data/releases.yml', 'iso_version', r'^v\d+\.\d+-ce\d+$'),
                           ('docs/_data/xoa_releases.yml', 'image_tag', r'^xoa-image-\d{8}-[0-9a-f]{7,}$')):
    entries = yaml.safe_load(open(path)) or []
    tags = [e.get(key) for e in entries]
    bad += [f'{path}: bad {key} {t!r}' for t in tags if not re.match(pattern, str(t))]
    bad += [f'{path}: {key} {t} listed twice' for t in sorted({t for t in tags if tags.count(t) > 1})]
    bad += [f'{path}: {e.get(key)} has no build_date' for e in entries if not e.get('build_date')]
print('\n'.join(bad) or 'ok')
sys.exit(1 if bad else 0)
PY

echo "==> spec parses with the macros CI defines"
rpmspec -P --define "_version 0.0.0" --define "_release 1" --define "_shortcommit 0000000" \
  SPECS/xcp-hl-release.spec > /dev/null

echo "==> the packaged signing key is the published one"
cmp SOURCES/RPM-GPG-KEY-xcp-ng-ce xcp-ng-ce-public.asc

echo "ci/check.sh passed"
