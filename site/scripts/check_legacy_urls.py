#!/usr/bin/env python3
"""Check every migrated Jekyll page path and explicit legacy heading anchor.

The Jekyll source tree was retired on 2026-11-11 (owner decision, see
site/CUTOVER.md). The legacy URL inventory is frozen in
site/assets/legacy-urls.json, recorded from the retired docs/ source at
xcp-hl fd949ed. Compare that inventory with actual output, rather than merely
validating aliases that happen to be declared.
"""
import json
import pathlib
import sys
from urllib.parse import urlsplit, unquote
from check_site import Page

root = pathlib.Path(sys.argv[1])
site = pathlib.Path(__file__).resolve().parents[1]
home = Page((root / 'index.html').read_text())
prefix = urlsplit(home.canonical).path
errors, count, anchors = [], 0, 0
inventory = json.loads((site / 'assets/legacy-urls.json').read_text())
for source in inventory:
    rel, url = source['path'], source['url']
    path = url.lstrip('/')
    if not path or path.endswith('/'):
        path += 'index.html'
    target = root / path
    if not target.is_file():
        errors.append(f'{rel}: missing legacy path {url}')
        continue
    count += 1
    page = Page(target.read_text())
    if page.redirect:
        u = urlsplit(page.redirect).path
        dest = unquote(u[len(prefix):]) if u.startswith(prefix) else u.lstrip('/')
        target = root / (dest + 'index.html' if dest.endswith('/') else dest)
        if not target.is_file():
            errors.append(f'{rel}: broken alias {page.redirect}')
            continue
        page = Page(target.read_text())
    for anchor in source['anchors']:
        anchors += 1
        if anchor not in page.ids:
            errors.append(f'{rel}: legacy anchor #{anchor} missing')
mapping = json.loads((site / 'assets/legacy-home.json').read_text())
for lang, entries in mapping.items():
    home_path = root / ('' if lang == 'en' else lang) / 'index.html'
    page = Page(home_path.read_text())
    for entry in entries:
        anchors += 1
        if entry['old'] not in page.ids:
            errors.append(f'{lang}: old homepage fragment #{entry["old"]} missing')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f'PASS: {count} legacy page paths and {anchors} legacy heading/homepage anchors')
