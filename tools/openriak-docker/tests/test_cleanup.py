import argparse
import contextlib
import datetime as dt
import io
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool
import openriak_cleanup as cleanup


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for name, value in {'REPOSITORY_ROOT': self.root, 'CACHE_ROOT': self.root / 'legacy',
                            'MULTIARCH_CACHE_ROOT': self.root / 'multiarch', 'STATIC_ROOT': self.root / 'static'}.items():
            patch = mock.patch.object(tool, name, value)
            patch.start()
            self.addCleanup(patch.stop)
        self.cutoff = cleanup.timestamp('2026-09-06T15:30:00+09:00')
        self.old = '2026-09-06T05:00:00Z'
        self.new = '2026-09-06T07:00:00Z'
        self.group = tool.MULTIARCH_CACHE_ROOT / '3.4.0' / '3.4.0-alpine-3.21-otp24'
        self.image = 'openriak/openriak-kv:3.4.0-alpine-3.21-otp24'

    def write(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value) if isinstance(value, dict) else value)
        return path

    def age(self, path, value=None):
        epoch = cleanup.timestamp(value or self.old).timestamp()
        for item in [path, *path.rglob('*')]:
            os.utime(item, (epoch, epoch), follow_symlinks=False)

    def report(self, root, value=None, run='20260906T050000.000000Z'):
        report = {'status': 'passed', 'image': self.image, 'run_id': run,
                  'started_at': self.old, 'finished_at': value or self.old,
                  'tags': [self.image, 'openriak/openriak-kv:3.4.0']}
        self.write(root / 'report.json', report)
        self.write(root / 'Dockerfile', 'approved image')
        self.age(root)
        return report

    def options(self, **overrides):
        return argparse.Namespace(**{'before': self.cutoff, 'remove_all': False, 'delete': False,
                                     'timeout': 1, **overrides})

    def test_cutoff_explicit_offset_and_exclusive_boundary(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            tool.parser().parse_args(['cleanup', '--before', '2026-09-06 15:30'])
        parsed = tool.parser().parse_args(['cleanup', '--before', '2026-09-06T15:30:00+09:00'])
        self.assertEqual(parsed.before, cleanup.timestamp('2026-09-06T06:30:00Z'))
        self.report(self.group)
        self.age(self.group, '2026-09-06T06:30:00Z')
        self.assertEqual(cleanup.file_plan(tool, self.cutoff, True), ([], []))

    def test_local_date_and_time_use_machine_timezone(self):
        try:
            with mock.patch.dict(os.environ, {'TZ': 'Asia/Tokyo'}):
                time.tzset()
                for value, expected in [
                    ('2026-09-06', '2026-09-06T00:00:00+09:00'),
                    ('2026-09-06T15:30:00', '2026-09-06T15:30:00+09:00'),
                    ('2026-09-06T06:30:00Z', '2026-09-06T06:30:00+00:00'),
                    ('2026-09-06T15:30:00-04:00', '2026-09-06T15:30:00-04:00'),
                ]:
                    with self.subTest(value=value):
                        parsed = tool.parser().parse_args(['cleanup', '--before', value])
                        self.assertEqual(parsed.before.isoformat(), expected)
        finally:
            time.tzset()

    def test_local_cutoff_uses_dst_offset_for_selected_date(self):
        try:
            with mock.patch.dict(os.environ, {'TZ': 'America/New_York'}):
                time.tzset()
                self.assertEqual(cleanup.cutoff_argument('2026-01-01').utcoffset(), dt.timedelta(hours=-5))
                self.assertEqual(cleanup.cutoff_argument('2026-07-01').utcoffset(), dt.timedelta(hours=-4))
        finally:
            time.tzset()

    def test_omitted_cutoff_is_now_captured_once_and_logged_exactly(self):
        self.assertIsNone(tool.parser().parse_args(['cleanup']).before)
        now = cleanup.timestamp('2026-09-06T15:30:00.123456+09:00')
        with mock.patch.object(cleanup.dt, 'datetime') as clock, \
                mock.patch.object(cleanup, 'file_plan', return_value=([], [])) as plan, \
                contextlib.redirect_stdout(io.StringIO()) as output:
            clock.now.return_value.astimezone.return_value = now
            self.assertEqual(cleanup.main(self.options(before=None), tool), 0)
        clock.now.assert_called_once_with()
        self.assertEqual(plan.call_args.args[1], now)
        self.assertTrue(output.getvalue().startswith('Cleanup cutoff (--before): 2026-09-06T15:30:00.123456+09:00\n'))

    def test_explicit_cutoff_is_logged_before_planning(self):
        with mock.patch.object(cleanup, 'file_plan', return_value=([], [])), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            cleanup.main(self.options(), tool)
        self.assertTrue(output.getvalue().startswith('Cleanup cutoff (--before): 2026-09-06T15:30:00.000000+09:00\n'))

    def test_invalid_dates_and_future_cutoffs_are_rejected(self):
        for value in ('2026-02-30', '2026-09-06T25:00:00', 'not-a-date'):
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                cleanup.cutoff_argument(value)
        future = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=1)
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(cleanup, 'file_plan') as plan, \
                self.assertRaises(tool.DockerToolError):
            cleanup.main(self.options(before=future), tool)
        plan.assert_not_called()

    def test_docker_nanosecond_timestamps_are_accepted(self):
        self.assertEqual(cleanup.timestamp('2025-10-31T05:45:27.462216428Z'),
                         cleanup.timestamp('2025-10-31T05:45:27.462216+00:00'))

    def test_normal_cleanup_preserves_current_runs_reports_and_recent_activity(self):
        self.report(self.group)
        current = self.group / 'runs/20260906T050000.000000Z'
        old = self.group / 'runs/20260906T040000.000000Z'
        active = self.group / 'runs/20260906T030000.000000Z'
        for run in (current, old, active):
            self.report(run)
        self.write(active / 'logs/build.log', 'recent activity')
        trees, files = cleanup.file_plan(tool, self.cutoff)
        self.assertEqual(trees, [])
        self.assertEqual(files, [old / 'Dockerfile'])
        self.assertNotIn(old / 'report.json', files)

    def test_new_finished_time_keeps_run_even_if_file_mtimes_are_old(self):
        run = self.group / 'runs/20260906T040000.000000Z'
        self.report(run, self.new)
        self.assertEqual(cleanup.file_plan(tool, self.cutoff, True), ([], []))

    def test_recent_run_id_keeps_incomplete_history(self):
        run = self.group / 'runs/20260906T070000.000000Z'
        self.report(run)
        self.assertEqual(cleanup.file_plan(tool, self.cutoff, True), ([], []))

    def test_full_cleanup_removes_old_current_cache_static_and_only_docker_metadata(self):
        report = self.report(self.group)
        published = tool.STATIC_ROOT / '3.4.0' / self.group.name
        self.write(published / 'Dockerfile', 'old download')
        self.age(published)
        version = tool.REPOSITORY_ROOT / 'tools/generated/openriak-kv/data/versions/3.4.0.json'
        retained = {'image': 'openriak/openriak-kv:new', 'testedAt': self.new}
        self.write(version, {'downloads': ['package.deb'], 'dockerImages': [
            {'image': self.image, 'testedAt': self.old}, retained]})
        with contextlib.redirect_stdout(io.StringIO()), \
                mock.patch.object(cleanup, 'process_table', return_value={}), \
                mock.patch.object(cleanup, 'docker_run'), \
                mock.patch.object(cleanup, 'docker_plan', return_value=([], [], [], False)):
            cleanup.main(self.options(remove_all=True, delete=True), tool)
        self.assertFalse(self.group.exists())
        self.assertFalse(published.exists())
        self.assertEqual(json.loads(version.read_text()), {'downloads': ['package.deb'], 'dockerImages': [retained]})

    def test_recent_metadata_protects_current_cache_and_downloads(self):
        self.report(self.group)
        published = tool.STATIC_ROOT / '3.4.0' / self.group.name
        self.write(published / 'Dockerfile', 'old bytes freshly tested')
        self.age(published)
        self.write(tool.REPOSITORY_ROOT / 'tools/generated/openriak-kv/data/versions/3.4.0.json', {
            'dockerImages': [{'image': self.image, 'testedAt': self.new,
                              'dockerfile': {'url': f'downloads/docker/3.4.0/{self.group.name}/Dockerfile'}}]})
        self.assertEqual(cleanup.file_plan(tool, self.cutoff, True), ([], []))

    def test_symlink_in_run_prevents_deletion(self):
        run = self.group / 'runs/20260906T040000.000000Z'
        self.report(run)
        (run / 'outside').symlink_to(self.root / 'unrelated')
        self.age(run)
        self.assertEqual(cleanup.file_plan(tool, self.cutoff, True), ([], []))

    def test_full_preview_never_stops_or_deletes(self):
        self.report(self.group)
        old_worker = {123: {'started': cleanup.timestamp(self.old)}}
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(cleanup, 'process_table', return_value={}), \
                mock.patch.object(cleanup, 'generator_workers', return_value=old_worker), \
                mock.patch.object(cleanup, 'stop_workers') as stop, mock.patch.object(cleanup, 'docker_run') as docker, \
                mock.patch.object(cleanup, 'docker_plan', return_value=([], [self.image], [], True)):
            cleanup.main(self.options(remove_all=True), tool)
        stop.assert_not_called()
        self.assertEqual(len(docker.call_args_list), 1)
        self.assertEqual(docker.call_args.args[1], 'info')
        self.assertTrue((self.group / 'report.json').exists())

    def test_newer_worker_blocks_full_apply_without_stopping_anyone(self):
        workers = {1: {'started': cleanup.timestamp(self.old)}, 2: {'started': cleanup.timestamp(self.new)}}
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(cleanup, 'process_table', return_value={}), \
                mock.patch.object(cleanup, 'generator_workers', return_value=workers), \
                mock.patch.object(cleanup, 'stop_workers') as stop, self.assertRaises(tool.DockerToolError):
            cleanup.main(self.options(remove_all=True, delete=True), tool)
        stop.assert_not_called()

    def test_worker_selector_matches_exact_repository_and_operation(self):
        script = str(tool.REPOSITORY_ROOT / 'tools/openriak-docker/openriak_docker.py')
        processes = {1: {'args': ['python3', script, 'refresh']},
                     2: {'args': ['python3', '/another/openriak_docker.py', 'refresh']},
                     3: {'args': ['python3', script, 'matrix']},
                     4: {'args': ['python3', script, 'cleanup']}}
        self.assertEqual(set(cleanup.generator_workers(tool, processes)), {1})

    def test_worker_pid_reuse_is_not_signalled(self):
        workers = {123: {'token': 'old'}}
        table = {123: {'token': 'new', 'ppid': 1}}
        with mock.patch.object(cleanup, 'process_table', side_effect=[table, table, {}]), \
                mock.patch.object(cleanup.os, 'kill') as kill:
            cleanup.stop_workers(tool, workers, 1)
        kill.assert_not_called()

    def test_worker_and_its_children_stop_without_signalling_unrelated_processes(self):
        workers = {123: {'token': 'worker'}}
        table = {123: {'token': 'worker', 'ppid': 1}, 124: {'token': 'build', 'ppid': 123},
                 125: {'token': 'other', 'ppid': 1}}
        with mock.patch.object(cleanup, 'process_table', side_effect=[table, table, table, {}]), \
                mock.patch.object(cleanup.os, 'kill') as kill:
            cleanup.stop_workers(tool, workers, 1)
        self.assertEqual([call.args[0] for call in kill.call_args_list], [123, 124])

    def test_stop_timeout_aborts_before_deleting_files(self):
        self.report(self.group)
        workers = {123: {'started': cleanup.timestamp(self.old)}}
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(cleanup, 'process_table', return_value={}), \
                mock.patch.object(cleanup, 'generator_workers', return_value=workers), \
                mock.patch.object(cleanup, 'docker_run'), \
                mock.patch.object(cleanup, 'stop_workers', side_effect=tool.DockerToolError('timeout')), \
                mock.patch.object(cleanup, 'docker_plan') as plan, self.assertRaises(tool.DockerToolError):
            cleanup.main(self.options(remove_all=True, delete=True), tool)
        plan.assert_not_called()
        self.assertTrue((self.group / 'Dockerfile').exists())

    def test_permission_check_precedes_worker_and_docker_actions(self):
        self.report(self.group)
        denied = self.group
        real_access = os.access
        def access(path, mode):
            return False if path == denied else real_access(path, mode)
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(cleanup.os, 'access', side_effect=access), \
                mock.patch.object(cleanup, 'process_table') as processes, \
                mock.patch.object(cleanup, 'docker_run') as docker, \
                self.assertRaises(tool.DockerToolError) as raised:
            cleanup.main(self.options(remove_all=True, delete=True), tool)
        self.assertIn(str(denied.absolute()), str(raised.exception))
        self.assertIn('owner UID', str(raised.exception))
        processes.assert_not_called()
        docker.assert_not_called()
        self.assertTrue((self.group / 'report.json').exists())

    def test_nested_directory_and_metadata_write_permissions_are_checked(self):
        nested = self.group / 'runs/old/logs'
        nested.mkdir(parents=True)
        for trees, files, changes, denied in [
            ([self.group], [], [], nested),
            ([], [nested / 'build.log'], [], nested),
            ([], [], [(nested / 'version.json', {}, 1)], nested),
        ]:
            with self.subTest(trees=trees, files=files, changes=changes), \
                    mock.patch.object(cleanup.os, 'access', side_effect=lambda path, mode: path != denied), \
                    self.assertRaises(tool.DockerToolError) as raised:
                cleanup.check_write_access(tool, trees, files, changes)
            self.assertIn(str(denied.absolute()), str(raised.exception))

    def test_read_only_file_can_be_deleted_when_parent_is_writable(self):
        path = self.write(self.root / 'read-only.log', 'evidence')
        path.chmod(0o400)
        cleanup.check_write_access(tool, [], [path], [])
        self.assertTrue(path.exists())

    def test_recursive_deletion_errors_include_full_path(self):
        path = self.group / 'runs/old/report.json'
        def rmtree(root, onerror):
            error = PermissionError(13, 'Permission denied', 'report.json')
            onerror(os.unlink, str(path), (PermissionError, error, None))
        with mock.patch.object(cleanup.shutil, 'rmtree', side_effect=rmtree), self.assertRaises(PermissionError) as raised:
            cleanup.remove_tree(self.group)
        self.assertEqual(raised.exception.filename, str(path.absolute()))

    def test_only_old_harness_containers_and_their_unused_networks_are_selected(self):
        def container(identifier, path, when=None):
            return {'Id': identifier, 'Image': 'image', 'Created': when or self.old, 'Config': {'Labels': {
                'com.docker.compose.project': identifier,
                'com.docker.compose.project.config_files': path}}}
        containers = [container('old', '/tmp/openriak-docker-test/compose.single.test.yaml'),
                      container('custom', '/home/peter/tmp/builds/openriak-docker-test/compose.cluster.test.yaml'),
                      container('other', '/home/peter/tmp/builds/other/compose.cluster.test.yaml'),
                      container('nested', '/home/peter/tmp/openriak-docker-test/nested/compose.cluster.test.yaml'),
                      container('new', '/tmp/openriak-docker-test/compose.cluster.test.yaml', self.new),
                      container('docs', '/repo/docker/compose.yaml'),
                      container('user', '/tmp/openriak-docker-test/compose.single.yaml')]
        def docker(*args, **kwargs):
            if args[1:3] == ('network', 'ls'):
                return mock.Mock(stdout='{"ID":"network"}\n{"ID":"other"}\n')
            if args[1:3] == ('network', 'inspect'):
                network = args[3]
                return mock.Mock(stdout=json.dumps([{'Id': network, 'Labels': {
                    'com.docker.compose.project': 'old' if network == 'network' else 'docs'},
                    'Containers': {'old': {}} if network == 'network' else {'docs': {}}}]))
            return mock.Mock(stdout='')
        with mock.patch.object(cleanup, 'inspect_all', side_effect=[containers, []]), \
                mock.patch.object(cleanup, 'docker_run', side_effect=docker):
            selected, _, networks, _ = cleanup.docker_plan(tool, self.cutoff)
        self.assertEqual([c['Id'] for c in selected], ['old', 'custom'])
        self.assertEqual(networks, ['network'])

    def test_docker_plan_preserves_recent_shared_and_unrelated_images(self):
        self.report(self.group)
        def image(identifier, tags, when=None):
            return {'Id': identifier, 'RepoTags': tags, 'Created': when or self.old,
                    'Config': {'Labels': {'org.openriak.image.tag': self.image}}}
        images = [image('old', [self.image, 'unrelated:alias']),
                  image('new', [self.image], self.new), image('used', [self.image]),
                  image('dangling', []), image('test', ['openriak/openriak-kv:test-old']),
                  {'Id': 'other', 'RepoTags': ['openriak-os-sink:latest'], 'Created': self.old, 'Config': {'Labels': {}}}]
        containers = [{'Id': 'c1', 'Image': 'used', 'Config': {'Labels': {}}, 'Created': self.old}]
        with mock.patch.object(cleanup, 'inspect_all', side_effect=[containers, images]), \
                mock.patch.object(cleanup, 'docker_run', return_value=mock.Mock(stdout='')):
            removed, tags, networks, builder = cleanup.docker_plan(tool, self.cutoff)
        self.assertEqual(removed, [])
        self.assertEqual(set(tags), {self.image, 'dangling', 'openriak/openriak-kv:test-old'})
        self.assertEqual(networks, [])

    def test_recent_rebuild_preserves_old_created_image(self):
        self.report(self.group)
        self.report(self.group / 'rebuilds/20260906T070000.000000Z', self.new)
        image = {'Id': 'old', 'Created': self.old, 'RepoTags': [self.image], 'Config': {'Labels': {}}}
        with mock.patch.object(cleanup, 'inspect_all', side_effect=[[], [image]]), \
                mock.patch.object(cleanup, 'docker_run', return_value=mock.Mock(stdout='')):
            self.assertEqual(cleanup.docker_plan(tool, self.cutoff)[1], [])

    def test_full_apply_prunes_only_dedicated_builder_with_cutoff(self):
        def run(*args, **kwargs):
            return mock.Mock(stdout='Driver: docker-container\nStatus: running\n' if args[1:3] == ('buildx', 'inspect') else '')
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(cleanup, 'process_table', return_value={}), \
                mock.patch.object(cleanup, 'docker_plan', return_value=([], [], [], True)), \
                mock.patch.object(cleanup, 'docker_run', side_effect=run) as docker:
            cleanup.main(self.options(remove_all=True, delete=True), tool)
        command = docker.call_args.args[1:]
        self.assertEqual(command[:6], ('buildx', 'prune', '--builder', tool.MULTIARCH_BUILDER, '--all', '--force'))
        self.assertEqual(command[6], '--filter')
        self.assertRegex(command[7], r'^until=\d+s$')

    def test_stopped_builder_is_bootstrapped_pruned_and_stopped_again(self):
        def run(*args, **kwargs):
            return mock.Mock(stdout='Name: openriak-kv-multiarch\nDriver:        docker-container\n\nNodes:\nStatus:                stopped\n')
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(cleanup, 'docker_run', side_effect=run) as docker:
            cleanup.prune_builder_cache(tool, self.cutoff)
        commands = [call.args[1:] for call in docker.call_args_list]
        self.assertEqual(commands[0], ('buildx', 'inspect', tool.MULTIARCH_BUILDER))
        self.assertEqual(commands[1], ('buildx', 'inspect', tool.MULTIARCH_BUILDER, '--bootstrap'))
        self.assertEqual(commands[2][:4], ('buildx', 'prune', '--builder', tool.MULTIARCH_BUILDER))
        self.assertEqual(commands[3], ('buildx', 'stop', tool.MULTIARCH_BUILDER))

    def test_builder_is_stopped_again_even_when_bootstrap_or_prune_fails(self):
        for failure in ('bootstrap', 'prune'):
            def run(*args, **kwargs):
                if (failure == 'bootstrap' and '--bootstrap' in args) or (failure == 'prune' and 'prune' in args):
                    raise tool.DockerToolError(failure + ' failed')
                return mock.Mock(stdout='Driver: docker-container\nStatus: stopped\n')
            with self.subTest(failure=failure), contextlib.redirect_stdout(io.StringIO()), \
                    mock.patch.object(cleanup, 'docker_run', side_effect=run) as docker, self.assertRaises(tool.DockerToolError):
                cleanup.prune_builder_cache(tool, self.cutoff)
            self.assertEqual(docker.call_args.args[1:], ('buildx', 'stop', tool.MULTIARCH_BUILDER))

    def test_prune_cutoff_is_calculated_after_bootstrap(self):
        after_bootstrap = self.cutoff + dt.timedelta(seconds=30)
        def run(*args, **kwargs):
            if 'prune' in args:
                self.assertEqual(args[-1], 'until=30s')
            return mock.Mock(stdout='Driver: docker-container\nStatus: stopped\n')
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(cleanup, 'docker_run', side_effect=run), \
                mock.patch.object(cleanup.dt, 'datetime') as clock:
            clock.now.return_value = after_bootstrap
            cleanup.prune_builder_cache(tool, self.cutoff)

    def test_unknown_or_mixed_builder_states_are_not_modified(self):
        for inspection in ('', 'Status: error\n', 'Status: stopped\nStatus: running\n', 'Driver: remote\nStatus: stopped\n'):
            with self.subTest(inspection=inspection), \
                    mock.patch.object(cleanup, 'docker_run', return_value=mock.Mock(stdout=inspection)) as docker, \
                    self.assertRaises(tool.DockerToolError):
                cleanup.prune_builder_cache(tool, self.cutoff)
            self.assertEqual(docker.call_count, 1)


if __name__ == '__main__':
    unittest.main()
