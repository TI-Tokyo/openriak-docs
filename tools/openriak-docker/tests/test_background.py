import argparse
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import types
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool
import core.background as background


class BackgroundTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        patch = mock.patch.object(tool, 'CACHE_ROOT', self.root / 'cache')
        patch.start()
        self.addCleanup(patch.stop)

    def test_launcher_detaches_and_preserves_arguments_without_shell_interpretation(self):
        options = argparse.Namespace(command='refresh', output=None)
        arguments = ['refresh', '--version', '3.4.0', '--version', '3.4.1', '--nohu', '--retry-failed',
                     '--vendor', 'TI Tokyo $(do-not-run)', '--timeout', '1800']
        with mock.patch.object(background.shutil, 'which', return_value='/usr/bin/nohup'), \
                mock.patch.object(background.subprocess, 'Popen', return_value=mock.Mock(pid=12345)) as popen, \
                contextlib.redirect_stdout(io.StringIO()) as capture:
            self.assertEqual(background.launch(tool, options, arguments), 0)
        command = popen.call_args.args[0]
        self.assertEqual(command[:4], ['/usr/bin/nohup', background.sys.executable, '-u', str(Path(tool.__file__).resolve())])
        self.assertEqual(command[4:], [arg for arg in arguments if arg != '--nohu'])
        kwargs = popen.call_args.kwargs
        self.assertIs(kwargs['start_new_session'], True)
        self.assertIs(kwargs['close_fds'], True)
        self.assertEqual(kwargs['stdin'], subprocess.DEVNULL)
        self.assertEqual(kwargs['stderr'], subprocess.STDOUT)
        self.assertNotIn('shell', kwargs)
        logfile = Path(kwargs['env']['OPENRIAK_DOCKER_LOG_FILE'])
        self.assertTrue(logfile.is_file())
        self.assertEqual(logfile.parent, tool.CACHE_ROOT / 'logs')
        self.assertRegex(logfile.name, r'^refresh-\d{4}-\d\d-\d\d_\d\d-\d\d-\d\d\.\d{6}[+-]\d{4}-.+\.log$')
        self.assertIn('PID: 12345', capture.getvalue())
        self.assertIn(str(logfile), capture.getvalue())
        self.assertIn('kill -TERM 12345', capture.getvalue())

    def test_standalone_logs_stay_outside_repository_cache_and_never_overwrite(self):
        output = self.root / 'company output'
        options = argparse.Namespace(command='generate', output=str(output))
        with mock.patch.object(background.shutil, 'which', return_value='/usr/bin/nohup'), \
                mock.patch.object(background.subprocess, 'Popen', return_value=mock.Mock(pid=123)), \
                contextlib.redirect_stdout(io.StringIO()):
            background.launch(tool, options, ['generate', '--nohup'])
            first, = (output / 'logs').glob('*.log')
            first.write_text('previous output')
            background.launch(tool, options, ['generate', '--nohup'])
        self.assertEqual(len(list((output / 'logs').glob('*.log'))), 2)
        self.assertEqual(first.read_text(), 'previous output')
        self.assertFalse(tool.CACHE_ROOT.exists())

    def test_missing_nohup_fails_before_creating_logs(self):
        with mock.patch.object(background.shutil, 'which', return_value=None), self.assertRaises(tool.DockerToolError):
            background.launch(tool, argparse.Namespace(command='refresh', output=None), ['refresh', '--nohup'])
        self.assertFalse(tool.CACHE_ROOT.exists())

    def test_main_launches_only_after_argument_validation_and_without_docker_work(self):
        arguments = ['refresh', '--version', '3.4.0', '--os-id', 'alpine-3.21-x86_64', '--otp', '24', '--nohup']
        with mock.patch.object(background, 'launch', return_value=0) as launch, \
                mock.patch.object(tool, 'refresh_group', side_effect=AssertionError('no foreground refresh')), \
                mock.patch.object(tool, 'docker_command', side_effect=AssertionError('no foreground Docker')):
            self.assertEqual(tool.main(arguments), 0)
        self.assertEqual(launch.call_args.args[2], arguments)
        with contextlib.redirect_stderr(io.StringIO()), mock.patch.object(background, 'launch') as launch:
            self.assertEqual(tool.main(['refresh', '--all', '--nohup']), 2)
        launch.assert_not_called()

    def test_whatif_never_launches_or_creates_logs(self):
        with contextlib.redirect_stdout(io.StringIO()), \
                mock.patch.object(background, 'launch', side_effect=AssertionError('whatif must not launch')), \
                mock.patch.object(tool, 'docker_command', side_effect=AssertionError('whatif must not contact Docker')):
            self.assertEqual(tool.main(['refresh', '--version', '3.4.0', '--os-id', 'alpine-3.21-x86_64',
                                        '--otp', '24', '--nohup', '--whatif', '--retry-failed']), 0)
        self.assertFalse(tool.CACHE_ROOT.exists())

    def test_header_logs_worker_pid_and_log_path(self):
        targets = tool.discover_targets(['3.4.0'])
        options = tool.parser().parse_args(['refresh', '--version', '3.4.0'])
        with mock.patch.dict(os.environ, {'OPENRIAK_DOCKER_LOG_FILE': '/tmp/worker.log'}), \
                mock.patch.object(os, 'getpid', return_value=54321), \
                contextlib.redirect_stdout(io.StringIO()) as capture:
            tool.print_refresh_header(options, targets)
        self.assertIn('PID:           54321', capture.getvalue())
        self.assertIn('Log file:      /tmp/worker.log', capture.getvalue())

    @unittest.skipUnless(shutil.which('nohup') and hasattr(os, 'getsid'), 'requires POSIX nohup')
    def test_real_detached_probe_survives_hangup_and_logs_stdout_and_stderr(self):
        # This is a tiny local Python probe, not a generator or Docker build.
        script = self.root / 'probe.py'
        script.write_text('''import json, os, signal, sys
print(json.dumps({'pid': os.getpid(), 'sid': os.getsid(0), 'stdin': sys.stdin.read(), 'args': sys.argv[1:]}), flush=True)
os.kill(os.getpid(), signal.SIGHUP)
print('survived hangup', flush=True)
print('stderr captured', file=sys.stderr, flush=True)
''')
        fake_tool = types.SimpleNamespace(__file__=str(script), CACHE_ROOT=self.root / 'probe-cache', DockerToolError=tool.DockerToolError)
        workers = []
        real_popen = subprocess.Popen
        def popen(*args, **kwargs):
            worker = real_popen(*args, **kwargs)
            workers.append(worker)
            return worker
        with mock.patch.object(background.subprocess, 'Popen', side_effect=popen), contextlib.redirect_stdout(io.StringIO()) as capture:
            background.launch(fake_tool, argparse.Namespace(command='refresh', output=None), ['refresh', '--nohup', 'value with spaces'])
        worker, = workers
        try:
            self.assertEqual(worker.wait(timeout=5), 0)
        finally:
            if worker.poll() is None:
                worker.terminate()
                worker.wait(timeout=5)
        logfile, = (fake_tool.CACHE_ROOT / 'logs').glob('*.log')
        text = logfile.read_text()
        info = json.loads(text.splitlines()[0])
        self.assertEqual(info['pid'], worker.pid)
        self.assertEqual(info['sid'], worker.pid)
        self.assertEqual(info['stdin'], '')
        self.assertEqual(info['args'], ['refresh', 'value with spaces'])
        self.assertIn('survived hangup', text)
        self.assertIn('stderr captured', text)
        self.assertIn(f'PID: {worker.pid}', capture.getvalue())
