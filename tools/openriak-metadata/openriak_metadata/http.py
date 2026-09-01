from __future__ import annotations

import hashlib
import json
import logging
import re
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path


SHA256 = re.compile(r"^[0-9a-f]{64}$")


class HttpClient:
    def __init__(self, timeout: float = 20, retries: int = 2, *,
                 cache_dir: Path | None = None, refresh: bool = False) -> None:
        self.timeout = timeout
        self.retries = retries
        self.cache_dir = cache_dir
        self.refresh = refresh

    def get(self, url: str) -> bytes:
        request = urllib.request.Request(url, headers={"User-Agent": "openriak-metadata/1.0"})
        for attempt in range(self.retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    return response.read()
            except urllib.error.HTTPError as exc:
                if exc.code < 500 or attempt == self.retries:
                    raise
            except (urllib.error.URLError, TimeoutError):
                if attempt == self.retries:
                    raise
            time.sleep(0.25 * (2**attempt))
        raise AssertionError("unreachable")

    def sha256(self, url: str) -> str:
        cache_path = self._checksum_cache_path(url)
        if cache_path and cache_path.is_file() and not self.refresh:
            try:
                cached = json.loads(cache_path.read_text(encoding="utf-8"))
                if cached.get("url") == url and SHA256.fullmatch(cached.get("value", "")):
                    logging.info("Using cached SHA-256 for %s", url)
                    return cached["value"]
            except (OSError, ValueError, TypeError):
                pass

        request = urllib.request.Request(url, headers={"User-Agent": "openriak-metadata/1.0"})
        for attempt in range(self.retries + 1):
            digest = hashlib.sha256()
            try:
                logging.info("Downloading %s for SHA-256", url)
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    while chunk := response.read(1024 * 1024):
                        digest.update(chunk)
                value = digest.hexdigest()
                if cache_path:
                    self._write_checksum_cache(cache_path, {"algorithm": "sha256", "url": url, "value": value})
                return value
            except urllib.error.HTTPError as exc:
                if exc.code < 500 or attempt == self.retries:
                    raise
            except (urllib.error.URLError, TimeoutError):
                if attempt == self.retries:
                    raise
            time.sleep(0.25 * (2**attempt))
        raise AssertionError("unreachable")

    def _checksum_cache_path(self, url: str) -> Path | None:
        if self.cache_dir is None:
            return None
        key = hashlib.sha256(url.encode("utf-8")).hexdigest()
        return self.cache_dir / "checksums" / f"{key}.json"

    @staticmethod
    def _write_checksum_cache(target: Path, value: dict) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=target.parent,
                                         prefix=f".{target.name}.", delete=False) as temporary:
            json.dump(value, temporary, sort_keys=True)
            temporary.write("\n")
            temporary_path = Path(temporary.name)
        temporary_path.replace(target)
