"""Read package trees locally or over SSH while retaining public download URLs."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import posixpath
import re
import shlex
import subprocess
from urllib.parse import quote, unquote, urlparse

from .packages import PackageCatalog

DEFAULT_WEB_ROOT = "https://files.tiot.jp/riak/"


def normalize_web_root(value: str) -> str:
    parsed = urlparse(value)
    if (parsed.scheme not in ("http", "https") or not parsed.hostname
            or parsed.username or parsed.password or parsed.query or parsed.fragment
            or any(c.isspace() for c in value)):
        raise ValueError("--web-root must be an HTTP(S) URL without credentials, query or fragment")
    return value.rstrip("/") + "/"


def parse_remote_copy(value: str) -> tuple[str, str]:
    match = re.fullmatch(r"((?:[^@\s/:]+@)?(?:\[[^\]\s]+\]|[^\s/:]+)):(.+)", value)
    if not match or match[1].startswith("-"):
        raise ValueError("--remote-copy must be an SSH path: [user@]host:/path/containing/kv/")
    host, root = match.groups()
    # Prefix relative paths so find cannot interpret them as options/expressions.
    if not root.startswith(("/", "./")):
        root = "./" + root
    return host, root


class CopyClient:
    def __init__(self, web_root: str) -> None:
        self.web_root = normalize_web_root(web_root)

    def relative_path(self, url: str) -> str:
        if not url.startswith(self.web_root):
            raise ValueError(f"Package URL is outside --web-root: {url}")
        relative = unquote(url[len(self.web_root):]).rstrip("/")
        if any(part in ("", ".", "..") for part in relative.split("/")):
            raise ValueError(f"Invalid package path: {url}")
        return relative

    def public_url(self, relative: str) -> str:
        return self.web_root + quote(relative, safe="/")


class LocalCopyClient(CopyClient):
    def __init__(self, root: Path, web_root: str) -> None:
        super().__init__(web_root)
        self.root = root.expanduser().resolve()

    def iter_files(self, url: str):
        directory = self.root / self.relative_path(url)
        if not directory.is_dir():
            raise FileNotFoundError(f"Package directory not found: {directory}")

        def fail(error):
            raise error

        for parent, _, names in os.walk(directory, onerror=fail):
            for name in sorted(names):
                path = Path(parent) / name
                if path.is_file() and not path.is_symlink():
                    yield self.public_url(path.relative_to(self.root).as_posix())

    def sha256(self, url: str) -> str:
        digest = hashlib.sha256()
        with (self.root / self.relative_path(url)).open("rb") as package:
            while chunk := package.read(1024 * 1024):
                digest.update(chunk)
        return digest.hexdigest()


class RemoteCopyClient(CopyClient):
    def __init__(self, root: str, web_root: str) -> None:
        super().__init__(web_root)
        self.host, self.root = parse_remote_copy(root)

    def _run(self, *arguments: str) -> bytes:
        result = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=20", "--", self.host,
             shlex.join(arguments)], capture_output=True, timeout=300,
        )
        if result.returncode:
            raise OSError(f"SSH package read failed: {result.stderr.decode('utf-8', 'replace').strip()}")
        return result.stdout

    def iter_files(self, url: str):
        relative = self.relative_path(url)
        directory = posixpath.join(self.root, relative)
        listing = self._run("find", directory, "-type", "f", "-print0")
        for entry in listing.split(b"\0"):
            if entry:
                path = entry.decode("utf-8")
                if not path.startswith(directory.rstrip("/") + "/"):
                    raise ValueError("SSH returned a file outside the package directory")
                yield self.public_url(relative + "/" + path[len(directory.rstrip("/")) + 1:])

    def sha256(self, url: str) -> str:
        path = posixpath.join(self.root, self.relative_path(url))
        output = self._run("sha256sum", "--", path).decode("utf-8").lstrip("\\")
        value = output.split()[0] if output.split() else ""
        if not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValueError(f"Invalid remote SHA-256 for {url}")
        return value


class CopyCatalog(PackageCatalog):
    def _crawl(self, root: str, alpine: bool = False):
        for url in self.client.iter_files(self.host + root):
            yield url, [unquote(p) for p in urlparse(url).path.split("/") if p][:-1]
