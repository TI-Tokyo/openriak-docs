import unittest

from openriak_metadata.packages import parse_package


class PackageParsingTests(unittest.TestCase):
    def parse(self, filename, product="kv", version="3.4.1", parts=None):
        parts = parts or ["riak", "kv", "3.4", version, "ubuntu", "noble64"]
        return parse_package(filename, product, version, "https://files.tiot.jp/" + filename, parts)

    def test_deb_variants_and_architectures(self):
        for otp in (24, 26):
            for arch in ("amd64", "arm64"):
                package = self.parse(f"riak_3.4.1-OTP{otp}_{arch}.deb")
                self.assertEqual((package.otp, package.architecture, package.target["id"]),
                                 (otp, arch, f"ubuntu-noble-{arch}"))

    def test_rpm_targets(self):
        rhel = self.parse("riak-3.4.1.OTP26-1.el9.x86_64.rpm", parts=["riak", "kv", "rhel", "9"])
        amazon = self.parse("riak-3.4.1.OTP24-1.amzn2023.aarch64.rpm", parts=["riak", "kv", "amazon"])
        self.assertEqual(rhel.target["id"], "rhel-9-x86_64")
        self.assertEqual(amazon.target["id"], "amazon-linux-2023-aarch64")

    def test_alpine_otp_variants(self):
        for otp in (24, 26):
            package = self.parse(f"riak-3.4.1.{otp}-r1.apk", parts=["alpine", "v3.21", "main", "x86_64"])
            self.assertEqual(package.target["id"], "alpine-3.21-x86_64")
            self.assertEqual(package.revision, "r1")

    def test_graviton_sub_architectures_are_retained(self):
        cases = [
            (["riak", "kv", "3.4", "3.4.1", "amazon", "2023 (graviton2)"], "Graviton 2"),
            (["riak", "kv", "3.4", "3.4.1", "amazon", "2023 (graviton 3)"], "Graviton 3"),
        ]
        for parts, expected in cases:
            with self.subTest(expected=expected):
                package = self.parse("riak-3.4.1.OTP26-1.amzn2023.aarch64.rpm", parts=parts)
                self.assertEqual(package.sub_architecture, expected)

    def test_non_installable_files_are_ignored(self):
        for filename in ("riak-3.4.1.OTP26-1.el9.src.rpm", "riak_3.4.1-OTP26_amd64.deb.sha",
                         "riak-openrc-3.4.1.26-r1.apk", "riak-debug-3.4.1.26-r1.apk"):
            self.assertIsNone(self.parse(filename))

    def test_historical_ubuntu_codenames_have_release_versions(self):
        for codename, release in (("trusty64", "14.04"), ("artful64", "17.10")):
            with self.subTest(codename=codename):
                package = self.parse(
                    "riak_3.4.1-OTP26_amd64.deb",
                    parts=["riak", "kv", "3.4", "3.4.1", "ubuntu", codename],
                )
                self.assertEqual(package.target["release_version"], release)

    def test_exact_product_and_version(self):
        self.assertIsNone(self.parse("riak-cs_3.4.1-OTP26_amd64.deb"))
        self.assertIsNone(self.parse("riak-ts_3.4.1-OTP26_amd64.deb"))
        self.assertIsNone(self.parse("riak_3.4.0-OTP26_amd64.deb"))
        self.assertIsNotNone(self.parse("riak-cs_3.4.1-OTP26_amd64.deb", product="cs"))


if __name__ == "__main__":
    unittest.main()
