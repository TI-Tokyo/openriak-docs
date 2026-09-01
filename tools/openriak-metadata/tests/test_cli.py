import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from openriak_metadata.cli import build_parser, main


class CliTests(unittest.TestCase):
    def test_exact_version_is_validated_by_main_contract(self):
        args = build_parser().parse_args(["generate", "--product", "kv", "--version", "1.10.0", "--output", "out"])
        self.assertEqual(args.version, "1.10.0")

    def test_generate_accepts_skip_defaults(self):
        args = build_parser().parse_args([
            "generate", "--product", "kv", "--version", "2.0.0",
            "--output", "out", "--skip-defaults",
        ])
        self.assertTrue(args.skip_defaults)
        self.assertEqual(args.checksum_workers, 4)

    def test_checksum_workers_must_be_positive(self):
        with self.assertRaises(SystemExit):
            main([
                "packages", "--product", "kv", "--version", "3.4.1",
                "--output", "out", "--checksum-workers", "0",
            ])

    def test_skip_defaults_writes_only_package_metadata(self):
        with tempfile.TemporaryDirectory() as temporary, patch(
            "openriak_metadata.cli.PackageCatalog"
        ) as catalog:
            catalog.return_value.discover.return_value = ([], {}, [])
            result = main([
                "generate", "--product", "kv", "--version", "2.0.0",
                "--output", temporary, "--skip-defaults",
            ])
            destination = Path(temporary) / "kv" / "2.0.0"
            self.assertEqual(result, 0)
            self.assertTrue((destination / "supported-os.json").is_file())
            self.assertTrue((destination / "downloads.json").is_file())
            self.assertFalse((destination / "defaults.json").exists())


if __name__ == "__main__":
    unittest.main()
