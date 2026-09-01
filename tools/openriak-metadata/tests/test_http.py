import hashlib
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from openriak_metadata.http import HttpClient


class Response(BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()


class HttpClientTests(unittest.TestCase):
    def test_sha256_streams_and_reuses_url_keyed_cache(self):
        payload = (b"OpenRiak package data" * 1000)
        expected = hashlib.sha256(payload).hexdigest()
        with tempfile.TemporaryDirectory() as temporary, patch(
            "urllib.request.urlopen", return_value=Response(payload)
        ) as urlopen:
            client = HttpClient(cache_dir=Path(temporary))
            self.assertEqual(client.sha256("https://files.example/package.rpm"), expected)
            self.assertEqual(client.sha256("https://files.example/package.rpm"), expected)
            self.assertEqual(urlopen.call_count, 1)
            cache_files = list((Path(temporary) / "checksums").glob("*.json"))
            self.assertEqual(len(cache_files), 1)


if __name__ == "__main__":
    unittest.main()
