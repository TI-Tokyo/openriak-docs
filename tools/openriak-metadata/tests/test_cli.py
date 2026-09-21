import argparse
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from openriak_metadata.cli import build_parser, main


class CliTests(unittest.TestCase):
    def test_help_describes_all_options_and_exits_before_generation(self):
        root = build_parser()
        commands = next(a for a in root._actions if isinstance(a, argparse._SubParsersAction))
        pages = [((), root), *(( (name,), parser) for name, parser in commands.choices.items())]
        with patch('openriak_metadata.cli.generate_version', side_effect=AssertionError('generation started')), \
             patch('openriak_metadata.cli.install_files', side_effect=AssertionError('repository changed')):
            for path, parser in pages:
                with self.subTest(command=path), patch('sys.stdout', new=io.StringIO()) as output:
                    self.assertTrue(parser.description)
                    for action in parser._actions:
                        if not isinstance(action, argparse._SubParsersAction):
                            self.assertTrue(action.help, action.dest)
                    with self.assertRaises(SystemExit) as exited:
                        main([*path, '--help'])
                    self.assertEqual(exited.exception.code, 0)
                    for action in parser._actions:
                        for option in action.option_strings:
                            self.assertIn(option, output.getvalue())

    def test_commands_imply_kv_and_share_staging_directory(self):
        parser = build_parser()
        package = parser.parse_args(["kv-packages", "--version", "1.10.0"])
        self.assertEqual(package.versions, ["1.10.0"])
        self.assertEqual(package.product, "kv")
        self.assertEqual(package.checksum_workers, 4)
        for command in ("kv-settings", "list", "deploy"):
            args = parser.parse_args([command])
            self.assertEqual(args.output, package.output)
            self.assertEqual(args.product, "kv")

    def test_old_commands_and_combined_deployment_are_removed(self):
        for args in (["generate"], ["packages"], ["defaults"],
                     ["kv-packages", "--version", "3.4.1", "--update-repo"],
                     ["kv-packages", "--version", "3.4.1", "--product", "cs"]):
            with self.subTest(args=args), patch("sys.stderr", new=io.StringIO()), self.assertRaises(SystemExit):
                main(args)

    def test_checksum_workers_must_be_positive(self):
        with self.assertRaises(SystemExit):
            main(["kv-packages", "--version", "3.4.1", "--checksum-workers", "0"])

    def test_empty_discovery_does_not_publish_staged_files(self):
        with tempfile.TemporaryDirectory() as temporary, patch("openriak_metadata.cli.PackageCatalog") as catalog:
            catalog.return_value.discover.return_value = ([], {}, [])
            self.assertEqual(main(["kv-packages", "--version", "2.0.0", "--output", temporary]), 2)
            self.assertFalse((Path(temporary) / "kv/2.0.0/downloads.json").exists())


if __name__ == "__main__":
    unittest.main()
