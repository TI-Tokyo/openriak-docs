"""Reusable EL9 bases, their consumers, and release-isolated approvals."""
import dataclasses
import json
import unittest
from unittest import mock
from test_openriak_docker import docker_tool as tool
import bases.workflow as base
from builders import pcre2


class El9BaseTests(unittest.TestCase):
    def options(self, name, *extra):
        return tool.parser().parse_args(['base', 'refresh', '--base', name,
                                        '--namespace', 'tiotjp', *extra])

    def test_each_base_selects_only_its_metadata_platforms_and_cache(self):
        for name in ('rhel-9', 'centos-9'):
            options = self.options(name)
            targets = base.selected_targets(options, tool)
            expected = {t.platform for t in tool.discover_targets()
                        if (t.family, t.release) == base.selected_release(options)}
            self.assertEqual({t.platform for t in targets}, expected)
            tag = base.base_tag(options, tool)
            self.assertTrue(str(base.cache_directory(options, tool)).endswith('/tiotjp/' + tag.replace(':', '/')))
            self.assertEqual(base.image_tags(targets[0].identity, ['openriak'], tool, tag),
                             ['tiotjp/' + tag, 'openriak/' + tag])
            with self.assertRaises(tool.DockerToolError):
                base.selected_targets(self.options(name, '--platform', 'linux/invalid'), tool)

    def test_patches_only_appear_in_reusable_bases(self):
        for name in ('rhel-9', 'centos-9'):
            options = self.options(name)
            targets = base.selected_targets(options, tool)
            pins = {t.platform: {'pinned': tool.base_image_for(t, upstream=True) + '@sha256:' + 'a' * 64}
                    for t in targets}
            source = base.render(targets, pins, tool)
            self.assertIn(pcre2.RPM_SOURCE_SHA256, source)
            self.assertIn('rpmbuild -ba', source)
            self.assertIn('invalid_frees', source)
            self.assertNotIn('files.tiot.jp', source)
            self.assertNotIn('/opt/openriak-package', source)
            self.assertNotIn('ENV RIAK_', source)
            all_targets = [dataclasses.replace(t, identity=targets[0].identity) for t in tool.discover_targets()
                           if (t.family, t.release) == base.selected_release(options)]
            for target in all_targets:
                pin = tool.base_image_for(target) + '@sha256:' + 'b' * 64
                child = tool.render_dockerfile(target, pin, 'cookie')
                self.assertIn('tiotjp/' + base.base_tag(options, tool) + '@sha256:', child)
                self.assertIn('COPY --from=runtime-base-', child)
                self.assertIn(tool.minimal.configuration(target)['package_tools_image'], child)
                self.assertIn('rpm --root /openriak-rootfs -Uvh', child)
                self.assertIn('Installed pcre2 is older than', child)
                self.assertNotIn('rpmbuild', child)
                self.assertNotIn('pcre2.src.rpm', child)
                self.assertNotIn('pcre2-regression.c', child)
            for group in tool.grouped_targets(all_targets):
                pins = {t.platform: {'pinned': tool.base_image_for(t) + '@sha256:' + 'b' * 64} for t in group}
                source = tool.render_multiarch_dockerfile(group, pins, 'cookie', [])
                self.assertNotIn('rpmbuild', source)
                self.assertIn('runtime-base-amd64', source)

    def test_child_rejects_mutable_or_wrong_os_tooling(self):
        target = base.selected_targets(self.options('rhel-9'), tool)[0]
        original = tool.minimal.configuration(target)
        for image in ('registry.access.redhat.com/ubi9/ubi:9.8', 'alpine:3.21@sha256:' + 'a' * 64):
            with mock.patch.object(tool.minimal, 'configuration', return_value={**original, 'package_tools_image': image}):
                with self.assertRaisesRegex(tool.minimal.ConfigurationError, 'pinned tools image'):
                    tool.render_dockerfile(target, 'tiotjp/rhel:9-for-openriak@sha256:' + 'b' * 64, 'cookie')

    def test_whatif_does_not_pull_build_or_create_approvals(self):
        import tempfile
        from pathlib import Path
        for name in ('rhel-9', 'centos-9'):
            with tempfile.TemporaryDirectory() as directory:
                options = self.options(name, '--whatif', '--cache-root', directory)
                with mock.patch.object(tool, 'run_logged', side_effect=AssertionError('must remain read-only')):
                    self.assertEqual(base.main(options, tool), 0)
                self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == '__main__':
    unittest.main()
