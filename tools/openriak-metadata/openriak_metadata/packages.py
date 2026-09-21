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
_JOINED_OTP_RPM = re.compile(
    r"^(?P<name>riak(?:-cs|-ts)?)-(?P<version>\d+\.\d+\.\d+)-OTP"
    r"(?P<otp>\d+)(?:\.\d+)*-(?P<rev>[^.]+)\."
    r"(?P<target>amzn\d+|el\d+)(?P<arch>x86_64|aarch64)\.rpm$"
)
_BUILD_DEB = re.compile(
    r"^openriak-(?P<product>kv|cs|ts)-(?P<version>\d+\.\d+\.\d+)-"
    r"otp(?P<otp>\d+)(?:\.\d+)*-(?P<arch>amd64|arm64|i386|armhf)\.deb$"
)
_BUILD_RPM = re.compile(
    r"^(?P<name>riak(?:-cs|-ts)?)-(?P<version>\d+\.\d+\.\d+)-"
    r"(?P<rev>[^.]+)\.otp(?P<otp>\d+)(?:\.\d+)*\."
    r"(?P<target>[^.]+)\.(?P<arch>[^.]+)\.rpm$"
)
_BUILD_APK = re.compile(
    r"^(?P<name>riak(?:-cs|-ts)?)-(?P<version>\d+\.\d+\.\d+)\."
    r"(?P<otp>\d+)-(?P<rev>r\d+)-otp(?P<full_otp>\d+(?:\.\d+)*)-"
    r"(?P<arch>x86_64|aarch64|armhf|armv7|x86)\.apk$"
)


def parse_package(filename: str, product: str, version: str, url: str, path_parts: list[str]):
    parsed = _original_parse_package(filename, product, version, url, path_parts)
    if parsed is not None:
        return parsed
    lower = filename.lower()
    if lower.endswith((".src.rpm", ".sha", ".sha1", ".sha256", ".sha512")):
        return None
    if any(marker in lower for marker in ("-openrc-", "-debug-", "-dev-", "-dialyzer-", "-reltool-")):
        return None
    built = _BUILD_DEB.match(filename) or _BUILD_RPM.match(filename) or _BUILD_APK.match(filename)
    if built:
        data = built.groupdict()
        if (data["version"] != version or data.get("product", product) != product
                or data.get("name", _NAMES[product]) != _NAMES[product]):
            return None
        if data.get("full_otp", data["otp"]).split(".")[0] != data["otp"]:
            return None
        fmt = filename.rsplit(".", 1)[-1]
        parts = path_parts
        if fmt == "apk":
            # Standalone exports use alpine/3.24 rather than alpine/v3.24/main/ARCH.
            parts = ["v" + part if i and path_parts[i - 1] == "alpine"
                     and re.fullmatch(r"\d+\.\d+", part) else part
                     for i, part in enumerate(path_parts)]
        target = normalize_target(parts, fmt, data["arch"], data.get("target"))
        return Package(product, version, int(data["otp"]), data["arch"],
                       _implementation._sub_architecture_from_path(path_parts), fmt, data.get("rev"),
                       filename, url, None, target)
    joined = _JOINED_OTP_RPM.match(filename)
    if joined and joined.group("name") == _NAMES[product] and joined.group("version") == version:
        data = joined.groupdict()
        target = normalize_target(path_parts, "rpm", data["arch"], data["target"])
        if not target:
            return None
        return Package(product, version, int(data["otp"]), data["arch"],
                       _implementation._sub_architecture_from_path(path_parts), "rpm", data["rev"],
                       filename, url, None, target)
    match = _LEGACY_DEB.match(filename) or _LEGACY_RPM.match(filename)
    if not match or match.group("name") != _NAMES[product] or match.group("version") != version:
        return None
    data = match.groupdict()
    file_format = filename.rsplit(".", 1)[-1]
    target = normalize_target(path_parts, file_format, data["arch"], data.get("target"))
    if not target:
        return None
    return Package(product, version, None, data["arch"], _implementation._sub_architecture_from_path(path_parts),
                   file_format, data.get("rev"),
                   filename, url, None, target)


def _target_sort_key(item: dict):
    release = item.get("release") or ""
    pieces = tuple((0, int(piece)) if piece.isdigit() else (1, piece)
                   for piece in re.split(r"[.-]", release))
    return item["family"], pieces, item["architecture"]


_implementation.parse_package = parse_package
_implementation._target_sort_key = _target_sort_key


class PackageCatalog(_PackageCatalog):
    def discover(self, product: str, version: str, product_path: str, **kwargs):
        targets, downloads, warnings = super().discover(product, version, product_path, **kwargs)
        warnings = [warning for warning in warnings if "HTTP Error 404" not in warning]
        return targets, downloads, warnings
