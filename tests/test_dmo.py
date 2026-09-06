"""Economic/source checks use small real DMO extracts, not invented observations."""
from pathlib import Path
import json
import unittest
from unittest.mock import patch
from pipeline.dmo import coupon, parse_stock, parse_auction, parse_calendar, parse_announcement, pdf_text, parse_quarterly_auctions

FIX = Path(__file__).parent / 'fixtures' / 'dmo'
CAT = json.loads((Path(__file__).parents[1] / 'catalogue/dmo.json').read_text())


def source(name):
    return next(s for s in CAT['notices'] if s['id'] == 'dmo-' + name)


class DmoTests(unittest.TestCase):
    def test_independent_stock_notice_crosscheck(self):
        # Separate official PAOF notices state outstanding stock after settlement.
        # Conventional 25 Aug notice: £30,685,599,000; linker 3 Sep: £8,424.999m.
        # Compare those independent publications to the 4 Sep XML snapshot.
        _, rows = parse_stock((FIX / 'stock.xml').read_bytes())
        by_id = {s['isin']: s for s in rows}
        self.assertIn('£30,685,599,000.00', (FIX / 'conventional-paof.txt').read_text())
        self.assertIn('£8,424.999 million', ' '.join((FIX / 'index-paof.txt').read_text().split()))
        self.assertAlmostEqual(by_id['GB00BVP99780']['nominalMillion'], 30685599000 / 1e6)
        self.assertAlmostEqual(by_id['GB00BT7J0134']['nominalMillion'], 8424.999)
        self.assertEqual(by_id['GB00BT7J0134']['type'], 'index-linked')
        self.assertGreater(by_id['GB00BT7J0134']['upliftedMillion'], 8424.999)
        self.assertEqual(by_id['GB00BVP99780']['maturityDate'], '2033-03-07')

    def test_conventional_result_figures_and_cover_rounding(self):
        row = parse_auction((FIX / 'conventional.txt').read_text(), source('conventional'))
        self.assertEqual((row['date'], row['yieldPct'], row['tailBp']), ('2026-08-25', 4.761, .2))
        self.assertEqual(row['allottedMillion'], 4000)
        self.assertEqual(round(row['bidsMillion'] / row['offeredMillion'], 2), row['cover'])
        self.assertIsNone(row['postAuctionMillion'])  # requires separate PAOF notice

    def test_linker_result_yield_is_real_tail_inapplicable(self):
        row = parse_auction((FIX / 'index.txt').read_text(), source('index'))
        self.assertEqual(row['yieldPct'], 2.496)
        self.assertEqual(row['yieldBasis'], 'real striking yield')
        self.assertEqual(row['cover'], 3.58)
        self.assertIsNone(row['tailBp'])
        self.assertEqual(row['allottedMillion'], 900)

    def test_calendar_counts_and_revised_date(self):
        events = parse_calendar((FIX / 'q2.txt').read_text(), source('q2'))
        self.assertEqual(len(events), 17)
        self.assertIn('2026-09-03', [e['date'] for e in events])
        self.assertNotIn('2026-09-02', [e['date'] for e in events])
        self.assertTrue(all(e['amountMillion'] is None for e in events))
        q3 = parse_calendar((FIX / 'q3.txt').read_text(), source('q3'))
        self.assertEqual(len(q3), 16)
        self.assertEqual(next(e['type'] for e in q3 if e['date'] == '2026-10-13'), 'tender')
        self.assertIn('22 May 2030', next(e['name'] for e in q3 if e['date'] == '2026-10-14'))

    def test_announced_auction_size_and_settlement(self):
        row = parse_announcement((FIX / 'announcement.txt').read_text(), source('announcement'))
        self.assertEqual(row['date'], '2026-09-10')
        self.assertEqual(row['settlementDate'], '2026-09-11')
        self.assertEqual(row['amountMillion'], 5000)
        self.assertEqual(row['isin'], 'GB00BWBR1P52')

    def test_schema_failures_are_not_empty_success(self):
        with self.assertRaises(ValueError):
            pdf_text(b'<html>Captcha</html>')
        with self.assertRaises(ValueError):
            parse_stock(b'<Data/>')
        raw = (FIX / 'stock.xml').read_bytes()
        with self.assertRaises(ValueError):
            parse_stock(raw.replace(b'2033-03-07', b'2025-03-07'))
        with self.assertRaises(ValueError):
            parse_stock(raw.replace(b'GB00BT7J0134', b'GB00BVP99780'))
        with self.assertRaises(ValueError):
            parse_calendar((FIX / 'q3.txt').read_text().replace('Tuesday 6 October', 'MISSING'), source('q3'))
        with self.assertRaises(ValueError):
            parse_auction((FIX / 'index.txt').read_text().replace('Times covered', 'Unknown field'), source('index'))


    def test_quarterly_history_rounding_and_missing_basis(self):
        identities = CAT['instrumentIdentities']
        rows = parse_quarterly_auctions((FIX / 'review.txt').read_text(), source('review'), identities)
        self.assertEqual(len(rows), 13)
        first = rows[0]
        self.assertEqual((first['date'], first['allottedMillion'], first['postAuctionMillion']), ('2026-04-09', 4000, 527.7))
        self.assertEqual((first['yieldPct'], first['cover'], first['tailBp']), (4.51, 3.30, .2))
        self.assertIsNone(first['offeredMillion'])
        self.assertIsNone(first['bidsMillion'])
        linker = next(r for r in rows if r['date'] == '2026-05-06')
        self.assertEqual(linker['yieldPct'], 1.46)
        self.assertIsNone(linker['tailBp'])  # source 0.0 must not imply conventional tail
        old = parse_quarterly_auctions((FIX / 'review-2025q3.txt').read_text(), source('review-2025q3'), identities)
        self.assertEqual(len(old), 18)
        self.assertIsNone(old[0]['postAuctionMillion'])  # blank green-gilt PAOF column
        self.assertEqual(old[0]['yieldPct'], 5.17)
        with self.assertRaises(ValueError):
            parse_quarterly_auctions((FIX / 'review.txt').read_text().replace('09-Apr-26', 'BROKEN'), source('review'), identities)

    def test_historical_auction_survives_security_leaving_live_stock(self):
        from pipeline.dmo import fetch_debt
        import xml.etree.ElementTree as ET
        root = ET.fromstring((FIX / 'stock.xml').read_bytes())
        for row in list(root):
            if row.attrib['ISIN_CODE'] == 'GB00BVP99780':
                root.remove(row)
        stock = ET.tostring(root)
        notices = {s['url']: s['id'].removeprefix('dmo-').encode() for s in CAT['notices']}
        def fetch(url):
            return stock if url == CAT['stock']['url'] else notices[url]
        def text(raw, layout=True):
            return (FIX / (raw.decode() + '.txt')).read_text()
        with patch('pipeline.dmo.pdf_text', side_effect=text):
            result = fetch_debt(fetch)
        self.assertNotIn('GB00BVP99780', [s['isin'] for s in result['securities']])
        self.assertTrue(any(a['isin'] == 'GB00BVP99780' and a['date'] == '2026-04-09' for a in result['auctions']))
        self.assertEqual(len(result['auctions']), 60)
        self.assertEqual(next(e['datePrecision'] for e in result['calendar'] if e['type'] == 'syndication'), 'week')

    def test_coupon_formats(self):
        self.assertEqual(coupon('4 1/8% Treasury Gilt 2033'), 4.125)
        self.assertEqual(coupon('4⅝% Treasury Gilt 2030'), 4.625)
        self.assertEqual(coupon('½% Treasury Gilt 2028'), .5)


if __name__ == '__main__':
    unittest.main()
