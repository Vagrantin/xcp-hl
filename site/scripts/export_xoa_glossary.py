#!/usr/bin/env python3
"""Export controlled terms for UI translation review, not runtime message IDs."""
import argparse
import hashlib
import json
import pathlib

from check_xoa_manual import LANGS, SITE


def export(glossary):
    if not isinstance(glossary, dict) or not glossary:
        raise ValueError('glossary must be a nonempty object')
    for key, term in glossary.items():
        if not isinstance(term, dict):
            raise ValueError(f'{key}: term must be an object')
        for lang in LANGS:
            locale = term.get(lang)
            if not isinstance(locale, dict) or any(not isinstance(locale.get(field), str) or not locale[field].strip()
                                                   for field in ('label', 'definition')):
                raise ValueError(f'{key}: missing {lang} label/definition')
    canonical = json.dumps(glossary, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return {
        'schemaVersion': 1,
        'source': 'Vagrantin/xcp-hl/site/data/xoa_glossary.json',
        'glossaryRevision': 'sha256:' + hashlib.sha256(canonical.encode()).hexdigest(),
        'locales': list(LANGS),
        'terms': [{'id': key, 'translations': glossary[key]} for key in sorted(glossary)],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--glossary', type=pathlib.Path, default=SITE / 'data/xoa_glossary.json')
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args()
    try:
        result = export(json.loads(args.glossary.read_text()))
    except (ValueError, OSError) as error:
        parser.error(str(error))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f"PASS: exported {len(result['terms'])} controlled terms in {'/'.join(LANGS).upper()}; {result['glossaryRevision']}")


if __name__ == '__main__':
    main()
