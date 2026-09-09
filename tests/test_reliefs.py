import unittest
from pipeline.reliefs import estimate,number,parse_pension,ods_rows,validate_reliefs
from io import BytesIO
from zipfile import ZipFile

class ReliefTests(unittest.TestCase):
    def test_missing_estimates_are_never_zero(self):
        for raw,status in [('Negligible','negligible'),('Disclosive','withheld'),('Not available','unavailable')]:
            e=estimate(raw,'2024-25')
            self.assertIsNone(e['costMillion']);self.assertEqual(e['status'],status)
        self.assertEqual(estimate('0','2024-25')['costMillion'],0)
        with self.assertRaises(ValueError):estimate('new unknown suppression','2024-25')
    def test_forecast_starts_at_relief_specific_year(self):
        self.assertEqual(estimate('1,200','2023-24','2024-25')['status'],'estimate')
        self.assertEqual(estimate('1,200','2024-25','2024-25')['status'],'forecast')
        self.assertTrue(estimate('Not available','2025-26','2024-25')['isForecast'])
    def test_ods_repeated_columns_preserve_column_alignment(self):
        raw=BytesIO()
        with ZipFile(raw,'w') as z:
            z.writestr('content.xml','''<root xmlns:t="urn:oasis:names:tc:opendocument:xmlns:table:1.0"><t:table t:name="Table_2"><t:table-row><t:table-cell>A</t:table-cell><t:table-cell t:number-columns-repeated="2"/><t:table-cell>B</t:table-cell><t:table-cell t:number-columns-repeated="1000000"/></t:table-row></t:table></root>''')
        row=ods_rows(raw.getvalue())['Table_2'][0]
        self.assertEqual(row[:4],['A','','','B']);self.assertEqual(len(row),20)
    def test_pension_not_applicable_remains_missing(self):
        d=parse_pension(b'tax_year,value_of_relief,tax_rate\n2024 to 2025,[z],Additional Rate\n')
        self.assertIsNone(d[0]['costMillion']);self.assertEqual(d[0]['status'],'not applicable')
    def test_malformed_pension_input_fails(self):
        with self.assertRaises(ValueError):parse_pension(b'tax_year,value\nbad year,100\n')
    def test_truncated_relief_dataset_fails(self):
        with self.assertRaises(ValueError):validate_reliefs({'reliefs':[]})
    def test_malformed_claimant_year_header_rejected(self):
        from unittest.mock import patch
        from pipeline.reliefs import parse_reliefs
        years=[f'{y} to {y+1}' for y in range(2020,2026)]
        header=['Name','Code','Tax type','Relief type','First forecast']+years
        sheets={key:[[],header,[]] for key in ('Table_2','Table_3','Table_4')}
        sheets['Table_5']=[[],header[:5]+['not a year']*6,[]]
        with patch('pipeline.reliefs.ods_rows',return_value=sheets):
            with self.assertRaisesRegex(ValueError,'claimant year'):parse_reliefs(b'not used')
