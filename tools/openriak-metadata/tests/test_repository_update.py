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
from openriak_metadata.source import Repository


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

    def command(self, name="kv-packages", *extra):
        args = [name, "--metadata-dir", str(self.root / "staged")]
        if name == "kv-packages":
            args += ["--version", "3.4.0", "--version", "3.4.1", "--refresh"]
        if name == "deploy":
            args += ["--repo", str(self.root)]
        return args + list(extra)

    def discover(self, product, version, files_path, **kwargs):
        filename = "riak-" + version + ".deb"
        return ([{"id": "ubuntu-noble-amd64", "family": "ubuntu", "package_family": "deb"}], {"ubuntu-noble-amd64": {"otp26-amd64": {
            "url": "https://files.tiot.jp/test/" + filename, "filename": filename,
            "checksum": {"algorithm": "sha256", "value": "a" * 64}}}}, [])

    def settings(self, args, product, targets):
        return {"schema_version": 2, "defaults_scope": "os", "product": "kv", "version": args.version,
                "status": "complete", "settings": {"ring_size": {}},
                "effective_defaults": {target["family"]: {"ring_size": {"value": 64}} for target in targets},
                "warnings": []}

    def snapshot(self):
        return {p.relative_to(self.metadata): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.metadata.rglob("*") if p.is_file()}

    def generate_packages(self):
        with patch("openriak_metadata.cli.PackageCatalog") as catalog:
            catalog.return_value.discover.side_effect = self.discover
            self.assertEqual(main(self.command()), 0)
        return catalog

    def test_four_command_workflow_only_deploy_updates_docs(self):
        before = self.snapshot()
        self.generate_packages()
        self.assertEqual(self.snapshot(), before)
        with patch("openriak_metadata.cli.generate_defaults", side_effect=self.settings) as settings, \
                patch("openriak_metadata.cli.PackageCatalog", side_effect=AssertionError("settings rediscovered packages")):
            self.assertEqual(main(self.command("kv-settings")), 0)
        self.assertEqual([call.args[0].version for call in settings.call_args_list], ["3.4.0", "3.4.1"])
        self.assertEqual(self.snapshot(), before)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(main(self.command("list")), 0)
        self.assertIn("GENERATED (UTC)", output.getvalue())
        self.assertEqual(output.getvalue().count("yes"), 6)
        self.assertIn("defaults.json", output.getvalue())
        self.assertEqual(self.snapshot(), before)
        with patch("openriak_metadata.cli.PackageCatalog", side_effect=AssertionError("deploy regenerated")), \
                patch("openriak_metadata.cli.generate_defaults", side_effect=AssertionError("deploy regenerated")):
            self.assertEqual(main(self.command("deploy")), 0)
        for version in ("3.4.0", "3.4.1"):
            for filename in ("supported-os.json", "downloads.json", "defaults.json"):
                self.assertEqual(json.loads((self.metadata / version / filename).read_text())["version"], version)
        after = self.snapshot()
        for path in before:
            if path.name in ("user-notes.txt", "os-aliases.json"):
                self.assertEqual(before[path], after[path])
        self.assertEqual(main(self.command("deploy")), 0)
        self.assertEqual(self.snapshot(), after)

    def test_package_only_deploy_preserves_existing_settings(self):
        before = self.snapshot()
        self.generate_packages()
        self.assertEqual(main(self.command("deploy")), 0)
        for version in ("3.4.0", "3.4.1"):
            self.assertEqual(self.snapshot()[Path(version) / "defaults.json"], before[Path(version) / "defaults.json"])

    def test_settings_command_extracts_from_exact_source_tag_using_staged_targets(self):
        self.generate_packages()
        source = self.root / "source"
        (source / "priv").mkdir(parents=True)
        (source / "rebar.config").write_text("[].")
        (source / "priv/riak.schema").write_text(
            '{mapping, "ring_size", "riak_core.ring_creation_size", [{default, 64}]}.'
        )
        repository = Repository("riak", "OpenRiak/riak", "fixture-commit", 0, source)
        with patch("openriak_metadata.cli.SourceResolver") as resolver, \
                patch("openriak_metadata.cli.PackageCatalog", side_effect=AssertionError("package discovery used")):
            resolver.return_value.resolve.return_value = (repository, [repository], [])
            self.assertEqual(main(self.command("kv-settings", "--version", "3.4.1", "--strict")), 0)
        resolver.return_value.resolve.assert_called_once_with("github.com/OpenRiak/riak", "riak-3.4.1")
        resolver.return_value.close.assert_called_once()
        document = json.loads((self.root / "staged/kv/3.4.1/defaults.json").read_text())
        self.assertEqual(document["effective_defaults"]["ubuntu"]["ring_size"]["value"], 64)
        self.assertEqual(document["status"], "complete")
        self.assertFalse((self.root / "staged/kv/3.4.0/defaults.json").exists())

    def test_failed_batch_preserves_previous_staged_metadata(self):
        self.generate_packages()
        stage = self.root / "staged"
        before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in stage.rglob("*.json")}
        for failure in ("warning", "exception", "empty"):
            def discover(product, version, *args, **kwargs):
                if version == "3.4.0":
                    return self.discover(product, version, *args, **kwargs)
                if failure == "exception":
                    raise OSError("server unavailable")
                if failure == "empty":
                    return [], {}, []
                targets, downloads, _ = self.discover(product, version, *args, **kwargs)
                return targets, downloads, ["one package could not be downloaded"]
            with self.subTest(failure=failure), patch("openriak_metadata.cli.PackageCatalog") as catalog:
                catalog.return_value.discover.side_effect = discover
                self.assertEqual(main(self.command()), 2)
            self.assertEqual({p: (p.read_bytes(), p.stat().st_mtime_ns) for p in before}, before)

    def test_invalid_later_version_is_rejected_before_any_discovery(self):
        with patch("openriak_metadata.cli.PackageCatalog") as catalog, contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            main(self.command("kv-packages", "--version", "../bad"))
        catalog.assert_not_called()

    def test_duplicate_versions_are_generated_once(self):
        with patch("openriak_metadata.cli.PackageCatalog") as catalog:
            catalog.return_value.discover.side_effect = self.discover
            self.assertEqual(main(self.command("kv-packages", "--version", "3.4.0")), 0)
        self.assertEqual(catalog.return_value.discover.call_count, 2)

    def test_bad_later_release_blocks_entire_deployment(self):
        self.generate_packages()
        before = self.snapshot()
        path = self.root / "staged/kv/3.4.1/downloads.json"
        original = json.loads(path.read_text())
        for failure in ("malformed", "checksum", "identity", "missing"):
            document = json.loads(json.dumps(original))
            if failure == "checksum":
                next(iter(document["downloads"]["ubuntu-noble-amd64"].values()))["checksum"]["value"] = "invalid"
            if failure == "identity":
                document["version"] = "3.4.0"
            path.write_text("invalid JSON" if failure == "malformed" else json.dumps(document))
            if failure == "missing":
                path.unlink()
            with self.subTest(failure=failure):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(main(self.command("list")), 2)
                self.assertIn("3.4.1:", output.getvalue())
                self.assertEqual(main(self.command("deploy")), 2)
                self.assertEqual(self.snapshot(), before)

    def test_version_filter_and_default_repository(self):
        self.generate_packages()
        before = self.snapshot()
        with patch("openriak_metadata.cli.REPOSITORY_ROOT", self.root):
            self.assertEqual(main(["deploy", "--output", str(self.root / "staged"), "--version", "3.4.1"]), 0)
        for path in before:
            if path.parts[0] == "3.4.0":
                self.assertEqual(self.snapshot()[path], before[path])

    def test_empty_stage_lists_cleanly_but_cannot_deploy_or_generate_settings(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(main(self.command("list")), 0)
        self.assertIn("No staged metadata", output.getvalue())
        self.assertEqual(main(self.command("deploy")), 2)
        self.assertEqual(main(self.command("kv-settings")), 2)

    def test_partial_settings_are_visible_and_strict_generation_preserves_old_settings(self):
        self.generate_packages()
        def partial(*args):
            document = self.settings(*args)
            document.update(status="partial", warnings=["unresolved source macro"])
            return document
        with patch("openriak_metadata.cli.generate_defaults", side_effect=partial):
            self.assertEqual(main(self.command("kv-settings")), 0)
            before = (self.root / "staged/kv/3.4.0/defaults.json").stat().st_mtime_ns
            self.assertEqual(main(self.command("kv-settings", "--strict")), 2)
            self.assertEqual((self.root / "staged/kv/3.4.0/defaults.json").stat().st_mtime_ns, before)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(main(self.command("list")), 0)
        self.assertIn("partial", output.getvalue())
        self.assertEqual(main(self.command("deploy")), 0)

    def test_settings_must_cover_new_package_os_families(self):
        self.generate_packages()
        with patch("openriak_metadata.cli.generate_defaults", side_effect=self.settings):
            self.assertEqual(main(self.command("kv-settings")), 0)
        path = self.root / "staged/kv/3.4.1/defaults.json"
        settings = json.loads(path.read_text())
        settings["effective_defaults"] = {}
        path.write_text(json.dumps(settings))
        before = self.snapshot()
        self.assertEqual(main(self.command("deploy")), 2)
        self.assertEqual(self.snapshot(), before)

    def test_list_shows_file_date_in_utc(self):
        self.generate_packages()
        path = self.root / "staged/kv/3.4.1/downloads.json"
        os.utime(path, (1704067200, 1704067200))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(main(self.command("list", "--version", "3.4.1")), 0)
        self.assertIn("2024-01-01 00:00:00", output.getvalue())
        self.assertNotIn("3.4.0", output.getvalue())

    def test_regeneration_refreshes_package_dates_and_preserves_staged_settings(self):
        self.generate_packages()
        with patch("openriak_metadata.cli.generate_defaults", side_effect=self.settings):
            self.assertEqual(main(self.command("kv-settings")), 0)
        directory = self.root / "staged/kv/3.4.1"
        settings = directory / "defaults.json"
        before = (settings.read_bytes(), settings.stat().st_mtime_ns)
        packages = directory / "downloads.json"
        os.utime(packages, (1704067200, 1704067200))
        self.generate_packages()
        self.assertGreater(packages.stat().st_mtime, 1704067200)
        self.assertEqual((settings.read_bytes(), settings.stat().st_mtime_ns), before)

    def test_deploy_failure_rolls_back_packages_and_settings_across_versions(self):
        self.generate_packages()
        with patch("openriak_metadata.cli.generate_defaults", side_effect=self.settings):
            self.assertEqual(main(self.command("kv-settings")), 0)
        before = self.snapshot()
        real_replace = os.replace

        def replace(source, target):
            if str(source).endswith("3.4.1-defaults.json.new"):
                raise PermissionError("injected settings installation failure")
            return real_replace(source, target)

        with patch("openriak_metadata.repository.os.replace", side_effect=replace):
            self.assertEqual(main(self.command("deploy")), 2)
        self.assertEqual(self.snapshot(), before)

    def test_failed_later_settings_generation_preserves_entire_previous_batch(self):
        self.generate_packages()
        with patch("openriak_metadata.cli.generate_defaults", side_effect=self.settings):
            self.assertEqual(main(self.command("kv-settings")), 0)
        stage = self.root / "staged"
        before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in stage.rglob("*.json")}

        def settings(args, *other):
            document = self.settings(args, *other)
            if args.version == "3.4.1":
                document["status"] = "unavailable"
            return document

        with patch("openriak_metadata.cli.generate_defaults", side_effect=settings):
            self.assertEqual(main(self.command("kv-settings")), 2)
        self.assertEqual({path: (path.read_bytes(), path.stat().st_mtime_ns) for path in before}, before)

    def test_malformed_target_or_settings_blocks_deployment_without_traceback(self):
        self.generate_packages()
        path = self.root / "staged/kv/3.4.1/supported-os.json"
        document = json.loads(path.read_text())
        document["operating_systems"][0]["id"] = ["invalid"]
        path.write_text(json.dumps(document))
        self.assertEqual(main(self.command("deploy")), 2)
        self.generate_packages()
        with patch("openriak_metadata.cli.generate_defaults", side_effect=self.settings):
            self.assertEqual(main(self.command("kv-settings")), 0)
        path = self.root / "staged/kv/3.4.1/defaults.json"
        document = json.loads(path.read_text())
        document["status"] = {"invalid": True}
        path.write_text(json.dumps(document))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(self.command("list")), 2)
        self.assertEqual(main(self.command("deploy")), 2)

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
