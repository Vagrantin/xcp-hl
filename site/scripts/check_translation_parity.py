#!/usr/bin/env python3
"""Assert every translated page still has the same structure as its English one.

    python3 site/scripts/check_translation_parity.py

Runs on the sources, not a build. For each page under content/en/ it compares
the same page under content/fr/ and content/ja/ on the things that must hold
in any language: the headings, the shortcode calls, the code fences, the table
rows, the front-matter keys, and which pages the internal links point at.
Prose is invisible to it by design — it catches a translation that has fallen
behind a structural edit, not one that is merely worded differently.

Two things it deliberately does NOT compare, because they are *supposed* to
differ per language (see "Migrating a translation" in site/README.md):

  - explicit {#anchors}, and the #fragment of an internal link. A heading's
    slug comes from its translated text, so the French roadmap anchor really
    is `clés-gpg-une-clé-de-signature-par-module` and a French page linking to
    it must say so. Only the page part of each link is compared.
  - the text of anything.

This exists because the translations drifted three separate ways at once and
nothing noticed: the landing page was edited in English only, a whole
"Updating the XOA-hl appliance" section existed in English and in neither
translation, and the fr/ja xolite-ce pages still described a mechanism that
had been replaced. It also caught the reverse — an English page that had
silently lost five changelog entries in migration while both translations
kept them.

Exits non-zero, listing every difference, if anything is out of step.
"""
import collections
import pathlib
import re
import sys

CONTENT = pathlib.Path(__file__).resolve().parent.parent / 'content'
SOURCE = 'en'


def facts(path):
    text = path.read_text(encoding='utf-8')
    fm = re.match(r'---\n(.*?)\n---\n', text, re.S)
    front = sorted(re.findall(r'^([A-Za-z_]+):', fm.group(1), re.M)) if fm else []
    body = text[fm.end():] if fm else text

    # Strip fenced blocks before counting headings: a shell comment like
    # "# 1. Clone the repo" inside ```bash is not a heading.
    outside, fenced = [], False
    for line in body.splitlines():
        if line.startswith('```'):
            fenced = not fenced
            continue
        if not fenced:
            outside.append(line)
    prose = '\n'.join(outside)

    return {
        'front-matter keys': front,
        'heading levels': [len(m.group(1)) for m in
                           re.finditer(r'^(#{1,6}) +\S', prose, re.M)],
        'shortcodes': dict(collections.Counter(
            re.findall(r'\{\{<\s*/?\s*([a-zA-Z0-9/_-]+)', body))),
        'code fences': body.count('```'),
        'table rows': sum(1 for l in prose.splitlines() if l.lstrip().startswith('|')),
        'link targets': sorted(t.split('#')[0] for t in
                               re.findall(r'\]\((/[^)]*)\)', body)),
        'external links': sorted(re.findall(r'\]\((https?://[^)]*)\)', body)),
    }


def main():
    src_root = CONTENT / SOURCE
    if not src_root.is_dir():
        sys.exit(f'{src_root}: no source-language content tree')

    langs = sorted(p.name for p in CONTENT.iterdir()
                   if p.is_dir() and p.name != SOURCE)
    pages = sorted(p.relative_to(src_root) for p in src_root.rglob('*.md'))
    if not pages:
        sys.exit(f'{src_root}: no pages found')

    problems = []
    for lang in langs:
        for rel in pages:
            other = CONTENT / lang / rel
            if not other.exists():
                problems.append(f'{lang}/{rel}: no translation of this page')
                continue
            a, b = facts(src_root / rel), facts(other)
            for key in a:
                if a[key] != b[key]:
                    problems.append(
                        f'{lang}/{rel} [{key}]\n'
                        f'      {SOURCE}: {a[key]}\n'
                        f'      {lang}: {b[key]}')
        # A page that exists only in a translation is drift too.
        for p in sorted((CONTENT / lang).rglob('*.md')):
            if p.relative_to(CONTENT / lang) not in pages:
                problems.append(f'{lang}/{p.relative_to(CONTENT / lang)}: '
                                f'no {SOURCE} page it corresponds to')

    checked = len(pages) * len(langs)
    if problems:
        print(f'✗ {len(problems)} difference(s) across {checked} translated pages:',
              file=sys.stderr)
        for p in problems:
            print(f'  {p}', file=sys.stderr)
        return 1
    print(f'✅ all {checked} translated pages match the {SOURCE} structure '
          f'({", ".join(langs)} × {len(pages)} pages)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
