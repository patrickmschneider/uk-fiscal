import unittest
from pipeline.isa import compare_relief_releases,clean_number,table_year
class IsaTests(unittest.TestCase):
    def test_isa_missing_is_not_zero(self):
        self.assertIsNone(clean_number('[too small]'))
        self.assertIsNone(clean_number('[not available]'))
        self.assertEqual(clean_number('0'),0)
        with self.assertRaises(ValueError):clean_number('suppressed new code')
    def test_year_preserves_provisional_header(self):
        self.assertEqual(table_year('2023 to 2024[provisional]'),'2023-24')
    def test_comparison_detects_reclassification_and_deleted_added(self):
        old={'reliefs':[{'hmrcCode':'A','name':'Original','taxHead':'VAT','classification':'structural'},{'hmrcCode':'B','name':'Removed','taxHead':'VAT','classification':'structural'}]}
        new={'reliefs':[{'hmrcCode':'A','name':'Original','taxHead':'VAT','classification':'non-structural'},{'hmrcCode':'C','name':'Added','taxHead':'VAT','classification':'structural'}]}
        result=compare_relief_releases(old,new)
        self.assertEqual(result['added'],['Added']);self.assertEqual(result['removed'],['Removed'])
        self.assertEqual(result['changed'][0]['fields'],['classification'])
    def test_comparison_ignores_retrieval_timestamp(self):
        row={'hmrcCode':'A','name':'A','taxHead':'VAT','retrievalDate':'one'}
        self.assertEqual(compare_relief_releases({'reliefs':[row]},{'reliefs':[{**row,'retrievalDate':'two'}]})['changed'],[])
