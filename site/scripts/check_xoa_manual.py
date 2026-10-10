#!/usr/bin/env python3
"""Validate the XOA-HL manual and generate its locale status data.

sourceRevision is a digest of the English body plus its declared English glossary
terms, not a Git HEAD: metadata edits and unrelated commits do not invalidate it.
Preview allows draft translations; --require-reviewed is the publication gate.
"""
import argparse
import hashlib
import json
import pathlib
import re
import sys

SITE = pathlib.Path(__file__).resolve().parent.parent
REQUIRED = ('_index.md', 'glossary.md', 'translation-status.md')
LANGS = ('en', 'fr', 'ja')


def read_page(path):
    text = path.read_text(encoding='utf-8').replace('\r\n', '\n')
    match = re.match(r'---\n(.*?)\n---\n(.*)', text, re.S)
    if not match:
        raise ValueError(f'{path}: missing YAML front matter')
    metadata = {}
    for line in match[1].splitlines():
        item = re.match(r'^([A-Za-z][A-Za-z0-9]*):\s*(.*?)\s*$', line)
        if item:
            metadata[item[1]] = item[2].strip('"\'')
    return metadata, match[2]


def source_revision(body, term_ids, glossary):
    # Whitespace at line ends and outer blank lines is editorial, not meaning.
    normalized = '\n'.join(line.rstrip() for line in body.splitlines()).strip()
    terms = {key: glossary[key]['en'] for key in sorted(term_ids)}
    payload = normalized + '\n' + json.dumps(terms, ensure_ascii=False, sort_keys=True)
    return 'sha256:' + hashlib.sha256(payload.encode('utf-8')).hexdigest()


def collect(site, require_reviewed=False):
    glossary = json.loads((site / 'data/xoa_glossary.json').read_text())
    for key, term in glossary.items():
        for lang in LANGS:
            if not term.get(lang, {}).get('label') or not term.get(lang, {}).get('definition'):
                raise ValueError(f'glossary {key}: missing {lang} label/definition')
    root = site / 'content/en/docs/xoa-hl'
    pages = sorted(p.relative_to(root) for p in root.rglob('*.md'))
    for required in REQUIRED:
        if pathlib.Path(required) not in pages:
            raise ValueError(f'missing required XOA-HL page: {required}')
    result = {lang: [] for lang in LANGS}
    keys = set()
    for rel in pages:
        meta, body = read_page(root / rel)
        term_ids = json.loads(meta.get('glossaryTerms', '[]'))
        if not isinstance(term_ids, list) or any(not isinstance(k, str) or k not in glossary for k in term_ids):
            raise ValueError(f'{rel}: unknown controlled glossary term')
        revision = source_revision(body, term_ids, glossary)
        key = meta.get('translationKey')
        if not key or key in keys:
            raise ValueError(f'{rel}: missing/duplicate translationKey')
        keys.add(key)
        route = 'docs/xoa-hl/' + (str(rel.parent) + '/' if rel.name == '_index.md' and str(rel.parent) != '.' else '' if rel.name == '_index.md' else rel.with_suffix('').as_posix() + '/')
        for lang in LANGS:
            other, _ = read_page(site / 'content' / lang / 'docs/xoa-hl' / rel)
            if other.get('translationKey') != key or other.get('glossaryTerms') != meta.get('glossaryTerms'):
                raise ValueError(f'{lang}/{rel}: translation identity/terms differ')
            declared = other.get('translationStatus')
            valid = ('source',) if lang == 'en' else ('draft', 'reviewed')
            if declared not in valid:
                raise ValueError(f'{lang}/{rel}: invalid translationStatus')
            status = declared if other.get('sourceRevision') == revision else 'stale'
            if status == 'stale' or require_reviewed and lang != 'en' and status != 'reviewed':
                raise ValueError(f'{lang}/{rel}: {status}; expected sourceRevision: {revision}')
            result[lang].append({'title': other['title'], 'path': route, 'status': status})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=pathlib.Path, default=SITE)
    parser.add_argument('--require-reviewed', action='store_true')
    args = parser.parse_args()
    try:
        result = collect(args.site, args.require_reviewed)
    except (ValueError, KeyError, OSError) as error:
        print(f'XOA-HL manual: {error}', file=sys.stderr)
        return 1
    output = args.site / 'data/xoa_manual_status.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    drafts = sum(row['status'] == 'draft' for rows in result.values() for row in rows)
    print(f'PASS: XOA-HL required pages, glossary IDs and source revisions; {drafts} draft translations')
    return 0


if __name__ == '__main__':
    sys.exit(main())
