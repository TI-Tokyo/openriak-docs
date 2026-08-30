"""Public package-catalog API, including conservative legacy grammars."""
from __future__ import annotations

import re

from . import _packages_impl as _implementation
from ._packages_impl import *
from ._packages_impl import PackageCatalog as _PackageCatalog

_original_parse_package = _implementation.parse_package
_NAMES = {"kv": "riak", "cs": "riak-cs", "ts": "riak-ts"}
_LEGACY_DEB = re.compile(r"^(?P<name>riak(?:-cs|-ts)?)_(?P<version>\d+\.\d+\.\d+)(?:-[^_]*)?_(?P<arch>[A-Za-z0-9_]+)\.deb$")
_LEGACY_RPM = re.compile(r"^(?P<name>riak(?:-cs|-ts)?)-(?P<version>\d+\.\d+\.\d+)-(?P<rev>[^.]+)\.(?P<target>[^.]+)\.(?P<arch>[^.]+)\.rpm$")


def parse_package(filename: str, product: str, version: str, url: str, path_parts: list[str]):
    parsed = _original_parse_package(filename, product, version, url, path_parts)
    if parsed is not None:
        return parsed
    lower = filename.lower()
    if lower.endswith((".src.rpm", ".sha", ".sha1", ".sha256", ".sha512")):
        return None
    if any(marker in lower for marker in ("-openrc-", "-debug-", "-dev-", "-dialyzer-", "-reltool-")):
        return None
    match = _LEGACY_DEB.match(filename) or _LEGACY_RPM.match(filename)
    if not match or match.group("name") != _NAMES[product] or match.group("version") != version:
        return None
    data = match.groupdict()
    file_format = filename.rsplit(".", 1)[-1]
    target = normalize_target(path_parts, file_format, data["arch"], data.get("target"))
    if not target:
        return None
    return Package(product, version, None, data["arch"], file_format, data.get("rev"),
                   filename, url, None, target)


def _target_sort_key(item: dict):
    release = item.get("release") or ""
    pieces = tuple((0, int(piece)) if piece.isdigit() else (1, piece)
                   for piece in re.split(r"[.-]", release))
    return item["family"], pieces, item["architecture"]


_implementation.parse_package = parse_package
_implementation._target_sort_key = _target_sort_key


class PackageCatalog(_PackageCatalog):
    def discover(self, product: str, version: str, product_path: str):
        targets, downloads, warnings = super().discover(product, version, product_path)
        warnings = [warning for warning in warnings if "HTTP Error 404" not in warning]
        return targets, downloads, warnings
