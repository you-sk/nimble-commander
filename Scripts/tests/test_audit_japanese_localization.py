"""Regression checks for the catalog guard, using isolated synthetic catalogs."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'ja_audit', Path(__file__).resolve().parents[1] / 'audit_japanese_localization.py')
audit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_module)


class CatalogAuditTest(unittest.TestCase):
    def check_entry(self, key, japanese=None, state='translated', filename='Example.xcstrings', english=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'Source'
            source.mkdir()
            languages = {}
            if japanese is not None:
                languages['ja'] = {'stringUnit': {'state': state, 'value': japanese}}
            if english is not None:
                languages['en'] = english
            (source / filename).write_text(json.dumps({'strings': {key: {'localizations': languages}}}))
            return audit_module.audit(root)

    def test_complete_catalog_passes(self):
        result = self.check_entry('Copy %@', '%@をコピー')
        self.assertEqual((result['entries'], result['missing'], result['unreviewed'], result['errors']),
                         (1, 0, 0, []))

    def test_missing_translation_is_counted(self):
        self.assertEqual(self.check_entry('Copy')['missing'], 1)

    def test_unreviewed_translation_is_counted(self):
        self.assertEqual(self.check_entry('Copy', 'コピー', state='needs_review')['unreviewed'], 1)

    def test_argument_type_mismatch_is_rejected(self):
        self.assertTrue(self.check_entry('Copy %@', '%dをコピー')['errors'])

    def test_rename_language_token_is_preserved(self):
        name = 'BatchRenamingDialog.xcstrings'
        self.assertFalse(self.check_entry('[N] Name', '[N] 名前', filename=name)['errors'])
        self.assertTrue(self.check_entry('[N] Name', '[E] 名前', filename=name)['errors'])

    def test_english_plural_substitution_uses_source_signature(self):
        english = {'stringUnit': {'value': 'Compressing %#@items@'}, 'substitutions': {'items': {}}}
        self.assertFalse(self.check_entry('Compressing %d items', '%d項目を圧縮中', english=english)['errors'])


if __name__ == '__main__':
    unittest.main()
