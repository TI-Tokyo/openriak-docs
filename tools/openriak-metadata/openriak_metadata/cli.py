from __future__ import annotations

import argparse
import json
import logging
import os
import re
from pathlib import Path

from .defaults import extract_defaults
from .http import HttpClient
from .packages import PackageCatalog
from .registry import PRODUCTS
from .source import SourceResolver

VERSION = re.compile(r"^\d+\.\d+\.\d+$")


def build_parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="openriak-metadata", description="Generate OpenRiak release metadata")
    subcommands = result.add_subparsers(dest="command", required=True)
    for name in ("generate", "packages", "defaults"):
        command = subcommands.add_parser(name)
        command.add_argument("--product", choices=sorted(PRODUCTS), required=True)
        command.add_argument("--version", required=True)
        command.add_argument("--output", type=Path, required=True)
        command.add_argument("--cache-dir", type=Path)
        command.add_argument("--refresh", action="store_true")
        command.add_argument("--strict", action="store_true")
        command.add_argument("--keep-workdir", action="store_true")
        command.add_argument("--log-level", choices=("debug", "info", "warning", "error"), default="info")
    return result


def main(argv: list[str] | None = None) -> int:
    cli = build_parser()
    args = cli.parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level.upper()), format="%(levelname)s: %(message)s")
    if not VERSION.fullmatch(args.version):
        cli.error("--version must be an exact major.minor.patch version")
    product = PRODUCTS[args.product]
    destination = args.output / args.product / args.version
    destination.mkdir(parents=True, exist_ok=True)
    targets: list[dict] = []
    statuses: list[str] = []
    logging.info("Discovering packages for %s %s", product["display_name"], args.version)
    try:
        targets, downloads, warnings = PackageCatalog(HttpClient()).discover(
            args.product, args.version, product["files_path"])
        package_status = "partial" if warnings else ("complete" if targets else "unavailable")
        if not targets:
            warnings.append("No matching binary packages were found.")
    except Exception as exc:
        targets, downloads, warnings, package_status = [], {}, [f"Package discovery failed: {exc}"], "unavailable"
    supported = {"schema_version": 1, "product": args.product, "product_name": product["display_name"],
                 "version": args.version, "status": package_status, "operating_systems": targets,
                 "warnings": sorted(set(warnings))}
    download_document = {"schema_version": 1, "product": args.product, "product_name": product["display_name"],
                         "version": args.version, "status": package_status, "downloads": downloads,
                         "warnings": sorted(set(warnings))}
    _validate_packages(supported, download_document)
    if args.command in ("generate", "packages"):
        write_json(destination / "supported-os.json", supported)
        write_json(destination / "downloads.json", download_document)
    statuses.append(package_status)
    if args.command in ("generate", "defaults"):
        defaults_document = generate_defaults(args, product, targets)
        write_json(destination / "defaults.json", defaults_document)
        statuses.append(defaults_document["status"])
    logging.info("Wrote metadata to %s", destination)
    return 2 if args.strict and any(status != "complete" for status in statuses) else 0


def generate_defaults(args, product: dict, targets: list[dict]) -> dict:
    if not product["defaults_supported"]:
        return {"schema_version": 1, "product": args.product, "product_name": product["display_name"],
                "version": args.version, "status": "not_implemented", "settings": {},
                "effective_defaults": {},
                "warnings": [f"Default extraction is not yet configured for {product['display_name']}."]}
    resolver = SourceResolver(args.cache_dir or default_cache_dir(), args.refresh, args.keep_workdir)
    try:
        tag = product["tag_template"].format(version=args.version)
        logging.info("Resolving exact source tag %s", tag)
        root, repositories, warnings = resolver.resolve(product["source_repository"], tag)
        document = extract_defaults(product, args.version, targets, root, repositories, warnings)
        if args.keep_workdir:
            document["working_directory"] = str(resolver.workdir)
        return document
    except Exception as exc:
        return {"schema_version": 1, "product": args.product, "product_name": product["display_name"],
                "version": args.version, "status": "unavailable", "settings": {},
                "effective_defaults": {}, "translations": [], "validators": {},
                "warnings": [f"Source/default extraction failed: {exc}"]}
    finally:
        resolver.close()


def default_cache_dir() -> Path:
    if os.environ.get("XDG_CACHE_HOME"):
        return Path(os.environ["XDG_CACHE_HOME"]) / "openriak-metadata"
    return Path.home() / ".cache" / "openriak-metadata"


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _validate_packages(supported: dict, downloads: dict) -> None:
    ids = {item["id"] for item in supported["operating_systems"]}
    if not set(downloads["downloads"]).issubset(ids):
        raise ValueError("downloads contain an unsupported OS identifier")
    seen = set()
    for variants in downloads["downloads"].values():
        for package in variants.values():
            if package["url"] in seen:
                raise ValueError(f"duplicate package URL: {package['url']}")
            seen.add(package["url"])
            if package["url"].rsplit("/", 1)[-1] != package["filename"]:
                raise ValueError(f"URL filename mismatch: {package['url']}")


if __name__ == "__main__":
    raise SystemExit(main())
