import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from test_openriak_docker import docker_tool as tool


class MinimalRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.groups = tool.grouped_targets(tool.discover_targets(['3.4.0', '3.4.1']))

    def test_enabled_releases_export_runtime_from_scratch_in_both_renderers(self):
        enabled = [g for g in self.groups if tool.minimal.configuration(g[0])]
        self.assertTrue(enabled)
        for group in enabled:
            bases = {t.platform: {'pinned': tool.base_image_for(t) + '@sha256:' + 'a' * 64} for t in group}
            shared = tool.render_multiarch_dockerfile(group, bases, 'cookie-test', [])
            for target in group:
                for source in (shared, tool.render_dockerfile(target, bases[target.platform]['pinned'], 'cookie-test')):
                    with self.subTest(image=target.image, grouped=source is shared):
                        self.assertIn('FROM scratch AS package-', source)
                        self.assertIn('COPY --from=install-', source)
                        self.assertIn('STOPSIGNAL SIGTERM', source)
                        self.assertEqual(source.count('COPY <<\'OPENRIAK_ENTRYPOINT\''), 1)
                        self.assertEqual(source.count('ENV RIAK_DISTRIBUTED_COOKIE="cookie-test"'), 1)
                        # Each installer must terminate before the final runtime stage.
                        self.assertLess(source.index('OPENRIAK_PACKAGE_INSTALL\n'), source.index('FROM scratch AS package-'))

    def test_runtime_configuration_changes_invalidate_cached_approval(self):
        group = next(g for g in self.groups if tool.minimal.configuration(g[0]))
        original = tool.group_input(group, 5, [])
        with mock.patch.object(tool.minimal, 'configuration', return_value={'strategy': 'different'}):
            changed = tool.group_input(group, 5, [])
        self.assertNotEqual(original, changed)
        self.assertIn('runtime_renderer_sha256', original)

    def test_failed_dependency_resolution_cannot_install_the_rpm(self):
        target = next(g[0] for g in self.groups
                      if (tool.minimal.configuration(g[0]) or {}).get('strategy') == 'rpm-root')
        stage = tool.minimal.package_stage(target, 'example:9@sha256:' + 'a' * 64,
                                          'amd64', 'download-amd64', tool.package_install_script(target))
        body = stage.split('set -eu\n', 1)[1].split('OPENRIAK_PACKAGE_INSTALL\n', 1)[0]
        stubs = '''mkdir() { :; }
sed() { :; }
dnf() { echo dependency-resolution-failed; return 27; }
rpm() { echo UNEXPECTED_RPM_INSTALL; return 92; }
'''
        result = subprocess.run(['sh', '-c', 'set -eu\n' + stubs + body], text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 27)
        self.assertNotIn('UNEXPECTED_RPM_INSTALL', result.stdout)

    def test_disabled_release_retains_existing_strategy(self):
        target = next(g[0] for g in self.groups if not tool.minimal.configuration(g[0]))
        source = tool.render_dockerfile(target, 'example:1@sha256:' + 'a' * 64, 'cookie')
        self.assertNotIn('COPY --from=install-', source)

    def test_invalid_release_package_stops_generation(self):
        target = next(g[0] for g in self.groups if g[0].family == 'rhel')
        for package in (None, '', 'redhat-release; true', ['redhat-release']):
            with self.subTest(package=package), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'runtime-images.json'
                path.write_text(json.dumps({'schema_version': 1, 'releases': {
                    target.family: {target.release: {'strategy': 'rpm-root', 'release_package': package}}}}))
                with mock.patch.object(tool.minimal, 'CONFIG_PATH', path):
                    with self.assertRaises(tool.minimal.ConfigurationError):
                        tool.render_dockerfile(target, 'example:9@sha256:' + 'a' * 64, 'cookie')

    def test_openssl_backport_is_shared_across_debian_versions_and_otps(self):
        groups = [g for g in self.groups if (g[0].family, g[0].release) == ('debian', '12')]
        self.assertTrue(groups)
        for group in groups:
            self.assertEqual(tool.minimal.configuration(group[0]).get('openssl_backport'),
                             tool.minimal.OPENSSL_VERSION)
        mode = {'strategy': 'clean-root', 'openssl_backport': tool.minimal.OPENSSL_VERSION}
        with mock.patch.object(tool.minimal, 'configuration', return_value=mode):
            for group in groups:
                bases = {t.platform: {'pinned': 'debian:bookworm-slim@sha256:' + 'a' * 64} for t in group}
                shared = tool.render_multiarch_dockerfile(group, bases, 'cookie', [])
                for target in group:
                    single = tool.render_dockerfile(target, bases[target.platform]['pinned'], 'cookie')
                    for source in (single, shared):
                        self.assertIn(tool.minimal.OPENSSL_SOURCE_SHA256, source)
                        self.assertIn(tool.minimal.OPENSSL_PACKAGING_SHA256, source)
                        self.assertIn('dpkg-buildpackage -b -us -uc -Pnoudeb -j4', source)
                        self.assertIn('for build in build_static build_shared', source)
                        self.assertIn('dpkg-source --before-build .', source)
                        self.assertIn('HARNESS_JOBS=4 make -C "$build" -o Makefile -o configdata.pm link-utils run_tests', source)
                        self.assertLess(source.index('for build in build_static build_shared'),
                                        source.index('cp /build/libssl3_'))
                        self.assertIn('target=/opt/openssl-packages,ro', source)
                        self.assertIn('COPY --from=install-', source)
                        self.assertNotIn('COPY --from=openssl-build-', source)

    def test_openssl_upgrade_never_downgrades_newer_vendor_packages(self):
        target = next(g[0] for g in self.groups if (g[0].family, g[0].release) == ('debian', '12'))
        mode = {'strategy': 'clean-root', 'openssl_backport': tool.minimal.OPENSSL_VERSION}
        with mock.patch.object(tool.minimal, 'configuration', return_value=mode):
            stage = tool.minimal.package_stage(target, 'debian:12', 'amd64', 'download', '')
        body = 'installed_openssl=' + stage.split('installed_openssl=', 1)[1].split('ldconfig', 1)[0]
        for version, upgrade in [('3.0.20-1~deb12u2', True),
                                 (tool.minimal.OPENSSL_DEB_VERSION, False),
                                 ('3.0.22-1~deb12u1', False), ('3.0.23-1~deb12u1', False)]:
            stubs = f'''dpkg-query() {{ echo '{version}'; }}
apt-get() {{ echo UPGRADED; }}
'''
            result = subprocess.run(['bash', '-ec', stubs + body], text=True, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual('UPGRADED' in result.stdout, upgrade, version)

    def test_openssl_backport_rejects_other_os_releases(self):
        for target in [g[0] for g in self.groups if (g[0].family, g[0].release) != ('debian', '12')]:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'runtime-images.json'
                path.write_text(json.dumps({'schema_version': 1, 'releases': {target.family: {
                    target.release: {'strategy': 'clean-root', 'openssl_backport': '3.0.22'}}}}))
                with mock.patch.object(tool.minimal, 'CONFIG_PATH', path):
                    with self.assertRaises(tool.minimal.ConfigurationError):
                        tool.minimal.configuration(target)

    def test_openssl_packages_cannot_export_when_either_suite_fails(self):
        target = next(g[0] for g in self.groups if (g[0].family, g[0].release) == ('debian', '12'))
        source = tool.minimal.openssl_build_stage(target, 'debian:12', 'amd64')
        loop = 'for build in build_static build_shared' + source.split(
            'for build in build_static build_shared', 1)[1].split('mkdir /packages', 1)[0]
        for failing in ('build_static', 'build_shared', 'neither'):
            with self.subTest(failing=failing), tempfile.TemporaryDirectory() as directory:
                stub = f'''make() {{
    if [ "$2" = '{failing}' ]; then return 9; fi
    echo 'Result: PASS'
}}
'''
                result = subprocess.run(['sh', '-ec', stub + loop.replace('/build/', directory + '/') +
                                         '\necho EXPORTED\n'], capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode == 0, failing == 'neither')
                self.assertEqual('EXPORTED' in result.stdout, failing == 'neither')


if __name__ == '__main__':
    unittest.main()
