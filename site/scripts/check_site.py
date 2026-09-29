#!/usr/bin/env python3
"""Check the rendered site, including minified HTML, aliases and local assets.

Usage: python3 site/scripts/check_site.py OUTPUT_DIR
No network calls: run on both the Pages subpath and standalone-root build.
"""
import pathlib
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urljoin, urlsplit

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.alternates = set(), [], {}
        self.canonical = self.redirect = self.lang = None
        self.real = False
        self.problems = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'html':
            self.lang = a.get('lang')
        if tag == 'article':
            self.real = True
        if 'screenshot-pending' in a.get('class', '').split():
            self.problems.append('unfilled screenshot placeholder')
        if tag == 'link':
            if a.get('rel') == 'canonical':
                self.canonical = a.get('href')
            if a.get('rel') == 'alternate' and a.get('hreflang'):
                self.alternates[a['hreflang']] = a.get('href')
        if tag == 'meta' and a.get('http-equiv', '').lower() == 'refresh':
            m = re.search(r'url\s*=\s*(.*)', a.get('content', ''), re.I)
            if m:
                self.redirect = m[1].strip(' "\'')
        for attr in ('href', 'src', 'poster'):
            if a.get(attr):
                asset = attr != 'href' or tag == 'link' and a.get('rel') in ('stylesheet', 'preload', 'modulepreload', 'icon')
                self.links.append((a[attr], asset))
        for item in a.get('srcset', '').split(','):
            if item.strip():
                self.links.append((item.strip().split()[0], True))


def check(root):
    root = pathlib.Path(root).resolve()
    pages = {p.relative_to(root).as_posix(): Page(p.read_text()) for p in root.rglob('*.html')}
    if 'index.html' not in pages or not pages['index.html'].canonical:
        return ['missing homepage/canonical'], 0, 0
    base = pages['index.html'].canonical
    site = urlsplit(base)
    prefix = site.path if site.path.endswith('/') else site.path + '/'
    errors, checked, aliases = [], 0, 0

    def resolve(url, origin):
        u = urlsplit(urljoin(origin, url))
        if u.scheme not in ('http', 'https'):
            return None, u
        if u.netloc != site.netloc:
            return None, u
        path = unquote(u.path)
        if not path.startswith(prefix):
            # Absolute links to another project on the same Pages host are external.
            return (None if urlsplit(url).netloc else False), u
        rel = path[len(prefix):]
        if not rel or rel.endswith('/'):
            rel += 'index.html'
        elif (root / rel).is_dir():
            rel += '/index.html'
        if not (root / rel).is_file():
            return False, u
        return rel, u

    for rel, p in pages.items():
        origin = urljoin(base, rel.removesuffix('index.html'))
        errors.extend(f'{rel}: {e}' for e in p.problems)
        links = list(p.links)
        if p.redirect:
            aliases += 1
            links.append((p.redirect, False))
        if p.real:
            for lang in ('en', 'fr', 'ja', 'x-default'):
                if lang not in p.alternates:
                    errors.append(f'{rel}: missing {lang} hreflang')
        for link, asset in links:
            target, u = resolve(link, origin)
            if target is None:
                if asset and u.scheme in ('http', 'https'):
                    errors.append(f'{rel}: external asset {link}')
                continue
            checked += 1
            if target is False:
                errors.append(f'{rel}: missing target {link}')
                continue
            if u.fragment and target in pages:
                destination = pages[target]
                if destination.redirect:
                    redirected, _ = resolve(destination.redirect, urljoin(base, target))
                    destination = pages.get(redirected, destination)
                fragment = unquote(u.fragment)
                if not fragment.startswith(':~:text=') and fragment not in destination.ids:
                    errors.append(f'{rel}: missing fragment {link}')
        if p.redirect:
            target, _ = resolve(p.redirect, origin)
            if target in pages and pages[target].lang != p.lang:
                errors.append(f'{rel}: alias changes language')
        if p.real and not p.canonical:
            errors.append(f'{rel}: missing canonical URL')
    for css in root.rglob('*.css'):
        for match in re.finditer(r'url\(\s*[\'"]?([^\s)\'"]+)', css.read_text()):
            value = match[1]
            target, u = resolve(value, urljoin(base, css.relative_to(root).as_posix()))
            if u.scheme in ('http', 'https') and (target is None or target is False):
                errors.append(f'{css.relative_to(root)}: external/missing CSS asset {value}')
    return sorted(set(errors)), checked, aliases

if __name__ == '__main__':
    errors, checked, aliases = check(sys.argv[1])
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(f'{len(errors)} site error(s)')
    print(f'PASS: {checked} local links/assets; {aliases} aliases; language alternates and screenshot assets')
