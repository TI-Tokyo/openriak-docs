"""Cache operations; dependencies are supplied by the public tool facade."""
from __future__ import annotations
from openriak_dependencies import matches as input_matches
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
from openriak_defaults import DEFAULT_TIMEOUT_SECONDS
DEFAULT_CLUSTER_NODES = 5


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


def initial_report(tool,
    target: Target,
    identifier: str,
    cluster_nodes: int,
    distributed_cookie: str,
) -> dict[str, Any]:
    package = target.package
    return {
        "schema_version": tool.MULTIARCH_SCHEMA_VERSION if target.grouped else tool.SCHEMA_VERSION,
        "identity": dataclasses.asdict(target.identity),
        "product": "openriak-kv",
        "status": "running",
        "run_id": identifier,
        "started_at": tool.isoformat(),
        "finished_at": None,
        "target": {
            "version": target.version,
            "os_id": target.os_id,
            "os_name": target.operating_system["display_name"],
            "os_family": target.family,
            "os_release": target.release,
            "otp": target.otp,
            "architecture": target.architecture,
            "docker_platform": target.platform,
            "download_id": target.download_id,
            **({"package_os_id": target.operating_system["alias_of"]}
               if "alias_of" in target.operating_system else {}),
        },
        "package": {
            "filename": package["filename"],
            "format": package["format"],
            "url": package["url"],
            "checksum": package["checksum"],
        },
        "image": target.image,
        "node": target.node_name,
        "generation": {
            "cluster_nodes": cluster_nodes,
            "distributed_cookie": distributed_cookie,
        },
        "metadata_sources": [
            f"content/openriak-kv/metadata/{target.version}/supported-os.json",
            f"content/openriak-kv/metadata/{target.version}/downloads.json",
            *([str(tool.OS_ALIASES_PATH.relative_to(tool.REPOSITORY_ROOT))]
              if "alias_of" in target.operating_system else []),
        ],
        "base_image": None,
        "volumes": {
            "config": {"container": "/etc/riak", "default": f"./{target.node_name}/config"},
            "data": {"container": "/var/lib/riak", "default": f"./{target.node_name}/data"},
            "logs": {"container": "/var/log/riak", "default": f"./{target.node_name}/logs"},
        },
        "network": {
            "address_assignment": "docker",
            "node_host": tool.default_node_host(1),
            "riak_node_name": f"openriak-kv@{tool.default_node_host(1)}",
        },
        "ports": {"protobuf": 8087, "http": 8098},
        "steps": [],
        "tests": {},
        "artifacts": {},
        "error": None,
    }


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


def report_artifact_filenames(tool, report: dict[str, Any]) -> tuple[str, ...]:
    environment = report.get("artifacts", {}).get("environment_example", {}).get("filename")
    return (*tool.ARTIFACT_FILENAMES[:3], ".env.example" if environment == ".env.example" else "example.env")


def cache_state(tool, target: Target, cluster_nodes: int = DEFAULT_CLUSTER_NODES) -> tuple[str, str]:
    report_path = target.cache_directory / "report.json"
    try:
        report = tool.read_json(report_path) if report_path.exists() else {}
    except (OSError, json.JSONDecodeError) as error:
        return "invalid", f"unreadable report: {error}"
    expected_paths = [target.cache_directory / filename for filename in tool.report_artifact_filenames(report)]
    present = [path for path in [report_path, *expected_paths] if path.exists()]
    if not present:
        return "missing", ""
    missing = [path.name for path in [report_path, *expected_paths] if not path.is_file()]
    if missing:
        return "invalid", f"missing files: {', '.join(missing)}"
    try:
        report = tool.read_json(report_path)
    except (OSError, json.JSONDecodeError) as error:
        return "invalid", f"unreadable report: {error}"
    if report.get("schema_version") != (tool.MULTIARCH_SCHEMA_VERSION if target.grouped else tool.SCHEMA_VERSION):
        return "invalid", "cache schema is obsolete"
    if report.get("status") != "passed":
        return "invalid", f"current report status is {report.get('status')!r}"
    if report.get("product") != "openriak-kv" or report.get("image") != target.image:
        return "invalid", "cache report does not match the selected OpenRiak target"
    if report.get("generation", {}).get("cluster_nodes") != cluster_nodes:
        return "invalid", "cached cluster node count differs from the requested value"
    artifact_names = {
        "dockerfile": "Dockerfile",
        "compose_single": "compose.single.yaml",
        "compose_cluster": "compose.cluster.yaml",
        "environment_example": tool.report_artifact_filenames(report)[-1],
    }
    for key, filename in artifact_names.items():
        artifact = report.get("artifacts", {}).get(key, {})
        path = target.cache_directory / filename
        if artifact.get("filename") != filename or artifact.get("sha256") != tool.sha256_file(path):
            return "invalid", f"artifact metadata does not match {filename}"
    return "valid", ""


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


def group_input(tool, targets, cluster_nodes, tags):
    from openriak_dependencies import inputs
    return inputs(tool, targets, cluster_nodes, tags)


def group_is_passed(tool, targets: list[Target], report: dict[str, Any], inputs: dict[str, Any]) -> bool:
    if report.get("status") != "passed" or not input_matches(tool, targets, report, inputs):
        return False
    if set(report.get("platform_results", {})) != {t.platform for t in targets}:
        return False
    if any(result.get("status") != "passed" for result in report["platform_results"].values()):
        return False
    root = targets[0].group_directory
    for artifact in report.get("artifacts", {}).values():
        path = root / artifact["filename"]
        if not path.is_file() or tool.sha256_file(path) != artifact["sha256"]:
            return False
    return len(report.get("artifacts", {})) == len(tool.ARTIFACT_FILENAMES)


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


def approved_group_report(tool, targets: list[Target]) -> dict[str, Any]:
    """Validate recorded approval of saved bytes, independently of today's renderer."""
    target = targets[0]
    root = target.group_directory
    path = root / "report.json"
    if not path.is_file():
        raise tool.DockerToolError(f"No approved cache for {target.image}")
    report = tool.read_json(path)
    if (report.get("schema_version") != tool.MULTIARCH_SCHEMA_VERSION
            or report.get("product") != "openriak-kv" or report.get("version") != target.version
            or report.get("image") != target.image or report.get("status") != "passed"
            or set(report.get("platforms", [])) != {t.platform for t in targets}
            or not tool.group_is_passed(targets, report, report.get("inputs", {}))):
        raise tool.DockerToolError(f"No complete, unchanged approval for {target.image}")
    tool.namespaced_tags(report.get("tags", []), [])
    if target.image not in report["tags"]:
        raise tool.DockerToolError(f"Approval is missing the primary image tag: {target.image}")
    keys = ("dockerfile", "compose_single", "compose_cluster", "environment_example")
    for key, filename in zip(keys, tool.ARTIFACT_FILENAMES):
        artifact = report.get("artifacts", {}).get(key, {})
        if artifact.get("filename") != filename or tool.sha256_file(root / filename) != artifact.get("sha256"):
            raise tool.DockerToolError(f"Approved artifact is missing or changed: {root / filename}")
    for platform in report["platforms"]:
        result = report["platform_results"][platform]
        proof_path = (root / result.get("report", "")).resolve()
        if not proof_path.is_relative_to(root.resolve()) or not proof_path.is_file():
            raise tool.DockerToolError(f"Missing platform approval for {target.image} {platform}")
        proof = tool.read_json(proof_path)
        tests = proof.get("tests", {})
        cluster_tests = tests.get("cluster_admin_test", {})
        if (proof.get("schema_version") != tool.MULTIARCH_SCHEMA_VERSION
                or proof.get("product") != "openriak-kv" or proof.get("status") != "passed"
                or proof.get("image") != target.image or proof.get("run_id") != result.get("run_id")
                or proof.get("target", {}).get("docker_platform") != platform
                or tests.get("admin_test", {}).get("status") != "passed"
                or tests.get("preserved_cookie", {}).get("status") != "passed"
                or tests.get("cluster", {}).get("status") != "passed"
                or tests.get("cluster", {}).get("coordinator_cookie_adoption") != "passed"
                or len(cluster_tests) != report.get("cluster_nodes")
                or any(test.get("status") != "passed" for test in cluster_tests.values())):
            raise tool.DockerToolError(f"Incomplete platform approval for {target.image} {platform}")
        for key in keys:
            if proof.get("artifacts", {}).get(key, {}).get("sha256") != report["artifacts"][key]["sha256"]:
                raise tool.DockerToolError(f"Platform approval does not cover current {key}: {target.image} {platform}")
    return report


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


def refresh_group(tool, targets: list[Target], options: argparse.Namespace, all_targets: list[Target],
                  builder_lifecycle: MultiarchBuilderLifecycle | None = None) -> bool:
    target = targets[0]
    root = target.group_directory
    tags = tool.image_aliases(target, all_targets)
    inputs = tool.group_input(targets, options.cluster_nodes, tags)
    report_path = root / "report.json"
    report = tool.read_json(report_path) if report_path.is_file() else {}
    from openriak_plan import evaluate
    plan = evaluate(tool, targets, options, all_targets)
    if plan["action"] == "SKIP":
        if report.get('inputs') != inputs:
            report['input_migration'] = {'verified_at': tool.isoformat(),
                'previous_inputs': report['inputs'], 'method': 'byte-identical generated artifacts'}
            report['inputs'] = inputs
            tool.write_json(report_path, report)
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
    from openriak_state import StepReport
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
