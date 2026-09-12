import time
import contextlib
import dataclasses
import io
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool
import commands.cleanup as cleanup
class BuilderLifecycleTests(unittest.TestCase):
    def test_restores_initial_state_after_multiple_groups(self):
        for initial in ('running', 'stopped', 'missing'):
            with self.subTest(initial=initial), tempfile.TemporaryDirectory() as directory:
                state = initial
                commands = []

                def run(command, *args, **kwargs):
                    nonlocal state
                    commands.append(command[1:])
                    self.assertEqual(kwargs['timeout_seconds'], 37)
                    if '--bootstrap' in command:
                        state = 'running'
                    elif 'create' in command:
                        state = 'stopped'
                    return subprocess.CompletedProcess(command, int(state == 'missing'),
                        f'Driver: docker-container\nStatus: {state}\n')

                with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(tool, 'docker_command', return_value='docker'), \
                        mock.patch.object(tool, 'run_logged', side_effect=run):
                    with tool.MultiarchBuilderLifecycle() as lifecycle:
                        for group in ('first', 'second'):
                            tool.ensure_multiarch_builder(pathlib.Path(directory) / group, 37, lifecycle)
                            self.assertNotIn(['buildx', 'stop', tool.MULTIARCH_BUILDER], commands)
                stops = [c for c in commands if c[:2] == ['buildx', 'stop']]
                self.assertEqual(len(stops), int(initial != 'running'))
                if stops:
                    self.assertEqual(commands[-1], stops[0])
                self.assertEqual(sum(c[:2] == ['buildx', 'create'] for c in commands), int(initial == 'missing'))

    def test_bootstrap_failure_and_interrupt_still_stop_builder(self):
        for failure in ('bootstrap', 'build', 'interrupt'):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as directory:
                def run(command, *args, **kwargs):
                    if failure == 'bootstrap' and '--bootstrap' in command:
                        raise tool.DockerToolError('bootstrap failed')
                    return subprocess.CompletedProcess(command, 0, 'Driver: docker-container\nStatus: stopped\n')
                with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(tool, 'docker_command', return_value='docker'), \
                        mock.patch.object(tool, 'run_logged', side_effect=run) as runner:
                    with self.assertRaises(KeyboardInterrupt if failure == 'interrupt' else tool.DockerToolError):
                        with tool.MultiarchBuilderLifecycle() as lifecycle:
                            tool.ensure_multiarch_builder(pathlib.Path(directory), 23, lifecycle)
                            if failure == 'interrupt':
                                raise KeyboardInterrupt
                            raise tool.DockerToolError('build failed')
                    self.assertEqual(runner.call_args.args[0], ['docker', 'buildx', 'stop', tool.MULTIARCH_BUILDER])

    def test_unknown_or_mixed_states_are_not_modified(self):
        for status in ('', 'Status: error\n', 'Status: running\nStatus: stopped\n', 'Driver: remote\nStatus: stopped\n'):
            with self.subTest(status=status), mock.patch.object(tool, 'docker_command', return_value='docker'), \
                    mock.patch.object(tool, 'run_logged', return_value=subprocess.CompletedProcess([], 0, status)) as run:
                with self.assertRaises(tool.DockerToolError):
                    with tool.MultiarchBuilderLifecycle() as lifecycle:
                        tool.ensure_multiarch_builder(pathlib.Path('/unused'), 5, lifecycle)
                self.assertEqual(run.call_count, 1)

    def test_both_refresh_modes_restore_builder_on_exit(self):
        for no_test in (False, True):
            for interrupted in (False, True):
                with self.subTest(no_test=no_test, interrupted=interrupted), tempfile.TemporaryDirectory() as directory:
                    root = pathlib.Path(directory)
                    with mock.patch.object(tool, 'MULTIARCH_CACHE_ROOT', root):
                        target = tool.discover_targets(['3.4.0'])[0]
                        grouped = dataclasses.replace(target, grouped=True)
                        tool.write_json(grouped.group_directory / 'report.json', {'status': 'passed'})
                        def build(group, options, *args):
                            lifecycle = args[-1]
                            tool.ensure_multiarch_builder(root, options.timeout, lifecycle)
                            if interrupted:
                                raise KeyboardInterrupt
                            return False  # Even an ordinary failed group must restore state.
                        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()), \
                                mock.patch.object(tool, 'discover_targets', return_value=[target]), \
                                mock.patch.object(tool, 'refresh_group', side_effect=build), \
                                mock.patch.object(tool, 'rebuild_approved_group', side_effect=build), \
                                mock.patch.object(tool, 'sync_download_metadata'), \
                                mock.patch.object(tool, 'docker_command', return_value='docker'), \
                                mock.patch.object(tool, 'run_logged', return_value=subprocess.CompletedProcess([], 0, 'Driver: docker-container\nStatus: stopped\n')) as run:
                            result = tool.main(['refresh', '--version', '3.4.0', '--timeout', '17', *(['--do-not-test'] if no_test else [])])
                            self.assertEqual(result, 130 if interrupted else 1)
                        self.assertEqual(run.call_args.args[0], ['docker', 'buildx', 'stop', tool.MULTIARCH_BUILDER])
                        self.assertEqual(run.call_args.kwargs['timeout_seconds'], 17)

    def test_unused_lifecycle_never_contacts_docker(self):
        with mock.patch.object(tool, 'docker_command', side_effect=AssertionError('no Docker')):
            with tool.MultiarchBuilderLifecycle():
                pass


class TimingAndConfigTests(unittest.TestCase):
    def test_command_timeout_defaults_and_overrides_agree(self):
        for command in ('refresh', 'generate', 'cleanup'):
            selection = [] if command == 'cleanup' else ['--version', '3.4.0']
            if command == 'generate':
                selection += ['--output', '/tmp/unused-openriak-output']
            self.assertEqual(tool.parser().parse_args([command, *selection]).timeout, 1800)
            self.assertEqual(tool.parser().parse_args([command, *selection, '--timeout', '29']).timeout, 29)

    def test_lifecycle_settings_render_every_service_and_invalidate_cache(self):
        targets = tool.grouped_targets(tool.discover_targets(['3.4.0']))[0]
        original = tool.group_input(targets, 5, [])
        timing = tool.LifecycleOptions(17, 71, 240, 5, 180)
        changed = [dataclasses.replace(t, lifecycle_options=timing) for t in targets]
        bases = {t.platform: {'pinned': tool.base_image_for(t) + '@sha256:' + 'a' * 64} for t in changed}
        dockerfile = tool.render_multiarch_dockerfile(changed, bases, 'cookie', [])
        self.assertIn('HEALTHCHECK --interval=17s --timeout=71s --start-period=240s --retries=5', dockerfile)
        self.assertEqual(tool.render_single_compose(changed[0]).count('stop_grace_period: 180s'), 1)
        self.assertEqual(tool.render_cluster_compose(changed[0], node_count=7).count('stop_grace_period: 180s'), 7)
        self.assertNotEqual(original, tool.group_input(changed, 5, []))

    def test_cli_lifecycle_options_reach_generator_and_validate_before_docker(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            args = ['generate', '--version', '3.4.0', '--output', directory,
                    '--healthcheck-interval', '15s', '--healthcheck-timeout', '2m',
                    '--healthcheck-start-period', '0', '--healthcheck-retries', '4', '--stop-grace-period', '3m']
            with mock.patch.object(tool, 'generate_group', return_value=True) as generate, \
                    mock.patch.object(tool, 'docker_command', side_effect=AssertionError('no Docker')):
                self.assertEqual(tool.main(args), 0)
            self.assertEqual(generate.call_args.args[0][0].lifecycle_options, tool.LifecycleOptions(15, 120, 0, 4, 180))
            with mock.patch.object(tool, 'docker_command', side_effect=AssertionError('no Docker')):
                self.assertEqual(tool.main(args + ['--healthcheck-retries', '0']), 2)
                self.assertEqual(tool.main(['refresh', '--version', '3.4.0', '--do-not-test', '--stop-grace-period', '3m']), 2)

    def test_readiness_commands_use_remaining_budget(self):
        with mock.patch.object(time, 'monotonic', return_value=95), \
                mock.patch.object(subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'pong')) as run:
            tool.run_before_deadline(['docker', 'exec', 'node', 'riak', 'ping'], 100, text=True)
            self.assertEqual(run.call_args.kwargs['timeout'], 5)
        with mock.patch.object(time, 'monotonic', return_value=100), \
                mock.patch.object(subprocess, 'run') as run, self.assertRaises(tool.DockerToolError):
            tool.run_before_deadline(['docker', 'inspect', 'node'], 100)
        run.assert_not_called()
        with mock.patch.object(time, 'monotonic', return_value=95), \
                mock.patch.object(subprocess, 'run', side_effect=subprocess.TimeoutExpired('docker', 5)), \
                self.assertRaisesRegex(tool.DockerToolError, 'exceeded the wait timeout'):
            tool.run_before_deadline(['docker', 'inspect', 'node'], 100)

    def test_cleanup_timeout_reaches_docker_and_has_readable_error(self):
        with mock.patch.object(tool, 'docker_command', return_value='docker'), \
                mock.patch.object(cleanup.subprocess, 'run', side_effect=subprocess.TimeoutExpired('docker', 19)) as run:
            with self.assertRaisesRegex(tool.DockerToolError, 'timed out after 19s'):
                cleanup.docker_run(tool, 'info', timeout=19)
            self.assertEqual(run.call_args.kwargs['timeout'], 19)
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(cleanup, 'docker_run',
                return_value=mock.Mock(stdout='Driver: docker-container\nStatus: stopped\n')) as run:
            cleanup.prune_builder_cache(tool, cleanup.timestamp('2026-09-06T00:00:00Z'), timeout=19)
            self.assertTrue(all(c.kwargs['timeout'] == 19 for c in run.call_args_list))

    def test_startup_and_diagnostic_failures_still_teardown_and_keep_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            target = dataclasses.replace(tool.discover_targets(['3.4.0'])[0], grouped=True, output_root=root / 'cache')
            work = root / 'custom-tmp' / 'openriak-docker-test'
            work.mkdir(parents=True)
            commands = []

            def run(command, log_path, **kwargs):
                commands.append(command)
                self.assertEqual(kwargs['timeout_seconds'], 29)
                if 'container' in command and 'inspect' in command:
                    return subprocess.CompletedProcess(command, 1, '')
                if 'RIAK_INIT_ONLY=1' in command:
                    for name in ('config', 'data', 'logs'):
                        (work / target.node_name / name).mkdir(parents=True)
                    (work / target.node_name / 'config/riak.conf').write_text('logger.max_file_size = 2MB\n')
                if 'up' in command or 'logs' in command:
                    raise tool.DockerToolError('simulated timeout')
                return subprocess.CompletedProcess(command, 0, '')

            base = tool.base_image_for(target)
            with mock.patch.object(tool, 'docker_command', return_value='docker'), \
                    mock.patch.object(tool, 'resolve_base_image', return_value=(base, base + '@sha256:' + 'a' * 64)), \
                    mock.patch.object(tempfile, 'mkdtemp', return_value=str(work)), \
                    mock.patch.object(tool, 'free_tcp_port', return_value=18098), \
                    mock.patch.object(tool, 'run_logged', side_effect=run):
                self.assertFalse(tool.refresh_target(target, 29))
            self.assertTrue(any('down' in command for command in commands))
            report = tool.read_json(target.cache_directory / 'report.json')
            self.assertEqual(report['status'], 'failed')
            self.assertEqual(report['cleanup_errors'], ['simulated timeout'])
            self.assertEqual(report['test_workdir'], str(work))
            self.assertIn('OPENRIAK_CLUSTER_WAIT_SECONDS=29', (work / '.env.cluster').read_text())

    def test_mapping_change_affects_base_and_cache_input_without_code_change(self):
        targets = tool.grouped_targets(tool.discover_targets(['3.4.0']))[0]
        original = tool.group_input(targets, 5, [])
        config = tool.read_json(tool.BASE_IMAGES_PATH)
        family = targets[0].family
        config['families'][family] = {'rules': [{'image': 'example/os:42'}]}
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / 'base-images.json'
            tool.write_json(path, config)
            with mock.patch.object(tool, 'BASE_IMAGES_PATH', path):
                self.assertEqual(tool.base_image_for(targets[0]), 'example/os:42')
                self.assertNotEqual(original, tool.group_input(targets, 5, []))
                for invalid in ('example/os:latest', 'example/os', 'example/os:{unknown}'):
                    config['families'][family]['rules'][0]['image'] = invalid
                    tool.write_json(path, config)
                    with self.assertRaises(tool.DockerToolError):
                        tool.base_image_for(targets[0])


if __name__ == '__main__':
    unittest.main()
