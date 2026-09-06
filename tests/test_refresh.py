import json
from pathlib import Path
import tempfile
import unittest
from pipeline.refresh import refresh,validate,promote,Fetcher,encode

class RefreshTests(unittest.TestCase):
    def test_failure_preserves_last_good_and_sets_failed_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);file=root/'public/data/composition.json';file.parent.mkdir(parents=True)
            saved=b'{"saved":"previous"}';file.write_bytes(saved)
            def fail(fetch):raise ValueError('corrupt spreadsheet')
            self.assertEqual(refresh(['composition'],root=root,adapters={'composition':fail}),['composition'])
            self.assertEqual(file.read_bytes(),saved)
            manifest=json.loads((file.parent/'manifest.json').read_text())
            self.assertEqual(manifest['groups']['composition']['status'],'failed')

    def test_archive_before_promotion_and_replay_idempotence(self):
        data={'schemaVersion':1,'asOf':'2025-26','years':[{'total':10,'items':[{'value':10}]}]}
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);fetch=Fetcher(root,offline=True)
            a=promote('composition',data,fetch,root);b=promote('composition',data,fetch,root)
            self.assertEqual(a,b)
            self.assertEqual((root/f'data/archive/releases/composition-{a}.json').read_bytes(),(root/'public/data/composition.json').read_bytes())

    def test_unsupported_schema_and_nan_fail(self):
        with self.assertRaisesRegex(ValueError,'Unsupported'):validate('debt',{'schemaVersion':2})
        with self.assertRaises(ValueError):validate('composition',{'schemaVersion':1,'years':[{'total':float('nan'),'items':[]}]})

if __name__=='__main__':unittest.main()
