from __future__ import annotations

import posixpath
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import quote, unquote, urljoin, urlparse

from .registry import ARCHES, DEBIAN, UBUNTU


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


@dataclass(frozen=True)
class Package:
    product: str
    version: str
    otp: int | None
    architecture: str
    format: str
    revision: str | None
    filename: str
    url: str
    checksum_url: str | None
    target: dict


_DEB = re.compile(r"^(?P<name>riak(?:-cs|-ts)?)_(?P<version>\d+\.\d+\.\d+)-OTP(?P<otp>\d+)_(?P<arch>[A-Za-z0-9_]+)\.deb$")
_RPM = re.compile(r"^(?P<name>riak(?:-cs|-ts)?)-(?P<version>\d+\.\d+\.\d+)\.OTP(?P<otp>\d+)-(?P<rev>[^.]+)\.(?P<target>[^.]+)\.(?P<arch>[^.]+)\.rpm$")
_APK = re.compile(r"^(?P<name>riak(?:-cs|-ts)?)-(?P<version>\d+\.\d+\.\d+)\.(?P<otp>\d+)-(?P<rev>r\d+)\.apk$")
_PRODUCT_NAMES = {"kv": "riak", "cs": "riak-cs", "ts": "riak-ts"}


def parse_package(filename: str, product: str, version: str, url: str, path_parts: list[str]) -> Package | None:
    lower = filename.lower()
    if lower.endswith((".src.rpm", ".sha", ".sha1", ".sha256", ".sha512")):
        return None
    if any(marker in lower for marker in ("-openrc-", "-debug-", "-dev-", "-dialyzer-", "-reltool-")):
        return None
    match = _DEB.match(filename) or _RPM.match(filename) or _APK.match(filename)
    if not match or match.group("name") != _PRODUCT_NAMES[product] or match.group("version") != version:
        return None
    data = match.groupdict()
    fmt = filename.rsplit(".", 1)[-1]
    arch = data.get("arch") or _arch_from_path(path_parts)
    if not arch:
        return None
    target = normalize_target(path_parts, fmt, arch, data.get("target"))
    if not target:
        return None
    return Package(product, version, int(data["otp"]) if data.get("otp") else None, arch, fmt,
                   data.get("rev"), filename, url, None, target)


def _arch_from_path(parts: list[str]) -> str | None:
    for item in reversed(parts):
        if item in ARCHES:
            return item
    return None


def normalize_target(parts: list[str], fmt: str, arch: str, rpm_target: str | None = None) -> dict | None:
    lowered = [p.lower().strip("/") for p in parts]
    source_label = next((p for p in reversed(lowered) if p and p not in ARCHES), "unknown")
    family: str
    release: str | None
    display: str
    if fmt == "apk":
        token = next((p[1:] for p in lowered if re.fullmatch(r"v\d+(?:\.\d+)+", p)), None)
        family, release, display = "alpine", token, f"Alpine Linux {token}" if token else "Alpine Linux"
    elif rpm_target and rpm_target.startswith("el"):
        family, release = "rhel", rpm_target[2:]
        display = f"Red Hat Enterprise Linux {release}"
        if any("oracle" in p for p in lowered):
            family, display = "oracle-linux", f"Oracle Linux {release}"
    elif rpm_target and rpm_target.startswith("amzn"):
        family, release = "amazon-linux", rpm_target[4:]
        display = f"Amazon Linux {release}"
    elif any("amazon" in p or p.startswith("amzn") for p in lowered):
        family = "amazon-linux"
        release = next((re.sub(r"\D", "", p) for p in lowered if "amazon" in p or p.startswith("amzn")), "") or None
        display = f"Amazon Linux {release}" if release else "Amazon Linux"
    elif any("oracle" in p for p in lowered):
        family = "oracle-linux"
        release = _numeric_release(lowered)
        display = f"Oracle Linux {release}" if release else "Oracle Linux"
    elif any(p in ("rhel", "redhat") or p.startswith("rhel") for p in lowered):
        family = "rhel"
        release = _numeric_release(lowered)
        display = f"Red Hat Enterprise Linux {release}" if release else "Red Hat Enterprise Linux"
    else:
        label = next((p for p in lowered if any(code in p for code in UBUNTU)), source_label)
        codename = next((code for code in UBUNTU if code in label), None)
        if codename or any("ubuntu" in p for p in lowered):
            family, release = "ubuntu", codename
            display = f"Ubuntu {UBUNTU.get(codename, codename or '')}".rstrip()
        elif any("raspbian" in p for p in lowered):
            family = "raspbian"
            codename = next((code for code in DEBIAN if code in lowered), None)
            release = DEBIAN.get(codename or "") or _numeric_release(lowered)
            display = f"Raspbian {release}" if release else "Raspbian"
        elif any("debian" in p for p in lowered) or any(code in lowered for code in DEBIAN):
            family, release = "debian", _numeric_release(lowered)
            if not release:
                codename = next((code for code in DEBIAN if code in lowered), None)
                release = DEBIAN.get(codename or "")
            display = f"Debian {release}" if release else "Debian"
        elif any("fedora" in p for p in lowered):
            family, release = "fedora", _numeric_release(lowered)
            display = f"Fedora {release}" if release else "Fedora"
        elif any(p in ("sles", "suse") or p.startswith("sles") for p in lowered):
            family, release = "sles", _numeric_release(lowered)
            display = f"SUSE Linux Enterprise Server {release}" if release else "SUSE Linux Enterprise Server"
        else:
            family, release, display = "unknown", None, source_label
    rid = release or source_label or "unknown"
    result = {"id": f"{family}-{rid}-{arch}", "family": family, "display_name": display,
              "release": release, "architecture": arch, "package_family": fmt,
              "source_label": source_label}
    if family == "ubuntu":
        result["release_version"] = UBUNTU.get(release or "")
    return result


def _numeric_release(parts: list[str]) -> str | None:
    for part in reversed(parts):
        found = re.search(r"(?:^|[^0-9])(\d+(?:\.\d+)?)(?:[^0-9]|$)", part)
        if found:
            return found.group(1)
    return None


class PackageCatalog:
    def __init__(self, client, host: str = "https://files.tiot.jp", checksum_workers: int = 4) -> None:
        self.client, self.host = client, host.rstrip("/")
        self.checksum_workers = checksum_workers

    def discover(self, product: str, version: str, product_path: str, *,
                 generate_checksums: bool = True) -> tuple[list[dict], dict, list[str]]:
        major_minor = ".".join(version.split(".")[:2])
        roots = [f"{product_path.rstrip('/')}/{major_minor}/{version}/", "/alpine/"]
        packages: list[Package] = []
        warnings: list[str] = []
        for root in roots:
            try:
                for url, parts in self._crawl(root, alpine=root == "/alpine/"):
                    package = parse_package(unquote(urlparse(url).path.rsplit("/", 1)[-1]), product, version, url, parts)
                    if package:
                        packages.append(package)
            except Exception as exc:
                warnings.append(f"Could not crawl {root}: {exc}")
        unique = {p.url: p for p in packages}
        packages = sorted(unique.values(), key=lambda p: (p.target["id"], p.otp or -1, p.revision or "", p.filename))
        checksums: dict[str, str] = {}
        if generate_checksums:
            with ThreadPoolExecutor(max_workers=self.checksum_workers) as executor:
                futures = {executor.submit(self.client.sha256, package.url): package for package in packages}
                for future in as_completed(futures):
                    package = futures[future]
                    try:
                        checksums[package.url] = future.result()
                    except Exception as exc:
                        warnings.append(f"Could not generate SHA-256 for {package.url}: {exc}")
        targets = {p.target["id"]: p.target for p in packages}
        operating_systems = []
        for target in sorted(targets.values(), key=_target_sort_key):
            item = dict(target)
            source_path = urlparse(next(p.url for p in packages if p.target["id"] == target["id"])).path.rsplit("/", 1)[0] + "/"
            item["source"] = {"repository": "alpine" if target["package_family"] == "apk" else "standard", "path": source_path}
            operating_systems.append(item)
        downloads: dict[str, dict] = {}
        for package in packages:
            key = f"otp{package.otp if package.otp is not None else '-unspecified'}-{package.architecture}"
            if package.revision:
                key += f"-{package.revision}"
            bucket = downloads.setdefault(package.target["id"], {})
            candidate = key
            suffix = 2
            while candidate in bucket:
                candidate, suffix = f"{key}-{suffix}", suffix + 1
            bucket[candidate] = {"otp": package.otp, "architecture": package.architecture,
                                     "package_revision": package.revision, "format": package.format,
                                     "filename": package.filename, "url": package.url,
                                     "checksum": ({"algorithm": "sha256", "value": checksums[package.url]}
                                                  if package.url in checksums else None)}
        return operating_systems, downloads, warnings

    def _crawl(self, root: str, alpine: bool = False):
        root_url = self.host + root
        expected = urlparse(root_url)
        queue = [root_url]
        seen: set[str] = set()
        while queue:
            url = queue.pop(0)
            if url in seen:
                continue
            seen.add(url)
            parser = _Links()
            parser.feed(self.client.get(url).decode("utf-8", "replace"))
            for href in parser.hrefs:
                child = urljoin(url, href)
                parsed = urlparse(child)
                if parsed.netloc != expected.netloc or not parsed.path.startswith(expected.path):
                    continue
                name = unquote(parsed.path.rstrip("/").rsplit("/", 1)[-1])
                if not name or name in (".", ".."):
                    continue
                if parsed.path.endswith("/"):
                    if alpine and not self._alpine_path_allowed(parsed.path):
                        continue
                    queue.append(child)
                else:
                    yield child, [unquote(p) for p in parsed.path.split("/") if p][:-1]

    @staticmethod
    def _alpine_path_allowed(path: str) -> bool:
        parts = [p for p in path.split("/") if p]
        if len(parts) <= 1:
            return True
        if len(parts) == 2:
            return bool(re.fullmatch(r"v\d+(?:\.\d+)+", parts[1]))
        if len(parts) == 3:
            return parts[2] == "main"
        return len(parts) == 4 and parts[3] in ARCHES


def _target_sort_key(item: dict):
    release = item.get("release") or ""
    pieces = tuple(int(x) if x.isdigit() else x for x in re.split(r"[.-]", release))
    return item["family"], pieces, item["architecture"]
