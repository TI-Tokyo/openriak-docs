import argparse
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool
from cache import storage


class StorageTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for name, value in {'REPOSITORY': self.root, 'WORK': self.root / '.work/openriak-docker',
                            'RECORDS': self.root / 'records/openriak-docker',
                            'ARTIFACTS': self.root / 'artifacts/openriak-docker'}.items():
            patch = mock.patch.object(storage, name, value)
            patch.start()
            self.addCleanup(patch.stop)
        self.relative = Path('images/3.4.1/example/report.json')
        self.report = {'status': 'passed', 'artifacts': {'dockerfile': {
            'filename': 'Dockerfile', 'sha256': storage.digest(b'approved')}}}
        self.path = storage.WORK / self.relative
        self.path.parent.mkdir(parents=True)
        (self.path.parent / 'Dockerfile').write_bytes(b'approved')
        self.path.write_bytes(storage.encoded(self.report))

    def test_snapshots_are_immutable_and_pointer_selects_latest(self):
        storage.capture_file(self.path)
        before = list(storage.RECORDS.rglob('history/*.json'))
        original = before[0].read_bytes()
        self.path.write_bytes(storage.encoded(dict(self.report, status='failed')))
        storage.capture_file(self.path)
        self.assertEqual(before[0].read_bytes(), original)
        self.assertEqual(len(list(storage.RECORDS.rglob('history/*.json'))), 2)
        self.assertEqual(json.loads(dict(storage.record_entries(storage.RECORDS))[self.relative])['status'], 'failed')

    def test_missing_work_can_be_restored_without_oci_or_raw_payloads(self):
        storage.capture_file(self.path)
        destination = self.root / 'fresh'
        storage.restore(destination)
        self.assertEqual((destination / self.relative).read_bytes(), self.path.read_bytes())
        self.assertEqual((destination / self.relative.parent / 'Dockerfile').read_bytes(), b'approved')
        self.assertEqual(list(destination.rglob('*.oci.tar')), [])

    def test_tampered_snapshot_and_invalid_pointer_are_rejected(self):
        storage.capture_file(self.path)
        snapshot = next(storage.RECORDS.rglob('history/*.json'))
        snapshot.write_text('{}')
        with self.assertRaisesRegex(ValueError, 'integrity'):
            list(storage.record_entries(storage.RECORDS))

    def test_tampered_download_does_not_replace_approved_source(self):
        storage.capture_file(self.path)
        (self.path.parent / 'Dockerfile').write_text('tampered')
        storage.capture_file(self.path)
        self.assertEqual((storage.ARTIFACTS / self.relative.parent / 'Dockerfile').read_bytes(), b'approved')

    def test_standalone_output_and_running_state_are_not_promoted(self):
        other = self.root / 'standalone/report.json'
        other.parent.mkdir()
        other.write_bytes(self.path.read_bytes())
        storage.capture_file(other)
        self.path.write_bytes(storage.encoded(dict(self.report, status='running')))
        storage.capture_file(self.path)
        self.assertFalse(storage.RECORDS.exists())

    def test_readonly_view_does_not_recreate_work_or_change_records(self):
        storage.capture_file(self.path)
        before = {p: p.read_bytes() for p in storage.RECORDS.rglob('*.json')}
        self.path.unlink()
        with mock.patch.object(tool, 'MULTIARCH_CACHE_ROOT', storage.WORK / 'images'), \
                mock.patch.object(tool, 'CACHE_ROOT', storage.WORK / 'legacy'):
            with storage.session(tool, argparse.Namespace(command='status', whatif=False)):
                self.assertEqual(json.loads((tool.MULTIARCH_CACHE_ROOT / '3.4.1/example/report.json').read_text()), self.report)
                self.assertFalse(self.path.exists())
        self.assertEqual(before, {p: p.read_bytes() for p in storage.RECORDS.rglob('*.json')})
        self.assertFalse(self.path.exists())

    def test_security_normalization_retains_rules_scores_versions_and_counts(self):
        rule = {'id': 'CVE-2026-1234', 'properties': {'security-severity': '7.5', 'fixed_version': '2'}}
        finding = {'ruleId': rule['id'], 'ruleIndex': 0, 'message': {'text': 'duplicate location'}}
        report = {'scans': {'linux/amd64': {'sarif': {'data': {'runs': [{
            'tool': {'driver': {'rules': [rule]}}, 'results': [finding, finding]}]}}}}}
        result = storage.compact_security(self.path, report)
        run = result['scans']['linux/amd64']['sarif']['data']['runs'][0]
        self.assertEqual(run['tool']['driver']['rules'], [rule])
        self.assertEqual(run['results'], [{'ruleId': rule['id'], 'ruleIndex': 0, 'occurrences': 2}])
        self.assertEqual(len(report['scans']['linux/amd64']['sarif']['data']['runs'][0]['results']), 2)
