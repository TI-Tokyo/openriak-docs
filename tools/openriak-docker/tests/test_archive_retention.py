import contextlib
import datetime as dt
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool
from cache.retention import archive_selection, merge_archive_selection
import commands.cleanup as cleanup
import core.locks as locks


class ArchiveRetentionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name)
        self.work = self.repo / '.work/openriak-docker'
        self.cutoff = dt.datetime(2026, 6, 15, tzinfo=dt.timezone.utc)
        self.old = self.cutoff - dt.timedelta(days=1)
        self.new = self.cutoff + dt.timedelta(days=1)
        for name, value in {'REPOSITORY_ROOT': self.repo, 'CACHE_ROOT': self.work / 'legacy',
                            'MULTIARCH_CACHE_ROOT': self.work / 'images', 'STATIC_ROOT': self.repo / 'static'}.items():
            patch = mock.patch.object(tool, name, value)
            patch.start()
            self.addCleanup(patch.stop)

    def write(self, relative, when=None, value='diagnostic'):
        path = self.work / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value) if isinstance(value, dict) else value)
        epoch = (when or self.old).timestamp()
        os.utime(path, (epoch, epoch))
        return path

    def test_90_day_boundary_and_all_archive_kinds(self):
        paths = [self.write(p) for p in (
            'images/pushes/run/image/scout-output/hash.gz', 'bases/run/logs/build.log',
            'images/version/tag/runs/run/image.oci.tar', 'distributed/bundles/plan.bundle.tar.gz',
            'migration-prototypes/old/history/hash.json', 'legacy/refresh.log',
            'experiments/amazon-amd64-scout.json', 'experiments/suse-sbom.json',
            'images/version/tag/runs/run/Dockerfile')]
        boundary = self.write('images/pushes/exact/scout-output/hash.gz', self.cutoff)
        recent = self.write('experiments/run/logs/recent.log', self.new)
        approval = self.write('images/version/tag/report.json', value={'status': 'passed'})
        source = self.write('images/version/tag/Dockerfile')
        expired, retained = archive_selection(self.work, self.cutoff)
        self.assertEqual(expired, set(paths))
        self.assertEqual(retained, {boundary, recent})
        self.assertNotIn(approval, expired)
        self.assertNotIn(source, expired)

    def test_recent_completion_keeps_old_files_but_new_current_does_not_pin_history(self):
        self.write('images/version/tag/report.json', self.new, {'status': 'passed', 'finished_at': self.new.isoformat()})
        self.write('images/version/tag/runs/old/report.json', self.old, {'status': 'passed', 'finished_at': self.old.isoformat()})
        old = self.write('images/version/tag/runs/old/logs/build.log')
        self.write('images/version/tag/runs/recent/report.json', self.new, {'status': 'passed', 'finished_at': self.new.isoformat()})
        recent = self.write('images/version/tag/runs/recent/logs/build.log')
        expired, retained = archive_selection(self.work, self.cutoff)
        self.assertEqual(expired, {old})
        self.assertEqual(retained, {recent})

    def test_running_and_unreadable_reports_retained_unless_clearing(self):
        self.write('images/pushes/running/report.json', value={'status': 'running'})
        running = self.write('images/pushes/running/scout-output/hash.gz')
        broken = self.write('images/pushes/broken/report.json', value='{')
        expired, retained = archive_selection(self.work, self.cutoff)
        self.assertFalse(expired)
        self.assertIn(running, retained)
        self.assertIn(broken, retained)
        expired, retained = archive_selection(self.work, self.cutoff, clear=True)
        self.assertIn(running, expired)
        self.assertIn(broken, expired)
        self.assertFalse(retained)

    def test_parent_cleanup_cannot_bypass_retention(self):
        recent = self.write('images/version/tag/runs/run/logs/build.log', self.new)
        old = self.write('images/version/tag/runs/old/logs/build.log')
        tree = self.work / 'images/version/tag'
        expired, retained = archive_selection(self.work, self.cutoff)
        self.assertEqual(merge_archive_selection([tree], [recent], expired, retained), ([], [old]))
        expired, retained = archive_selection(self.work, self.cutoff, clear=True)
        self.assertEqual(merge_archive_selection([tree], [], expired, retained), ([tree], []))

    def test_symlinks_are_not_followed_or_selected(self):
        external = self.repo / 'outside.log'
        external.write_text('keep')
        self.work.mkdir(parents=True)
        (self.work / 'link.log').symlink_to(external)
        (self.work / 'logs').symlink_to(self.repo, target_is_directory=True)
        self.assertEqual(archive_selection(self.work, self.cutoff, clear=True), (set(), set()))
        self.assertEqual(external.read_text(), 'keep')

    def test_clear_preview_and_delete_preserve_durable_records_and_sources(self):
        archive = self.write('images/version/tag/runs/run/image.oci.tar', self.new)
        source = self.write('images/version/tag/Dockerfile')
        retained = self.repo / 'records/openriak-docker/approval.json'
        retained.parent.mkdir(parents=True)
        retained.write_text('retained approval')
        args = ['cleanup', '--clear-archives', '--before', '2020-01-01']
        with contextlib.redirect_stdout(io.StringIO()) as output, mock.patch.object(cleanup, 'docker_run') as docker:
            self.assertEqual(cleanup.main(tool.parser().parse_args(args), tool), 0)
            self.assertTrue(archive.exists())
            self.assertIn('clear all local archives', output.getvalue())
            self.assertEqual(cleanup.main(tool.parser().parse_args(args + ['--delete']), tool), 0)
            docker.assert_not_called()
        self.assertFalse(archive.exists())
        self.assertTrue(source.exists())
        self.assertEqual(retained.read_text(), 'retained approval')

    def test_active_generator_lock_blocks_clear_before_deletion(self):
        archive = self.write('images/pushes/run/scout-output/hash.gz')
        args = tool.parser().parse_args(['cleanup', '--clear-archives', '--delete'])
        with locks.activity(tool), contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(tool.DockerToolError, 'Resource is in use'):
            cleanup.main(args, tool)
        self.assertTrue(archive.exists())

    def test_cli_default_cutoff_is_90_days_and_before_can_only_shorten_selection(self):
        now = dt.datetime.now().astimezone()
        old = self.write('legacy/old.log', now - dt.timedelta(days=91))
        recent = self.write('legacy/recent.log', now - dt.timedelta(days=89))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            cleanup.main(tool.parser().parse_args(['cleanup']), tool)
        self.assertIn('Archive retention: 90 days', output.getvalue())
        earlier = (now - dt.timedelta(days=92)).isoformat()
        with contextlib.redirect_stdout(io.StringIO()):
            cleanup.main(tool.parser().parse_args(['cleanup', '--before', earlier, '--delete']), tool)
        self.assertTrue(old.exists())
        with contextlib.redirect_stdout(io.StringIO()):
            cleanup.main(tool.parser().parse_args(['cleanup', '--delete']), tool)
        self.assertFalse(old.exists())
        self.assertTrue(recent.exists())
