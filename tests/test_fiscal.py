import csv
import io
from pathlib import Path
import unittest
from pipeline.fiscal import parse_pusf, parse_gdp, fetch_fiscal, ONS_URL, GDP_URL

FIXTURE=Path(__file__).parent/'fixtures/pusf-sample.csv'

class FiscalTests(unittest.TestCase):
    def test_published_july_2026(self):
        data=parse_pusf(FIXTURE.read_bytes())
        self.assertEqual(data['releaseDate'],'2026-08-21')
        self.assertEqual(data['observations'][-1]['borrowing'],1800)
        ytd=[r for r in data['observations'] if '2026-04'<=r['date']<='2026-07']
        self.assertAlmostEqual(sum(r['borrowing'] for r in ytd),56696)
        self.assertEqual(data['observations'][-1]['debtPct'],94.1)

    def modify(self,fn):
        rows=list(csv.reader(io.StringIO(FIXTURE.read_text())))
        fn(rows);out=io.StringIO();csv.writer(out).writerows(rows);return out.getvalue().encode()

    def test_missing_month_fails(self):
        raw=self.modify(lambda rows:rows.pop(next(i for i,r in enumerate(rows) if r[0]=='2025 FEB')))
        with self.assertRaisesRegex(ValueError,'Missing month'):parse_pusf(raw)

    def test_bad_identity_is_rejected(self):
        def corrupt(rows):rows[-1][rows[1].index('DZLS')]='-1800'
        with self.assertRaisesRegex(ValueError,'Borrowing reconciliation'):parse_pusf(self.modify(corrupt))

    def test_missing_core_is_not_zero(self):
        def corrupt(rows):rows[-1][rows[1].index('JW2O')]=''
        with self.assertRaisesRegex(ValueError,'Missing core'):parse_pusf(self.modify(corrupt))

    def test_html_and_schema_drift_fail(self):
        with self.assertRaises(ValueError):parse_pusf(b'<html>Denied</html>')
        def corrupt(rows):rows[1][rows[1].index('DZLS')]='OTHER'
        with self.assertRaisesRegex(ValueError,'Missing required'):parse_pusf(self.modify(corrupt))

    def test_revised_old_period_is_preserved(self):
        def revise(rows):
            row=next(r for r in rows if r[0]=='2025 JAN')
            for code in ['DZLS','KX5Q','JW2Q']:row[rows[1].index(code)]=str(float(row[rows[1].index(code)])+235)
        before=parse_pusf(FIXTURE.read_bytes());after=parse_pusf(self.modify(revise))
        a=next(r for r in before['observations'] if r['date']=='2025-01')
        b=next(r for r in after['observations'] if r['date']=='2025-01')
        self.assertEqual(b['borrowing']-a['borrowing'],235)

class GDPTests(unittest.TestCase):
    fixture = Path(__file__).parent/'fixtures/gdp-bktl.csv'

    def modified(self, fn):
        rows = list(csv.reader(io.StringIO(self.fixture.read_text())))
        fn(rows)
        output = io.StringIO()
        csv.writer(output).writerows(rows)
        return output.getvalue().encode()

    def test_official_four_quarter_total_and_release(self):
        data = parse_gdp(self.fixture.read_bytes())
        self.assertEqual(data['releaseDate'], '2026-08-13')
        self.assertEqual(data['asOf'], '2026-06')
        # Independent sum of published 2025 Q3 through 2026 Q2 observations.
        self.assertEqual(data['observations'][-1]['rollingAnnualMillion'],
                         760095 + 773133 + 789783 + 780013)
        self.assertFalse(any(o['date'] == '2026-07' for o in data['observations']))

    def test_missing_quarter_is_not_bridged(self):
        raw = self.modified(lambda rows: rows.remove(next(r for r in rows if r[0] == '2025 Q4')))
        data = parse_gdp(raw)
        self.assertIsNone(data['observations'][-1]['rollingAnnualMillion'])
        self.assertIsNone(next(r for r in data['observations'] if r['date'] == '2025-12')['rollingAnnualMillion'])

    def test_wrong_series_and_nonpositive_gdp_fail(self):
        raw = self.modified(lambda rows: rows[1].__setitem__(1, 'YBHA'))
        with self.assertRaisesRegex(ValueError, 'Expected ONS BKTL'):
            parse_gdp(raw)
        raw = self.modified(lambda rows: rows[-1].__setitem__(1, '0'))
        with self.assertRaisesRegex(ValueError, 'positive'):
            parse_gdp(raw)

    def test_duplicate_quarter_fails(self):
        raw = self.modified(lambda rows: rows.append(rows[-1].copy()))
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            parse_gdp(raw)

    def test_fiscal_refresh_includes_independent_gdp_source(self):
        inputs = {ONS_URL: FIXTURE.read_bytes(), GDP_URL: self.fixture.read_bytes()}
        data = fetch_fiscal(inputs.__getitem__)
        self.assertEqual(data['asOf'], '2026-07')
        self.assertEqual(data['gdp']['asOf'], '2026-06')
        self.assertEqual(data['gdp']['sources'][0]['id'], 'ons-gdp-bktl')

if __name__=='__main__':unittest.main()
