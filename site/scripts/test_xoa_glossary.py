"""The UI review export preserves Unicode/IDs and tracks every locale's meaning."""
import copy
import json
import unittest

from check_xoa_manual import SITE
from export_xoa_glossary import export


class GlossaryExport(unittest.TestCase):
    def setUp(self):
        self.glossary = json.loads((SITE / 'data/xoa_glossary.json').read_text())

    def test_export_preserves_all_ids_and_japanese_terms(self):
        data = export(self.glossary)
        self.assertEqual([term['id'] for term in data['terms']], sorted(self.glossary))
        vm = next(term for term in data['terms'] if term['id'] == 'vm')
        self.assertEqual(vm['translations']['ja'], self.glossary['vm']['ja'])
        self.assertEqual(json.loads(json.dumps(data, ensure_ascii=False)), data)

    def test_key_order_is_editorial_but_localized_meaning_changes_revision(self):
        revision = export(self.glossary)['glossaryRevision']
        self.assertEqual(export(dict(reversed(list(self.glossary.items()))))['glossaryRevision'], revision)
        changed = copy.deepcopy(self.glossary)
        changed['vm']['ja']['definition'] += ' 新しい説明。'
        self.assertNotEqual(export(changed)['glossaryRevision'], revision)

    def test_incomplete_locale_cannot_be_exported_as_complete(self):
        del self.glossary['vm']['ja']['definition']
        with self.assertRaisesRegex(ValueError, 'vm: missing ja'):
            export(self.glossary)


if __name__ == '__main__':
    unittest.main()
