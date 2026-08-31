import unittest

from openriak_metadata.packages import parse_package


class LegacyPackageTests(unittest.TestCase):
    def test_package_without_otp_is_retained(self):
        package = parse_package("riak_3.4.1_amd64.deb", "kv", "3.4.1",
                                "https://files.example/riak_3.4.1_amd64.deb",
                                ["riak", "kv", "3.4", "3.4.1", "ubuntu", "noble64"])
        self.assertIsNone(package.otp)
        self.assertEqual(package.architecture, "amd64")

    def test_joined_rpm_platform_and_architecture_are_split(self):
        package = parse_package(
            "riak-3.0.1-OTP22.3-1.amzn2x86_64.rpm", "kv", "3.0.1",
            "https://files.example/riak-3.0.1-OTP22.3-1.amzn2x86_64.rpm",
            ["riak", "kv", "3.0", "3.0.1", "amazon", "2"],
        )
        self.assertEqual(package.otp, 22)
        self.assertEqual(package.architecture, "x86_64")
        self.assertEqual(package.target["id"], "amazon-linux-2-x86_64")

    def test_historical_distribution_paths_are_classified(self):
        cases = [
            ("riak-2.0.0-1.fc19.x86_64.rpm", "2.0.0", ["riak", "kv", "2.0", "2.0.0", "fedora", "19"], "fedora-19-x86_64"),
            ("riak-2.0.0-1.sles11.x86_64.rpm", "2.0.0", ["riak", "kv", "2.0", "2.0.0", "sles", "11"], "sles-11-x86_64"),
            ("riak_3.2.5_armhf.deb", "3.2.5", ["riak", "kv", "3.2", "3.2.5", "raspbian", "bullseye"], "raspbian-11-armhf"),
        ]
        for filename, version, parts, expected in cases:
            with self.subTest(filename=filename):
                package = parse_package(filename, "kv", version,
                                        "https://files.example/" + filename, parts)
                self.assertEqual(package.target["id"], expected)


if __name__ == "__main__":
    unittest.main()
