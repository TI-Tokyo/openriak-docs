import json
import os
import shutil
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
test() { :; }
dnf() { echo dependency-resolution-failed; return 27; }
rpm() {
    case "$*" in
        *-Uvh*) echo UNEXPECTED_RPM_INSTALL; return 92 ;;
        *) printf '0 10.40 6.el9.openriak1\n' ;;
    esac
}
'''
        result = subprocess.run(['sh', '-c', 'set -eu\n' + stubs + body], text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 27)
        self.assertNotIn('UNEXPECTED_RPM_INSTALL', result.stdout)

    def test_disabled_release_retains_existing_strategy(self):
        target = next(g[0] for g in self.groups if not tool.minimal.configuration(g[0]))
        source = tool.render_dockerfile(target, 'example:1@sha256:' + 'a' * 64, 'cookie')
        self.assertNotIn('COPY --from=install-', source)

    def test_optional_rpm_removal_keeps_dependency_failures_fatal(self):
        script = tool.minimal.remove_rpm_packages({'remove_packages': ['sudo', 'vim-minimal']})
        # Both optional packages exist, but a remaining dependency rejects erase.
        result = subprocess.run(['sh', '-c', '''set -eu
rpm() {
    case "$1" in
        -q) return 0 ;;
        -e) echo dependency-still-required; return 42 ;;
        *) return 99 ;;
    esac
}
''' + script + '\necho UNEXPECTED_SUCCESS'], text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 42)
        self.assertNotIn('UNEXPECTED_SUCCESS', result.stdout)
        self.assertNotIn('--nodeps', script)

    def test_launcher_without_sudo_preserves_arguments_and_exit_status(self):
        with tempfile.TemporaryDirectory() as directory:
            commands = Path(directory) / 'usr/sbin'
            commands.mkdir(parents=True)
            runuser = commands / 'runuser'
            runuser.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\nexit 37\n')
            runuser.chmod(0o755)
            launcher = commands / 'riak'
            launcher.write_text('#!/bin/sh\nsudo -H -E -u riak -- "$@"\n')
            launcher.chmod(0o755)
            subprocess.run(['sh', '-ec', tool.minimal.launcher_without_sudo(
                {'remove_packages': ['sudo']}, directory)], check=True, timeout=5)
            result = subprocess.run([str(launcher), 'admin', 'argument with spaces', '$(literal)'],
                env={**os.environ, 'PATH': str(commands) + os.pathsep + os.environ['PATH']},
                capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 37)
            self.assertEqual(result.stdout.splitlines(),
                             ['-u', 'riak', '--', 'admin', 'argument with spaces', '$(literal)'])

    @unittest.skipUnless(shutil.which('dpkg'), 'dpkg is needed for Debian version comparison')
    def test_minimum_security_package_rejects_stale_mirror_and_accepts_newer_fix(self):
        check = tool.minimal.minimum_package_check({'minimum_packages': {'libc6': '2.35-0ubuntu3.15'}})
        for version, expected in [('2.35-0ubuntu3.14', False), ('2.35-0ubuntu3.15', True),
                                  ('2.35-0ubuntu3.16', True)]:
            with self.subTest(version=version), tempfile.TemporaryDirectory() as directory:
                query = Path(directory) / 'dpkg-query'
                query.write_text("#!/bin/sh\necho '" + version + "'\n")
                query.chmod(0o755)
                result = subprocess.run(['sh', '-c', 'set -eu\n' + check],
                    env={**os.environ, 'PATH': directory + os.pathsep + os.environ['PATH']},
                    capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode == 0, expected)

    def test_cleanup_configuration_rejects_invalid_packages_and_versions(self):
        targets = [g[0] for g in self.groups]
        for target, settings in [
                (next(t for t in targets if t.family == 'ubuntu'), {'minimum_packages': {'libc6': '1; false'}}),
                (next(t for t in targets if t.family == 'ubuntu'), {'remove_tar': 'true'}),
                (next(t for t in targets if t.family == 'rhel'), {'remove_packages': ['sudo; false']}),
                (next(t for t in targets if t.family == 'ubuntu'), {'remove_packages': ['sudo']})]:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'runtime-images.json'
                path.write_text(json.dumps({'schema_version': 1, 'releases': {target.family: {
                    target.release: {'strategy': 'clean-root', **settings}}}}))
                with mock.patch.object(tool.minimal, 'CONFIG_PATH', path):
                    with self.assertRaises(tool.minimal.ConfigurationError):
                        tool.minimal.configuration(target)

    def test_rpm_security_floor_failure_stops_installation(self):
        check = tool.minimal.minimum_package_check(
            {'minimum_packages': {'gzip': '1.9-15.el8_10'}}, 'rpm', '/openriak-rootfs')
        result = subprocess.run(['sh', '-c', '''set -eu
rpm() { printf '%s\\n' "$@"; return 17; }
''' + check.replace(' >/dev/null', '') + 'echo UNEXPECTED_SUCCESS'],
            text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 17)
        self.assertNotIn('UNEXPECTED_SUCCESS', result.stdout)

    def test_security_floors_apply_to_every_version_otp_and_architecture(self):
        expected = {('ubuntu', 'noble'): {'libc6': '2.39-0ubuntu8.9'},
                    ('rocky', '8'): {'gzip': '1.9-15.el8_10'},
                    ('rocky', '9'): {'coreutils-single': '8.32-41.el9_8.1',
                                     'glib2': '2.68.4-19.el9_8.10',
                                     'expat': '2.5.0-6.el9_8.3', 'pam': '1.5.1-28.el9_8.1'}}
        covered = set()
        for group in self.groups:
            for target in group:
                key = (target.family, target.release)
                if key not in expected:
                    continue
                covered.add(key)
                mode = tool.minimal.configuration(target)
                self.assertEqual(mode['minimum_packages'], expected[key])
                source = tool.render_dockerfile(target, 'example:1@sha256:' + 'a' * 64)
                for version in expected[key].values():
                    self.assertIn(version, source)
        self.assertEqual(covered, set(expected))

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
