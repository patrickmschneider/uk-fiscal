"""Regression against actual OBR March 2026 Annex A table text.

Fixture is extracted with pypdf from the official EFO PDF, pages 110–117
(physical pages 115–122); URL in pipeline.outlook.EFO_URL.
"""
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
try:
    from pipeline import outlook
except ImportError:
    import outlook

FIXTURES=Path(__file__).parent/'fixtures'
if not (FIXTURES/'outlook_tables.json').exists():FIXTURES=Path(__file__).parent

class Page:
    def __init__(self,text):self.text=text
    def extract_text(self):return self.text

class OutlookTests(unittest.TestCase):
    def parsed(self,texts=None):
        texts=texts or json.loads((FIXTURES/'outlook_tables.json').read_text())
        reader=type('Reader',(),{'pages':[Page(t)for t in texts]})()
        with patch.object(outlook,'PdfReader',return_value=reader):return outlook.parse_efo(b'fixture')

    def test_actual_source_forecast_and_rounding(self):
        current=self.parsed()[1]
        self.assertEqual(current['forecastStart'],'2025-26')
        self.assertEqual(current['rows'][0]['status'],'outturn')
        self.assertEqual(current['rows'][1]['status'],'forecast')
        self.assertEqual(current['rows'][1]['borrowingBn'],132.7)
        self.assertEqual(current['rows'][-1]['borrowingBn'],59.0)
        self.assertEqual(current['rows'][-1]['debtPct'],95.1)
        self.assertEqual(current['rows'][-2]['currentBudgetDeficitBn'],-23.6)
        self.assertEqual(current['rows'][1]['structuralPrimaryBalancePct'],-.9)
        self.assertEqual(current['rows'][1]['structuralBorrowingPct'],3.9)
        self.assertEqual(current['rows'][1]['structuralBorrowingBn'],117.9)
        self.assertEqual(current['rows'][1]['outputGapPct'],-.8)
        self.assertEqual(current['rows'][2]['gdpDeflatorGrowth'],2.0)

    def test_reconstructed_vintage_keeps_previous_assumptions(self):
        prior=self.parsed()[0]
        self.assertTrue(prior['reconstructed'])
        self.assertEqual(prior['rows'][1]['borrowingBn'],138.2)
        self.assertEqual(prior['rows'][-2]['currentBudgetDeficitBn'],-21.7)
        self.assertEqual(prior['rows'][2]['bankRate'],3.6)
        self.assertEqual(prior['rows'][1]['netFinancialLiabilitiesPct'],83.1)
        self.assertEqual(prior['rows'][1]['structuralPrimaryBalancePct'],-1.1)

    def test_unexpected_vintage_fails_closed(self):
        texts=json.loads((FIXTURES/'outlook_tables.json').read_text())
        with self.assertRaisesRegex(ValueError,'header missing'):
            self.parsed([t.replace('2030-31','2031-32')for t in texts])

    def test_duplicate_label_rejected(self):
        with self.assertRaisesRegex(ValueError,'exactly one'):
            outlook.vector('X 1 2 3 4 5 6 7\nX 1 2 3 4 5 6 7\n','X')

    def test_corrupted_accounting_fails_closed(self):
        texts=json.loads((FIXTURES/'outlook_tables.json').read_text())
        with self.assertRaisesRegex(ValueError,'identity'):
            self.parsed([t.replace('152.7 132.7 115.5','152.7 232.7 115.5')for t in texts])

if __name__=='__main__':unittest.main()
