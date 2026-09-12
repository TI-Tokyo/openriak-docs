import contextlib
import dataclasses
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool
import bases.workflow as base


class PatchedBaseTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.options = tool.parser().parse_args(['base', 'refresh', '--namespace', 'tiotjp',
                                                '--cache-root', self.directory.name])
        self.targets = base.selected_targets(self.options, tool)
        self.root = base.cache_directory(self.options, tool)
        self.history = self.root / 'runs' / 'fixture-run'
        self.history.mkdir(parents=True)
        self.bases = {t.platform: {'requested': tool.base_image_for(t, upstream=True),
            'pinned': tool.base_image_for(t, upstream=True) + '@sha256:' + 'a' * 64} for t in self.targets}
        source = base.render(self.targets, self.bases, tool)
        for path in (self.root / 'Dockerfile', self.history / 'Dockerfile'):
            path.write_text(source)
        self.archive = self.history / 'image.oci.tar'
        self.archive.write_bytes(b'Archive validation is covered by test_push; mock only its parsed result here.')
        self.metadata = {'digest': 'sha256:' + 'b' * 64, 'platforms': {}, 'manifests': {},
                         'layout_index': {'manifests': [{'annotations': {
                             'org.opencontainers.image.ref.name': 'bookworm-slim-for-openriak'}}]}}
        proofs = {}
        for i, target in enumerate(self.targets):
            digest = 'sha256:' + f'{i+1:064x}'
            image_id = 'sha256:' + f'{i+100:064x}'
            self.metadata['platforms'][target.platform] = {'digest': digest}
            self.metadata['manifests'][digest] = {'manifest': {'config': {'digest': image_id}}}
            proofs[target.platform] = {'status': 'passed', 'image_id': image_id}
        self.report = {'schema_version': 1, 'product': 'openriak-base', 'status': 'passed',
            'image': 'tiotjp/' + 'debian:bookworm-slim-for-openriak', 'tags': ['tiotjp/' + 'debian:bookworm-slim-for-openriak'],
            'identity': dataclasses.asdict(self.targets[0].identity),
            'run_id': self.history.name, 'platforms': list(proofs), 'tests': proofs,
            'base_images': self.bases, 'dockerfile_sha256': tool.sha256_file(self.root / 'Dockerfile'),
            'archive_sha256': tool.sha256_file(self.archive),
            'digest': self.metadata['digest'],
            'inputs': {'identity': dataclasses.asdict(self.targets[0].identity), 'platforms': list(proofs),
                       'tags': ['tiotjp/' + 'debian:bookworm-slim-for-openriak'],
                       'upstreams': {t.platform: tool.base_image_for(t, upstream=True) for t in self.targets}}}
        self.save()

    def save(self):
        tool.write_json(self.root / 'report.json', self.report)
        tool.write_json(self.history / 'report.json', self.report)

    def test_platforms_come_from_metadata_and_tags_use_selected_namespace(self):
        expected = {t.platform for t in tool.discover_targets(None) if (t.family, t.release) == ('debian', '12')}
        self.assertEqual({t.platform for t in self.targets}, expected)
        self.assertEqual(base.image_tags(self.targets[0].identity, ['openriak', 'tiotjp'], tool, base.base_tag(self.options, tool)),
                         ['tiotjp/' + 'debian:bookworm-slim-for-openriak', 'openriak/' + 'debian:bookworm-slim-for-openriak'])
        self.options.platforms = ['linux/invalid']
        with self.assertRaises(tool.DockerToolError):
            base.selected_targets(self.options, tool)

    def test_base_has_pinned_sources_and_labels_without_openriak_or_cookie(self):
        source = (self.root / 'Dockerfile').read_text()
        self.assertIn(tool.minimal.OPENSSL_SOURCE_SHA256, source)
        self.assertIn('link-utils run_tests', source)
        self.assertIn('FROM patched-${TARGETARCH} AS final', source)
        self.assertIn('org.openriak.os.release="bookworm"', source)
        self.assertIn('org.openriak.os.version="12"', source)
        self.assertNotIn('ENV RIAK_', source)
        self.assertNotIn('files.tiot.jp', source)
        for t in self.targets:
            self.assertIn(self.bases[t.platform]['pinned'], source)

    def test_children_use_namespaced_base_and_do_not_compile_openssl(self):
        mode = {'strategy': 'clean-root', 'openssl_backport': tool.minimal.OPENSSL_VERSION,
                'base_image': 'debian:bookworm-slim-for-openriak'}
        groups = [g for g in tool.grouped_targets(tool.discover_targets(['3.4.0', '3.4.1']))
                  if (g[0].family, g[0].release) == ('debian', '12')]
        with mock.patch.object(tool.minimal, 'configuration', return_value=mode):
            for group in groups:
                targets = [dataclasses.replace(t, identity=self.targets[0].identity) for t in group]
                pins = {t.platform: {'pinned': tool.base_image_for(t) + '@sha256:' + 'b' * 64} for t in targets}
                self.assertEqual(tool.base_image_for(targets[0]), 'tiotjp/' + 'debian:bookworm-slim-for-openriak')
                self.assertEqual(tool.base_image_for(targets[0], upstream=True), 'debian:bookworm-slim')
                sources = [tool.render_multiarch_dockerfile(targets, pins, 'cookie', [])]
                sources.extend(tool.render_dockerfile(t, pins[t.platform]['pinned'], 'cookie') for t in targets)
                for source in sources:
                    self.assertIn('tiotjp/' + 'debian:bookworm-slim-for-openriak' + '@sha256:', source)
                    self.assertNotIn('openssl-build-', source)
                    self.assertNotIn('dpkg-buildpackage', source)
                    self.assertIn('dpkg --compare-versions', source)
                    self.assertIn(tool.minimal.OPENSSL_DEB_VERSION, source)

    def test_production_mapping_applies_to_every_debian_12_target(self):
        targets = [t for t in tool.discover_targets(None)
                   if (t.family, t.release) == ('debian', '12')]
        self.assertTrue(targets)
        for target in targets:
            for namespace in ('openriak', 'tiotjp'):
                selected = dataclasses.replace(target, identity=tool.ImageIdentity(namespace=namespace))
                self.assertEqual(tool.base_image_for(selected), namespace + '/' + 'debian:bookworm-slim-for-openriak')
                self.assertEqual(tool.base_image_for(selected, upstream=True), 'debian:bookworm-slim')

    def test_libblkid_backport_is_tested_and_tar_is_removed_after_installation(self):
        source = base.render(self.targets, self.bases, tool)
        self.assertIn(tool.minimal.LIBBLKID_SOURCE_SHA256, source)
        self.assertIn(tool.minimal.LIBBLKID_PACKAGING_SHA256, source)
        self.assertIn(tool.minimal.LIBBLKID_PATCH_SHA256, source)
        self.assertIn('valgrind --error-exitcode=99 --leak-check=full', source)
        self.assertIn('regression did not reject vulnerable source', source)
        self.assertLess(source.index('/opt/libblkid-packages/*.deb'), source.index(tool.minimal.remove_tar_script()))
        self.assertIn('test ! -e /usr/bin/tar', base.runtime_check(self.targets[0]))
        for target in self.targets:
            rendered = tool.render_dockerfile(target, self.bases[target.platform]['pinned'], 'test-cookie')
            self.assertIn('source=/usr/bin/tar,target=/usr/local/bin/tar,ro', rendered)
            self.assertLess(rendered.index('install -y --no-install-recommends tar'), rendered.index('cp /opt/openriak-package/'))
            self.assertLess(rendered.index('apt-get purge -y --allow-remove-essential perl-base'), rendered.index(tool.minimal.remove_tar_script()))
            self.assertIn(tool.minimal.LIBBLKID_DEB_VERSION, rendered)
            self.assertIn('test ! -e /usr/local/bin/tar', tool.minimal.runtime_check(target))

    def test_tar_bootstrap_rejects_unpinned_tools_image(self):
        target = self.targets[0]
        mode = {**tool.minimal.configuration(target), 'package_tools_image': 'debian:bookworm-slim'}
        with mock.patch.object(tool.minimal, 'configuration', return_value=mode):
            with self.assertRaisesRegex(tool.minimal.ConfigurationError, 'pinned Bookworm'):
                tool.render_dockerfile(target, self.bases[target.platform]['pinned'], 'test-cookie')

    def test_approved_archive_must_match_tested_image_and_unchanged_files(self):
        with mock.patch.object(base.push, 'archive_metadata', return_value=self.metadata):
            self.assertEqual(base.approval(self.root, tool)[0], self.report)
            platform = self.targets[0].platform
            self.report['tests'][platform]['image_id'] = 'sha256:' + 'f' * 64
            self.save()
            with self.assertRaisesRegex(tool.DockerToolError, 'tested platform'):
                base.approval(self.root, tool)
        self.archive.write_bytes(b'changed')
        with self.assertRaisesRegex(tool.DockerToolError, 'archive changed'):
            base.approval(self.root, tool)

    def test_approval_rejects_changed_dockerfile_and_unrelated_repository_tag(self):
        with (self.root / 'Dockerfile').open('a') as stream:
            stream.write('# changed\n')
        with self.assertRaisesRegex(tool.DockerToolError, 'Dockerfile changed'):
            base.approval(self.root, tool)
        self.report['tags'].append('tiotjp/unrelated:tag')
        self.save()
        with self.assertRaisesRegex(tool.DockerToolError, 'publish only'):
            base.approval(self.root, tool)

    def test_reuse_and_push_whatif_do_not_run_docker_or_write_reports(self):
        before = (self.root / 'report.json').read_bytes()
        with mock.patch.object(base.push, 'archive_metadata', return_value=self.metadata), \
                mock.patch.object(tool, 'run_logged') as run, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(base.main(self.options, tool), 0)
            self.options.action = 'push'
            self.options.whatif = True
            self.assertEqual(base.main(self.options, tool), 0)
            run.assert_not_called()
        self.assertEqual((self.root / 'report.json').read_bytes(), before)

    def test_changed_generation_requires_explicit_force(self):
        self.options.vendor = 'Changed vendor'
        with mock.patch.object(base.push, 'archive_metadata', return_value=self.metadata), \
                mock.patch.object(tool, 'run_logged') as run:
            with self.assertRaisesRegex(tool.DockerToolError, 'inputs changed'):
                base.main(self.options, tool)
            run.assert_not_called()

    def test_failed_base_cannot_be_pushed(self):
        self.report['status'] = 'failed'
        self.save()
        _, plans, _, blocked = base.push_plan(self.options, tool)
        self.assertFalse(plans)
        self.assertEqual(len(blocked), 1)

    def test_nohup_uses_the_base_cache_log_directory(self):
        self.options.nohup = True
        arguments = ['base', 'refresh', '--namespace', 'tiotjp', '--nohup']
        with mock.patch('core.background.launch', return_value=0) as launch:
            self.assertEqual(base.main(self.options, tool, arguments), 0)
        forwarded_tool, options, forwarded = launch.call_args.args
        self.assertIs(forwarded_tool, tool)
        self.assertEqual(options.output, str(self.root))
        self.assertEqual(options.command, 'base-refresh')
        self.assertEqual(forwarded, arguments)


if __name__ == '__main__':
    unittest.main()
