#!/usr/bin/env python3
"""Check publication identities and rendered EN/FR/JA release matrices."""
import argparse
from datetime import date
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
data = ROOT / 'docs/_data'
iso = yaml.safe_load((data / 'releases.yml').read_text())
images = yaml.safe_load((data / 'xoa_releases.yml').read_text())
archive = json.loads((data / 'legacy_iso_releases.json').read_text())
proof = json.loads((data / 'release-provenance.json').read_text())
for rows, key in [(iso, 'iso_version'), (images, 'image_tag'), (archive, 'tag')]:
    tags = [r[key] for r in rows]
    assert len(tags) == len(set(tags)), f'duplicate {key}'
    for row in rows:
        date.fromisoformat(row['build_date'])
assert not {r['iso_version'] for r in iso} & {r['tag'] for r in archive}
for row in iso:
    assert re.fullmatch(r'v\d+\.\d+-ce\d+', row['iso_version'])
    for key, component in row['components'].items():
        assert component.get('version'), (row, key)
        if component.get('rpm'):
            assert not component['rpm'].endswith('.rpm'), 'use rpm -q identity'
            assert component['rpm'].startswith({'xolite_ce':'xo-lite-ce-', 'xoa_proxy':'xoa-proxy-', 'xcp_hl_release':'xcp-hl-release-'}[key])
    p = proof['iso'].get(row['iso_version'])
    if p and p['status'] == 'recorded':
        rpm = row['components']['xcp_hl_release']['rpm'] + '.rpm'
        assert any('Adding pkg:' in line and line.endswith('/' + rpm) for line in p['evidence'])
for row in images:
    assert re.fullmatch(r'xoa-image-\d{8}-[a-f0-9]{7,}', row['image_tag'])
    assets = [row['asset']] if row.get('asset') else row.get('assets', [])
    assert assets and len(assets) == len(set(assets)), row
    assert all(re.fullmatch(r'[a-zA-Z0-9_.-]+\.xva(?:\.gz)?', a) for a in assets)
    assert bool(row.get('rpm')) == bool(row.get('rpm_tag')), row
    if row.get('rpm_tag'):
        m = re.fullmatch(r'v(.+)-ce(\d+)', row['rpm_tag'])
        assert m and row['rpm'].startswith(f'xoa-hl-{m[1]}-{m[2]}.')
    assert bool(row.get('upstream_url')) == bool(row.get('upstream_xo')), row
print(f'Validated {len(iso)} ISO rows, {len(archive)} legacy ISOs, {len(images)} images')

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href', '')
            assert href and not href.endswith(('/releases/tag/', '/releases/download/')), href
            self.links.append(href)

parser = argparse.ArgumentParser()
parser.add_argument('--site', type=Path)
args = parser.parse_args()
if args.site:
    for relative in ['release-matrix/index.html', 'fr/release-matrix.html', 'ja/release-matrix.html']:
        path = args.site / relative
        if not path.exists():
            path = path.with_suffix('') / 'index.html'
        html = path.read_text()
        parsed = Links()
        parsed.feed(html)
        for row in images:
            repo = row.get('repo', 'build-xoa-hl')
            for asset in ([row['asset']] if row.get('asset') else row['assets']):
                assert f'https://github.com/Vagrantin/{repo}/releases/download/{row["image_tag"]}/{asset}' in parsed.links
        for row in archive:
            assert f'https://github.com/Vagrantin/xcp-ng-ce-iso/releases/tag/{row["tag"]}' in parsed.links
        assert 'xcp-hl-release-0.0.5-5.g157727f.xcpng8.3.noarch' in html
    print('Rendered EN/FR/JA matrices: all image/legacy links present, no empty links')
