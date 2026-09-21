import contextlib
import hashlib
import io
import json
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from openriak_metadata.cli import main
from openriak_metadata.copies import RemoteCopyClient
from openriak_metadata.packages import parse_package


class CopyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / "build's artifacts $(false)"
        self.output = self.root / "out"
        self.web_root = "https://downloads.example/custom/riak/"
        self.files = {
            "ubuntu/resolute64/openriak-kv-3.4.1-otp26.2.5.21-amd64.deb": b"debian package",
            "oracle/9/riak-3.4.1-1.otp24.3.4.17.el9.aarch64.rpm": b"rpm package",
            "alpine/3.24/riak-3.4.1.26-r1-otp26.2.5.21-x86_64.apk": b"alpine package",
            "amazon/2023 (graviton 3)/riak-3.4.1.OTP26-1.amzn2023.aarch64.rpm": b"legacy rpm",
        }
        for relative, contents in self.files.items():
            self.add_file("kv/3.4/3.4.1/" + relative, contents)
        self.add_file("kv/3.4/3.4.1/alpine/3.24/riak-openrc-3.4.1.26-r1-otp26.2.5.21-x86_64.apk", b"ignore")
        self.add_file("kv/3.4/3.4.1/ubuntu/noble64/openriak-kv-3.4.0-otp26.2.5.21-amd64.deb", b"wrong version")
        self.add_file("kv/3.4/3.4.1/ubuntu/noble64/openriak-cs-3.4.1-otp26.2.5.21-amd64.deb", b"wrong product")
        self.add_file("kv/3.4/3.4.1/ubuntu/resolute64/SHA256SUMS", b"not a package")
        for relative in self.files:
            self.add_file("kv/3.4/3.4.1/" + relative + ".sha", b"stale checksum")
            self.add_file("kv/3.4/3.4.1/" + relative + ".cdx.json", b"sbom")

    def add_file(self, relative, contents):
        target = self.source / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)

    def command(self, *options):
        return ["kv-packages", "--version", "3.4.1",
                "--output", str(self.output), "--strict", *options]

    def documents(self):
        directory = self.output / "kv/3.4.1"
        return [json.loads((directory / name).read_text())
                for name in ("supported-os.json", "downloads.json")]

    def test_local_copy_hashes_packages_offline_and_maps_public_urls(self):
        with patch("openriak_metadata.cli.HttpClient", side_effect=AssertionError("HTTP used")):
            result = main(self.command("--local-copy", str(self.source), "--web-root", self.web_root.rstrip("/")))
        self.assertEqual(result, 0)
        supported, downloads = self.documents()
        self.assertEqual(supported["status"], "complete")
        targets = {item["id"]: item for item in supported["operating_systems"]}
        self.assertEqual(set(targets), {"ubuntu-resolute-amd64", "oracle-linux-9-aarch64",
                                        "alpine-3.24-x86_64", "amazon-linux-2023-aarch64"})
        self.assertEqual(targets["ubuntu-resolute-amd64"]["release_version"], "26.04")
        packages = [item for variants in downloads["downloads"].values() for item in variants.values()]
        self.assertEqual(len(packages), len(self.files))
        for item in packages:
            relative = next(path for path in self.files if path.endswith("/" + item["filename"]))
            self.assertTrue(item["url"].startswith(self.web_root + "kv/3.4/3.4.1/"))
            self.assertEqual(item["checksum"]["value"], hashlib.sha256(self.files[relative]).hexdigest())
        self.assertTrue(any("%20" in item["url"] for item in packages))

    def test_local_copy_expands_home_and_rehashes_changed_bytes(self):
        relative = next(iter(self.files))
        with patch("pathlib.Path.home", return_value=self.root), patch.dict("os.environ", {"HOME": str(self.root)}):
            self.assertEqual(main(self.command("--local-copy", "~/" + self.source.name)), 0)
        before = self.documents()[1]
        self.add_file("kv/3.4/3.4.1/" + relative, b"rebuilt")
        self.assertEqual(main(self.command("--local-copy", str(self.source))), 0)
        after = self.documents()[1]
        old = next(iter(before["downloads"]["ubuntu-resolute-amd64"].values()))
        new = next(iter(after["downloads"]["ubuntu-resolute-amd64"].values()))
        self.assertNotEqual(old["checksum"], new["checksum"])
        self.assertTrue(new["url"].startswith("https://files.tiot.jp/riak/kv/"))

    def test_ssh_copy_matches_local_copy_and_quotes_shell_paths(self):
        self.assertEqual(main(self.command("--local-copy", str(self.source), "--web-root", self.web_root)), 0)
        expected = self.documents()
        run = subprocess.run

        def ssh(command, **kwargs):
            self.assertEqual(command[:7], ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=20", "--", "user@server"])
            remote_args = shlex.split(command[-1])
            self.assertIn(remote_args[0], ("find", "sha256sum"))
            # Execute the actual remote command in a local shell to check quoting
            # and the find/sha256sum protocol, without contacting an SSH server.
            return run(["sh", "-c", command[-1]], **kwargs)

        with patch("openriak_metadata.copies.subprocess.run", side_effect=ssh) as remote, \
                patch("openriak_metadata.cli.HttpClient", side_effect=AssertionError("HTTP used")):
            self.assertEqual(main(self.command("--remote-copy", "user@server:" + str(self.source) + "/",
                                               "--web-root", self.web_root)), 0)
        self.assertEqual(remote.call_count, 1 + len(self.files))
        self.assertEqual(self.documents(), expected)

    def test_ssh_errors_and_bad_checksums_fail(self):
        client = RemoteCopyClient("user@server:/riak", self.web_root)
        with patch("openriak_metadata.copies.subprocess.run", return_value=subprocess.CompletedProcess([], 1, b"", b"Permission denied")):
            with self.assertRaisesRegex(OSError, "Permission denied"):
                list(client.iter_files(self.web_root + "kv/3.4/3.4.1/"))
            self.assertEqual(main(self.command("--remote-copy", "user@server:/riak")), 2)
        with patch.object(client, "_run", return_value=b"invalid digest"):
            with self.assertRaisesRegex(ValueError, "Invalid remote SHA-256"):
                client.sha256(self.web_root + "kv/package.deb")

    def test_invalid_options_fail_before_generation(self):
        options = [
            ["--local-copy", str(self.source), "--remote-copy", "user@server:/riak"],
            ["--local-copy", str(self.source / "kv")],
            ["--remote-copy", "/local/path"],
            ["--remote-copy", "-bad:/riak"],
            ["--web-root", "file:///riak/"],
            ["--web-root", "https://files.example/riak/?query=yes"],
            ["--web-root", "https://files.example/riak/#fragment"],
        ]
        for args in options:
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()), \
                    patch("openriak_metadata.cli.generate_version") as generate, self.assertRaises(SystemExit):
                main(self.command(*args))
            generate.assert_not_called()

    def test_missing_later_version_leaves_repository_unchanged(self):
        metadata = self.root / "repo/content/openriak-kv/metadata/3.4.1"
        metadata.mkdir(parents=True)
        existing = metadata / "downloads.json"
        existing.write_text("original")
        result = main(["kv-packages", "--version", "3.4.1", "--version", "3.4.2",
                       "--local-copy", str(self.source), "--output", str(self.output)])
        self.assertEqual(result, 2)
        self.assertEqual(existing.read_text(), "original")
        self.assertFalse((metadata / "supported-os.json").exists())

    def test_explicit_web_root_is_used_for_http_discovery(self):
        root = self.web_root + "kv/3.4/3.4.1/"
        filename = "openriak-kv-3.4.1-otp26.2.5.21-amd64.deb"
        pages = {
            root: b'<a href="ubuntu/">ubuntu</a>',
            root + "ubuntu/": b'<a href="resolute64/">resolute64</a>',
            root + "ubuntu/resolute64/": f'<a href="{filename}">package</a>'.encode(),
        }
        with patch("openriak_metadata.cli.HttpClient") as client:
            client.return_value.get.side_effect = pages.__getitem__
            client.return_value.sha256.return_value = "a" * 64
            self.assertEqual(main(self.command("--web-root", self.web_root)), 0)
        downloads = self.documents()[1]["downloads"]
        package = next(iter(downloads["ubuntu-resolute-amd64"].values()))
        self.assertEqual(package["url"], root + "ubuntu/resolute64/" + filename)
        self.assertEqual(client.return_value.get.call_count, 3)

    def test_build_names_match_exact_product_version_and_otp(self):
        for filename in ("openriak-cs-3.4.1-otp26.2.5.21-amd64.deb",
                         "riak-cs-3.4.1-1.otp26.2.5.21.el9.aarch64.rpm",
                         "riak-cs-3.4.1.26-r1-otp26.2.5.21-x86_64.apk"):
            parts = ["cs", "3.4", "3.4.1", "alpine", "3.24"]
            self.assertIsNotNone(parse_package(filename, "cs", "3.4.1", "https://example/" + filename, parts))
            self.assertIsNone(parse_package(filename, "kv", "3.4.1", "https://example/" + filename, parts))
            self.assertIsNone(parse_package(filename, "cs", "3.4.0", "https://example/" + filename, parts))
        self.assertIsNone(parse_package("riak-3.4.1.24-r1-otp26.2.5.21-x86_64.apk", "kv", "3.4.1",
                                        "https://example/package.apk", ["alpine", "3.24"]))


if __name__ == "__main__":
    unittest.main()
