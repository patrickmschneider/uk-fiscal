import unittest
from pathlib import Path
from pipeline.obr import discover_profile, parse_profile, fetch_forecast, LATEST_URL

FIXTURES = Path(__file__).resolve().parents[1] / 'tests/fixtures/obr'


class ForecastTests(unittest.TestCase):
    def setUp(self):
        self.raw = (FIXTURES / 'ons-july-2026-forecast.csv').read_bytes()
        self.page = (FIXTURES / 'ons-july-2026.html').read_text()

    def test_official_profile(self):
        url, published = discover_profile(self.page)
        result = parse_profile(self.raw, url, published)
        self.assertEqual(result['vintage'], 'March 2026')
        self.assertEqual(result['publicationDate'], '2026-08-21')
        self.assertEqual(result['cumulative'][3], {'period': '2026-07', 'value': 54.4})
        self.assertEqual(result['cumulative'][-1], {'period': '2027-03', 'value': 115.4})
        # Seasonal surplus is retained rather than forced to rise monotonically.
        self.assertLess(result['cumulative'][9]['value'], result['cumulative'][8]['value'])

    def test_fetch_discovers_download(self):
        url, _ = discover_profile(self.page)
        contents = {LATEST_URL: self.page.encode(), url: self.raw}
        self.assertEqual(fetch_forecast(contents.__getitem__)['fiscalYear'], '2026-27')

    def test_rejects_missing_forecast_or_wrong_units(self):
        for raw in [self.raw.replace(b'OBR forecast 2026', b'outturn 2026'), self.raw.replace('£ billion'.encode(), b'percent')]:
            with self.assertRaises(ValueError):
                parse_profile(raw, 'source', '2026-08-21')

    def test_rejects_missing_month(self):
        with self.assertRaises(ValueError):
            parse_profile(self.raw.replace(b'"Mar ","129.8","","115.4"', b''), 'source', '2026-08-21')

    def test_refuses_ambiguous_source(self):
        with self.assertRaises(ValueError):
            discover_profile(self.page + self.page)
