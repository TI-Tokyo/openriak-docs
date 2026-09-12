import contextlib
import io
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool
import openriak_distributed as distributed
import openriak_remote as remote
import openriak_remote_worker as agent


class RemoteTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.key = self.root / 'key with spaces'
        self.key.write_text('test placeholder; never a real private key')
        self.config = self.root / 'nodes.json'
        self.plan_path = self.root / 'plan.json'
        self.deployment_path = self.root / 'deployment.json'
        self.node = {'host': 'peter@worker.example.com', 'workdir': '/home/peter/builds',
                     'ssh_key': str(self.key), 'port': 22}
        self.quiet = contextlib.redirect_stdout(io.StringIO())
        self.quiet.__enter__()
        self.addCleanup(self.quiet.__exit__, None, None, None)
        tool.write_json(self.config, {'schema_version': 1, 'nodes': {'worker': self.node}})
        self.assertEqual(tool.main(['distribute', 'plan', '--version', '3.4.1', '--os-id',
                                   'debian-11-amd64', '--workers', '1', '--output', str(self.plan_path)]), 0)
        self.plan = tool.read_json(self.plan_path)
        self.start_options = tool.parser().parse_args(['distribute', 'start', '--plan', str(self.plan_path),
            '--nodes-file', str(self.config), '--deployment', str(self.deployment_path)])

    def deployment(self):
        node = dict(self.node, name='worker', worker=1, remote_dir='/home/peter/builds/run', status='running')
        data = {'kind': 'openriak-ssh-deployment', 'schema_version': 1, 'id': 'test-deployment',
                'plan': self.plan, 'nodes': [node], 'results_dir': str(self.root / 'results')}
        tool.write_json(self.deployment_path, data)
        return data

    def monitor_options(self, *extra):
        return tool.parser().parse_args(['distribute', 'monitor', '--deployment', str(self.deployment_path), *extra])

    def test_add_node_stores_only_key_path_and_requires_explicit_replace(self):
        options = ['distribute', 'add-node', 'second', 'peter@192.0.2.10', '--workdir', '~/builds',
                   '--ssh-key', str(self.key), '--nodes-file', str(self.config)]
        with mock.patch.object(remote, 'execute', side_effect=AssertionError('add-node is local')):
            self.assertEqual(tool.main(options), 0)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(tool.main(options), 2)
            self.assertEqual(tool.main(options + ['--replace']), 0)
        text = self.config.read_text()
        self.assertNotIn(self.key.read_text(), text)
        self.assertEqual(tool.read_json(self.config)['nodes']['second']['ssh_key'], str(self.key))
        self.assertEqual(self.config.stat().st_mode & 0o777, 0o600)

    def healthy_check(self, tool, node, options, action, **values):
        return {'ok': True, 'platform': 'linux/amd64', 'repair_tmpdir': '/home/peter/openriak-builds/tmp',
                'tmpdir': '/tmp'}

    def test_check_nodes_runs_probes_with_strict_host_verification(self):
        result = json.dumps(self.healthy_check(None, None, None, None))
        with mock.patch.object(remote, 'execute', return_value=result) as execute:
            self.assertEqual(tool.main(['distribute', 'check-nodes', '--nodes-file', str(self.config)]), 0)
        command, timeout = execute.call_args.args[1:]
        self.assertEqual(command[0], 'ssh')
        self.assertEqual(command[-2], 'peter@worker.example.com')
        self.assertEqual([json.loads(shlex.split(call.args[1][-1])[-1])['action']
                          for call in execute.call_args_list], ['prerequisites', 'arm64', 'bind'])
        self.assertIn('BatchMode=yes', command)
        self.assertIn('StrictHostKeyChecking=yes', command)
        self.assertEqual(command[command.index('-i') + 1], str(self.key))
        self.assertEqual(timeout, tool.DEFAULT_TIMEOUT_SECONDS + 40)

    def test_check_nodes_continues_after_login_failure(self):
        data = tool.read_json(self.config)
        data['nodes']['second'] = dict(self.node, host='peter@192.0.2.10')
        tool.write_json(self.config, data)
        healthy = self.healthy_check(None, None, None, None)
        with mock.patch.object(remote, 'node_check_call', side_effect=[tool.DockerToolError('login denied'), healthy, healthy, healthy]) as execute:
            self.assertEqual(tool.main(['distribute', 'check-nodes', '--nodes-file', str(self.config)]), 1)
        self.assertEqual(execute.call_count, 4)

    def test_check_nodes_repairs_only_after_approval_and_rechecks(self):
        healthy = self.healthy_check(None, None, None, None)
        failed = {'ok': False, 'error': 'exec format error', 'repairable': True}
        with mock.patch.object(remote, 'node_check_call', side_effect=[healthy, failed, healthy, healthy, healthy]) as probe, \
                mock.patch('builtins.input', return_value='yes') as prompt, mock.patch.object(sys.stdin, 'isatty', return_value=True):
            self.assertEqual(tool.main(['distribute', 'check-nodes', '--nodes-file', str(self.config)]), 0)
        prompt.assert_called_once()
        self.assertEqual([call.args[3] for call in probe.call_args_list],
                         ['prerequisites', 'arm64', 'install-arm64', 'arm64', 'bind'])

    def test_check_nodes_declined_and_noninteractive_repairs_do_not_install(self):
        healthy = self.healthy_check(None, None, None, None)
        failed = {'ok': False, 'error': 'exec format error', 'repairable': True}
        for tty, extra in [(True, []), (False, []), (True, ['--no-fix'])]:
            with self.subTest(tty=tty, extra=extra), \
                    mock.patch.object(remote, 'node_check_call', side_effect=[healthy, failed, healthy]) as probe, \
                    mock.patch('builtins.input', return_value='no'), mock.patch.object(sys.stdin, 'isatty', return_value=tty):
                self.assertEqual(tool.main(['distribute', 'check-nodes', '--nodes-file', str(self.config), *extra]), 1)
            self.assertEqual([call.args[3] for call in probe.call_args_list], ['prerequisites', 'arm64', 'bind'])

    def test_check_nodes_saves_only_verified_tmpdir_and_passes_it_to_future_launch(self):
        healthy = self.healthy_check(None, None, None, None)
        failed = {'ok': False, 'error': 'different temporary files', 'repairable': True}
        for verified in (False, True):
            with self.subTest(verified=verified):
                temporary = healthy['repair_tmpdir']
                with mock.patch.object(remote, 'node_check_call', side_effect=[healthy, healthy, failed,
                        {'ok': True, 'tmpdir': temporary}, dict(healthy, tmpdir=temporary) if verified else failed]) as probe, \
                        mock.patch('builtins.input', side_effect=AssertionError('--yes should not prompt')):
                    self.assertEqual(tool.main(['distribute', 'check-nodes', '--nodes-file', str(self.config), '--yes']), 0 if verified else 1)
                node = tool.read_json(self.config)['nodes']['worker']
                self.assertEqual(node.get('tmpdir'), temporary if verified else None)
                self.assertEqual(probe.call_args.args[1]['tmpdir'], temporary)
        deployment = self.deployment()
        node = dict(deployment['nodes'][0], tmpdir=temporary)
        self.assertEqual(remote.request_for(deployment, node, 'start')['tmpdir'], temporary)

    def test_queue_restart_selects_only_requested_worker_and_keeps_old_results(self):
        data = self.deployment()
        data['plan']['workers'] = 2
        data['plan']['id'] = distributed.digest({k: v for k, v in data['plan'].items() if k != 'id'})
        untouched = dict(data['nodes'][0], name='local', worker=2)
        data['nodes'].append(untouched)
        original_results = self.root / 'retrieved'
        original_results.mkdir()
        (original_results / 'evidence').write_text('keep')
        data['nodes'][0].update(local_results=str(original_results), fetched_signature='old')
        tool.write_json(self.deployment_path, data)
        def call(tool, node, options, request):
            self.assertEqual(node['name'], 'worker')
            self.assertEqual(request['action'], 'restart')
            return {'status': 'running', 'pid': 99, 'restart_id': request['restart_id']}
        args = ['distribute', 'restart', '--deployment', str(self.deployment_path),
                '--node', 'worker', '--nodes-file', str(self.config)]
        with mock.patch.object(remote, 'remote_call', side_effect=call):
            self.assertEqual(tool.main(args), 0)
        after = tool.read_json(self.deployment_path)
        self.assertEqual(after['nodes'][1], untouched)
        self.assertEqual(after['plan'], data['plan'])
        self.assertEqual((original_results / 'evidence').read_text(), 'keep')
        self.assertTrue(after['nodes'][0]['result_subdirectory'].startswith('worker-retry-'))
        self.assertEqual(after['nodes'][0]['attempt_history'][0]['fetched_signature'], 'old')

    def test_queue_restart_reuses_request_id_after_lost_response(self):
        self.deployment()
        requests = []
        def call(tool, node, options, request):
            requests.append(request)
            if len(requests) == 1:
                raise tool.DockerToolError('SSH reply lost')
            return {'status': 'running', 'pid': 99, 'restart_id': request['restart_id']}
        args = ['distribute', 'restart', '--deployment', str(self.deployment_path),
                '--node', 'worker', '--nodes-file', str(self.config)]
        with mock.patch.object(remote, 'remote_call', side_effect=call):
            self.assertEqual(tool.main(args), 1)
            self.assertEqual(tool.main(args), 0)
        self.assertEqual(requests[0]['restart_id'], requests[1]['restart_id'])

    def test_unsafe_destinations_and_invalid_timeouts_are_rejected(self):
        for field, value in [('host', '-oProxyCommand=bad'), ('host', 'user@host;bad'),
                             ('workdir', '/tmp/../etc'), ('workdir', '/tmp/$(bad)'), ('port', 0)]:
            with self.subTest(field=field), self.assertRaises(tool.DockerToolError):
                remote.validate_node(tool, 'worker', dict(self.node, **{field: value}))
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(tool.main(['distribute', 'check-nodes', '--timeout', '0']), 2)

    def test_ssh_arguments_are_quoted_for_remote_shell(self):
        arguments = ['python3', '-c', "print('hello; $(false)')", 'with spaces']
        command = remote.ssh_command(self.node, self.start_options, arguments)
        self.assertEqual(shlex.split(command[-1]), arguments)

    def test_start_stages_via_scp_and_reconnects_without_duplicate_launch(self):
        launch = {'status': 'running', 'pid': 42, 'log': '/home/peter/builds/run/worker.log'}
        calls = []
        def call(tool, node, options, request):
            calls.append(request['action'])
            if request['action'] == 'prepare':
                return {'remote_dir': '/home/peter/builds/run'}
            if request['action'] == 'status':
                return launch if 'start' in calls else {'status': 'staged'}
            return launch
        with mock.patch.object(remote, 'remote_call', side_effect=call), mock.patch.object(remote, 'scp') as scp:
            self.assertEqual(remote.start(tool, self.start_options), 0)
            first = tool.read_json(self.deployment_path)
            self.assertEqual(remote.start(tool, self.start_options), 0)
            second = tool.read_json(self.deployment_path)
        self.assertEqual(calls.count('start'), 1)
        self.assertEqual(scp.call_count, 1)
        self.assertEqual(first['bundle_sha256'], second['bundle_sha256'])
        self.assertEqual(second['nodes'][0]['remote']['pid'], 42)
        with tarfile.open(first['bundle']) as archive:
            self.assertNotIn('nodes.json', archive.getnames())
            self.assertTrue(all(self.key.name not in n for n in archive.getnames()))

    def test_run_launches_all_nodes_with_plan_and_node_based_defaults(self):
        self.assertEqual(tool.main(['distribute', 'add-node', 'local', '--local', '--workdir',
                                   str(self.root / 'local'), '--nodes-file', str(self.config)]), 0)
        plan_path = self.root / 'nightly plan.json'
        self.assertEqual(tool.main(['distribute', 'plan', '--version', '3.4.1', '--os-id', 'debian-11-amd64',
                                   '--workers', '2', '--output', str(plan_path)]), 0)
        launches = []
        def call(tool, node, options, request):
            if request['action'] == 'prepare':
                return {'remote_dir': request['remote_dir']}
            if request['action'] == 'status':
                return {'status': 'staged'}
            launches.append((node['name'], request))
            return {'status': 'running', 'pid': 100 + node['worker']}
        args = ['distribute', 'run', '--plan', str(plan_path), '--nodes-file', str(self.config)]
        with mock.patch.object(remote, 'remote_call', side_effect=call), mock.patch.object(remote, 'scp'), mock.patch.object(remote, 'execute'):
            self.assertEqual(tool.main(args), 0)
            deployment = tool.read_json(plan_path.with_suffix('.remote.json'))
            self.assertEqual(deployment['results_dir'], str(plan_path.with_suffix('.results')))
            self.assertEqual([name for name, _ in launches], ['local', 'worker'])
            for node in deployment['nodes']:
                self.assertEqual(node['result_subdirectory'], node['name'])
                self.assertIn('/nightly_plan/' + node['name'] + '/', node['remote_dir'])
            custom = self.root / 'custom-results'
            self.assertEqual(tool.main(args + ['--deployment', str(self.root / 'custom.remote.json'), '--output', str(custom)]), 0)
            self.assertEqual(tool.read_json(self.root / 'custom.remote.json')['results_dir'], str(custom))

    def test_run_and_start_are_aliases_and_worker_remains_separate(self):
        for command in ('run', 'start'):
            options = tool.parser().parse_args(['distribute', command, '--plan', str(self.plan_path)])
            self.assertFalse(hasattr(options, 'worker'))
            self.assertIsNone(options.results_dir)
        options = tool.parser().parse_args(['distribute', 'worker', '--plan', str(self.plan_path),
                                           '--worker', '1', '--output', str(self.root / 'worker')])
        self.assertEqual(options.worker, 1)

    def test_start_recovers_lost_launch_response(self):
        attempts = []
        def call(tool, node, options, request):
            if request['action'] == 'prepare':
                return {'remote_dir': '/home/peter/builds/run'}
            if request['action'] == 'status':
                return {'status': 'running', 'pid': 42} if attempts else {'status': 'staged'}
            attempts.append('launched')
            raise tool.DockerToolError('SSH connection lost after launch')
        with mock.patch.object(remote, 'remote_call', side_effect=call), mock.patch.object(remote, 'scp') as scp:
            self.assertEqual(remote.start(tool, self.start_options), 1)
            self.assertEqual(remote.start(tool, self.start_options), 0)
        self.assertEqual(attempts, ['launched'])
        self.assertEqual(scp.call_count, 1)
        self.assertNotIn('error', tool.read_json(self.deployment_path)['nodes'][0])

    def test_worker_count_mismatch_prevents_remote_commands(self):
        config = tool.read_json(self.config)
        config['nodes']['second'] = dict(self.node, host='peter@192.0.2.10')
        tool.write_json(self.config, config)
        with mock.patch.object(remote, 'remote_call', side_effect=AssertionError('no SSH')), self.assertRaisesRegex(tool.DockerToolError, 'needs 1 nodes'):
            remote.start(tool, self.start_options)

    def failed_receipt(self):
        return {'plan_id': self.plan['id'], 'worker': 1, 'status': 'failed',
                'results': {self.plan['jobs'][0]['image_tag']: {'status': 'failed', 'error': 'build error'}}}

    def test_monitor_waits_then_fetches_failed_results_and_log_once(self):
        deployment = self.deployment()
        deployment['nodes'][0]['result_subdirectory'] = 'worker'
        tool.write_json(self.deployment_path, deployment)
        snapshot = {'status': 'failed', 'pid': 42, 'receipt': self.failed_receipt()}
        def copy(tool, node, options, source, destination, **kwargs):
            destination = Path(destination)
            if kwargs.get('recursive'):
                tool.write_json(destination / 'results/worker.json', snapshot['receipt'])
            else:
                destination.write_text('build failed diagnostic log')
        responses = [{'status': 'running', 'pid': 42}, snapshot, snapshot]
        with mock.patch.object(remote, 'remote_call', side_effect=responses), mock.patch.object(remote, 'scp', side_effect=copy) as scp, mock.patch.object(remote.time, 'sleep') as sleep:
            self.assertEqual(remote.monitor(tool, self.monitor_options('--watch'), []), 1)
        sleep.assert_called_once_with(15)
        self.assertEqual(scp.call_count, 2)
        data = tool.read_json(self.deployment_path)
        result = Path(data['nodes'][0]['local_results'])
        self.assertEqual(result.name, 'worker')
        self.assertEqual((result / 'remote-worker.log').read_text(), 'build failed diagnostic log')
        with mock.patch.object(remote, 'remote_call', return_value=snapshot), mock.patch.object(remote, 'scp', side_effect=AssertionError('already fetched')):
            self.assertEqual(remote.monitor(tool, self.monitor_options(), []), 1)

    def test_running_worker_is_not_fetched_and_network_failure_is_not_completion(self):
        self.deployment()
        with mock.patch.object(remote, 'remote_call', return_value={'status': 'running', 'pid': 42}), mock.patch.object(remote, 'scp', side_effect=AssertionError('running')):
            self.assertEqual(remote.monitor(tool, self.monitor_options(), []), 0)
        with mock.patch.object(remote, 'remote_call', side_effect=tool.DockerToolError('network unavailable')):
            self.assertEqual(remote.monitor(tool, self.monitor_options(), []), 1)
        self.assertFalse((self.root / 'results/worker-1').exists())
        self.assertEqual(tool.read_json(self.deployment_path)['nodes'][0]['status'], 'running')

    def test_monitor_only_prints_new_status_and_preserves_finish_time(self):
        data = self.deployment()
        data['plan']['workers'] = 2
        data['plan']['id'] = distributed.digest({k: v for k, v in data['plan'].items() if k != 'id'})
        data['nodes'].append(dict(data['nodes'][0], name='other', worker=2))
        tool.write_json(self.deployment_path, data)
        failed = {'status': 'failed', 'pid': 42,
                  'receipt': {'finished_at': '2026-09-11T09:08:45Z'}}
        running = {'status': 'running', 'pid': 43}
        changed_pid = dict(running, pid=44)
        complete = {'status': 'complete', 'pid': 44,
                    'receipt': {'finished_at': '2026-09-11T11:30:00Z'}}
        # Four polls: unchanged failure throughout, a new PID, then completion.
        responses = [failed, running, failed, running, failed, changed_pid, failed, complete]
        def fetched(tool, options, deployment, node, snapshot):
            if snapshot['status'] in remote.TERMINAL:
                node['fetched_signature'] = 'fetched'
        output = io.StringIO()
        with mock.patch.object(remote, 'remote_call', side_effect=responses), \
                mock.patch.object(remote, 'fetch_node', side_effect=fetched) as fetch, \
                mock.patch.object(remote.time, 'sleep'), \
                mock.patch.object(tool, 'log_timestamp', return_value='CURRENT POLL TIME'), \
                contextlib.redirect_stdout(output):
            self.assertEqual(remote.monitor(tool, self.monitor_options('--watch'), []), 1)
        lines = output.getvalue().splitlines()
        self.assertEqual(lines.count('worker: finished (failed) at 2026-09-11T09:08:45Z; recorded PID 42; task counts unavailable; no tasks running'), 1)
        self.assertEqual(sum('other: running; PID 43' in line for line in lines), 1)
        self.assertEqual(sum('other: running; PID 44' in line for line in lines), 1)
        self.assertIn('other: finished (successful) at 2026-09-11T11:30:00Z; recorded PID 44; task counts unavailable; no tasks running', lines)
        self.assertEqual(fetch.call_count, 8)

    def test_monitor_suppresses_repeated_errors_and_reports_recovery(self):
        self.deployment()
        failed = {'status': 'failed', 'pid': 42}
        responses = [tool.DockerToolError('offline'), tool.DockerToolError('offline'),
                     {'status': 'running', 'pid': 42}, failed]
        def fetched(tool, options, deployment, node, snapshot):
            if snapshot['status'] in remote.TERMINAL:
                node['fetched_signature'] = 'fetched'
        output = io.StringIO()
        with mock.patch.object(remote, 'remote_call', side_effect=responses), \
                mock.patch.object(remote, 'fetch_node', side_effect=fetched), \
                mock.patch.object(remote.time, 'sleep'), contextlib.redirect_stdout(output):
            self.assertEqual(remote.monitor(tool, self.monitor_options('--watch'), []), 1)
        self.assertEqual(output.getvalue().count('ERROR: offline'), 1)
        self.assertIn('worker: running; PID 42 (checked now)', output.getvalue())
        self.assertIn('worker: finished (failed) (finish time unavailable); recorded PID 42; task counts unavailable; no tasks running', output.getvalue())

    def test_monitor_distinguishes_finished_assignments_from_unattempted_tasks(self):
        data = self.deployment()
        job = data['plan']['jobs'][0]
        data['plan']['jobs'].append(dict(job, image_tag='second-image'))
        data['plan']['id'] = distributed.digest({k: v for k, v in data['plan'].items() if k != 'id'})
        tool.write_json(self.deployment_path, data)
        for results, expected in [
                ({job['image_tag']: {'status': 'failed'}},
                 '1/2 image groups attempted; 0 passed, 1 failed; 1 not attempted'),
                ({job['image_tag']: {'status': 'failed'}, 'second-image': {'status': 'passed'}},
                 '2/2 image groups attempted; 1 passed, 1 failed; all assigned tasks finished')]:
            with self.subTest(expected=expected):
                output = io.StringIO()
                snapshot = {'status': 'failed', 'pid': 42, 'receipt': {'results': results}}
                with mock.patch.object(remote, 'remote_call', return_value=snapshot), \
                        mock.patch.object(remote, 'fetch_node'), contextlib.redirect_stdout(output):
                    self.assertEqual(remote.monitor(tool, self.monitor_options(), []), 1)
                self.assertIn(expected, output.getvalue())

    def test_partial_scp_failure_keeps_results_unpublished_and_can_retry(self):
        data = self.deployment()
        snapshot = {'status': 'failed', 'pid': 42, 'receipt': self.failed_receipt()}
        with mock.patch.object(remote, 'scp', side_effect=tool.DockerToolError('transfer interrupted')), self.assertRaises(tool.DockerToolError):
            remote.fetch_node(tool, self.monitor_options(), data, data['nodes'][0], snapshot)
        self.assertFalse((self.root / 'results/worker-1').exists())
        self.assertEqual(list((self.root / 'results').iterdir()), [])

    def test_changed_receipt_during_scp_is_rejected(self):
        data = self.deployment()
        snapshot = {'status': 'failed', 'pid': 42, 'receipt': self.failed_receipt()}
        with mock.patch.object(remote, 'scp'), mock.patch.object(remote, 'remote_call', return_value={'status': 'running', 'pid': 43}), self.assertRaisesRegex(tool.DockerToolError, 'changed during transfer'):
            remote.fetch_node(tool, self.monitor_options(), data, data['nodes'][0], snapshot)
        self.assertFalse((self.root / 'results/worker-1').exists())

    def test_fetch_recovers_promotion_before_controller_checkpoint(self):
        data = self.deployment()
        snapshot = {'status': 'failed', 'pid': 42, 'receipt': self.failed_receipt()}
        signature = distributed.digest(snapshot)
        destination = self.root / 'results/worker-1'
        tool.write_json(destination / 'worker.json', snapshot['receipt'])
        tool.write_json(destination / 'remote-fetch.json', {'signature': signature, 'deployment': data['id']})
        with mock.patch.object(remote, 'scp', side_effect=AssertionError('no repeat transfer')):
            self.assertTrue(remote.fetch_node(tool, self.monitor_options(), data, data['nodes'][0], snapshot))

    def test_logs_use_ssh_tail_follow_and_ctrl_c_leaves_build_running(self):
        self.deployment()
        options = tool.parser().parse_args(['distribute', 'logs', '--deployment', str(self.deployment_path), '--node', 'worker'])
        with mock.patch.object(remote.subprocess, 'run', side_effect=KeyboardInterrupt) as run:
            self.assertEqual(remote.logs(tool, options), 130)
        command = run.call_args.args[0]
        self.assertEqual(shlex.split(command[-1]), ['tail', '-n', '100', '-f', '/home/peter/builds/run/worker.log'])
        self.assertIsNone(run.call_args.kwargs['timeout'])

    def test_timeouts_are_reported_without_claiming_remote_build_stopped(self):
        with mock.patch.object(remote.subprocess, 'run', side_effect=subprocess.TimeoutExpired(['ssh'], 10)), self.assertRaisesRegex(tool.DockerToolError, 'keep running'):
            remote.execute(tool, ['ssh', 'host', 'true'], 10)


class LocalNodeTests(unittest.TestCase):
    setUp = RemoteTests.setUp
    monitor_options = RemoteTests.monitor_options

    def add_local(self, name='local', *extra):
        return tool.main(['distribute', 'add-node', name, '--local', '--workdir',
                         str(self.root / 'local work'), '--nodes-file', str(self.config), *extra])

    def test_local_registration_and_check_need_no_ssh_or_key(self):
        result = json.dumps(RemoteTests.healthy_check(self, None, None, None, None))
        with mock.patch.object(remote, 'ssh_command', side_effect=AssertionError('no SSH')), \
                mock.patch.object(remote, 'execute', return_value=result) as execute:
            self.assertEqual(self.add_local(), 0)
            self.assertEqual(tool.main(['distribute', 'check-nodes', '--node', 'local',
                                       '--nodes-file', str(self.config)]), 0)
        self.assertEqual(execute.call_args.args[1][0], sys.executable)
        node = tool.read_json(self.config)['nodes']['local']
        self.assertEqual(node['transport'], 'local')
        self.assertNotIn('ssh_key', node)
        self.assertNotIn('host', node)
        self.assertFalse((self.root / 'local work').exists())

    def test_local_registration_rejects_ssh_settings_and_protected_workdir(self):
        for extra in (['--ssh-key', str(self.key)], ['--port', '22']):
            with self.subTest(extra=extra), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(self.add_local('local', *extra), 2)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(tool.main(['distribute', 'add-node', 'local', 'peter@localhost', '--local',
                                       '--workdir', str(self.root / 'local')]), 2)
        with self.assertRaises(tool.DockerToolError):
            remote.validate_node(tool, 'local', {'transport': 'local', 'workdir': str(tool.STATIC_ROOT)})

    def test_duplicate_local_workers_are_rejected_before_launch(self):
        self.add_local('first')
        self.add_local('second')
        plan_path = self.root / 'two-workers.json'
        self.assertEqual(tool.main(['distribute', 'plan', '--version', '3.4.1', '--os-id', 'debian-11-amd64',
                                   '--workers', '2', '--output', str(plan_path)]), 0)
        options = tool.parser().parse_args(['distribute', 'start', '--plan', str(plan_path), '--node', 'first',
                                           '--node', 'second', '--nodes-file', str(self.config)])
        with mock.patch.object(remote, 'remote_call', side_effect=AssertionError('no launch')), self.assertRaisesRegex(tool.DockerToolError, 'one local worker'):
            remote.start(tool, options)

    def test_local_stage_launch_monitor_fetch_and_logs_with_fake_worker(self):
        self.add_local()
        fake = self.root / 'fake-worker.py'
        fake.write_text("import json, os, pathlib, sys\np=pathlib.Path(sys.argv[sys.argv.index('--plan')+1]); plan=json.loads(p.read_text()); out=pathlib.Path(sys.argv[sys.argv.index('--output')+1]); (out/'worker.json').write_text(json.dumps({'plan_id':plan['id'],'worker':1,'pid':os.getpid(),'status':'complete','results':{}})); print('local fake worker completed',flush=True)\n")
        plan = {'workers': 1, 'jobs': [], 'sources': {'openriak_docker.py': tool.sha256_file(fake)}, 'metadata': {}}
        plan['id'] = distributed.digest(plan)
        tool.write_json(self.plan_path, plan)
        def bundle(tool, plan, plan_path, destination):
            with tarfile.open(destination, 'w:gz') as archive:
                archive.add(fake, arcname='tools/openriak-docker/openriak_docker.py')
                archive.add(plan_path, arcname='plan.json')
        self.start_options.node = ['local']
        with mock.patch.object(distributed, 'load_plan', return_value=plan), mock.patch.object(distributed, 'plan_targets'), mock.patch.object(distributed, 'write_bundle', side_effect=bundle), mock.patch.object(remote, 'ssh_command', side_effect=AssertionError('no SSH')), mock.patch.object(remote, 'scp', side_effect=AssertionError('no SCP')):
            self.assertEqual(remote.start(tool, self.start_options), 0)
            launched = tool.read_json(self.deployment_path)
            deadline = time.monotonic() + 5
            def pause(seconds):
                self.assertLess(time.monotonic(), deadline, 'worker did not finish')
                time.sleep(.05)
            with mock.patch.object(remote, 'time', mock.Mock(sleep=pause)):
                self.assertEqual(remote.monitor(tool, self.monitor_options('--watch'), []), 0)
            self.assertEqual(remote.start(tool, self.start_options), 0)
        finished = tool.read_json(self.deployment_path)
        self.assertEqual(launched['nodes'][0]['remote']['pid'], finished['nodes'][0]['remote']['pid'])
        result = Path(finished['nodes'][0]['local_results'])
        self.assertIn('local fake worker completed', (result / 'remote-worker.log').read_text())
        options = tool.parser().parse_args(['distribute', 'logs', '--deployment', str(self.deployment_path), '--node', 'local', '--no-follow'])
        with mock.patch.object(remote.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)) as tail:
            self.assertEqual(remote.logs(tool, options), 0)
        self.assertEqual(tail.call_args.args[0][0], 'tail')


class RemoteAgentTests(unittest.TestCase):
    def test_receipt_from_manual_restart_is_not_fetched_as_the_original_task(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tool.write_json(root / 'launch.json', {'pid': 42, 'start_ticks': '100', 'plan_id': 'plan', 'worker': 1})
            tool.write_json(root / 'results/worker.json', {'plan_id': 'plan', 'worker': 1, 'pid': 43, 'status': 'running'})
            with mock.patch.object(agent.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, '', '')):
                self.assertEqual(agent.status(root)['status'], 'unknown')

    def test_monitoring_unstaged_node_does_not_create_remote_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'not-created'
            result = agent.control({'action': 'status', 'remote_dir': str(root), 'plan_id': 'plan', 'worker': 1})
            self.assertEqual(result['status'], 'staged')
            self.assertFalse(root.exists())

    def test_stop_uses_pidfd_and_never_signals_finished_or_reused_pids(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request = {'remote_dir': str(root), 'plan_id': 'plan', 'worker': 1, 'action': 'stop'}
            running = {'status': 'running', 'pid': 42, 'start_ticks': '100'}
            with mock.patch.object(agent, 'status', return_value=running), \
                    mock.patch.object(agent.os, 'pidfd_open', return_value=123), \
                    mock.patch.object(agent.os, 'close'), \
                    mock.patch.object(agent, 'start_ticks', return_value='100'), \
                    mock.patch.object(agent.signal, 'pidfd_send_signal') as send:
                self.assertTrue(agent.control(request)['stop_requested'])
                send.assert_called_once_with(123, agent.signal.SIGTERM)
            with mock.patch.object(agent, 'status', return_value={'status': 'failed'}), \
                    mock.patch.object(agent.os, 'pidfd_open', side_effect=AssertionError('no signal')):
                self.assertEqual(agent.control(request)['status'], 'failed')
            with mock.patch.object(agent, 'status', return_value=running), \
                    mock.patch.object(agent.os, 'pidfd_open', return_value=123), \
                    mock.patch.object(agent.os, 'close'), \
                    mock.patch.object(agent, 'start_ticks', return_value='200'), \
                    mock.patch.object(agent.signal, 'pidfd_send_signal', side_effect=AssertionError('no signal')), \
                    self.assertRaisesRegex(ValueError, 'PID changed'):
                agent.control(request)

    def test_restart_preserves_receipt_and_source_and_does_not_duplicate_launch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'source').mkdir()
            (root / 'source/unchanged').write_text('frozen')
            (root / 'results').mkdir()
            old = {'status': 'failed', 'plan_id': 'plan', 'worker': 1, 'pid': 42}
            tool.write_json(root / 'results/worker.json', old)
            tool.write_json(root / 'launch.json', old)
            runner = 'print("fake retry")\n'
            import hashlib
            request = {'remote_dir': str(root), 'plan_id': 'plan', 'worker': 1, 'action': 'restart',
                       'restart_id': 'attempt2', 'runner': runner,
                       'runner_sha256': hashlib.sha256(runner.encode()).hexdigest()}
            with mock.patch.object(agent, 'status', return_value=old), \
                    mock.patch.object(agent.subprocess, 'Popen', return_value=mock.Mock(pid=99)) as launch, \
                    mock.patch.object(agent, 'start_ticks', return_value='123'):
                result = agent.control(request)
            self.assertEqual(result['pid'], 99)
            self.assertEqual(tool.read_json(root / 'attempts/attempt2/worker.json'), old)
            self.assertFalse((root / 'results/worker.json').exists())
            self.assertEqual((root / 'source/unchanged').read_text(), 'frozen')
            self.assertIn(str(root / 'attempts/attempt2/retry.py'), launch.call_args.args[0])
            with mock.patch.object(agent, 'status', return_value=result), \
                    mock.patch.object(agent.subprocess, 'Popen', side_effect=AssertionError('duplicate')):
                self.assertEqual(agent.control(request)['pid'], 99)
            with mock.patch.object(agent, 'status', return_value={'status': 'running', 'pid': 100}), \
                    self.assertRaisesRegex(ValueError, 'must be stopped'):
                agent.control(dict(request, restart_id='attempt3'))

    def test_ps_does_not_confuse_reused_pid_with_live_worker(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tool.write_json(root / 'launch.json', {'pid': 42, 'start_ticks': '100', 'plan_id': 'plan', 'worker': 1})
            tool.write_json(root / 'results/worker.json', {'plan_id': 'plan', 'worker': 1, 'status': 'complete'})
            with mock.patch.object(agent.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'S unrelated process', '')) as ps, mock.patch.object(agent, 'start_ticks', return_value='200'):
                self.assertEqual(agent.status(root)['status'], 'complete')
            self.assertEqual(ps.call_args.args[0][0], 'ps')

    def test_nohup_launch_and_ps_monitor_using_a_local_fake_worker(self):
        # Exercise the actual helper and process lifecycle locally, with a tiny
        # fake worker that writes a receipt; no SSH, Docker, or real build occurs.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'remote'
            source = Path(directory) / 'source'
            script = source / 'tools/openriak-docker/openriak_docker.py'
            script.parent.mkdir(parents=True)
            script.write_text("import json, pathlib, sys, time\np=pathlib.Path(sys.argv[sys.argv.index('--plan')+1]); plan=json.loads(p.read_text()); out=pathlib.Path(sys.argv[sys.argv.index('--output')+1]); time.sleep(.2); (out/'worker.json').write_text(json.dumps({'plan_id':plan['id'],'worker':1,'status':'complete','results':{}})); print('fake worker finished',flush=True)\n")
            script.write_text(script.read_text() + "import os\nprint('TMPDIR=' + os.environ['TMPDIR'], flush=True)\n")
            plan = {'workers': 1, 'sources': {'openriak_docker.py': tool.sha256_file(script)}, 'metadata': {}}
            plan['id'] = distributed.digest(plan)
            tool.write_json(source / 'plan.json', plan)
            root.mkdir()
            archive_path = root / 'initial.tar.gz'
            with tarfile.open(archive_path, 'w:gz') as archive:
                archive.add(script, arcname='tools/openriak-docker/openriak_docker.py')
                archive.add(source / 'plan.json', arcname='plan.json')
            checksum = tool.sha256_file(archive_path)
            archive_path.rename(root / f'bundle-{checksum}.tar.gz')
            request = {'remote_dir': str(root), 'plan_id': plan['id'], 'worker': 1, 'action': 'start', 'sha256': checksum,
                       'tmpdir': directory}
            result = subprocess.run([sys.executable, agent.__file__, json.dumps(request)], text=True, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            launched = json.loads(result.stdout)
            self.assertGreater(launched['pid'], 0)
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                state = agent.control(dict(request, action='status'))
                if state['status'] == 'complete':
                    break
                time.sleep(.05)
            self.assertEqual(state['status'], 'complete')
            self.assertIn('fake worker finished', (root / 'worker.log').read_text())
            self.assertIn('TMPDIR=' + directory, (root / 'worker.log').read_text())
            self.assertEqual(agent.control(request)['pid'], launched['pid'])

    def test_bundle_traversal_and_symlinks_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive_path = root / 'bad.tar.gz'
            with tarfile.open(archive_path, 'w:gz') as archive:
                entry = tarfile.TarInfo('../escape')
                archive.addfile(entry, io.BytesIO(b''))
            checksum = tool.sha256_file(archive_path)
            archive_path.rename(root / f'bundle-{checksum}.tar.gz')
            with self.assertRaisesRegex(ValueError, 'Unsafe'):
                agent.extract(root, {'sha256': checksum})
            self.assertFalse((root.parent / 'escape').exists())


if __name__ == '__main__':
    unittest.main()
