import unittest
from unittest.mock import patch
from pipeline.obr_history import parse_databank,WORKBOOK

class DatabankTests(unittest.TestCase):
    def test_official_historical_balances_and_matched_denominator(self):
        data=parse_databank(WORKBOOK.read_bytes())
        self.assertEqual(len(data['rows']),51)
        self.assertEqual(data['rows'][0]['year'],'1975-76')
        self.assertEqual(data['rows'][-1]['year'],'2025-26')
        r=next(r for r in data['rows'] if r['year']=='1990-91')
        self.assertAlmostEqual(r['structuralBorrowingBn'],5.782467574316762)
        self.assertAlmostEqual(r['deficitInterestBn'],14.157)
        self.assertAlmostEqual(r['structuralPrimaryBalanceBn'],8.374532425683237)
        self.assertEqual(r['gdpBn'],681.464)
        self.assertEqual(len(data['fileSha256']),64)

    def test_unreviewed_vintage_is_rejected(self):
        class Sheet:
            values=[['released on 21 September 2026']]
        with patch('pipeline.obr_history.openpyxl.load_workbook',return_value={'Aggregates (£bn)':Sheet(),'Aggregates (per cent of GDP)':Sheet()}):
            with self.assertRaisesRegex(ValueError,'Review the new'):
                parse_databank(b'fixture')
