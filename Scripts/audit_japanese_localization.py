#!/usr/bin/env python3
"""Audit Japanese String Catalog coverage and interpolation signatures (stdlib only)."""
import argparse
import json
import re
from pathlib import Path

FORMAT = re.compile(r'%%|%(?:\d+\$)?(?:l[lu]?|z)?[@diufoxXsc]')
RENAME_TOKEN = re.compile(r'^(\[[^\]]+\]|\[\[|\]\])(?: |$)')


def audit(root):
    rows, errors = [], []
    for path in sorted((root / 'Source').rglob('*.xcstrings')):
        catalog = json.loads(path.read_text())
        row = {'path': str(path.relative_to(root)), 'entries': len(catalog['strings']),
               'missing': 0, 'unreviewed': 0}
        for key, entry in catalog['strings'].items():
            languages = entry.get('localizations', {})
            ja = languages.get('ja', {}).get('stringUnit')
            if ja is None:
                row['missing'] += 1
                continue
            row['unreviewed'] += ja.get('state') != 'translated'
            english = languages.get('en', {})
            source = english.get('stringUnit', {}).get('value', key)
            if 'substitutions' in english:
                source = key
            value = ja['value']
            if FORMAT.findall(source) != FORMAT.findall(value):
                errors.append(f'{row["path"]}: {key!r}: format signature differs')
            if path.name == 'BatchRenamingDialog.xcstrings':
                before, after = RENAME_TOKEN.match(source), RENAME_TOKEN.match(value)
                if before and (not after or before[1] != after[1]):
                    errors.append(f'{row["path"]}: {key!r}: rename token differs')
        rows.append(row)
    return {'catalogs': len(rows), 'entries': sum(r['entries'] for r in rows),
            'missing': sum(r['missing'] for r in rows),
            'unreviewed': sum(r['unreviewed'] for r in rows),
            'errors': errors, 'files': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if coverage or signatures are incomplete')
    args = parser.parse_args()
    result = audit(Path(__file__).resolve().parents[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(args.check and bool(result['missing'] or result['unreviewed'] or result['errors']))


if __name__ == '__main__':
    raise SystemExit(main())
