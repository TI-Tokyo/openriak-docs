"""Cache approvals operations."""
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
DEFAULT_CLUSTER_NODES = 5


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


def group_input(tool, targets, cluster_nodes, tags):
    from cache.dependencies import inputs
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
