import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from openriak_metadata.cli import main
from openriak_metadata.repository import install_packages


class RepositoryUpdateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.metadata = self.root / 'content/openriak-kv/metadata'
        for version in ('3.4.0', '3.4.1'):
            directory = self.metadata / version
            directory.mkdir(parents=True)
            for filename in ('supported-os.json', 'downloads.json', 'defaults.json', 'user-notes.txt'):
                (directory / filename).write_text('original ' + version + ' ' + filename)
        (self.metadata / 'os-aliases.json').write_text('unchanged aliases')

    def command(self):
        return ['packages', '--product', 'kv', '--version', '3.4.0', '--version', '3.4.1',
                '--refresh', '--update-repo', str(self.root)]

    def discover(self, product, version, files_path, **kwargs):
        filename = 'riak-' + version + '.deb'
        return ([{'id': 'ubuntu-noble-amd64'}], {'ubuntu-noble-amd64': {'otp26-amd64': {
            'url': 'https://files.tiot.jp/test/' + filename, 'filename': filename,
            'checksum': {'algorithm': 'sha256', 'value': 'a' * 64}}}}, [])

    def snapshot(self):
        return {p.relative_to(self.root): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.root.rglob('*') if p.is_file()}

    def test_repeated_versions_install_only_package_metadata_after_all_discovery(self):
        before = self.snapshot()
        def discover(*args, **kwargs):
            self.assertEqual(self.snapshot(), before)
            return self.discover(*args, **kwargs)
        with patch('openriak_metadata.cli.PackageCatalog') as catalog, patch('openriak_metadata.cli.HttpClient') as client:
            catalog.return_value.discover.side_effect = discover
            self.assertEqual(main(self.command()), 0)
        self.assertEqual([c.args[1] for c in catalog.return_value.discover.call_args_list], ['3.4.0', '3.4.1'])
        self.assertTrue(all(c.kwargs['refresh'] for c in client.call_args_list))
        for version in ('3.4.0', '3.4.1'):
            for filename in ('supported-os.json', 'downloads.json'):
                data = json.loads((self.metadata / version / filename).read_text())
                self.assertEqual(data['version'], version)
                self.assertEqual(data['status'], 'complete')
        after = self.snapshot()
        for path in before:
            if path.name not in ('supported-os.json', 'downloads.json'):
                self.assertEqual(before[path], after[path])
        self.assertEqual(set(before), set(after))

    def test_second_version_failure_does_not_install_first_version_without_strict_flag(self):
        for failure in ('warning', 'exception', 'empty'):
            before = self.snapshot()
            def discover(product, version, *args, **kwargs):
                if version == '3.4.0':
                    return self.discover(product, version, *args, **kwargs)
                if failure == 'exception':
                    raise OSError('server unavailable')
                if failure == 'empty':
                    return [], {}, []
                targets, downloads, _ = self.discover(product, version, *args, **kwargs)
                return targets, downloads, ['one package could not be downloaded']
            with self.subTest(failure=failure), patch('openriak_metadata.cli.PackageCatalog') as catalog:
                catalog.return_value.discover.side_effect = discover
                self.assertEqual(main(self.command()), 2)
            self.assertEqual(self.snapshot(), before)

    def test_invalid_later_version_is_rejected_before_any_discovery(self):
        with patch('openriak_metadata.cli.PackageCatalog') as catalog, contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            main(self.command() + ['--version', '../bad'])
        catalog.assert_not_called()

    def test_duplicate_versions_are_generated_once(self):
        with patch('openriak_metadata.cli.PackageCatalog') as catalog:
            catalog.return_value.discover.side_effect = self.discover
            self.assertEqual(main(self.command() + ['--version', '3.4.0']), 0)
        self.assertEqual(catalog.return_value.discover.call_count, 2)

    def test_output_and_update_repo_are_mutually_exclusive(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            main(self.command() + ['--output', str(self.root / 'output')])

    def test_update_repo_defaults_to_checkout(self):
        with patch('openriak_metadata.cli.REPOSITORY_ROOT', self.root), patch('openriak_metadata.cli.PackageCatalog') as catalog:
            catalog.return_value.discover.side_effect = self.discover
            self.assertEqual(main(self.command()[:-1]), 0)

    def test_standalone_output_accepts_multiple_versions_and_preserves_repository(self):
        original = {p: p.read_bytes() for p in self.metadata.rglob('*') if p.is_file()}
        with patch('openriak_metadata.cli.PackageCatalog') as catalog:
            catalog.return_value.discover.side_effect = self.discover
            self.assertEqual(main(['packages', '--product', 'kv', '--version', '3.4.0', '--version', '3.4.1',
                                   '--output', str(self.root / 'output')]), 0)
        self.assertTrue((self.root / 'output/kv/3.4.0/downloads.json').is_file())
        self.assertTrue((self.root / 'output/kv/3.4.1/downloads.json').is_file())
        self.assertEqual(original, {p: p.read_bytes() for p in self.metadata.rglob('*') if p.is_file()})

    def stage(self):
        root = self.root / 'staged'
        for version in ('3.4.0', '3.4.1'):
            directory = root / 'kv' / version
            directory.mkdir(parents=True)
            for filename in ('supported-os.json', 'downloads.json'):
                (directory / filename).write_text('replacement ' + filename)
        return root

    def test_install_failure_restores_original_files_and_mtimes(self):
        stage = self.stage()
        before = self.snapshot()
        real_replace = os.replace
        def replace(source, target):
            if str(source).endswith('3.4.1-supported-os.json.new'):
                raise PermissionError('injected disk failure')
            return real_replace(source, target)
        with patch('openriak_metadata.repository.os.replace', side_effect=replace), self.assertRaises(PermissionError):
            install_packages(stage, self.root, 'kv', ['3.4.0', '3.4.1'])
        self.assertEqual(self.snapshot(), before)

    def test_identical_metadata_is_not_rewritten(self):
        stage = self.stage()
        install_packages(stage, self.root, 'kv', ['3.4.0', '3.4.1'])
        before = self.snapshot()
        self.assertEqual(install_packages(stage, self.root, 'kv', ['3.4.0', '3.4.1']), 0)
        self.assertEqual(self.snapshot(), before)

    def test_symlink_destination_rejected_before_any_replacement(self):
        stage = self.stage()
        target = self.metadata / '3.4.1/downloads.json'
        target.unlink()
        target.symlink_to(self.metadata / '3.4.0/downloads.json')
        before = self.snapshot()
        with self.assertRaises(ValueError):
            install_packages(stage, self.root, 'kv', ['3.4.0', '3.4.1'])
        self.assertEqual(self.snapshot(), before)


if __name__ == '__main__':
    unittest.main()
