from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
import shutil
import tempfile

from .copies import (CopyCatalog, DEFAULT_WEB_ROOT, LocalCopyClient, RemoteCopyClient,
                     normalize_web_root, parse_remote_copy)
from .defaults import extract_defaults
from .cli_commands import generate_cli_commands
from .http import HttpClient
from .packages import PackageCatalog
from .registry import PRODUCTS
from .repository import install_files
from .source import SourceResolver
from .staging import (VERSION, inspect_release, list_releases, read_document,
                      staged_versions, validate_packages, validate_settings, validate_cli_commands)

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if not (REPOSITORY_ROOT / "content" / "openriak-kv" / "metadata").is_dir():
    REPOSITORY_ROOT = Path.cwd()
DEFAULT_OUTPUT = REPOSITORY_ROOT / "artifacts" / "openriak-metadata"


def build_parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        prog="openriak-metadata", description="Stage, inspect and deploy OpenRiak metadata",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=("Workflow:\n"
                "  openriak-metadata kv-packages --version 3.4.0 --version 3.4.1\n"
                "  openriak-metadata kv-settings\n"
                "  openriak-metadata kv-cli-commands --version 3.4.0 --version 3.4.1\n"
                "  openriak-metadata list\n"
                "  openriak-metadata deploy\n\n"
                "Generation writes to artifacts/openriak-metadata/; only deploy updates Hugo metadata."),
    )
    subcommands = result.add_subparsers(dest="command", required=True)
    for name, description in (
        ("kv-packages", "Generate and stage OpenRiak KV package metadata"),
        ("kv-settings", "Generate and stage KV settings using staged package OS targets"),
        ("kv-cli-commands", "Discover KV CLI commands, options, help and OS service variants"),
        ("list", "List staged metadata dates, status and deployment readiness"),
        ("deploy", "Deploy validated staged metadata to the Hugo docs metadata folder"),
    ):
        command = subcommands.add_parser(name, help=description, description=description)
        command.set_defaults(product="kv")
        command.add_argument("--metadata-dir", "--output", dest="output", type=Path, default=DEFAULT_OUTPUT,
                             metavar="DIR", help="Staged metadata directory (default: %(default)s); files live beneath DIR/kv/VERSION")
        command.add_argument("--version", action="append", dest="versions", required=name in ("kv-packages", "kv-cli-commands"),
                             metavar="VERSION", help="Exact release version (repeatable); other commands default to all staged KV versions")
        command.add_argument("--log-level", choices=("debug", "info", "warning", "error"), default="info",
                             help="Diagnostic verbosity (default: %(default)s)")
        if name == "deploy":
            command.add_argument("--repo", type=Path, default=REPOSITORY_ROOT, metavar="PATH",
                                 help="Docs checkout to update (default: %(default)s)")
        if name in ("list", "deploy"):
            continue
        command.add_argument("--cache-dir", type=Path, help="HTTP and source cache directory (default: $XDG_CACHE_HOME/openriak-metadata or ~/.cache/openriak-metadata)")
        command.add_argument("--refresh", action="store_true", help="Refresh cached checksums, source repositories and CLI runtime image before generation")
        command.add_argument("--strict", action="store_true", help="Require complete metadata; otherwise partial settings/CLI discovery may be staged for inspection")
        if name in ("kv-settings", "kv-cli-commands"):
            command.add_argument("--keep-workdir", action="store_true", help="Retain temporary source working directories after extraction")
        if name == "kv-cli-commands":
            command.add_argument("--runtime-image", metavar="TAG",
                                 help="Runtime image tag/digest (default: tiotjp/openriak-kv:VERSION-alpine-3.24); {version} expands for each release")
            command.add_argument("--docs-root", type=Path, default=REPOSITORY_ROOT, metavar="PATH",
                                 help="Checkout containing the historical CLI discovery docs (default: %(default)s)")
        if name == "kv-packages":
            source = command.add_mutually_exclusive_group()
            source.add_argument("--local-copy", type=Path, metavar="DIR",
                                help="Discover and hash packages in a local directory containing kv/")
            source.add_argument("--remote-copy", metavar="USER@HOST:PATH",
                                help="Discover and hash packages over SSH in a directory containing kv/")
            command.add_argument("--web-root", metavar="URL",
                                 help=f"Public URL prefix before kv/ (default: {DEFAULT_WEB_ROOT}); also used for discovery when no copy is selected")
            command.add_argument("--checksum-workers", type=int, default=4,
                                 help="Number of packages hashed concurrently over HTTP, locally or over SSH (default: 4)")
    return result


def main(argv: list[str] | None = None) -> int:
    cli = build_parser()
    args = cli.parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level.upper()), format="%(levelname)s: %(message)s")
    if any(not VERSION.fullmatch(version) for version in args.versions or []):
        cli.error("--version must be an exact major.minor.patch version")
    if getattr(args, "checksum_workers", 1) < 1:
        cli.error("--checksum-workers must be at least 1")
    try:
        if getattr(args, "web_root", None) is not None:
            args.web_root = normalize_web_root(args.web_root)
        if getattr(args, "remote_copy", None) is not None:
            parse_remote_copy(args.remote_copy)
        if getattr(args, "local_copy", None) is not None:
            args.local_copy = args.local_copy.expanduser().resolve()
            if not (args.local_copy / "kv").is_dir():
                raise ValueError(f"--local-copy must contain kv/: {args.local_copy}")
    except ValueError as error:
        cli.error(str(error))
    try:
        args.output = args.output.expanduser().absolute()
        versions = list(dict.fromkeys(args.versions)) if args.versions else staged_versions(args.output)
        if args.command == "list":
            return list_releases(args.output, versions)
        if not versions:
            raise ValueError("No staged metadata; run kv-packages --version VERSION first")
        if args.command == "deploy":
            return deploy(args, versions)
        # Publish a generation batch only after every requested version validates.
        # Previous deployable results survive failed regeneration.
        with tempfile.TemporaryDirectory(prefix="openriak-metadata-") as temporary:
            stage = Path(temporary)
            files = {}
            for version in versions:
                current = argparse.Namespace(**{**vars(args), "version": version, "output": stage,
                                                "package_input": args.output})
                if generate_version(current):
                    return 2
                names = {"kv-packages": ("supported-os.json", "downloads.json"),
                         "kv-settings": ("defaults.json",), "kv-cli-commands": ("cli-commands.json",)}[args.command]
                for name in names:
                    files[Path(version) / name] = stage / "kv" / version / name
            install_files(files, args.output / "kv", skip_identical=False)
        logging.info("Staged %s file(s) in %s; use list to inspect, then deploy", len(files), args.output)
        return 0
    except (OSError, ValueError) as error:
        logging.error("Metadata update failed: %s", error)
        return 2


def deploy(args, versions: list[str]) -> int:
    repository = args.repo.expanduser().absolute()
    destination = repository / "content" / "openriak-kv" / "metadata"
    if not destination.is_dir():
        raise ValueError(f"Repository metadata directory not found in {repository}; use --repo PATH")
    if args.output.resolve() == destination.resolve() or args.output.resolve() in destination.resolve().parents:
        raise ValueError("Staged metadata and the deployment destination must be separate")
    # Validate exactly the snapshot we will install, even if generation runs again.
    with tempfile.TemporaryDirectory(prefix="openriak-metadata-deploy-") as temporary:
        snapshot = Path(temporary)
        files = {}
        for version in versions:
            release = inspect_release(args.output, version)
            if release.errors:
                raise ValueError(f"{version}: " + "; ".join(release.errors))
            for name, source in release.files.items():
                target = snapshot / "kv" / version / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                files[Path(version) / name] = target
            checked = inspect_release(snapshot, version)
            if checked.errors:
                raise ValueError(f"{version}: " + "; ".join(checked.errors))
        count = install_files(files, destination)
    logging.info("Deployed %s changed metadata file(s) to %s", count, destination)
    return 0


def generate_version(args) -> int:
    product = PRODUCTS["kv"]
    destination = args.output / "kv" / args.version
    if args.command == "kv-cli-commands":
        args.cache_dir = args.cache_dir or default_cache_dir()
        document = generate_cli_commands(args, args.docs_root.expanduser().resolve())
        for warning in document.get("warnings", []):
            logging.warning("KV %s CLI: %s", args.version, warning)
        validate_cli_commands(document, require_complete=args.strict)
        write_json(destination / "cli-commands.json", document)
        logging.info("Discovered %s CLI entries for KV %s (%s)", len(document['commands']), args.version, document['status'])
        return 0
    if args.command == "kv-settings":
        package_root = args.package_input / "kv" / args.version
        supported = read_document(package_root / "supported-os.json", args.version)
        downloads = read_document(package_root / "downloads.json", args.version)
        validate_packages(supported, downloads)
        document = generate_defaults(args, product, supported["operating_systems"])
        for warning in document.get("warnings", []):
            logging.warning("KV %s settings: %s", args.version, warning)
        validate_settings(document, supported["operating_systems"])
        if args.strict and document["status"] != "complete":
            raise ValueError(f"KV {args.version} settings are incomplete (--strict)")
        write_json(destination / "defaults.json", document)
        return 0
    logging.info("Discovering packages for OpenRiak KV %s", args.version)
    web_root = args.web_root
    catalog_class = PackageCatalog
    if args.local_copy is not None:
        web_root = web_root or DEFAULT_WEB_ROOT
        client = LocalCopyClient(args.local_copy, web_root)
        catalog_class = CopyCatalog
    elif args.remote_copy is not None:
        web_root = web_root or DEFAULT_WEB_ROOT
        client = RemoteCopyClient(args.remote_copy, web_root)
        catalog_class = CopyCatalog
    else:
        client = HttpClient(cache_dir=args.cache_dir or default_cache_dir(), refresh=args.refresh)
    try:
        targets, downloads, warnings = catalog_class(client, checksum_workers=args.checksum_workers, web_root=web_root).discover(
            "kv", args.version, product["files_path"], generate_checksums=True)
    except Exception as error:
        raise ValueError(f"Package discovery failed for {args.version}: {error}") from error
    package_status = "partial" if warnings else ("complete" if targets else "unavailable")
    if not targets:
        warnings.append("No matching binary packages were found.")
    common = {"schema_version": 1, "product": "kv", "product_name": product["display_name"],
              "version": args.version, "status": package_status, "warnings": sorted(set(warnings))}
    supported = {**common, "operating_systems": targets}
    download_document = {**common, "downloads": downloads}
    for warning in warnings:
        logging.warning("KV %s: %s", args.version, warning)
    validate_packages(supported, download_document)
    write_json(destination / "supported-os.json", supported)
    write_json(destination / "downloads.json", download_document)
    return 0


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



if __name__ == "__main__":
    raise SystemExit(main())
