from __future__ import annotations
import hashlib
import json
import pathlib
from typing import Any
from core.context import context


def read_json(path: pathlib.Path) -> dict[str, Any]:
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def write_json(path: pathlib.Path, value: dict[str, Any]) -> None:
    from publishing.cve_storage import atomic_write
    atomic_write(path, (json.dumps(value, indent=2, sort_keys=True) + '\n').encode())
    from cache.storage import capture_file
    capture_file(path)


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda : handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()
