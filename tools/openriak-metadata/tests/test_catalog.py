import urllib.error
import unittest
import hashlib
from pathlib import Path

from openriak_metadata.packages import PackageCatalog


FIXTURES = Path(__file__).parent / "fixtures"


class FixtureClient:
    def get(self, url):
        names = {
            "https://files.example/alpine/": "alpine-root.html",
            "https://files.example/alpine/v3.21/": "alpine-version.html",
            "https://files.example/alpine/v3.21/main/": "alpine-main.html",
            "https://files.example/alpine/v3.21/main/x86_64/": "alpine-x86_64.html",
        }
        if url not in names:
            raise urllib.error.HTTPError(url, 404, "not found", {}, None)
        return (FIXTURES / names[url]).read_bytes()

    def sha256(self, url):
        return hashlib.sha256(url.encode("utf-8")).hexdigest()


class CatalogTests(unittest.TestCase):
    def test_alpine_is_independent_and_revisions_are_retained(self):
        targets, downloads, warnings = PackageCatalog(FixtureClient(), "https://files.example").discover(
            "kv", "3.4.1", "/riak/kv/")
        self.assertEqual(warnings, [])
        self.assertEqual([item["id"] for item in targets], ["alpine-3.21-x86_64"])
        variants = downloads["alpine-3.21-x86_64"]
        self.assertEqual(set(variants), {"otp24-x86_64-r0", "otp24-x86_64-r1", "otp26-x86_64-r1"})
        self.assertTrue(all(item["filename"].startswith("riak-3.4.1.") for item in variants.values()))
        self.assertTrue(all(item["checksum"]["algorithm"] == "sha256" for item in variants.values()))
        self.assertTrue(all(len(item["checksum"]["value"]) == 64 for item in variants.values()))


if __name__ == "__main__":
    unittest.main()
