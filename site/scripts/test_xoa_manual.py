"""Regression checks for semantic translation drift and the publication gate."""
import copy
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

from check_xoa_manual import SITE, collect, inspect, read_page, source_revision


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

    def test_backup_tutorial_is_required_and_translation_drift_blocks_publication(self):
        page = self.site / 'content/en/docs/xoa-hl/backup-restore.md'
        original = page.read_text()
        page.write_text(original + '\nA new restore prerequisite.\n')
        with self.assertRaisesRegex(ValueError, 'stale'):
            collect(self.site)
        page.unlink()
        with self.assertRaisesRegex(ValueError, 'missing required.*backup-restore'):
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

    def review_all(self):
        """Synthetic records test the gate; these are never real review evidence."""
        rows, _ = inspect(self.site)
        reviews = {}
        for lang in ('fr', 'ja'):
            for row in rows[lang]:
                reviews.setdefault(row['translationKey'], {})[lang] = {
                    'sourceRevision': row['sourceRevision'],
                    'translationRevision': row['translationRevision'],
                    'technicalReviewer': 'fixture-technical',
                    'languageReviewer': 'fixture-language',
                    'reviewedAt': '2026-10-11',
                    'reviewUrl': 'https://github.com/example/fixture/pull/1#pullrequestreview-1',
                }
            for page in (self.site / 'content' / lang / 'docs/xoa-hl').rglob('*.md'):
                page.write_text(page.read_text().replace('translationStatus: draft', 'translationStatus: reviewed'))
        (self.site / 'data/xoa_manual_reviews.json').write_text(json.dumps({'schemaVersion': 1, 'reviews': reviews}))

    def test_reviewed_status_cannot_be_claimed_without_a_record(self):
        page = self.site / 'content/fr/docs/xoa-hl/_index.md'
        page.write_text(page.read_text().replace('translationStatus: draft', 'translationStatus: reviewed'))
        rows, problems = inspect(self.site)
        self.assertEqual(next(r['status'] for r in rows['fr'] if r['path'] == 'docs/xoa-hl/'), 'draft')
        self.assertTrue(any('missing human review record' in p['reason'] for p in problems))
        with self.assertRaisesRegex(ValueError, 'missing human review record'):
            collect(self.site)
        english = self.site / 'content/en/docs/xoa-hl/_index.md'
        english.write_text(english.read_text() + '\nChanged source meaning.\n')
        rows, _ = inspect(self.site)
        self.assertEqual(next(r['status'] for r in rows['fr'] if r['path'] == 'docs/xoa-hl/'), 'stale')

    def test_current_review_records_allow_reviewed_publication(self):
        self.review_all()
        rows = collect(self.site, require_reviewed=True)
        self.assertTrue(all(r['status'] == 'reviewed' for lang in ('fr', 'ja') for r in rows[lang]))

    def test_translated_meaning_change_invalidates_human_review(self):
        self.review_all()
        page = self.site / 'content/fr/docs/xoa-hl/automation.md'
        page.write_text(page.read_text() + '\nUne nouvelle instruction.\n')
        with self.assertRaisesRegex(ValueError, 'different translated body/glossary revision'):
            collect(self.site)

    def test_localized_glossary_change_invalidates_only_affected_reviews(self):
        self.review_all()
        path = self.site / 'data/xoa_glossary.json'
        glossary = json.loads(path.read_text())
        glossary['vm']['fr']['definition'] += ' Nouveau sens.'
        path.write_text(json.dumps(glossary))
        _, problems = inspect(self.site)
        affected = {p['page'] for p in problems}
        expected = {p.name for p in (self.site / 'content/fr/docs/xoa-hl').glob('*.md')
                    if 'vm' in json.loads(read_page(p)[0]['glossaryTerms'])}
        self.assertEqual(affected, expected)
        self.assertTrue(all(p['locale'] == 'fr' for p in problems))

    def test_english_drift_reports_every_affected_locale_and_page(self):
        for name in ('automation.md', 'configuration.md'):
            page = self.site / 'content/en/docs/xoa-hl' / name
            page.write_text(page.read_text() + '\nA changed instruction.\n')
        rows, problems = inspect(self.site)
        self.assertEqual(len(problems), 6)
        self.assertEqual({p['locale'] for p in problems}, {'en', 'fr', 'ja'})
        self.assertEqual({p['page'] for p in problems}, {'automation.md', 'configuration.md'})
        self.assertEqual(sum(r['status'] == 'stale' for r in rows['fr']), 2)

    def test_review_evidence_requires_names_date_and_url(self):
        for field in ('technicalReviewer', 'languageReviewer', 'reviewedAt', 'reviewUrl'):
            with self.subTest(field=field):
                self.review_all()
                path = self.site / 'data/xoa_manual_reviews.json'
                data = json.loads(path.read_text())
                key = read_page(self.site / 'content/en/docs/xoa-hl/_index.md')[0]['translationKey']
                data['reviews'][key]['fr'].pop(field)
                path.write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, field):
                    collect(self.site)

    def test_failed_gate_still_writes_complete_json_queue(self):
        report = self.site / 'queue.json'
        run = subprocess.run([sys.executable, str(SITE / 'scripts/check_xoa_manual.py'),
                              '--site', str(self.site), '--require-reviewed', '--report', str(report)],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)
        data = json.loads(report.read_text())
        self.assertEqual(len(data['reviewQueue']), 32)
        self.assertEqual(len(data['problems']), 32)
        self.assertIn('ja/automation.md', run.stderr)
        self.assertIn('fr/translation-status.md', run.stderr)

    def test_invalid_manifest_and_unknown_review_identity_fail_closed(self):
        path = self.site / 'data/xoa_manual_reviews.json'
        for data in ({'schemaVersion': 99, 'reviews': {}},
                     {'schemaVersion': 1, 'reviews': {'unknown': {'fr': {}}}}):
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                collect(self.site)


if __name__ == '__main__':
    unittest.main()
