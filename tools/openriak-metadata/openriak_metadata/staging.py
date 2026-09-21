"""Inspect and validate the metadata shared by generation, listing and deployment."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlparse

VERSION = re.compile(r"^\d+\.\d+\.\d+$")
FILENAMES = ("supported-os.json", "downloads.json", "defaults.json", "cli-commands.json")


def staged_versions(root: Path) -> list[str]:
    product = root / "kv"
    if not product.is_dir():
        return []
    return sorted((path.name for path in product.iterdir()
                   if path.is_dir() and VERSION.fullmatch(path.name)),
                  key=lambda version: tuple(map(int, version.split("."))))


def read_document(path: Path, version: str) -> dict:
    if path.is_symlink() or path.parent.is_symlink() or path.parent.parent.is_symlink():
        raise ValueError(f"Metadata symlinks are not supported: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("product") != "kv" or value.get("version") != version:
        raise ValueError(f"Mismatched product/version in {path.name}")
    if value.get("schema_version") not in (1, 2):
        raise ValueError(f"Unsupported schema in {path.name}")
    return value


def validate_packages(supported: dict, downloads: dict) -> None:
    if any(document.get("status") != "complete" or document.get("warnings")
           for document in (supported, downloads)):
        raise ValueError("Package metadata must be complete without discovery warnings")
    targets = supported.get("operating_systems")
    if not isinstance(targets, list) or not targets or not isinstance(downloads.get("downloads"), dict):
        raise ValueError("Package metadata must contain operating systems and downloads")
    if any(not isinstance(item, dict)
           or not isinstance(item.get("id"), str) or not item["id"]
           or not isinstance(item.get("family"), str) or not item["family"] for item in targets):
        raise ValueError("Invalid operating system target")
    ids = {item["id"] for item in targets}
    if len(ids) != len(targets) or set(downloads["downloads"]) != ids:
        raise ValueError("Operating systems and package downloads do not match")
    if any(not isinstance(variants, dict) or not variants for variants in downloads["downloads"].values()):
        raise ValueError("Every operating system must have package downloads")
    try:
        _validate_packages(supported, downloads)
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError(f"Malformed package metadata: {error}") from error


def validate_settings(document: dict, targets: list[dict]) -> None:
    # The Hugo adapter accepts partial defaults (e.g. unresolved source macros).
    if document.get("status") not in ("complete", "partial"):
        raise ValueError("KV settings must be complete or partial")
    if not isinstance(document.get("settings"), dict) or not document["settings"]:
        raise ValueError("KV settings contain no extracted settings")
    effective = document.get("effective_defaults")
    if not isinstance(effective, dict) or any(not isinstance(value, dict) for value in effective.values()):
        raise ValueError("Invalid effective KV settings")
    if document["schema_version"] == 2:
        if document.get("defaults_scope") != "os":
            raise ValueError("Schema 2 KV settings must use OS scope")
        required = {target["family"] for target in targets}
    else:
        required = {target["id"] for target in targets}
    missing = required - effective.keys()
    if missing:
        raise ValueError("KV settings missing OS targets: " + ", ".join(sorted(missing)) + "; run kv-settings")


@dataclass
class Release:
    version: str
    files: dict[str, Path] = field(default_factory=dict)
    documents: dict[str, dict] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


def validate_cli_commands(document: dict, *, require_complete: bool = True) -> None:
    if document.get('schema_version') != 1 or document.get('status') not in ('complete', 'partial'):
        raise ValueError('Invalid CLI metadata schema/status')
    if require_complete and (document['status'] != 'complete' or document.get('warnings')):
        raise ValueError('CLI discovery is incomplete; resolve the warnings before deployment')
    if not isinstance(document.get('commands'), list) or not document['commands']:
        raise ValueError('CLI metadata contains no commands')
    if not isinstance(document.get('source'), dict) or not document['source'].get('commit'):
        raise ValueError('CLI metadata is missing source provenance')
    if not isinstance(document.get('runtime'), dict) or not document['runtime'].get('id'):
        raise ValueError('CLI metadata is missing runtime image identity')
    identifiers = set()
    for item in document['commands']:
        if (not isinstance(item, dict) or not isinstance(item.get('id'), str) or not item['id']
                or not isinstance(item.get('path'), list) or not item['path']
                or not all(isinstance(part, str) and part for part in item['path'])
                or item.get('context') not in ('shell', 'erlang')
                or not isinstance(item.get('invocation'), str)
                or not isinstance(item.get('deprecated'), bool)
                or not isinstance(item.get('help'), str)
                or not isinstance(item.get('options'), list)
                or not isinstance(item.get('provenance'), list) or not item['provenance']):
            raise ValueError('Malformed CLI command entry')
        if item['id'] in identifiers:
            raise ValueError('Duplicate CLI command identifier: ' + item['id'])
        identifiers.add(item['id'])
    for item in document['commands']:
        if not isinstance(item.get('subcommands'), list) or any(child not in identifiers for child in item['subcommands']):
            raise ValueError('CLI command references an unknown subcommand')
    if not isinstance(document.get('service_variants'), list):
        raise ValueError('CLI metadata is missing service variants')


def inspect_release(root: Path, version: str) -> Release:
    result = Release(version)
    directory = root / "kv" / version
    for name in FILENAMES:
        path = directory / name
        if not path.exists() and not path.is_symlink():
            continue
        result.files[name] = path
        try:
            result.documents[name] = read_document(path, version)
        except (OSError, ValueError) as error:
            result.errors.append(f"{name}: {error}")
    has_packages = any(name in result.files for name in FILENAMES[:2]) or 'defaults.json' in result.files
    if has_packages and not all(name in result.documents for name in FILENAMES[:2]):
        result.errors.append("Missing valid package metadata; run kv-packages")
    elif has_packages:
        try:
            supported = result.documents["supported-os.json"]
            validate_packages(supported, result.documents["downloads.json"])
            if "defaults.json" in result.documents:
                validate_settings(result.documents["defaults.json"], supported["operating_systems"])
        except (ValueError, KeyError, TypeError, AttributeError) as error:
            result.errors.append(str(error))
    if 'cli-commands.json' in result.documents:
        try:
            validate_cli_commands(result.documents['cli-commands.json'])
        except (ValueError, KeyError, TypeError, AttributeError) as error:
            result.errors.append(str(error))
    if not result.files:
        result.errors.append('No staged metadata for this version')
    return result


def list_releases(root: Path, versions: list[str]) -> int:
    print(f"Staged metadata: {root}")
    if not versions:
        print("No staged metadata. Run kv-packages first.")
        return 0
    print(f"{'VERSION':<12} {'FILE':<20} {'GENERATED (UTC)':<20} {'STATUS':<12} DEPLOYABLE")
    failed = False
    for version in versions:
        release = inspect_release(root, version)
        failed |= bool(release.errors)
        for name, path in release.files.items():
            stamp = datetime.fromtimestamp(path.lstat().st_mtime, timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            status = str(release.documents.get(name, {}).get("status", "invalid"))
            print(f"{version:<12} {name:<20} {stamp:<20} {status:<12} {'no' if release.errors else 'yes'}")
        for error in release.errors:
            print(f"{version}: {error}")
    return 2 if failed else 0


def _validate_packages(supported: dict, downloads: dict, *, require_checksums: bool = True) -> None:
    ids = {item["id"] for item in supported["operating_systems"]}
    if not set(downloads["downloads"]).issubset(ids):
        raise ValueError("downloads contain an unsupported OS identifier")
    seen = set()
    for variants in downloads["downloads"].values():
        for package in variants.values():
            if package["url"] in seen:
                raise ValueError(f"duplicate package URL: {package['url']}")
            seen.add(package["url"])
            if unquote(urlparse(package["url"]).path.rsplit("/", 1)[-1]) != package["filename"]:
                raise ValueError(f"URL filename mismatch: {package['url']}")
            checksum = package.get("checksum")
            if checksum is None and not require_checksums:
                continue
            if not isinstance(checksum, dict) or checksum.get("algorithm") != "sha256":
                raise ValueError(f"missing SHA-256 checksum: {package['url']}")
            if not re.fullmatch(r"[0-9a-f]{64}", checksum.get("value", "")):
                raise ValueError(f"invalid SHA-256 checksum: {package['url']}")
