#!/usr/bin/env python3
"""Export numbered manual items for editorial screenshot review, without capture.

IDs are positional within a page, not permanent task IDs. Bind any later image
decision to pageRevision as well as itemRevision; insertions can renumber items.
Unnumbered instructions still need editorial review. This is not a Markdown
renderer, a screenshot approval, or functional appliance evidence.
"""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess

from check_xoa_manual import SITE, read_page


def digest(text):
    normalized = '\n'.join(line.rstrip() for line in text.splitlines()).strip()
    return 'sha256:' + hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def numbered_items(text):
    """Locate ordered items outside YAML, fenced code and HTML comments.

    Include nested items, recording their indentation. A page-wide ordinal
    disambiguates list restarts, duplicate headings and repeated marker numbers.
    Cues contain the marker line; pageRevision covers continuation paragraphs.
    """
    lines = text.replace('\r\n', '\n').splitlines()
    start = 0
    if lines and lines[0] == '---':
        start = lines.index('---', 1) + 1
    headings = []
    fence = None
    comment = False
    items = []
    for index in range(start, len(lines)):
        raw = lines[index]
        if fence:
            if re.fullmatch(re.escape(fence[0]) + '{' + str(fence[1]) + r',}\s*', raw.lstrip()):
                fence = None
            continue
        # Comments can contain Markdown examples; they are not reader steps.
        visible = ''
        rest = raw
        while rest:
            if comment:
                before, found, rest = rest.partition('-->')
                if not found:
                    break
                comment = False
            else:
                before, found, rest = rest.partition('<!--')
                visible += before
                if not found:
                    break
                comment = True
        stripped = visible.lstrip()
        match = re.match(r'^(`{3,}|~{3,})(.*)$', stripped)
        if match:
            fence = (match[1][0], len(match[1]))
            continue
        heading = re.match(r'^(#{1,6})\s+(.+?)\s*#*$', visible)
        if heading:
            level = len(heading[1])
            headings = [entry for entry in headings if entry[0] < level]
            headings.append((level, heading[2]))
        item = re.match(r'^( *)(\d+)[.)]\s+(\S.*)$', visible)
        if item:
            items.append({
                'ordinal': len(items) + 1,
                'sourceLine': index + 1,
                'headingPath': [title for _, title in headings],
                'indent': len(item[1]),
                'marker': int(item[2]),
                'cue': item[3],
                'itemRevision': digest(visible.strip()),
            })
    if fence or comment:
        raise ValueError('unclosed code fence or HTML comment')
    return items


def inventory(site, source_commit):
    root = site / 'content/en/docs/xoa-hl'
    pages = []
    keys = set()
    for path in sorted(root.rglob('*.md')):
        meta, body = read_page(path)
        key = meta.get('translationKey')
        if not key or key in keys:
            raise ValueError(f'{path}: missing/duplicate translationKey')
        keys.add(key)
        items = numbered_items(path.read_text(encoding='utf-8'))
        for item in items:
            item['id'] = f'{key}/item-{item["ordinal"]:03d}'
            item['disposition'] = 'pending-editorial-review'
        pages.append({
            'sourcePath': path.relative_to(site.parent).as_posix(),
            'translationKey': key,
            'title': meta['title'],
            'pageRevision': digest(body),
            'localePaths': {lang: path.relative_to(site.parent).as_posix().replace('/en/', f'/{lang}/', 1)
                            for lang in ('fr', 'ja')},
            'items': items,
        })
    if not pages:
        raise ValueError(f'{root}: no manual pages')
    return {
        'schemaVersion': 1,
        'sourceCommit': source_commit,
        'scope': 'Numbered Markdown items; unnumbered instructions require separate editorial review.',
        'evidence': 'Source inventory only; no image approval or appliance test result.',
        'pageCount': len(pages),
        'pagesWithNumberedItems': sum(bool(p['items']) for p in pages),
        'itemCount': sum(len(p['items']) for p in pages),
        'pages': pages,
    }


def markdown(report):
    def cell(value):
        return str(value).replace('|', r'\|').replace('\n', ' ')

    lines = ['# XOA-HL numbered-item review inventory', '',
             f'Source commit: `{report["sourceCommit"]}`.', '',
             f'{report["pageCount"]} pages; {report["pagesWithNumberedItems"]} with numbered items; '
             f'{report["itemCount"]} items.', '', report['scope'], '', report['evidence'], '',
             'IDs are positional within each page. Match pageRevision and itemRevision in the JSON '
             'before reusing a decision from another revision. All entries await editorial review; '
             'a prepared Jenkins request does not approve a screenshot.', '',
             '| Source | Numbered items |', '| --- | --- |']
    for page in report['pages']:
        lines.append(f'| `{page["sourcePath"]}` | {len(page["items"])} |')
    for page in report['pages']:
        if not page['items']:
            continue
        lines += ['', f'## {page["title"]}', '', f'Source: `{page["sourcePath"]}`.', '',
                  '| Item ID | Source line | Heading path | Cue | Disposition |',
                  '| --- | --- | --- | --- | --- |']
        for item in page['items']:
            lines.append('| ' + ' | '.join(cell(value) for value in (
                item['id'], item['sourceLine'], ' / '.join(item['headingPath']),
                item['cue'], item['disposition'])) + ' |')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    parser.add_argument('--markdown', type=pathlib.Path)
    args = parser.parse_args()
    source_commit = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=SITE.parent, text=True).strip()
    report = inventory(SITE, source_commit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(markdown(report), encoding='utf-8')
    print(f'Inventoried {report["itemCount"]} numbered items across '
          f'{report["pagesWithNumberedItems"]} of {report["pageCount"]} manual pages; '
          'no capture or approval performed.')


if __name__ == '__main__':
    main()
