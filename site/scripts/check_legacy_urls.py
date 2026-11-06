#!/usr/bin/env python3
"""Check every migrated Jekyll page path and explicit legacy heading anchor.

The old source stays under docs/ through cutover acceptance. Compare it with
actual output, rather than merely validating aliases that happen to be declared.
"""
import json
import pathlib
import re
import sys
from urllib.parse import urlsplit, unquote
from check_site import Page

root = pathlib.Path(sys.argv[1])
legacy = pathlib.Path(__file__).resolve().parents[2] / 'docs'
home = Page((root / 'index.html').read_text())
prefix = urlsplit(home.canonical).path
errors, count, anchors = [], 0, 0
for source in legacy.rglob('*.md'):
    rel = source.relative_to(legacy)
    if any(p.startswith('_') for p in rel.parts) or rel.name == 'README.md':
        continue
    text = source.read_text()
    if not text.startswith('---\n'):
        continue
    front = text.split('---', 2)[1]
    permalink = re.search(r'^permalink:\s*[\'"]?([^\s\'"]+)', front, re.M)
    url = permalink[1] if permalink else '/' + (rel.as_posix().removesuffix('index.md') if rel.name == 'index.md' else str(rel.with_suffix('.html')))
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
    for anchor in re.findall(r'\{:\s*#([^\s}]+)', text):
        anchors += 1
        if anchor not in page.ids:
            errors.append(f'{rel}: legacy anchor #{anchor} missing')
mapping = json.loads((legacy.parent / 'site/assets/legacy-home.json').read_text())
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
