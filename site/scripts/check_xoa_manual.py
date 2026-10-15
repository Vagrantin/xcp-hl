#!/usr/bin/env python3
"""Validate the XOA-HL manual and generate its locale status data.

sourceRevision is a digest of the English body plus its declared English glossary
terms, not a Git HEAD: metadata edits and unrelated commits do not invalidate it.
Preview allows draft translations. Reviewed claims require matching human
records; --require-reviewed gates publication of every FR/JA manual page.
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import re
import sys

SITE = pathlib.Path(__file__).resolve().parent.parent
REQUIRED = ('_index.md', 'glossary.md', 'translation-status.md',
            'first-login.md', 'create-vm.md', 'backup-restore.md',
            'maintenance.md', 'configuration-backup.md', 'troubleshooting.md',
            'vm-operations.md', 'storage-networks.md', 'vm-transfer.md', 'hosts-pools.md', 'permissions.md', 'sign-in-otp.md',
            'templates.md', 'concepts.md', 'configuration.md', 'automation.md')
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


def translation_revision(body, term_ids, glossary, lang):
    """Bind human review to the translated body and localized declared terms."""
    localized = {key: {'en': term[lang]} for key, term in glossary.items()}
    return source_revision(body, term_ids, localized)


def review_problem(record, source, translation):
    if not isinstance(record, dict):
        return 'missing human review record'
    for field in ('technicalReviewer', 'languageReviewer'):
        if not isinstance(record.get(field), str) or not record[field].strip():
            return f'missing {field}'
    date = record.get('reviewedAt')
    if not isinstance(date, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
        return 'reviewedAt must be an ISO date (YYYY-MM-DD)'
    try:
        datetime.date.fromisoformat(date)
    except (TypeError, ValueError):
        return 'reviewedAt must be an ISO date (YYYY-MM-DD)'
    if not re.fullmatch(r'https://github\.com/[^/\s]+/[^/\s]+/(pull|issues)/[0-9]+(?:#[^\s]+)?',
                        record.get('reviewUrl', '') if isinstance(record.get('reviewUrl'), str) else ''):
        return 'reviewUrl must identify a GitHub PR or issue review'
    if record.get('sourceRevision') != source:
        return 'review record is for a different English source revision'
    if record.get('translationRevision') != translation:
        return 'review record is for a different translated body/glossary revision'
    return None


def inspect(site, require_reviewed=False):
    """Collect every freshness/review problem; structural errors remain fatal."""
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
    problems = []
    manifest = json.loads((site / 'data/xoa_manual_reviews.json').read_text())
    if not isinstance(manifest, dict) or type(manifest.get('schemaVersion')) is not int or manifest['schemaVersion'] != 1 or not isinstance(manifest.get('reviews'), dict):
        raise ValueError('xoa_manual_reviews.json: expected schemaVersion 1 and reviews object')
    reviews = manifest['reviews']
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
            other, translated_body = read_page(site / 'content' / lang / 'docs/xoa-hl' / rel)
            if other.get('translationKey') != key or other.get('glossaryTerms') != meta.get('glossaryTerms'):
                raise ValueError(f'{lang}/{rel}: translation identity/terms differ')
            declared = other.get('translationStatus')
            valid = ('source',) if lang == 'en' else ('draft', 'reviewed')
            if declared not in valid:
                raise ValueError(f'{lang}/{rel}: invalid translationStatus')
            status = declared if other.get('sourceRevision') == revision else 'stale'
            translated_revision = translation_revision(translated_body, term_ids, glossary, lang)
            reason = 'stale English source revision' if status == 'stale' else None
            if lang != 'en' and declared == 'reviewed':
                locale_reviews = reviews.get(key, {})
                if not isinstance(locale_reviews, dict):
                    raise ValueError(f'{key}: review locales must be an object')
                invalid_review = review_problem(locale_reviews.get(lang), revision, translated_revision)
                if invalid_review:
                    reason = reason or invalid_review
                    if status != 'stale':
                        status = 'stale' if locale_reviews.get(lang) else 'draft'
            if require_reviewed and lang != 'en' and status != 'reviewed':
                reason = reason or f'{status}; human technical/language review required'
            row = {'title': other['title'], 'path': route, 'status': status,
                   'translationKey': key, 'sourceRevision': revision,
                   'translationRevision': translated_revision}
            result[lang].append(row)
            if reason:
                problems.append({'locale': lang, 'page': rel.as_posix(), 'reason': reason,
                                 'expectedSourceRevision': revision,
                                 'expectedTranslationRevision': translated_revision})
    for key, locales in reviews.items():
        if key not in keys or not isinstance(locales, dict) or any(lang not in ('fr', 'ja') for lang in locales):
            raise ValueError(f'{key}: unknown review page/locale')
    return result, problems


def collect(site, require_reviewed=False):
    result, problems = inspect(site, require_reviewed)
    if problems:
        raise ValueError('\n'.join(f"{p['locale']}/{p['page']}: {p['reason']}; expected sourceRevision: {p['expectedSourceRevision']}" for p in problems))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=pathlib.Path, default=SITE)
    parser.add_argument('--require-reviewed', action='store_true')
    parser.add_argument('--report', type=pathlib.Path, help='Write the full machine-readable review queue, including failures')
    args = parser.parse_args()
    try:
        result, problems = inspect(args.site, args.require_reviewed)
    except (ValueError, KeyError, OSError) as error:
        (args.site / 'data/xoa_manual_status.json').unlink(missing_ok=True)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps({'schemaVersion': 1, 'fatalError': str(error)}, ensure_ascii=False, indent=2) + '\n')
        print(f'XOA-HL manual: {error}', file=sys.stderr)
        return 1
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        queue = [dict(locale=lang, **row) for lang in ('fr', 'ja') for row in result[lang] if row['status'] != 'reviewed']
        args.report.write_text(json.dumps({'schemaVersion': 1, 'pages': result, 'reviewQueue': queue, 'problems': problems}, ensure_ascii=False, indent=2) + '\n')
    output = args.site / 'data/xoa_manual_status.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    if problems:
        for problem in problems:
            print(f"XOA-HL manual: {problem['locale']}/{problem['page']}: {problem['reason']}; expected sourceRevision: {problem['expectedSourceRevision']}", file=sys.stderr)
        print(f'{len(problems)} affected page/locale records; no review metadata was changed', file=sys.stderr)
        return 1
    drafts = sum(row['status'] == 'draft' for rows in result.values() for row in rows)
    print(f'PASS: XOA-HL required pages, glossary IDs and source revisions; {drafts} draft translations')
    return 0


if __name__ == '__main__':
    sys.exit(main())
