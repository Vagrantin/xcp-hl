#!/usr/bin/env python3
"""Assert the language switcher on every built page points at that same page.

Run against a built site:

    hugo --destination ../_site_hugo
    python3 site/scripts/check_switcher.py _site_hugo

Every page carrying Hextra's language switcher (the navbar globe, top right,
and the sidebar selector, bottom left — both render the same
`language-switch.html` partial) must offer exactly one entry per configured
language, and each entry must resolve to THAT SAME PAGE in the target
language: the page's own path with its language prefix swapped. An entry
pointing at a different page, at a home page, or at the wrong language is a
bug, and one this site has actually shipped.

It shipped because the default language had no `contentDir` and so silently
adopted the other languages' content trees as its own — see "Every language
needs its own contentDir" in site/README.md. Nothing in the build failed; the
site looked right in every screenshot taken of it. This check is what would
have caught it, so it runs in CI.

Exits non-zero, listing every bad entry, if anything is wrong.
"""
import pathlib
import re
import sys
from html.parser import HTMLParser

HERE = pathlib.Path(__file__).resolve().parent
HUGO_TOML = HERE.parent / 'hugo.toml'


class PageParser(HTMLParser):
    """Pull the page's language, its canonical URL and its switcher entries.

    A real parser, not a regex: `hugo --minify` strips attribute quotes
    (`href=/docs/`), which a regex over `href="([^"]+)"` silently finds
    nothing in — so the check would have passed every page in CI while
    reading none of them.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.canonical = None
        self.entries = []          # [(label, href)] in document order
        self._ul_depth = 0         # >0 while inside the switcher's <ul>
        self._href = None
        self._text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html' and self.lang is None:
            self.lang = a.get('lang')
        elif tag == 'link' and a.get('rel') == 'canonical' and self.canonical is None:
            self.canonical = a.get('href')
        elif tag == 'ul':
            if self._ul_depth or 'hextra-language-options' in (a.get('class') or '').split():
                self._ul_depth += 1
        elif tag == 'a' and self._ul_depth:
            self._href = a.get('href')
            self._text = []

    def handle_endtag(self, tag):
        if tag == 'ul' and self._ul_depth:
            self._ul_depth -= 1
        elif tag == 'a' and self._ul_depth and self._href is not None:
            self.entries.append((''.join(self._text).strip(), self._href))
            self._href = None

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)


def read_languages():
    """{languageName: code} and the default language, straight from hugo.toml.

    Parsed rather than hardcoded so that adding a language to hugo.toml
    extends this check automatically instead of silently narrowing it. The
    switcher markup carries no hreflang attribute, so the displayed
    `languageName` is the only thing tying a link to its language.
    """
    text = HUGO_TOML.read_text(encoding='utf-8')
    m = re.search(r'^\s*defaultContentLanguage\s*=\s*[\'"]([^\'"]+)', text, re.M)
    default = m.group(1) if m else 'en'

    names, code = {}, None
    for line in text.splitlines():
        m = re.match(r'\s*\[languages\.([A-Za-z0-9_-]+)\]', line)
        if m:
            code = m.group(1)
            continue
        m = re.match(r'\s*languageName\s*=\s*[\'"](.+?)[\'"]', line)
        if m and code:
            names[m.group(1)] = code
    if not names:
        sys.exit(f'{HUGO_TOML}: no [languages.*] with a languageName found')
    if default not in names.values():
        sys.exit(f'{HUGO_TOML}: defaultContentLanguage {default!r} is not a configured language')
    return names, default


def site_prefix(root):
    """The path the site is served under, e.g. '/xcp-hl/' on project Pages.

    Taken from the home page's canonical URL, so the check works against a
    build made with any --baseURL.
    """
    home = root / 'index.html'
    if home.is_file():
        p = PageParser()
        p.feed(home.read_text(encoding='utf-8', errors='replace'))
        if p.canonical:
            path = re.sub(r'^https?://[^/]+', '', p.canonical)
            if path.startswith('/'):
                return path if path.endswith('/') else path + '/'
    return '/'


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '_site_hugo')
    if not root.is_dir():
        sys.exit(f'{root}: not a directory — build the site first')

    names, default_lang = read_languages()
    codes = set(names.values())
    prefixed = sorted(codes - {default_lang})
    prefix = site_prefix(root)

    def split_lang(url_path):
        """'/xcp-hl/fr/docs/' -> ('fr', 'docs/'); '/xcp-hl/docs/' -> ('en', 'docs/')."""
        rest = url_path[len(prefix):] if url_path.startswith(prefix) else url_path.lstrip('/')
        for lang in prefixed:
            if rest == lang or rest.startswith(lang + '/'):
                return lang, rest[len(lang):].lstrip('/')
        return default_lang, rest

    def join_lang(lang, bare):
        return prefix + ('' if lang == default_lang else lang + '/') + bare

    checked, errors = 0, []
    for f in sorted(root.rglob('index.html')):
        html = f.read_text(encoding='utf-8', errors='replace')
        if 'hextra-language-options' not in html:
            continue
        page = PageParser()
        page.feed(html)
        if not page.entries:
            errors.append(f'{f.relative_to(root)}: switcher markup present but no entries parsed')
            continue
        checked += 1

        url_path = prefix + str(f.relative_to(root).as_posix()).removesuffix('index.html')
        page_lang, bare = split_lang(url_path)
        if page.lang and page.lang != page_lang:
            errors.append(
                f'{url_path}: served as <html lang="{page.lang}">, '
                f'but its URL puts it in {page_lang}'
            )

        seen = {}
        for label, href in page.entries:
            if label not in names:
                errors.append(f'{url_path}: switcher entry with unknown label {label!r}')
                continue
            seen[names[label]] = href

        for missing in sorted(codes - set(seen)):
            errors.append(f'{url_path}: switcher offers no {missing} entry')

        for lang, href in sorted(seen.items()):
            want = join_lang(lang, bare)
            if href != want:
                errors.append(f'{url_path}: {lang} -> {href} (expected {want})')

    if not checked:
        sys.exit(f'{root}: no page carries a language switcher — nothing was checked')

    if errors:
        print(f'✗ {len(errors)} problem(s) across {checked} pages with a switcher:',
              file=sys.stderr)
        for e in errors:
            print(f'  {e}', file=sys.stderr)
        return 1

    print(f'✅ language switcher correct on all {checked} pages '
          f'({", ".join(sorted(codes))})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
