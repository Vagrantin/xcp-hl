#!/usr/bin/env python3
"""Validate generated release notes and their three rendered language pages."""

import argparse
from datetime import date
from html.parser import HTMLParser
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPOS = {
    'build-xoa-hl', 'xcp-hl', 'xcp-ng-ce-iso',
    'xoa-hl', 'xoa-proxy', 'xolite-ce',
}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = set()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'a':
            self.links.add(values.get('href'))
        if 'id' in values:
            self.ids.add(values['id'])


def valid_release(row):
    assert set(row) == {'tag', 'date', 'channel', 'repository', 'components', 'changes'}, row
    assert row['repository'] in {'xcp-ng-ce-iso', 'build-xoa-hl'}, row
    assert re.fullmatch(r'[A-Za-z0-9._-]+', row['tag']), row
    date.fromisoformat(row['date'])
    assert row['channel'] in {'stable', 'candidate'}, row
    assert isinstance(row['components'], list) and row['components'], row
    assert isinstance(row['changes'], list), row
    for component in row['components']:
        assert set(component) == {'repository', 'version'}, component
        assert component['repository'] in REPOS, component
        assert re.fullmatch(r'[A-Za-z0-9._-]+', component['version']), component
    for change in row['changes']:
        assert set(change) == {'repository', 'title', 'url'}, change
        assert change['repository'] in REPOS and change['title'].strip(), change
        assert re.fullmatch(
            rf'https://github\.com/Vagrantin/{change["repository"]}/pull/[1-9][0-9]*',
            change['url'],
        ), change


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', type=Path)
    args = parser.parse_args()
    rows = json.loads((ROOT / 'docs/_data/changelog.json').read_text())
    assert isinstance(rows, list), 'changelog must be a list'
    tags = [row['tag'] for row in rows]
    assert len(tags) == len(set(tags)), 'duplicate release tag'
    for row in rows:
        valid_release(row)
    print(f'Validated {len(rows)} changelog releases')
    if args.site:
        for path in ['changelog.html', 'fr/changelog.html', 'ja/changelog.html']:
            page = Page()
            page.feed((args.site / path).read_text())
            for row in rows:
                assert f'release-{row["tag"].lower()}' in page.ids, (path, row['tag'])
                assert f'https://github.com/Vagrantin/{row["repository"]}/releases/tag/{row["tag"]}' in page.links, (path, row['tag'])
                for change in row['changes']:
                    assert change['url'] in page.links, (path, change['url'])
        print('Rendered EN/FR/JA changelogs contain every release and pull request link')


if __name__ == '__main__':
    main()
