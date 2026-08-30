import unittest

from openriak_metadata.packages import parse_package


class LegacyPackageTests(unittest.TestCase):
    def test_package_without_otp_is_retained(self):
        package = parse_package("riak_3.4.1_amd64.deb", "kv", "3.4.1",
                                "https://files.example/riak_3.4.1_amd64.deb",
                                ["riak", "kv", "3.4", "3.4.1", "ubuntu", "noble64"])
        self.assertIsNone(package.otp)
        self.assertEqual(package.architecture, "amd64")


if __name__ == "__main__":
    unittest.main()
