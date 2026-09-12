"""Images exports operations."""
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


def build_group_images(tool,
    target: Target, platforms: list[str], tags: list[str], context: pathlib.Path,
    history: pathlib.Path, report: dict[str, Any], timeout: int, no_cache: bool = False,
) -> None:
    docker = tool.docker_command()
    logs = history / "logs"
    tag_args = [part for tag in tags for part in ("--tag", tag)]
    print(f"{tool.log_timestamp()}   Exporting OCI image for {', '.join(platforms)} with {len(tags)} tag(s)", flush=True)
    tool.record_step(report, "export_oci_image", lambda: tool.run_logged(
        [docker, "buildx", "build", "--builder", tool.MULTIARCH_BUILDER, "--platform", ",".join(platforms),
         "--pull=false", *(["--no-cache"] if no_cache else []), *tag_args,
         "--output", f"type=oci,dest={history / 'image.oci.tar'}", str(context)],
        logs / "image-export.log", timeout_seconds=timeout))
    report["oci_archive"] = str((history / "image.oci.tar").relative_to(target.group_directory))
    report["build_tags"] = tags
    host_arch = tool.run_logged([docker, "info", "--format", "{{.Architecture}}"], logs / "host-platform.log", timeout_seconds=timeout).stdout.strip()
    host_platform = tool.ARCHITECTURE_PLATFORMS.get(host_arch)
    if host_platform in platforms:
        # Reuse the just-built layers while loading the host image and every alias.
        tool.record_step(report, "load_local_tags", lambda: tool.run_logged(
            [docker, "buildx", "build", "--builder", tool.MULTIARCH_BUILDER, "--platform", host_platform,
             "--pull=false", "--load", *tag_args, str(context)],
            logs / "local-tags.log", timeout_seconds=timeout))
        report["local_tags_platform"] = host_platform
    else:
        print(f"{tool.log_timestamp()}   No {host_arch} package in this group; all tags are in the OCI archive", flush=True)


def rebuild_approved_group(tool, targets: list[Target], options: argparse.Namespace,
                           builder_lifecycle: MultiarchBuilderLifecycle | None = None) -> bool:
    target = targets[0]
    root = target.group_directory
    approval = tool.approved_group_report(targets)
    tags = tool.namespaced_tags(approval["tags"], options.extra_namespace)
    history = root / "rebuilds" / tool.run_id()
    history.mkdir(parents=True, exist_ok=False)
    report = {
        "schema_version": 1, "operation": "rebuild_without_tests", "status": "running",
        "image": target.image, "build_tags": tags, "platforms": approval["platforms"],
        "started_at": tool.isoformat(), "finished_at": None, "steps": [], "error": None,
        "tests": {"status": "not_run"}, "approved_run_id": approval["run_id"],
        "approved_artifacts": approval["artifacts"],
    }
    tool.write_json(history / "report.json", report)
    tool.write_json(history / "approval.json", approval)
    try:
        # Snapshot approved inputs so another refresh cannot change them during a build.
        for artifact in approval["artifacts"].values():
            destination = history / artifact["filename"]
            shutil.copy2(root / artifact["filename"], destination)
            if tool.sha256_file(destination) != artifact["sha256"]:
                raise tool.DockerToolError(f"Approved file changed during rebuild preparation: {destination.name}")
        (history / ".dockerignore").write_text("*\n")
        tool.ensure_multiarch_builder(history / "logs", options.timeout, builder_lifecycle)
        tool.build_group_images(target, approval["platforms"], tags, history, history, report, options.timeout, no_cache=True)
        report["status"] = "built"
    except KeyboardInterrupt:
        report["status"] = "interrupted"
        report["error"] = "Stopped by operator"
        raise
    except (tool.DockerToolError, OSError) as error:
        report["status"] = "failed"
        report["error"] = str(error)
        print(f"{tool.log_timestamp()}   FAILED: {error}", flush=True)
    finally:
        report["finished_at"] = tool.isoformat()
        tool.write_json(history / "report.json", report)
    return report["status"] == "built"
