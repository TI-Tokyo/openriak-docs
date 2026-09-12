import shutil
import subprocess
import argparse
import contextlib
import dataclasses
import io
import json
import pathlib
import tempfile
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool


class StandaloneTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.docs_cache = self.root / 'docs-cache'
        self.output = self.root / 'company'
        self.patches = mock.patch.object(tool, 'MULTIARCH_CACHE_ROOT', self.docs_cache)
        self.patches.start()
        self.addCleanup(self.patches.stop)
        self.targets = tool.discover_targets(['3.4.1'])
        self.group = next(g for g in tool.grouped_targets(self.targets) if g[0].image_tag == '3.4.1-alpine-3.21-otp26')
        self.identity = tool.ImageIdentity('TI Tokyo', 'https://github.com/TI-Tokyo/openriak-docs',
                                           'https://www.tiot.jp/openriak-docs/', 'tiotjp')
        self.bases = {t.platform: {'requested': tool.base_image_for(t),
                                  'pinned': tool.base_image_for(t) + '@sha256:' + 'a' * 64,
                                  'resolved_at': '2026-09-01T00:00:00Z'} for t in self.group}
        tool.write_json(self.group[0].group_directory / 'report.json', {'base_images': self.bases, 'status': 'passed'})

    def command(self):
        return ['generate', '--version', '3.4.1', '--os-id', 'alpine-3.21-x86_64', '--otp', '26',
                '--output', str(self.output), '--no-docs', '--vendor', self.identity.vendor,
                '--source', self.identity.source, '--url', self.identity.url, '--namespace', self.identity.namespace]

    def run_generation(self, command=None):
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(tool, 'docker_command', side_effect=AssertionError('must reuse pins')), \
                mock.patch.object(tool, 'refresh_target', side_effect=AssertionError('must not test')), \
                mock.patch.object(tool, 'build_group_images', side_effect=AssertionError('must not build')), \
                mock.patch.object(tool, 'sync_download_metadata', side_effect=AssertionError('must not update docs')), \
                mock.patch.object(tool, 'publish_group', side_effect=AssertionError('must not publish')):
            return tool.main(command or self.command())

    def test_standalone_generation_uses_cached_pins_and_company_identity_without_docs(self):
        before = {p.relative_to(self.docs_cache): p.read_bytes() for p in self.docs_cache.rglob('*') if p.is_file()}
        self.assertEqual(self.run_generation(), 0)
        root = self.output / '3.4.1' / self.group[0].image_tag
        report = tool.read_json(root / 'report.json')
        self.assertEqual(report['status'], 'generated')
        self.assertEqual(report['tests'], {'status': 'not_run'})
        self.assertEqual(report['identity'], dataclasses.asdict(self.identity))
        self.assertEqual(report['base_images'], self.bases)
        self.assertIn('tiotjp/openriak-kv:latest', report['tags'])
        self.assertTrue(all(tag.startswith('tiotjp/openriak-kv:') for tag in report['tags']))
        source = (root / 'Dockerfile').read_text()
        for name, value in [('vendor', self.identity.vendor), ('source', self.identity.source), ('url', self.identity.url)]:
            self.assertIn(f'LABEL org.opencontainers.image.{name}={json.dumps(value)}', source)
        self.assertIn('LABEL org.openriak.image.tag="tiotjp/openriak-kv:3.4.1-alpine-3.21-otp26"', source)
        for filename in tool.ARTIFACT_FILENAMES:
            self.assertTrue((root / filename).is_file())
        for filename in ['compose.single.yaml', 'compose.cluster.yaml']:
            self.assertIn('image: tiotjp/openriak-kv:3.4.1-alpine-3.21-otp26', (root / filename).read_text())
        after = {p.relative_to(self.docs_cache): p.read_bytes() for p in self.docs_cache.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(self.run_generation(), 0)  # unchanged generation reuses output
        self.assertEqual(len(list((root / 'runs').iterdir())), 1)

    def test_defaults_and_identity_changes_affect_cache_compatibility(self):
        target = self.group[0]
        labels = tool.image_labels(target)
        self.assertEqual(labels['org.opencontainers.image.vendor'], 'OpenRiak')
        self.assertEqual(labels['org.opencontainers.image.source'], 'https://github.com/OpenRiak/openriak-docs')
        self.assertEqual(labels['org.opencontainers.image.url'], 'https://openriak.org')
        baseline = tool.group_input(self.group, 5, tool.image_aliases(target, self.targets))
        for name, value in dataclasses.asdict(self.identity).items():
            identity = dataclasses.replace(tool.ImageIdentity(), **{name: value})
            group = [dataclasses.replace(t, identity=identity) for t in self.group]
            self.assertNotEqual(tool.group_input(group, 5, tool.image_aliases(group[0], self.targets)), baseline)
        changed = [dataclasses.replace(t, identity=self.identity) for t in self.group]
        self.assertIn('tiotjp/openriak-kv:latest', tool.image_aliases(changed[0], self.targets))
        self.assertIn('mirror/openriak-kv:latest', tool.namespaced_tags(tool.image_aliases(changed[0], self.targets), ['mirror']))

    def test_output_guards_keep_standalone_results_out_of_docs(self):
        for path in [tool.REPOSITORY_ROOT, tool.REPOSITORY_ROOT / 'content/company',
                     tool.REPOSITORY_ROOT / 'tools/generated/company', self.docs_cache / 'company', tool.CACHE_ROOT]:
            with self.subTest(path=path), self.assertRaises(tool.DockerToolError):
                tool.standalone_output(str(path))
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(tool.main(['refresh', '--version', '3.4.1', '--no-docs']), 2)
        link = self.root / 'linked-cache'
        link.symlink_to(self.docs_cache, target_is_directory=True)
        with self.assertRaises(tool.DockerToolError):
            tool.standalone_output(str(link))

    def test_nested_output_symlinks_cannot_escape_to_docs(self):
        self.output.mkdir()
        (self.output / '3.4.1').symlink_to(self.docs_cache, target_is_directory=True)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.run_generation(), 2)
        group = [dataclasses.replace(t, output_root=self.output) for t in self.group]
        with self.assertRaises(tool.DockerToolError):
            tool.validate_output_targets(group)

    def test_passing_company_refresh_cannot_publish_or_sync(self):
        command = self.command()
        command[0] = 'refresh'
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(tool, 'refresh_group', return_value=True) as refresh, \
                mock.patch.object(tool, 'sync_download_metadata', side_effect=AssertionError('must not sync')):
            self.assertEqual(tool.main(command), 0)
        group = refresh.call_args.args[0]
        self.assertEqual(group[0].output_root, self.output)
        self.assertEqual(group[0].identity, self.identity)
        with mock.patch.object(tool, 'sync_download_metadata', side_effect=AssertionError('must not sync')), \
                mock.patch.object(shutil, 'copy2', side_effect=AssertionError('must not publish')):
            tool.publish_group(group, {'status': 'passed'})

    def test_changed_output_is_not_overwritten_without_force(self):
        self.assertEqual(self.run_generation(), 0)
        file = self.output / '3.4.1' / self.group[0].image_tag / 'Dockerfile'
        file.write_text('operator edit\n')
        self.assertEqual(self.run_generation(), 1)
        self.assertEqual(file.read_text(), 'operator edit\n')

    def test_force_generates_new_pins_and_cookie_and_preserves_previous_files(self):
        self.assertEqual(self.run_generation(), 0)
        root = self.output / '3.4.1' / self.group[0].image_tag
        previous = tool.read_json(root / 'report.json')
        (root / 'Dockerfile').write_text('operator edit\n')
        options = tool.parser().parse_args(self.command() + ['--force'])
        group = [dataclasses.replace(t, identity=self.identity, output_root=self.output) for t in self.group]
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(tool, 'resolve_base_image',
                side_effect=lambda t, *args: (tool.base_image_for(t), tool.base_image_for(t) + '@sha256:' + 'b' * 64)) as pull:
            self.assertTrue(tool.generate_group(group, options, self.targets))
        report = tool.read_json(root / 'report.json')
        self.assertEqual(pull.call_count, len(group))
        self.assertNotEqual(report['distributed_cookie'], previous['distributed_cookie'])
        self.assertEqual((root / 'runs' / report['run_id'] / 'previous/Dockerfile').read_text(), 'operator edit\n')
        self.assertTrue((root / 'runs' / previous['run_id'] / 'report.json').exists())

    def test_rebuild_mode_rejects_label_changes(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(tool.main(['refresh', '--version', '3.4.1', '--do-not-test', '--vendor', 'Company']), 2)

    def test_label_arguments_reject_invalid_values(self):
        for option, value in [('--vendor', 'bad\nLABEL injected=value'), ('--source', 'file:///tmp/source'),
                              ('--url', 'not a url'), ('--namespace', 'Upper/Case')]:
            with self.subTest(option=option), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                tool.parser().parse_args(['refresh', '--version', '3.4.1', option, value])

    def test_progress_counters_and_continuation_timestamps_align(self):
        capture = io.StringIO()
        many = self.targets
        count = len(many)
        width = len(str(count))
        prefix_width = len(f"[{count}/{count}] ")
        def refresh(*args):
            print(f'{tool.log_timestamp()}   Exporting OCI image')
            return True
        with contextlib.redirect_stdout(capture), mock.patch.object(tool, 'discover_targets', return_value=many), \
                mock.patch.object(tool, 'grouped_targets', return_value=[[t] for t in many]), \
                mock.patch.object(tool, 'refresh_group', side_effect=refresh), mock.patch.object(tool, 'sync_download_metadata'):
            self.assertEqual(tool.main(['refresh', '--version', '3.4.1']), 0)
        lines = capture.getvalue().splitlines()
        self.assertTrue(any(line.startswith(f'[{1:0{width}d}/{count}] ') for line in lines))
        self.assertTrue(any(line.startswith(f'[{count}/{count}] ') for line in lines))
        continuation = [line for line in lines if 'Exporting OCI' in line or 'PASSED ' in line]
        self.assertEqual(len(continuation), count * 2)
        self.assertTrue(all(line.startswith(' ' * prefix_width + '20') for line in continuation))
        partial = io.StringIO()
        writer = tool.IndentedProgress(partial, 8)
        for part in ['first', ' line\nnext', '\n', '\n', 'last']:
            writer.write(part)
        self.assertEqual(partial.getvalue(), '        first line\n        next\n\n        last')

    def test_metadata_sync_lines_have_timestamps_and_progress_indentation(self):
        capture = io.StringIO()
        output = 'Synced OpenRiak KV 3.4.0: 18 tested Docker targets.\n\nSynced OpenRiak KV 3.4.1: 17 tested Docker targets.\n'
        with contextlib.redirect_stdout(tool.IndentedProgress(capture, 8)), \
                mock.patch.object(shutil, 'which', return_value='/usr/bin/node'), \
                mock.patch.object(subprocess, 'run', return_value=mock.Mock(returncode=0, stdout=output)), \
                mock.patch.object(tool, 'log_timestamp', return_value='2026-09-06 19:00:00'):
            tool.sync_download_metadata(['3.4.0', '3.4.1'])
        self.assertEqual(capture.getvalue(), ''.join(
            '        2026-09-06 19:00:00 ' + line + '\n' for line in output.splitlines() if line))
