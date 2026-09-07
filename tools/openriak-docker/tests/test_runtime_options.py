import json
import os
import pathlib
import shlex
import subprocess
import tempfile
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool


class RuntimeOptionsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = pathlib.Path(self.temporary.name)

    def initialize(self, configuration=None, overrides=None, pending=False):
        config = self.root / 'config'
        defaults = self.root / 'defaults'
        config.mkdir(exist_ok=True)
        defaults.mkdir(exist_ok=True)
        (defaults / 'riak.conf').write_text('''distributed_cookie = package-cookie
nodename = package@localhost
    ##          ring_size  =        64
storage_backend = bitcask
##logger.max_files=20
''')
        if configuration is not None:
            (config / 'riak.conf').write_text(configuration)
        if pending:
            (config / '.openriak-config-pending').touch()
            (config / '.openriak-cookie-pending').touch()
        source = tool.ENTRYPOINT_SCRIPT.split('\nulimit -n ', 1)[0]
        for original, replacement in [
            ('config_dir=/etc/riak', f'config_dir={shlex.quote(str(config))}'),
            ('data_dir=/var/lib/riak', f'data_dir={shlex.quote(str(self.root / "data"))}'),
            ('log_dir=/var/log/riak', f'log_dir={shlex.quote(str(self.root / "logs"))}'),
            ('defaults_dir=/opt/openriak-defaults/etc-riak', f'defaults_dir={shlex.quote(str(defaults))}'),
            ('/run/riak', str(self.root / 'run')),
        ]:
            source = source.replace(original, replacement)
        # Exercise the actual startup/configuration code without modifying host accounts.
        stubs = '''
chown() { :; }
id() { case "$1" in -u|-g) echo 1001;; esac; }
getent() { return 2; }
usermod() { echo "usermod $*"; }
groupmod() { echo "groupmod $*"; }
'''
        source = source.replace('set -eu\n', 'set -eu\n' + stubs, 1)
        env = dict(os.environ)
        env.update({name: default for name, (default, _) in tool.RUNTIME_OPTIONS.items()})
        env.update(RIAK_NODE_HOST='node-01.cluster-a.openriak', RIAK_DISTRIBUTED_COOKIE='new-image-cookie',
                   RIAK_RING_SIZE='8', RIAK_STORAGE_BACKEND='leveled', RIAK_ANTI_ENTROPY='passive',
                   RIAK_TICTACAAE_ACTIVE='active', RIAK_TICTACAAE_STOREHEADS='enabled',
                   RIAK_HTTP_LISTENER='0.0.0.0:8098', RIAK_PB_LISTENER='0.0.0.0:8087',
                   OPENRIAK_CLUSTER_MODE='single', RIAK_INIT_ONLY='1')
        env.update(overrides or {})
        result = subprocess.run(['sh', '-c', source], env=env, capture_output=True, text=True, timeout=10)
        return result, (config / 'riak.conf').read_text() if (config / 'riak.conf').exists() else ''

    def test_first_start_initializes_settings_and_rotation(self):
        result, config = self.initialize(overrides={'TZ': 'Asia/Tokyo', 'RIAK_LOG_MAX_FILE_SIZE': '5MB', 'RIAK_LOG_MAX_FILES': '4'})
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        for setting in ['ring_size = 8', 'storage_backend = leveled', 'logger.max_file_size = 5MB', 'logger.max_files = 4',
                        'nodename = openriak-kv@node-01.cluster-a.openriak', 'distributed_cookie = new-image-cookie']:
            self.assertIn(setting, config)
        self.assertRegex(result.stdout, r'T\d\d:\d\d:\d\d\+09:00 \[openriak-entrypoint\]')
        self.assertFalse((self.root / 'config' / '.openriak-config-pending').exists())

    def test_daemon_inherits_mounted_log_directory(self):
        header = tool.ENTRYPOINT_SCRIPT.split('\nlog() {', 1)[0]
        command = 'riak_command() {' + tool.ENTRYPOINT_SCRIPT.split('riak_command() {', 1)[1].split('\nriak_admin_command() {', 1)[0]
        executable = self.root / 'su-exec'
        executable.write_text('#!/bin/sh\nprintf "%s\\n" "$RUNNER_LOG_DIR"\n')
        executable.chmod(0o755)
        script = header + '\n' + command + '\nriak_command daemon\n'
        result = subprocess.run(['sh', '-c', script], capture_output=True, text=True,
                                env={**os.environ, 'RUNNER_LOG_DIR': '/usr/lib/riak/log',
                                     'PATH': str(self.root) + os.pathsep + os.environ['PATH']})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '/var/log/riak\n')

    def test_existing_config_preserved_byte_for_byte_despite_changed_environment(self):
        original = '''nodename = openriak-kv@custom.cluster
 distributed_cookie = stable-cookie
ring_size = 64
storage_backend = bitcask
##tictacaae_active = active
listener.http.internal = 127.0.0.1:8099
logger.max_files = 7
logger.max_file_size = 23MB
'''
        result, config = self.initialize(original, {'RIAK_RING_SIZE': '16', 'RIAK_STORAGE_BACKEND': 'leveled'})
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(config, original)
        self.assertIn('preserving ring_size', result.stdout)

    def test_interrupted_seeding_is_completed(self):
        result, config = self.initialize('distributed_cookie = package-cookie\n##ring_size=64\n', pending=True)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn('ring_size = 8', config)
        self.assertIn('distributed_cookie = new-image-cookie', config)

    def test_invalid_timezone_fails_before_config_changes(self):
        for zone in ['../etc/passwd', '/etc/passwd', 'Mars/Olympus', 'Asia/Tokyo\nUTC']:
            with self.subTest(zone=zone):
                result, config = self.initialize(overrides={'TZ': zone})
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(config, '')
                self.assertIn('timezone:', result.stdout)

    def test_uid_gid_overrides_and_invalid_ids(self):
        result, _ = self.initialize(overrides={'RIAK_UID': '12001', 'RIAK_GID': '12002'})
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn('groupmod -g 12002 riak', result.stdout)
        self.assertIn('usermod -g 12002 riak', result.stdout)
        self.assertIn('usermod -u 12001 riak', result.stdout)
        for identity in ['0', '-1', 'abc', '1000;echo bad', '4294967295', '99999999999']:
            result, _ = self.initialize(overrides={'RIAK_UID': identity})
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn('usermod ', result.stdout)

    def test_timezone_has_dst_and_utc_default(self):
        result, _ = self.initialize()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('+00:00 [openriak-entrypoint]', result.stdout)
        for epoch, offset in [(1704067200, '-0500'), (1719792000, '-0400')]:
            output = subprocess.check_output(['date', '-d', '@' + str(epoch), '+%z'], env={**os.environ, 'TZ': 'America/New_York'}, text=True)
            self.assertEqual(output.strip(), offset)

    def test_uid_and_gid_collisions_rejected_before_account_changes(self):
        function = tool.ENTRYPOINT_SCRIPT.split("configure_identity() {", 1)[1].split("\nriak_command() {", 1)[0]
        for collision in ["passwd", "group"]:
            script = '''set -eu
RIAK_UID=12001
RIAK_GID=12002
log() { echo "$*"; }
id() { echo 1001; }
usermod() { echo UNEXPECTED_ACCOUNT_CHANGE; }
groupmod() { echo UNEXPECTED_ACCOUNT_CHANGE; }
''' + f'getent() {{ if [ "$1" = "{collision}" ]; then echo "another-account:x:12001:12002"; else return 2; fi; }}\n'
            result = subprocess.run(["sh", "-c", script + "configure_identity() {" + function + "\nconfigure_identity"], text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("belongs to another-account", result.stdout)
            self.assertNotIn("UNEXPECTED_ACCOUNT_CHANGE", result.stdout)

    def test_existing_config_without_nodename_fails_explicitly(self):
        result, config = self.initialize('distributed_cookie = old-cookie\nring_size = 64\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('requires a live nodename', result.stdout)
        self.assertEqual(config, 'distributed_cookie = old-cookie\nring_size = 64\n')

    def test_integration_runtime_verifier_detects_mismatches(self):
        target = tool.grouped_targets(tool.discover_targets(['3.4.1']))[0][0]
        output = '+0900\n19001\n19002\n19001:19002\n19001:19002\n19001:19002\n'
        inspection = {'Config': {'Labels': tool.image_labels(target)},
                      'HostConfig': {'LogConfig': {'Type': 'json-file', 'Config': {'max-size': '10m', 'max-file': '3'}}}}
        with mock.patch.object(tool, 'docker_command', return_value='docker'), mock.patch.object(tool, 'run_logged') as run:
            run.side_effect = [mock.Mock(stdout=output), mock.Mock(stdout=json.dumps([inspection])), mock.Mock(returncode=0)]
            result = tool.verify_runtime_options('node', target, 1800, self.root / 'test.log')
            self.assertEqual(result['status'], 'passed')
            if target.family == 'alpine':
                self.assertEqual(result['dependencies'], {'curl': 'absent', 'libcurl': 'absent', 'coreutils': 'installed'})
                run.side_effect = [mock.Mock(stdout=output), mock.Mock(stdout=json.dumps([inspection])),
                                   tool.DockerToolError('Unexpected curl package')]
                with self.assertRaisesRegex(tool.DockerToolError, 'Unexpected curl'):
                    tool.verify_runtime_options('node', target, 1800, self.root / 'test.log')
            run.side_effect = [mock.Mock(stdout=output.replace('+0900', '+0000'))]
            with self.assertRaises(tool.DockerToolError):
                tool.verify_runtime_options('node', target, 1800, self.root / 'test.log')
            for problem in ['labels', 'rotation']:
                invalid = json.loads(json.dumps(inspection))
                if problem == 'labels':
                    invalid['Config']['Labels']['org.opencontainers.image.version'] = 'wrong-version'
                else:
                    invalid['HostConfig']['LogConfig']['Config'] = {}
                run.side_effect = [mock.Mock(stdout=output), mock.Mock(stdout=json.dumps([invalid]))]
                with self.assertRaises(tool.DockerToolError):
                    tool.verify_runtime_options('node', target, 1800, self.root / 'test.log')

    def test_os_labels_include_release_name_and_metadata_version(self):
        targets = tool.discover_targets(['3.4.0', '3.4.1'])
        for target in targets:
            labels = tool.image_labels(target)
            if target.family == 'ubuntu':
                expected = {'jammy': '22.04', 'noble': '24.04'}[target.release]
            else:
                expected = str(target.operating_system.get('release_version') or target.release)
            with self.subTest(image=target.image):
                self.assertEqual(labels['org.openriak.os.release'], target.release)
                self.assertEqual(labels['org.openriak.os.version'], expected)

    def test_generated_options_match_across_all_artifacts_and_labels(self):
        targets = tool.discover_targets(['3.4.0', '3.4.1'])
        for group in tool.grouped_targets(targets):
            target = group[0]
            bases = {t.platform: {'pinned': 'example:1@sha256:' + 'a' * 64} for t in group}
            source = tool.render_multiarch_dockerfile(group, bases, 'cookie', [])
            single = tool.render_single_compose(target, 'cookie')
            cluster = tool.render_cluster_compose(target, distributed_cookie='cookie')
            env = tool.render_environment_example(target, 'cookie')
            with self.subTest(image=target.image):
                for name, (default, comment) in tool.RUNTIME_OPTIONS.items():
                    self.assertIn(f'ENV {name}={json.dumps(default)}', source)
                    self.assertIn(f'{name}={default}', env)
                    expression = f'{name}: "${{{name}:-{default}}}"'
                    self.assertEqual(single.count(expression), 1)
                    self.assertEqual(cluster.count(expression), 5)
                    self.assertIn(comment, source)
                for name, (default, _) in tool.COMPOSE_OPTIONS.items():
                    self.assertIn(f'{name}={default}', env)
                    self.assertEqual(cluster.count('${' + name + ':-' + default + '}'), 5)
                for key, value in tool.image_labels(target).items():
                    self.assertEqual(source.count(f'LABEL {key}={json.dumps(value)}'), 1)
                self.assertIn('tzdata' if target.family not in {'suse', 'sles'} else 'timezone', source)
                self.assertIn('driver: json-file', single)
