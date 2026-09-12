import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool
import publishing.workflow as push
import test_approved_rebuild as rebuild_tests


class PushTests(unittest.TestCase):
    def setUp(self):
        rebuild_tests.ApprovedRebuildTests.setUp(self)
        self.history = self.root / 'runs' / self.report['run_id']
        self.history.mkdir(parents=True)
        for name in tool.ARTIFACT_FILENAMES:
            shutil.copy2(self.root / name, self.history / name)
        self.archive = self.history / 'image.oci.tar'
        self.report.update(oci_archive=str(self.archive.relative_to(self.root)), build_tags=self.report['tags'],
                           steps=[{'name': 'export_oci_image', 'status': 'passed'}])
        self.save_approval()
        self.blobs = {}

        def blob(data, media_type):
            raw = data if isinstance(data, bytes) else json.dumps(data).encode()
            digest = push.sha256(raw)
            self.blobs['blobs/' + digest.replace(':', '/')] = raw
            return {'digest': digest, 'size': len(raw), 'mediaType': media_type}

        manifests = []
        for target in self.group:
            config = blob({'os': 'linux', 'architecture': target.platform.split('/')[1], 'config': {'Labels': {'test': 'retained'}}},
                          'application/vnd.oci.image.config.v1+json')
            layer = blob(b'layer contents', 'application/vnd.oci.image.layer.v1.tar')
            manifest = blob({'schemaVersion': 2, 'config': config, 'layers': [layer]}, 'application/vnd.oci.image.manifest.v1+json')
            manifest['platform'] = {'os': 'linux', 'architecture': target.platform.split('/')[1]}
            manifests.append(manifest)
        index = {'schemaVersion': 2, 'mediaType': 'application/vnd.oci.image.index.v1+json', 'manifests': manifests}
        self.root_descriptor = blob(index, 'application/vnd.oci.image.index.v1+json')
        self.root_raw = json.dumps(index)
        self.blobs['index.json'] = json.dumps({'schemaVersion': 2, 'manifests': [dict(self.root_descriptor,
            annotations={'org.opencontainers.image.ref.name': t.split(':', 1)[1]}) for t in self.report['tags']]}).encode()
        self.blobs['oci-layout'] = b'{"imageLayoutVersion":"1.0.0"}'
        self.write_archive()
        self.arguments = ['push', '--version', '3.4.1', '--os-id', 'alpine-3.21-x86_64', '--otp', '26',
                          '--scan-retries', '1', '--scan-retry-delay', '0']
        self.options = tool.parser().parse_args(self.arguments)
        self.options.skopeo = 'skopeo'
        self.options.docker = 'docker'
        self.options.auth_args = []
        self.registry = {}
        self.events = []
        self.fail_tag = None
        self.scan_failures = 0

    def save_approval(self):
        tool.write_json(self.root / 'report.json', self.report)
        tool.write_json(self.history / 'report.json', self.report)

    def write_archive(self):
        with tarfile.open(self.archive, 'w') as archive:
            for name, raw in self.blobs.items():
                member = tarfile.TarInfo(name)
                member.size = len(raw)
                archive.addfile(member, io.BytesIO(raw))

    def use_single_manifest(self, descriptor, include_platform=True):
        self.root_descriptor = dict(descriptor)
        if not include_platform:
            self.root_descriptor.pop('platform', None)
        self.root_raw = self.blobs['blobs/' + descriptor['digest'].replace(':', '/')].decode()
        self.blobs['index.json'] = json.dumps({'schemaVersion': 2, 'manifests': [
            dict(self.root_descriptor, annotations={'org.opencontainers.image.ref.name': t.split(':', 1)[1]})
            for t in self.report['tags']]}).encode()
        self.write_archive()

    def test_direct_manifests_preserve_digest_and_validate_platforms(self):
        descriptors = json.loads(self.root_raw)['manifests']
        for descriptor in descriptors:
            platform = 'linux/' + descriptor['platform']['architecture']
            for include_platform in (True, False):
                with self.subTest(platform=platform, include_platform=include_platform):
                    self.use_single_manifest(descriptor, include_platform)
                    archive = push.archive_metadata(self.archive, [platform])
                    self.assertEqual(archive['digest'], descriptor['digest'])
                    self.assertEqual(set(archive['platforms']), {platform})
                    self.assertIsNone(archive['index'])
                    self.assertEqual(archive['manifest'], json.loads(self.root_raw))
                    self.assertEqual(archive['manifests'][descriptor['digest']]['config']['config']['Labels'],
                                     {'test': 'retained'})
                    with self.assertRaisesRegex(ValueError, 'every approved platform'):
                        push.archive_metadata(self.archive, self.report['platforms'])
        descriptor = dict(descriptors[0], platform={'os': 'linux', 'architecture': 'incorrect'})
        self.use_single_manifest(descriptor)
        with self.assertRaisesRegex(ValueError, 'configuration/platform mismatch'):
            push.archive_metadata(self.archive, ['linux/incorrect'])

    def test_direct_manifest_push_and_scan_use_original_digest(self):
        descriptor = json.loads(self.root_raw)['manifests'][0]
        self.use_single_manifest(descriptor, include_platform=False)
        platform = 'linux/' + descriptor['platform']['architecture']
        plan = {'image': self.report['image'], 'approval': self.report,
                'approval_path': str(self.root / 'report.json'),
                'approval_sha256': tool.sha256_file(self.root / 'report.json'),
                'archive_path': str(self.archive), 'archive_sha256': tool.sha256_file(self.archive),
                'tags': self.report['tags'], 'archive': push.archive_metadata(self.archive, [platform])}
        report = {'pushes': [], 'scans': {}}
        with mock.patch.object(push, 'execute', side_effect=self.fake_execute), contextlib.redirect_stdout(io.StringIO()):
            push.push_tags(plan, report, self.options, tool, lambda: None)
            push.scan_image(plan, report, self.options, tool, lambda: None)
        self.assertTrue(all(p['verified'] and p['registry_digest'] == descriptor['digest'] for p in report['pushes']))
        self.assertEqual(report['scan_status'], 'complete')
        self.assertEqual(set(report['scans']), {platform})
        scans = [c for c in self.events if 'scout' in c]
        self.assertEqual(len(scans), 3)
        self.assertTrue(all(c[-1].endswith('@' + descriptor['digest']) for c in scans))

    def fake_execute(self, command, timeout):
        self.events.append(command)
        result = {'command': command, 'exit_code': 0, 'stdout': '', 'stderr': '', 'error': None}
        if command[-1] in ('--version', 'version'):
            result['stdout'] = 'test-version'
        elif command[-2:] == ['copy', '--help']:
            result['stdout'] = '--all --preserve-digests'
        elif 'inspect' in command:
            tag = command[-1].removeprefix('docker://docker.io/')
            result.update(stdout=self.registry.get(tag, ''), exit_code=0 if tag in self.registry else 1)
        elif 'copy' in command and '--help' not in command:
            tag = command[-1].removeprefix('docker://docker.io/')
            if tag == self.fail_tag:
                result.update(exit_code=1, stderr='Upload failed')
            else:
                self.registry[tag] = self.root_raw
        elif 'scout' in command:
            if self.scan_failures:
                self.scan_failures -= 1
                result.update(exit_code=1, stderr='Not indexed yet')
            elif 'sarif' in command:
                result['stdout'] = json.dumps({'version': '2.1.0', 'runs': [{'tool': {'driver': {'name': 'scout', 'rules': [
                    {'id': 'CVE-2026-1234', 'properties': {'fixed_version': '2', 'purls': ['pkg:apk/example@1']}}]}},
                    'results': [{'ruleId': 'CVE-2026-1234', 'message': {'text': 'Full evidence'}, 'properties': {'additional': 'kept'}}]}]})
            elif 'sbom' in command:
                result['stdout'] = json.dumps({'artifacts': [{'name': 'example', 'licenses': ['MIT'], 'locations': ['/lib/example']}],
                                              'source': {'target': {'manifestDigest': command[-1].split('@')[-1]}}})
            else:
                result['stdout'] = 'Full CVE details, CVSS and EPSS'
        else:
            raise AssertionError(command)
        return result

    def run_main(self, extra=()):
        with mock.patch.object(push, 'execute', side_effect=self.fake_execute), \
                mock.patch.object(push.shutil, 'which', side_effect=lambda n: n), \
                mock.patch.object(push, 'docker_auth', return_value=contextlib.nullcontext([])), \
                mock.patch.object(push.time, 'sleep', side_effect=lambda n: self.events.append(['sleep', n])), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return tool.main([*self.arguments, *extra])

    def reports(self):
        from publishing.cve_storage import hydrate_report
        return [hydrate_report(p) for p in sorted(Path(self.temporary.name).glob('pushes/*/*/*/cve-report.json'))]

    def test_all_aliases_and_platforms_are_pushed_then_scanned_by_digest(self):
        before = (self.root / 'report.json').read_bytes()
        self.assertEqual(self.run_main(['--extra-namespace', 'tiotjp']), 0)
        report, = self.reports()
        expected_tags = tool.namespaced_tags(self.report['tags'], ['tiotjp'])
        self.assertEqual([p['tag'] for p in report['pushes']], expected_tags)
        copies = [c for c in self.events if 'copy' in c and '--help' not in c]
        self.assertEqual(len(copies), len(expected_tags))
        for c in copies:
            self.assertIn('--all', c)
            self.assertIn('--preserve-digests', c)
            self.assertIn(f'oci-archive:{self.archive}:{self.target.image_tag}', c)
        wait = self.events.index(['sleep', 5])
        self.assertTrue(all(self.events.index(c) < wait for c in copies))
        scans = [c for c in self.events if 'scout' in c and c[-1] != 'version']
        self.assertEqual(len(scans), 3 * len(self.group))
        self.assertTrue(all(self.events.index(c) > wait for c in scans))
        self.assertTrue(all(c[-1].startswith('registry://docker.io/openriak/openriak-kv@sha256:') for c in scans))
        for record in report['scans'].values():
            self.assertEqual(record['finding_count'], 1)
            self.assertEqual(record['cve_ids'], ['CVE-2026-1234'])
            self.assertEqual(record['sarif']['data']['runs'][0]['results'][0]['properties'], {'additional': 'kept'})
            self.assertEqual(record['sbom']['data']['artifacts'][0]['licenses'], ['MIT'])
        self.assertEqual(report['status'], 'complete')  # CVEs do not mean scan failure.
        self.assertEqual((self.root / 'report.json').read_bytes(), before)

    def test_already_published_digest_skips_upload_but_scans(self):
        self.registry = {tag: self.root_raw for tag in self.report['tags']}
        self.assertEqual(self.run_main(), 0)
        self.assertFalse(any('copy' in c and '--help' not in c for c in self.events))
        report, = self.reports()
        self.assertTrue(all(p['status'] == 'already_present' for p in report['pushes']))
        self.assertEqual(report['scan_status'], 'complete')

    def test_failed_alias_does_not_scan_wrong_digest_and_other_aliases_continue(self):
        self.fail_tag = self.report['tags'][0]
        self.registry[self.fail_tag] = '{"schemaVersion":2,"manifests":[]}'
        self.assertEqual(self.run_main(), 1)
        report, = self.reports()
        self.assertFalse(report['pushes'][0]['verified'])
        self.assertTrue(all(p['verified'] for p in report['pushes'][1:]))
        self.assertEqual(report['scan_status'], 'complete')
        self.assertEqual(report['status'], 'failed')

    def test_no_verified_push_means_no_scan(self):
        original = self.fake_execute
        def fail_copies(command, timeout):
            if 'copy' in command and '--help' not in command:
                self.fail_tag = command[-1].removeprefix('docker://docker.io/')
            return original(command, timeout)
        with mock.patch.object(self, 'fake_execute', side_effect=fail_copies):
            self.assertEqual(self.run_main(), 1)
        report, = self.reports()
        self.assertEqual(report['scan_status'], 'not_scanned_no_verified_push')
        self.assertFalse(report['scans'])

    def test_scan_retries_and_failure_preserve_all_attempts(self):
        self.scan_failures = 1
        self.assertEqual(self.run_main(), 0)
        report, = self.reports()
        first = next(iter(report['scans'].values()))
        self.assertEqual(len(first['sarif']['attempts']), 2)
        self.assertEqual(first['sarif']['attempts'][0]['stderr'], 'Not indexed yet')
        self.scan_failures = 100
        self.assertEqual(self.run_main(), 1)
        last = self.reports()[-1]
        self.assertEqual(last['scan_status'], 'failed')
        self.assertTrue(all('finding_count' not in s for s in last['scans'].values()))

    def test_whatif_requires_no_tools_credentials_network_or_writes(self):
        files = set(Path(self.temporary.name).rglob('*'))
        with mock.patch.object(push, 'execute', side_effect=AssertionError('external command')), \
                mock.patch.object(push, 'docker_auth', side_effect=AssertionError('credentials')), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(tool.main([*self.arguments, '--whatif']), 0)
        self.assertEqual(set(Path(self.temporary.name).rglob('*')), files)

    def test_push_accepts_published_portable_approval_without_rewriting_history(self):
        saved = json.loads(json.dumps(self.report))
        for artifact in saved['artifacts'].values():
            artifact['url'] = './' + artifact['filename']
        tool.write_json(self.history / 'report.json', saved)
        historical = (self.history / 'report.json').read_bytes()
        for status in ('running', 'passed', 'failed'):
            current = dict(self.report, publication={'status': status, 'finished_at': '2026-09-12T00:00:00Z'})
            tool.write_json(self.root / 'report.json', current)
            with self.subTest(status=status), \
                    mock.patch.object(push, 'execute', side_effect=AssertionError('no external command')), \
                    mock.patch.object(push, 'docker_auth', side_effect=AssertionError('no credentials')), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tool.main([*self.arguments, '--whatif']), 0)
            self.assertEqual((self.history / 'report.json').read_bytes(), historical)
            self.assertEqual(tool.read_json(self.root / 'report.json'), current)

    def test_publication_equivalence_keeps_all_test_and_build_evidence_strict(self):
        saved = json.loads(json.dumps(self.report))
        for artifact in saved['artifacts'].values():
            artifact['url'] = './' + artifact['filename']
        tool.write_json(self.history / 'report.json', saved)
        for field, value in [('finished_at', 'changed'), ('inputs', {'changed': True}),
                             ('tags', [self.target.image, 'openriak/openriak-kv:unapproved']),
                             ('worker', {'host': 'different'}), ('steps', []),
                             ('platform_results', {})]:
            current = dict(self.report, publication={'status': 'passed'}, **{field: value})
            tool.write_json(self.root / 'report.json', current)
            with self.subTest(field=field), contextlib.redirect_stdout(io.StringIO()):
                _, plans, _, blocked = push.make_plan(self.options, tool)
            self.assertEqual(plans, [])
            self.assertEqual(len(blocked), 1)

    def test_publication_equivalence_does_not_ignore_unknown_urls_or_artifact_fields(self):
        for location in ('current', 'history'):
            for field, value in [('url', 'https://unexpected.example/Dockerfile'),
                                 ('sha256', 'a' * 64), ('filename', 'different'),
                                 ('extra', 'unapproved')]:
                with self.subTest(location=location, field=field):
                    self.save_approval()
                    changed = json.loads(json.dumps(self.report))
                    changed['artifacts']['dockerfile'][field] = value
                    path = self.root / 'report.json' if location == 'current' else self.history / 'report.json'
                    tool.write_json(path, changed)
                    _, plans, _, blocked = push.make_plan(self.options, tool)
                    self.assertEqual(plans, [])
                    self.assertEqual(len(blocked), 1)

    def test_old_skopeo_is_blocked_before_upload_or_credentials(self):
        original = self.fake_execute
        def old_skopeo(command, timeout):
            result = original(command, timeout)
            if command[-2:] == ['copy', '--help']:
                result['stdout'] = '--all --format'
            return result
        files = set(Path(self.temporary.name).rglob('*'))
        with mock.patch.object(self, 'fake_execute', side_effect=old_skopeo):
            self.assertEqual(self.run_main(), 2)
        self.assertFalse(any('inspect' in c or ('copy' in c and '--help' not in c) for c in self.events))
        self.assertEqual(set(Path(self.temporary.name).rglob('*')), files)

    def test_changed_approval_missing_archive_and_tampered_blob_block_before_push(self):
        original = (self.root / 'Dockerfile').read_bytes()
        (self.root / 'Dockerfile').write_text('modified')
        self.assertEqual(self.run_main(), 2)
        self.assertFalse(self.events)
        (self.root / 'Dockerfile').write_bytes(original)
        self.archive.unlink()
        self.assertEqual(self.run_main(), 2)
        self.assertFalse(self.events)
        key = next(k for k in self.blobs if k.startswith('blobs/'))
        self.blobs[key] = b'corrupted content'
        self.write_archive()
        self.assertEqual(self.run_main(), 2)
        self.assertFalse(self.events)

    def test_archive_rejects_missing_platform_and_symlink(self):
        with self.assertRaisesRegex(ValueError, 'Unexpected'):
            push.archive_metadata(self.archive, [])
        with tarfile.open(self.archive, 'a') as archive:
            member = tarfile.TarInfo('unsafe-link')
            member.type = tarfile.SYMTYPE
            member.linkname = '/etc/passwd'
            archive.addfile(member)
        with self.assertRaisesRegex(ValueError, 'Non-regular'):
            push.archive_metadata(self.archive, self.report['platforms'])

    def test_interruption_keeps_report_and_leaves_approval_alone(self):
        original = self.fake_execute
        def interrupt(command, timeout):
            if 'copy' in command and '--help' not in command:
                raise KeyboardInterrupt
            return original(command, timeout)
        with mock.patch.object(self, 'fake_execute', side_effect=interrupt):
            self.assertEqual(self.run_main(), 130)
        report, = self.reports()
        self.assertEqual(report['status'], 'interrupted')
        self.assertEqual(tool.read_json(self.root / 'report.json')['status'], 'passed')

    def test_cli_guards_and_nonfinite_waits(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(tool.main(['push', '--all']), 2)
            self.assertEqual(tool.main([*self.arguments, '--namespace', 'BAD/namespace']), 2)
            for extra in (['--wait-seconds', 'nan'], ['--wait-seconds', '-1'], ['--timeout', '0'], ['--scan-retries', '-1']):
                self.assertEqual(tool.main([*self.arguments, *extra]), 2)

    def test_credential_helper_bridge_is_private_and_removed_without_secret_logging(self):
        config = Path(self.temporary.name) / 'docker-config'
        config.mkdir()
        tool.write_json(config / 'config.json', {'credsStore': 'test-helper'})
        result = subprocess.CompletedProcess([], 0, json.dumps({'Username': 'user', 'Secret': 'private-test-token'}).encode(), b'')
        with mock.patch.dict(os.environ, {'DOCKER_CONFIG': str(config)}), \
                mock.patch.object(push.subprocess, 'run', return_value=result) as run:
            with push.docker_auth(self.options, tool) as args:
                path = Path(args[1])
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)
                self.assertEqual(set(tool.read_json(path)['auths']), {'docker.io'})
                self.assertNotIn('private-test-token', str(run.call_args))
                self.assertEqual(run.call_args.kwargs['input'], b'https://index.docker.io/v1/\n')
            self.assertFalse(path.exists())

    def test_timeout_retains_partial_output_and_is_not_success(self):
        with mock.patch.object(push.subprocess, 'run', side_effect=subprocess.TimeoutExpired(['test'], 1, b'partial', b'failed')):
            result = push.execute(['test'], 1)
        self.assertIsNone(result['exit_code'])
        self.assertEqual(result['stdout'], 'partial')
        self.assertIn('timed out', result['error'])

    def test_malformed_sarif_is_retried_and_never_claims_zero_findings(self):
        record = {}
        result = {'exit_code': 0, 'stdout': '{"version":"2.1.0","runs":[]}', 'stderr': '', 'error': None}
        with mock.patch.object(push, 'execute', side_effect=lambda *a: dict(result)), mock.patch.object(push.time, 'sleep'):
            push.collect_scout('registry://example@sha256:abc', 'linux/amd64', 'sarif', self.options, record, lambda: None)
        self.assertEqual(record['sarif']['status'], 'failed')
        self.assertEqual(len(record['sarif']['attempts']), 2)
        self.assertNotIn('data', record['sarif'])

    def test_valid_sarif_with_no_findings_is_accepted(self):
        record = {}
        data = {'version': '2.1.0', 'runs': [{'tool': {'driver': {'name': 'scout'}}, 'results': []}]}
        with mock.patch.object(push, 'execute', return_value={'exit_code': 0, 'stdout': json.dumps(data)}):
            push.collect_scout('registry://example@sha256:abc', 'linux/amd64', 'sarif', self.options, record, lambda: None)
        self.assertEqual(record['sarif']['status'], 'complete')
        self.assertEqual(record['sarif']['data'], data)

    def test_copy_error_after_registry_commit_is_reported_and_scanned(self):
        original = self.fake_execute
        def copy_error(command, timeout):
            result = original(command, timeout)
            if 'copy' in command and '--help' not in command:
                result.update(exit_code=1, stderr='Connection closed after manifest upload')
            return result
        with mock.patch.object(self, 'fake_execute', side_effect=copy_error):
            self.assertEqual(self.run_main(), 1)
        report, = self.reports()
        self.assertTrue(all(p['verified'] and p['status'] == 'verified_after_copy_error' for p in report['pushes']))
        self.assertEqual(report['scan_status'], 'complete')


if __name__ == '__main__':
    unittest.main()
