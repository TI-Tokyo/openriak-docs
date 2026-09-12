import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool
import openriak_node_check as checks


class NodeCheckTests(unittest.TestCase):
    def request(self, action, **values):
        return dict(action=action, timeout=27, image='alpine:3.21',
                    binfmt_image='test/binfmt:version', platform='linux/amd64', **values)

    def test_arm64_runtime_uses_real_container_output(self):
        with mock.patch.object(checks, 'container', return_value='aarch64') as run:
            self.assertTrue(checks.check(self.request('arm64'))['ok'])
        self.assertEqual(run.call_args.args, (['--platform', 'linux/arm64', 'alpine:3.21', 'uname', '-m'], 27))
        with mock.patch.object(checks, 'container', return_value='x86_64'):
            self.assertFalse(checks.check(self.request('arm64'))['ok'])

    def test_arm64_only_offers_emulation_for_exec_format_error(self):
        for error, repairable in [('exec /bin/uname: exec format error', True), ('registry unavailable', False)]:
            with self.subTest(error=error), mock.patch.object(checks, 'container', side_effect=RuntimeError(error)):
                result = checks.check(self.request('arm64'))
                self.assertFalse(result['ok'])
                self.assertEqual(result['repairable'], repairable)

    def test_bind_checks_both_directions_and_removes_scratch_files(self):
        with tempfile.TemporaryDirectory() as directory:
            def run(arguments, timeout):
                self.assertEqual(arguments[:2], ['--platform', 'linux/amd64'])
                mount = arguments[arguments.index('--mount') + 1]
                folder = Path(mount.split('source=')[1].split(',target=')[0])
                self.assertEqual(folder.parent, Path(directory))
                token = (folder / 'from-host').read_text()
                (folder / 'from-container').write_text(token)
                return token
            with mock.patch.object(checks, 'container', side_effect=run):
                self.assertTrue(checks.check(self.request('bind', tmpdir=directory))['ok'])
            self.assertEqual(list(Path(directory).iterdir()), [])
            # A successful container exit alone does not prove the bind worked.
            with mock.patch.object(checks, 'container', return_value='wrong file'):
                self.assertFalse(checks.check(self.request('bind', tmpdir=directory))['ok'])
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_timeout_removes_only_owned_probe_container(self):
        with mock.patch.object(checks, 'command', side_effect=[subprocess.TimeoutExpired('docker', 27), '']) as command:
            with self.assertRaises(subprocess.TimeoutExpired):
                checks.container(['--platform', 'linux/arm64', 'alpine:3.21', 'uname', '-m'], 27)
        run, cleanup = command.call_args_list
        name = run.args[0][run.args[0].index('--name') + 1]
        self.assertTrue(name.startswith('openriak-worker-check-'))
        self.assertEqual(cleanup.args, (['docker', 'rm', '--force', name], 10))

    def test_bind_does_not_offer_tmpdir_repair_for_registry_errors(self):
        with tempfile.TemporaryDirectory() as directory, \
                mock.patch.object(checks, 'container', side_effect=checks.CommandError('registry unavailable')):
            result = checks.check(self.request('bind', tmpdir=directory))
        self.assertFalse(result['ok'])
        self.assertFalse(result['repairable'])

    def test_installer_is_privileged_and_arm64_only(self):
        with mock.patch.object(checks, 'container', return_value='installed') as run:
            self.assertTrue(checks.check(self.request('install-arm64'))['ok'])
        self.assertEqual(run.call_args.args, (['--privileged', 'test/binfmt:version', '--install', 'arm64'], 27))

    def test_tmpdir_repair_stays_under_home_without_hidden_or_symlink_paths(self):
        with tempfile.TemporaryDirectory() as directory, mock.patch.object(checks.Path, 'home', return_value=Path(directory)):
            root = Path(directory)
            for folder in [root / '.hidden/tmp', root / '../outside', root]:
                with self.subTest(folder=folder), self.assertRaises(ValueError):
                    checks.check(self.request('create-tmpdir', tmpdir=str(folder)))
            (root / 'link').symlink_to(root, target_is_directory=True)
            with self.assertRaises(ValueError):
                checks.check(self.request('create-tmpdir', tmpdir=str(root / 'link/tmp')))
            folder = root / 'openriak-builds/tmp'
            self.assertEqual(checks.check(self.request('create-tmpdir', tmpdir=str(folder)))['tmpdir'], str(folder))

    def test_prerequisites_check_actual_daemon_and_build_tools(self):
        with tempfile.TemporaryDirectory() as directory, \
                mock.patch.object(checks.shutil, 'which', return_value='/usr/bin/program'), \
                mock.patch.object(checks, 'command', side_effect=[json.dumps({'Architecture': 'x86_64', 'DockerRootDir': '/var/lib/docker'}), 'buildx', 'compose']) as run:
            result = checks.check(self.request('prerequisites', workdir=directory))
        self.assertTrue(result['ok'])
        self.assertEqual(result['platform'], 'linux/amd64')
        self.assertEqual([call.args[0][:2] for call in run.call_args_list],
                         [['docker', 'info'], ['docker', 'buildx'], ['docker', 'compose']])
