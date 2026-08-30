import unittest

from openriak_metadata.cli import build_parser


class CliTests(unittest.TestCase):
    def test_exact_version_is_validated_by_main_contract(self):
        args = build_parser().parse_args(["generate", "--product", "kv", "--version", "1.10.0", "--output", "out"])
        self.assertEqual(args.version, "1.10.0")


if __name__ == "__main__":
    unittest.main()
