"""Regression checks for semantic translation drift and the publication gate."""
import copy
import pathlib
import shutil
import tempfile
import unittest

from check_xoa_manual import SITE, collect, source_revision


class TranslationDrift(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.site = pathlib.Path(self.temp.name)
        shutil.copytree(SITE / 'content', self.site / 'content')
        shutil.copytree(SITE / 'data', self.site / 'data')

    def tearDown(self):
        self.temp.cleanup()

    def test_preview_accepts_drafts_but_reviewed_publication_rejects_them(self):
        self.assertEqual(collect(self.site)['fr'][0]['status'], 'draft')
        with self.assertRaisesRegex(ValueError, 'draft'):
            collect(self.site, require_reviewed=True)

    def test_english_meaning_change_blocks_old_source_revisions(self):
        page = self.site / 'content/en/docs/xoa-hl/_index.md'
        page.write_text(page.read_text() + '\nA new prerequisite.\n')
        with self.assertRaisesRegex(ValueError, 'stale'):
            collect(self.site)

    def test_unknown_term_cannot_silently_drop_from_glossary(self):
        page = self.site / 'content/en/docs/xoa-hl/_index.md'
        page.write_text(page.read_text().replace('"appliance"', '"missing-term"'))
        with self.assertRaisesRegex(ValueError, 'unknown controlled glossary term'):
            collect(self.site)

    def test_source_hash_ignores_editorial_whitespace_but_tracks_term_meaning(self):
        glossary = {'vm': {'en': {'label': 'VM', 'definition': 'Guest system'}}}
        first = source_revision('A task.\n', ['vm'], glossary)
        self.assertEqual(first, source_revision('\nA task.  \n\n', ['vm'], glossary))
        changed = copy.deepcopy(glossary)
        changed['vm']['en']['definition'] = 'Changed meaning'
        self.assertNotEqual(first, source_revision('A task.\n', ['vm'], changed))

    def test_missing_locale_and_required_page_fail_closed(self):
        (self.site / 'content/ja/docs/xoa-hl/glossary.md').unlink()
        with self.assertRaises(FileNotFoundError):
            collect(self.site)
        (self.site / 'content/en/docs/xoa-hl/_index.md').unlink()
        with self.assertRaisesRegex(ValueError, 'missing required'):
            collect(self.site)

    def test_beginner_guide_cannot_disappear_from_all_locales(self):
        # Parity alone accepts removal from all locales; the manual contract must not.
        for lang in ('en', 'fr', 'ja'):
            (self.site / f'content/{lang}/docs/xoa-hl/create-vm.md').unlink()
        with self.assertRaisesRegex(ValueError, 'missing required XOA-HL page: create-vm.md'):
            collect(self.site)


if __name__ == '__main__':
    unittest.main()
