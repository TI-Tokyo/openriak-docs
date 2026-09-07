import copy
import gzip
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import openriak_cve_storage as storage


class CveStorageTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'cve-report.json'
        self.data = {'version': '2.1.0', 'runs': [{'results': [
            {'ruleId': 'CVE-2026-1234', 'locations': ['/lib/example'] * 1000}]}]}
        self.raw = json.dumps(self.data, indent=3) + '\n'
        self.report = {'schema_version': 1, 'status': 'complete', 'scans': {'linux/amd64': {
            'sarif': {'status': 'complete', 'data': self.data, 'attempts': [
                {'exit_code': 1, 'stdout': 'incomplete JSON {', 'stderr': 'try again'},
                {'exit_code': 0, 'stdout': self.raw, 'stderr': 'diagnostics'}]},
            'details': {'status': 'complete', 'data': 'Details: 日本語\n',
                        'attempts': [{'stdout': 'Details: 日本語\n'}]}}}}
        self.path.write_text(json.dumps(self.report, indent=2))

    def test_round_trip_preserves_every_field_and_exact_stdout_once(self):
        before = self.path.read_bytes()
        self.assertTrue(storage.migrate_report(self.path))
        compact = json.loads(self.path.read_text())
        output = compact['scans']['linux/amd64']['sarif']
        self.assertNotIn('data', output)
        self.assertNotIn('stdout', output['attempts'][1])
        self.assertEqual(output['data_file']['path'], output['attempts'][1]['stdout_file']['path'])
        self.assertEqual(storage.read_output(self.path, output['attempts'][1]['stdout_file']), self.raw)
        self.assertEqual(len(list(self.path.parent.glob('scout-output/*.gz'))), 3)
        restored = storage.hydrate_report(self.path)
        restored.pop('storage_migration')
        restored['schema_version'] = 1
        self.assertEqual(restored, self.report)
        self.assertLess(sum(p.stat().st_size for p in self.path.parent.rglob('*') if p.is_file()), len(before))
        after = self.path.read_bytes()
        self.assertFalse(storage.migrate_report(self.path))
        self.assertEqual(self.path.read_bytes(), after)

    def test_legacy_edited_parsed_data_is_retained_separately(self):
        self.report['scans']['linux/amd64']['sarif']['data'] = {'edited': True}
        storage.write_report(self.path, self.report)
        output = self.report['scans']['linux/amd64']['sarif']
        self.assertNotEqual(output['data_file']['path'], output['attempts'][1]['stdout_file']['path'])
        full = storage.hydrate_report(self.path)['scans']['linux/amd64']['sarif']
        self.assertEqual(full['data'], {'edited': True})
        self.assertEqual(full['attempts'][1]['stdout'], self.raw)

    def test_bad_sidecar_is_rejected_and_original_report_survives_failed_migration(self):
        original = self.path.read_bytes()
        with mock.patch.object(storage, 'store_output', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                storage.migrate_report(self.path)
        self.assertEqual(self.path.read_bytes(), original)
        storage.migrate_report(self.path)
        ref = json.loads(self.path.read_text())['scans']['linux/amd64']['sarif']['data_file']
        sidecar = self.path.parent / ref['path']
        sidecar.write_bytes(gzip.compress(b'{}'))
        with self.assertRaisesRegex(ValueError, 'integrity'):
            storage.hydrate_report(self.path)
        sidecar.unlink()
        with self.assertRaises(FileNotFoundError):
            storage.hydrate_report(self.path)

    def test_running_reports_are_not_replaced(self):
        self.report['status'] = 'scanning'
        self.path.write_text(json.dumps(self.report))
        original = self.path.read_bytes()
        with self.assertRaisesRegex(ValueError, 'still be in use'):
            storage.migrate_report(self.path)
        self.assertEqual(self.path.read_bytes(), original)

    def test_invalid_paths_and_symlinks_are_rejected(self):
        storage.migrate_report(self.path)
        ref = json.loads(self.path.read_text())['scans']['linux/amd64']['sarif']['data_file']
        with self.assertRaises(ValueError):
            storage.read_output(self.path, {**ref, 'path': '../escape.gz'})
        with tempfile.TemporaryDirectory() as outside:
            file = self.path.parent / ref['path']
            target = Path(outside) / 'output.gz'
            target.write_bytes(file.read_bytes())
            file.unlink()
            file.symlink_to(target)
            with self.assertRaisesRegex(ValueError, 'escapes'):
                storage.read_output(self.path, ref)


if __name__ == '__main__':
    unittest.main()
