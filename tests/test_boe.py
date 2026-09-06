"""Parser safeguards plus optional local official-workbook regression.

The official fixture is local-only pending redistribution permission.
"""
import io
import unittest
import zipfile
from datetime import datetime
from pathlib import Path
from openpyxl import Workbook
from pipeline.boe import parse_zip


def synthetic_zip(sheet='4. spot curve', filename='GLC Nominal daily data.xlsx', rates=(4.1, None, -0.2)):
    wb = Workbook()
    ws = wb.active
    ws.title = sheet
    ws.append(['Synthetic parser test fixture — not real observations'])
    ws.append(['years', 0.5, 1, 2])
    ws.append([datetime(2026, 1, 5), *rates])
    excel = io.BytesIO()
    wb.save(excel)
    result = io.BytesIO()
    with zipfile.ZipFile(result, 'w') as z:
        z.writestr(filename, excel.getvalue())
    return result.getvalue()


class CurveTests(unittest.TestCase):
    def test_missing_tenors_not_filled_and_negative_rates_valid(self):
        result = parse_zip(synthetic_zip())
        self.assertEqual(result['2026-01-05'], [{'tenor': 0.5, 'rate': 4.1}, {'tenor': 1.0, 'rate': None}, {'tenor': 2.0, 'rate': -0.2}])

    def test_legacy_nominal_sheet_name(self):
        self.assertEqual(parse_zip(synthetic_zip()), parse_zip(synthetic_zip(sheet='4. nominal spot curve')))

    def test_empty_non_trading_dates_excluded(self):
        with self.assertRaisesRegex(ValueError, 'No dated nominal spot rates'):
            parse_zip(synthetic_zip(rates=(None, None, None)))

    def test_official_current_workbook(self):
        fixture = Path(__file__).resolve().parents[1] / 'data/fixtures/boe/2026-09-06-latest-yield-curve-data.zip'
        if not fixture.exists():
            self.skipTest('Local official fixture absent; download privately to validate real source')
        curves = parse_zip(fixture.read_bytes())
        self.assertEqual(sorted(curves), ['2026-09-01', '2026-09-02', '2026-09-03'])
        self.assertEqual(len(curves['2026-09-03']), 80)
        self.assertEqual(curves['2026-09-03'][19]['tenor'], 10.0)
        self.assertAlmostEqual(curves['2026-09-03'][19]['rate'], 5.1575084015148365)
        self.assertAlmostEqual(curves['2026-09-03'][-1]['rate'], 5.619299573940564)

    def test_rejects_other_curves(self):
        for raw in [synthetic_zip(sheet='5. forward curve'), synthetic_zip(filename='GLC Real daily data.xlsx')]:
            with self.assertRaises(ValueError):
                parse_zip(raw)

    def test_rejects_non_numeric_rates(self):
        with self.assertRaises(ValueError):
            parse_zip(synthetic_zip(rates=(4.1, 'changed layout', 2)))
