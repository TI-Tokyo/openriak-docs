import argparse
import contextlib
import copy
import io
import pathlib
import tempfile
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool
import images.whatif as whatif


class WhatifTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.cache = pathlib.Path(self.temporary.name)
        patch = mock.patch.object(tool, 'MULTIARCH_CACHE_ROOT', self.cache)
        patch.start()
        self.addCleanup(patch.stop)
        self.targets = tool.discover_targets(['3.4.0', '3.4.1'])
        self.group = next(g for g in tool.grouped_targets(self.targets) if g[0].image_tag == '3.4.0-alpine-3.21-otp24')
        self.root = self.group[0].group_directory
        self.root.mkdir(parents=True)
        for filename in tool.ARTIFACT_FILENAMES:
            (self.root / filename).write_text('approved ' + filename)
        self.artifacts = tool.artifact_downloads(self.group[0], *(self.root / n for n in tool.ARTIFACT_FILENAMES))
        self.tags = tool.image_aliases(self.group[0], self.targets)
        self.inputs = tool.group_input(self.group, 5, self.tags)
        self.report = {
            'schema_version': tool.MULTIARCH_SCHEMA_VERSION, 'product': 'openriak-kv', 'version': '3.4.0',
            'status': 'passed', 'image': self.group[0].image, 'tags': self.tags, 'cluster_nodes': 5,
            'inputs': self.inputs, 'artifacts': self.artifacts, 'distributed_cookie': 'saved-cookie',
            'generated_artifacts': {n: tool.sha256_file(self.root / n) for n in tool.ARTIFACT_FILENAMES},
            'base_images': {t.platform: {'pinned': 'alpine@sha256:abc'} for t in self.group},
            'platforms': [t.platform for t in self.group], 'platform_results': {},
        }
        for target in self.group:
            proof = tool.initial_report(target, 'approved', 5, 'saved-cookie')
            proof.update(status='passed', finished_at=tool.isoformat(), artifacts=self.artifacts)
            proof['tests'] = {'admin_test': {'status': 'passed'}, 'preserved_cookie': {'status': 'passed'},
                              'cluster': {'status': 'passed', 'coordinator_cookie_adoption': 'passed'},
                              'cluster_admin_test': {str(i): {'status': 'passed'} for i in range(5)}}
            path = target.cache_directory / 'runs/approved/report.json'
            tool.write_json(path, proof)
            tool.write_json(target.cache_directory / 'report.json', proof)
            for name in tool.ARTIFACT_FILENAMES:
                (target.cache_directory / name).write_bytes((self.root / name).read_bytes())
            self.report['platform_results'][target.platform] = {
                'status': 'passed', 'run_id': 'approved', 'report': str(path.relative_to(self.root))}
        self.save()

    def save(self):
        tool.write_json(self.root / 'report.json', self.report)

    def plan(self, **overrides):
        options = argparse.Namespace(**dict({'do_not_test': False, 'extra_namespace': [], 'cluster_nodes': 5,
                                            'force': False, 'retry_failed': True}, **overrides))
        return whatif.inspect_group(tool, self.group, options, self.targets)

    def test_passed_group_skips_and_content_fingerprints_still_invalidate(self):
        self.assertEqual(self.plan()['action'], 'SKIP')
        for key in ('runtime_sha256', 'renderer_sha256'):
            with self.subTest(key=key):
                self.report['inputs'] = dict(self.inputs, **{key: 'old-code-hash'})
                self.save()
                plan = self.plan()
                self.assertEqual(plan['action'], 'REBUILD')
                self.assertTrue(any(whatif.INPUT_NAMES[key] + ' changed' in line for line in plan['reasons']))
                self.assertTrue(all(action == 'REBUILD + TEST' for _, action, _ in plan['platforms']))
                self.assertFalse(tool.group_is_passed(self.group, self.report, self.inputs))

    def test_input_differences_name_affected_package_and_setting(self):
        self.report['inputs'] = copy.deepcopy(self.inputs)
        self.report['inputs']['packages']['linux/amd64']['checksum'] = 'old-checksum'
        self.report['inputs']['cluster_nodes'] = 3
        self.save()
        reasons = '\n'.join(self.plan()['reasons'])
        self.assertIn('Package/base-image selection [linux/amd64] changed', reasons)
        self.assertIn('Cluster size changed: 3 -> 5', reasons)

    def test_incompatible_default_is_blocked_instead_of_claiming_it_will_build(self):
        (self.root / 'Dockerfile').write_text('modified')
        plan = self.plan(retry_failed=False)
        self.assertEqual(plan['action'], 'BLOCKED')
        self.assertIn('Requires --retry-failed or --force', plan['reasons'])
        self.assertTrue(any('Cached file content changed: Dockerfile' in line for line in plan['reasons']))

    def test_missing_artifact_is_reported(self):
        (self.root / 'example.env').unlink()
        plan = self.plan()
        self.assertIn('Missing cached file: example.env', plan['reasons'])
        self.assertEqual(plan['action'], 'REBUILD')

    def test_force_retests_all_passed_architectures(self):
        plan = self.plan(force=True)
        self.assertEqual(plan['action'], 'REBUILD')
        self.assertIn('--force requested', plan['reasons'][0])
        self.assertEqual([action for _, action, _ in plan['platforms']], ['REBUILD + TEST'] * 2)

    def test_partial_retry_keeps_matching_passed_architecture(self):
        self.report['status'] = 'failed'
        self.report['platform_results']['linux/arm64']['status'] = 'failed'
        self.save()
        arm = next(t for t in self.group if t.platform == 'linux/arm64')
        proof = tool.read_json(arm.cache_directory / 'report.json')
        proof['status'] = 'failed'
        tool.write_json(arm.cache_directory / 'report.json', proof)
        plan = self.plan()
        self.assertEqual(plan['action'], 'REBUILD')
        self.assertEqual([(p, a) for p, a, _ in plan['platforms']],
                         [('linux/amd64', 'SKIP'), ('linux/arm64', 'REBUILD + TEST')])
        self.assertIn("current report status is 'failed'", plan['platforms'][1][2])

    def test_no_cache_builds_without_retry_flag(self):
        (self.root / 'report.json').unlink()
        plan = self.plan(retry_failed=False)
        self.assertEqual(plan['action'], 'REBUILD')
        self.assertIn('No cached group report', plan['reasons'])

    def test_approved_rebuild_shows_extra_tags_without_retesting(self):
        self.report['inputs']['runtime_sha256'] = 'old-code'
        self.save()
        plan = self.plan(do_not_test=True, extra_namespace=['tiotjp'])
        self.assertEqual(plan['action'], 'REBUILD')
        self.assertTrue(any('tiotjp/openriak-kv:' in line for line in plan['reasons']))
        self.assertTrue(all('tests disabled' in reason for _, _, reason in plan['platforms']))

    def test_approved_mode_skips_nonpassed_reports(self):
        self.report['status'] = 'failed'
        self.save()
        self.assertEqual(self.plan(do_not_test=True)['action'], 'SKIP')

    def test_cli_is_read_only_and_does_not_require_docker(self):
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.cache.rglob('*') if p.is_file()}
        output = io.StringIO()
        with contextlib.ExitStack() as stack:
            for name in ('docker_command', 'refresh_group', 'rebuild_approved_group', 'write_json',
                         'resolve_base_image', 'publish_group', 'sync_download_metadata', 'render_group_assets'):
                stack.enter_context(mock.patch.object(tool, name, side_effect=AssertionError('whatif must not call ' + name)))
            # Keep the real fingerprint calculation: mocking render_group_assets would
            # otherwise make inspect.getsource fail before the read-only checks.
            stack.enter_context(mock.patch.object(tool, 'group_input', return_value=self.inputs))
            stack.enter_context(contextlib.redirect_stdout(output))
            result = tool.main(['refresh', '--version', '3.4.0', '--os-id', 'alpine-3.21-x86_64',
                                '--otp', '24', '--retry-failed', '--whatif'])
        self.assertEqual(result, 0)
        self.assertIn('WOULD SKIP', output.getvalue())
        self.assertIn('0 group(s) would rebuild, 1 would skip, 0 blocked', output.getvalue())
        after = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.cache.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_all_whatif_does_not_require_yes_and_uses_padded_counters(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), mock.patch.object(tool, 'docker_command', side_effect=AssertionError('no Docker')):
            self.assertEqual(tool.main(['refresh', '--all', '--whatif', '--force']), 0)
        count = len(tool.grouped_targets(tool.discover_targets()))
        width = len(str(count))
        for index in range(1, count + 1):
            self.assertIn(f'[{index:0{width}d}/{count}]', output.getvalue())

    def test_unreadable_cache_is_blocked_without_writing_a_replacement(self):
        path = self.root / 'report.json'
        path.write_text('invalid JSON')
        with contextlib.redirect_stdout(io.StringIO()) as output:
            result = tool.main(['refresh', '--version', '3.4.0', '--os-id', 'alpine-3.21-x86_64',
                                '--otp', '24', '--whatif', '--retry-failed'])
        self.assertEqual(result, 1)
        self.assertIn('BLOCKED openriak/openriak-kv:', output.getvalue())
        self.assertIn('Cannot use cached report', output.getvalue())
        self.assertEqual(path.read_text(), 'invalid JSON')


if __name__ == '__main__':
    unittest.main()
