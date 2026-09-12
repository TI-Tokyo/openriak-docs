"""Cache operations; dependencies are supplied by the public tool facade."""
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

from publishing.downloads import artifact_downloads, sync_download_metadata, publish_current_run, cached_current_reports, sync_static, publish_group
from cache.approvals import initial_report, report_artifact_filenames, cache_state, group_input, group_is_passed, approved_group_report
from images.exports import build_group_images, rebuild_approved_group
DEFAULT_CLUSTER_NODES = 5






























def refresh_group(tool, targets: list[Target], options: argparse.Namespace, all_targets: list[Target],
                  builder_lifecycle: MultiarchBuilderLifecycle | None = None) -> bool:
    target = targets[0]
    root = target.group_directory
    tags = tool.image_aliases(target, all_targets)
    inputs = tool.group_input(targets, options.cluster_nodes, tags)
    report_path = root / "report.json"
    report = tool.read_json(report_path) if report_path.is_file() else {}
    from images.planning import evaluate
    plan = evaluate(tool, targets, options, all_targets)
    if plan["action"] == "SKIP":
        print(f"{tool.log_timestamp()} SKIPPED {target.image} (all platforms passed)", flush=True)
        tool.publish_group(targets, report, timeout_seconds=options.timeout)
        return True
    if plan["action"] == "BLOCKED":
        raise tool.DockerToolError("; ".join(plan["reasons"]))
    identifier = tool.run_id()
    history = root / "runs" / identifier
    logs = history / "logs"
    history.mkdir(parents=True, exist_ok=False)
    reusable = plan["reuse_artifacts"]
    previous = report
    report = {
        "schema_version": tool.MULTIARCH_SCHEMA_VERSION, "product": "openriak-kv",
        "status": "running", "image": target.image, "tags": tags,
        "identity": dataclasses.asdict(target.identity),
        "run_id": identifier, "started_at": tool.isoformat(), "finished_at": None,
        "worker": {"pid": os.getpid(), "host": socket.gethostname()},
        "inputs": inputs, "platforms": [t.platform for t in targets],
        "targets": [{"os_id": t.os_id, "download_id": t.download_id, "architecture": t.architecture} for t in targets],
        "version": target.version, "os_family": target.family, "os_release": target.release,
        "os_name": target.operating_system["display_name"], "otp": target.otp,
        "node": target.node_name, "cluster_nodes": options.cluster_nodes,
        "steps": [], "platform_results": {}, "artifacts": {}, "error": None,
    }
    from core.state import StepReport
    report = StepReport(report, lambda value: tool.write_json(report_path, value))
    tool.write_json(report_path, report)
    try:
        if reusable:
            report["base_images"] = previous["base_images"]
            report["distributed_cookie"] = previous["distributed_cookie"]
        else:
            report["base_images"] = {}
            report["distributed_cookie"] = tool.generate_distributed_cookie()
            for platform_target in targets:
                print(f"{tool.log_timestamp()}   Pulling {tool.base_image_for(platform_target)} for {platform_target.platform}", flush=True)
                base, pinned = tool.resolve_base_image(platform_target, logs / platform_target.platform.replace("/", "-"), options.timeout)
                report["base_images"][platform_target.platform] = {"requested": base, "pinned": pinned, "resolved_at": tool.isoformat()}
            cookie = report["distributed_cookie"]
            tool.render_group_assets(targets, report["base_images"], cookie, tags, options.cluster_nodes, root)
        report["generated_artifacts"] = {name: tool.sha256_file(root / name) for name in tool.ARTIFACT_FILENAMES}
        for name in tool.ARTIFACT_FILENAMES:
            shutil.copy2(root / name, history / name)
        tool.write_json(report_path, report)
        (root / ".dockerignore").write_text("*\n")
        tool.ensure_multiarch_builder(logs, options.timeout, builder_lifecycle)
        skipped_platforms = {platform for platform, action, _ in plan['platforms'] if action == 'SKIP'}
        for platform_target in targets:
            if platform_target.platform in skipped_platforms:
                print(f"{tool.log_timestamp()}   SKIPPED {platform_target.platform} (same shared files passed)", flush=True)
                passed = True
            else:
                print(f"{tool.log_timestamp()}   Testing {platform_target.platform} (timeout {options.timeout}s per phase)", flush=True)
                passed = tool.refresh_target(platform_target, options.timeout, options.keep_test_workdir, options.cluster_nodes,
                    lambda message: print(f"{tool.log_timestamp()}     {message}", flush=True), prepared=report)
                print(f"{tool.log_timestamp()}   {'PASSED' if passed else 'FAILED'} {platform_target.platform}", flush=True)
            platform_report = tool.read_json(platform_target.cache_directory / "report.json")
            report["platform_results"][platform_target.platform] = {
                "status": "passed" if passed else "failed", "run_id": platform_report["run_id"],
                "finished_at": platform_report["finished_at"],
                "report": str((platform_target.cache_directory / "runs" / platform_report["run_id"] / "report.json").relative_to(root)),
                "artifacts": platform_report["artifacts"],
            }
            tool.write_json(report_path, report)
        if not all(result["status"] == "passed" for result in report["platform_results"].values()):
            raise tool.DockerToolError("One or more architecture tests failed; shared downloads will not be published")
        tool.build_group_images(target, report["platforms"],
            tool.namespaced_tags(tags, getattr(options, "extra_namespace", [])), root, history, report, options.timeout)
        report["artifacts"] = tool.artifact_downloads(target, *(root / name for name in tool.ARTIFACT_FILENAMES))
        report["status"] = "passed"
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
        tool.write_json(report_path, report)
        tool.write_json(history / "report.json", report)
    tool.publish_group(targets, report, timeout_seconds=options.timeout)
    return report["status"] == "passed"


def generate_group(tool, targets: list[Target], options: argparse.Namespace, all_targets: list[Target]) -> bool:
    """Render standalone files; no build, test approval, or docs publication."""
    target = targets[0]
    if target.output_root is None:
        raise tool.DockerToolError("generate requires a standalone --output path")
    root = target.group_directory
    tags = tool.image_aliases(target, all_targets)
    inputs = tool.group_input(targets, options.cluster_nodes, tags)
    report_path = root / "report.json"
    previous = tool.read_json(report_path) if report_path.is_file() else {}
    if previous and not options.force:
        valid = (previous.get("status") in {"generated", "passed"} and previous.get("inputs") == inputs
                 and len(previous.get("generated_artifacts", {})) == len(tool.ARTIFACT_FILENAMES)
                 and all((root / name).is_file() and tool.sha256_file(root / name) == previous["generated_artifacts"].get(name)
                         for name in tool.ARTIFACT_FILENAMES))
        if valid:
            print(f"{tool.log_timestamp()} SKIPPED {target.image} (unchanged files already exist)", flush=True)
            return True
        raise tool.DockerToolError(f"Output already contains changed or incompatible files; use --force: {root}")
    if not previous and not options.force and any((root / name).exists() for name in tool.ARTIFACT_FILENAMES):
        raise tool.DockerToolError(f"Output contains files without a generation report; use --force: {root}")
    history = root / "runs" / tool.run_id()
    history.mkdir(parents=True, exist_ok=False)
    # Keep any previous current files, including operator edits, before replacement.
    for filename in (*tool.ARTIFACT_FILENAMES, "report.json"):
        if (root / filename).is_file():
            (history / "previous").mkdir(exist_ok=True)
            shutil.copy2(root / filename, history / "previous" / filename)
    report = {
        "schema_version": tool.MULTIARCH_SCHEMA_VERSION, "product": "openriak-kv", "operation": "generate",
        "status": "running", "tests": {"status": "not_run"}, "run_id": history.name,
        "image": target.image, "tags": tags, "identity": dataclasses.asdict(target.identity),
        "version": target.version, "cluster_nodes": options.cluster_nodes, "inputs": inputs,
        "platforms": [t.platform for t in targets], "base_images": {}, "artifacts": {},
        "started_at": tool.isoformat(), "finished_at": None, "steps": [], "error": None,
    }
    try:
        for platform_target in targets:
            requested = tool.base_image_for(platform_target)
            base = None
            if not options.force:
                docs_target = dataclasses.replace(platform_target, identity=tool.ImageIdentity(), output_root=None)
                docs_report_path = docs_target.group_directory / "report.json"
                cached = [previous]
                if docs_report_path.is_file():
                    cached.append(tool.read_json(docs_report_path))
                for candidate in cached:
                    value = candidate.get("base_images", {}).get(platform_target.platform, {})
                    if (value.get("requested") == requested
                            and re.fullmatch(re.escape(requested) + r"@sha256:[0-9a-f]{64}", value.get("pinned", ""))):
                        base = dict(value)
                        print(f"{tool.log_timestamp()}   Reusing recorded base digest for {requested} ({platform_target.platform})", flush=True)
                        break
            if base is None:
                print(f"{tool.log_timestamp()}   Pulling and pinning {requested} for {platform_target.platform}", flush=True)
                requested, pinned = tool.resolve_base_image(platform_target, history / "logs" / platform_target.platform.replace("/", "-"), options.timeout)
                base = {"requested": requested, "pinned": pinned, "resolved_at": tool.isoformat()}
            report["base_images"][platform_target.platform] = base
        report["distributed_cookie"] = tool.generate_distributed_cookie()
        tool.render_group_assets(targets, report["base_images"], report["distributed_cookie"], tags,
                            options.cluster_nodes, history)
        for filename in tool.ARTIFACT_FILENAMES:
            shutil.copy2(history / filename, root / filename)
        (root / ".dockerignore").write_text("*\n")
        report["generated_artifacts"] = {name: tool.sha256_file(root / name) for name in tool.ARTIFACT_FILENAMES}
        report["artifacts"] = tool.artifact_downloads(target, *(root / name for name in tool.ARTIFACT_FILENAMES))
        report["status"] = "generated"
    except KeyboardInterrupt:
        report["status"] = "interrupted"
        report["error"] = "Stopped by operator"
        raise
    except (tool.DockerToolError, OSError) as error:
        report["status"] = "failed"
        report["error"] = str(error)
        print(f"{tool.log_timestamp()} FAILED: {error}", flush=True)
    finally:
        report["finished_at"] = tool.isoformat()
        tool.write_json(history / "report.json", report)
        tool.write_json(report_path, report)
    return report["status"] == "generated"
