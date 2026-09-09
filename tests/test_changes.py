import unittest
from pipeline.changes import compare_release
class ChangesTests(unittest.TestCase):
 def test_history_revisions_are_not_new_periods(self):
  a={'observations':[{'date':'2026-01','receipts':1000}]};b={'observations':[{'date':'2026-01','receipts':1200},{'date':'2026-02','receipts':1000}]}
  x=compare_release('fiscal',a,b)
  self.assertEqual(x['revisedValues'],1);self.assertEqual(x['addedPeriods'],['2026-02']);self.assertEqual(len(x['largeRevisions']),1)
 def test_disappearing_history_rejected(self):
  with self.assertRaises(ValueError):compare_release('fiscal',{'observations':[{'date':'2026-01'}]},{'observations':[]})
 def test_forecast_vintage_cannot_disappear(self):
  with self.assertRaises(ValueError):compare_release('outlook',{'vintages':[{'id':'old'}]},{'vintages':[{'id':'new'}]})
