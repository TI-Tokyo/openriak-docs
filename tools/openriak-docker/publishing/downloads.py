"""Publishing downloads operations."""
from __future__ import annotations
from cache.dependencies import matches as input_matches
import argparse
import contextlib
import dataclasses
import json
import os
import pathlib
import re
import shutil
import socket
import subprocess
from typing import Any, Callable, Iterable
from core.defaults import DEFAULT_TIMEOUT_SECONDS


def artifact_downloads(tool,
    target: Target,
    dockerfile: pathlib.Path,
    compose_single: pathlib.Path,
    compose_cluster: pathlib.Path,
    environment_example: pathlib.Path,
) -> dict[str, Any]:
    base_url = "." if target.output_root is not None else f"downloads/docker/{target.version}/{target.image_tag}"
    return {
        "dockerfile": {
            "filename": "Dockerfile",
            "url": f"{base_url}/Dockerfile",
            "sha256": tool.sha256_file(dockerfile),
        },
        "compose_single": {
            "filename": "compose.single.yaml",
            "url": f"{base_url}/compose.single.yaml",
            "sha256": tool.sha256_file(compose_single),
        },
        "compose_cluster": {
            "filename": "compose.cluster.yaml",
            "url": f"{base_url}/compose.cluster.yaml",
            "sha256": tool.sha256_file(compose_cluster),
        },
        "environment_example": {
            "filename": "example.env",
            "url": f"{base_url}/example.env",
            "sha256": tool.sha256_file(environment_example),
        },
    }


def sync_download_metadata(tool, versions: Iterable[str], timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> None:
    versions = sorted(set(versions), key=tool.semver_key)
    if not versions:
        return
    from cache import storage
    if tool.MULTIARCH_CACHE_ROOT == storage.WORK / 'images':
        storage.capture_tree()
    node = shutil.which("node")
    if not node:
        raise tool.DockerToolError("Node.js is required to update Docker download metadata; install Node.js and run sync-static")
    command = [node, str(tool.REPOSITORY_ROOT / "tools/scripts/sync-product-metadata.js"), "--docker-only"]
    for version in versions:
        command.extend(["--include-version", f"openriak-kv={version}"])
    try:
        result = subprocess.run(command, cwd=tool.REPOSITORY_ROOT, text=True, capture_output=True, timeout=timeout_seconds)
    except subprocess.TimeoutExpired as error:
        raise tool.DockerToolError(f"Docker download metadata update timed out after {timeout_seconds}s; cached test results are retained") from error
    if result.returncode:
        raise tool.DockerToolError(f"Could not update Docker download metadata: {result.stderr.strip()}; cached test results are retained")
    print("".join(f"{tool.log_timestamp()} {line}\n" for line in result.stdout.splitlines() if line.strip()), end="", flush=True)


def publish_current_run(tool, target: Target, run_root: pathlib.Path, report: dict[str, Any]) -> None:
    current = target.cache_directory
    current.mkdir(parents=True, exist_ok=True)
    for filename in tool.ARTIFACT_FILENAMES:
        source = run_root / filename
        if source.is_file():
            shutil.copy2(source, current / filename)
    with contextlib.suppress(FileNotFoundError):
        (current / "compose.yaml").unlink()
    tool.write_json(run_root / "report.json", report)
    tool.write_json(current / "report.json", report)

    if target.grouped or target.output_root is not None:
        return

    if report["status"] == "passed":
        target.static_directory.mkdir(parents=True, exist_ok=True)
        for filename in tool.ARTIFACT_FILENAMES:
            shutil.copy2(run_root / filename, target.static_directory / filename)
        with contextlib.suppress(FileNotFoundError):
            (target.static_directory / "compose.yaml").unlink()
    elif target.static_directory.exists():
        for filename in tool.ARTIFACT_FILENAMES:
            with contextlib.suppress(FileNotFoundError):
                (target.static_directory / filename).unlink()
    tool.sync_download_metadata([target.version])


def cached_current_reports(tool, ) -> Iterable[tuple[pathlib.Path, dict[str, Any]]]:
    if not tool.CACHE_ROOT.exists():
        return []
    reports: list[tuple[pathlib.Path, dict[str, Any]]] = []
    for path in tool.CACHE_ROOT.glob("*/*/*/report.json"):
        try:
            reports.append((path, tool.read_json(path)))
        except (OSError, json.JSONDecodeError):
            continue
    return reports


def sync_static(tool, ) -> int:
    copied = 0
    versions = set()
    for report_path, report in tool.cached_current_reports():
        versions.add(report["target"]["version"])
        if report.get("schema_version") != tool.SCHEMA_VERSION or report.get("status") != "passed":
            continue
        target_data = report["target"]
        matches = tool.discover_targets(
            [target_data["version"]],
            os_id=target_data["os_id"],
            download_id=target_data["download_id"],
        )
        if len(matches) != 1:
            raise tool.DockerToolError(f"Cached report no longer matches metadata: {report_path}")
        target = matches[0]
        destination = target.static_directory
        destination.mkdir(parents=True, exist_ok=True)
        for filename in tool.report_artifact_filenames(report):
            source = report_path.parent / filename
            if not source.is_file():
                raise tool.DockerToolError(f"Cached report is missing {source}")
            shutil.copy2(source, destination / filename)
        with contextlib.suppress(FileNotFoundError):
            (destination / "compose.yaml").unlink()
        copied += 1
    for group in tool.grouped_targets(tool.discover_targets()):
        report_path = group[0].group_directory / "report.json"
        if report_path.is_file():
            report = tool.read_json(report_path)
            if report.get("status") == "passed":
                identity = tool.ImageIdentity(**report.get("identity", {}))
                tool.publish_group([dataclasses.replace(t, identity=identity) for t in group], report)
                copied += 1
    tool.sync_download_metadata(versions)
    return copied


def publish_group(tool, targets: list[Target], report: dict[str, Any], timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> None:
    if report.get("status") != "passed":
        return
    target = targets[0]
    if target.output_root is not None:
        return
    report['publication'] = {'status': 'running', 'started_at': tool.isoformat()}
    tool.write_json(target.group_directory / 'report.json', report)
    try:
        target.static_directory.mkdir(parents=True, exist_ok=True)
        for artifact in report["artifacts"].values():
            source = target.group_directory / artifact["filename"]
            if tool.sha256_file(source) != artifact["sha256"]:
                raise tool.DockerToolError(f"Grouped artifact checksum mismatch: {source}")
            shutil.copy2(source, target.static_directory / source.name)
        tool.sync_download_metadata([target.version], timeout_seconds=timeout_seconds)
    except BaseException as error:
        report['publication'].update(status='failed', error=str(error), finished_at=tool.isoformat())
        raise
    else:
        report['publication'].update(status='passed', finished_at=tool.isoformat())
    finally:
        tool.write_json(target.group_directory / 'report.json', report)
