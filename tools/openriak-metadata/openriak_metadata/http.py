from __future__ import annotations

import time
import urllib.error
import urllib.request


class HttpClient:
    def __init__(self, timeout: float = 20, retries: int = 2) -> None:
        self.timeout = timeout
        self.retries = retries

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

