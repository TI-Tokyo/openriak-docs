#!/usr/bin/env python3
"""Generate, test, cache, and publish OpenRiak KV Docker configurations."""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime as dt
import fnmatch
import hashlib
import inspect
import http.client
import io
import json
import os
import pathlib
import re
import secrets
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib.parse
from typing import Any, Callable, Iterable

from openriak_defaults import DEFAULT_TIMEOUT_SECONDS
import openriak_minimal as minimal
from builders import registry as builders
import openriak_render
import openriak_testing
import openriak_execution
import openriak_locks
import openriak_cache
import openriak_discovery


SCHEMA_VERSION = 3
MINIMUM_OPENRIAK_VERSION = (3, 4, 0)
REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[2]
METADATA_ROOT = REPOSITORY_ROOT / "content" / "openriak-kv" / "metadata"
OS_ALIASES_PATH = METADATA_ROOT / "os-aliases.json"
CACHE_ROOT = REPOSITORY_ROOT / "tools" / "cache" / "openriak-docker"
STATIC_ROOT = REPOSITORY_ROOT / "content" / "static" / "openriak-kv" / "downloads" / "docker"
MULTIARCH_SCHEMA_VERSION = 4
MULTIARCH_CACHE_ROOT = REPOSITORY_ROOT / "tools" / "cache" / "openriak-docker-multiarch"
MULTIARCH_BUILDER = "openriak-kv-multiarch"
DEFAULT_CLUSTER_NODES = 5
CONTROL_DIRECTORY = "/var/lib/openriak-cluster-control"
ARTIFACT_FILENAMES = (
    "Dockerfile",
    "compose.single.yaml",
    "compose.cluster.yaml",
    "example.env",
)

ARCHITECTURE_PLATFORMS = {
    "x86_64": "linux/amd64",
    "amd64": "linux/amd64",
    "aarch64": "linux/arm64",
    "arm64": "linux/arm64",
    "armhf": "linux/arm/v7",
}

BASE_IMAGES_PATH = pathlib.Path(__file__).with_name("base-images.json")


class DockerToolError(RuntimeError):
    """An expected target, Docker, or test failure."""


@dataclasses.dataclass(frozen=True)
class ImageIdentity:
    vendor: str = "OpenRiak"
    source: str = "https://github.com/OpenRiak/openriak-docs"
    url: str = "https://openriak.org"
    namespace: str = "openriak"


@dataclasses.dataclass(frozen=True)
class LifecycleOptions:
    healthcheck_interval: int = 10
    healthcheck_timeout: int = 60
    healthcheck_start_period: int = 120
    healthcheck_retries: int = 3
    stop_grace_period: int = 120


def duration_seconds(value: str) -> int:
    match = re.fullmatch(r"([0-9]+)([smh]?)", value)
    if not match:
        raise argparse.ArgumentTypeError("Use whole seconds or a duration such as 30s, 2m, or 1h")
    return int(match[1]) * {"": 1, "s": 1, "m": 60, "h": 3600}[match[2]]


@dataclasses.dataclass(frozen=True)
class Target:
    version: str
    operating_system: dict[str, Any]
    download_id: str
    package: dict[str, Any]
    grouped: bool = False
    identity: ImageIdentity = dataclasses.field(default_factory=ImageIdentity)
    output_root: pathlib.Path | None = None
    lifecycle_options: LifecycleOptions = dataclasses.field(default_factory=LifecycleOptions)

    @property
    def os_id(self) -> str:
        return str(self.operating_system["id"])

    @property
    def family(self) -> str:
        return str(self.operating_system["family"])

    @property
    def release(self) -> str:
        return str(self.operating_system["release"])

    @property
    def architecture(self) -> str:
        return str(self.package["architecture"])

    @property
    def otp(self) -> str:
        raw = self.package.get("otp")
        if raw is not None and str(raw):
            return str(raw)
        explicit = re.search(r"(?:^|[-_.])OTP([0-9]+(?:\.[0-9]+)?)(?:[-_.]|$)", self.package["filename"], re.I)
        if explicit:
            return explicit.group(1)
        alpine = re.match(
            rf"^riak-{re.escape(self.version)}\.([0-9]+)-r[0-9]+\.apk$",
            self.package["filename"],
            re.I,
        )
        if alpine:
            return alpine.group(1)
        raise DockerToolError(
            f"Unable to infer OTP version for {self.version}/{self.os_id}/{self.download_id}"
        )

    @property
    def platform(self) -> str:
        try:
            return ARCHITECTURE_PLATFORMS[self.architecture]
        except KeyError as error:
            raise DockerToolError(f"Unsupported Docker architecture: {self.architecture}") from error

    @property
    def image_tag(self) -> str:
        return "-".join(
            [self.version, self.family, self.release, f"otp{self.otp}"]
            + ([] if self.grouped else [self.architecture])
        ).lower()

    @property
    def image(self) -> str:
        return f"{self.identity.namespace}/openriak-kv:{self.image_tag}"

    @property
    def node_name(self) -> str:
        return f"openriak-kv-{self.image_tag}-node"

    @property
    def cache_directory(self) -> pathlib.Path:
        if self.grouped:
            return self.group_directory / "platforms" / self.platform.replace("/", "-")
        return (self.output_root or CACHE_ROOT) / self.version / self.os_id / self.download_id

    @property
    def group_directory(self) -> pathlib.Path:
        return (self.output_root or MULTIARCH_CACHE_ROOT) / self.version / self.image_tag

    @property
    def static_directory(self) -> pathlib.Path:
        return STATIC_ROOT / self.version / self.image_tag


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def isoformat(value: dt.datetime | None = None) -> str:
    return (value or utc_now()).isoformat(timespec="seconds").replace("+00:00", "Z")


def log_timestamp(value: dt.datetime | None = None) -> str:
    return (value or dt.datetime.now().astimezone()).strftime("%Y-%m-%d %H:%M:%S")


def run_id(value: dt.datetime | None = None) -> str:
    return (value or utc_now()).strftime("%Y%m%dT%H%M%S.%fZ")


def generate_distributed_cookie() -> str:
    """Return a Docker-target-specific, shell-safe Erlang distribution cookie."""
    return f"openriak-{secrets.token_hex(16)}"


def default_node_host(index: int) -> str:
    if index < 1 or index > 253:
        raise DockerToolError("OpenRiak node indexes must be between 1 and 253")
    return f"node-{index:02d}.cluster-a.openriak"


def read_json(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: pathlib.Path, value: dict[str, Any]) -> None:
    from openriak_cve_storage import atomic_write
    atomic_write(path, (json.dumps(value, indent=2, sort_keys=True) + "\n").encode())


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def semver_key(version: str) -> tuple[int, ...]:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise DockerToolError(f"Invalid OpenRiak KV version directory: {version}")
    return tuple(int(item) for item in match.groups())


def natural_key(value: Any) -> tuple[tuple[int, Any], ...]:
    return tuple(
        (0, int(part)) if part.isdigit() else (1, part.lower())
        for part in re.split(r"([0-9]+)", str(value or ""))
    )


def metadata_versions() -> list[str]:
    return openriak_discovery.metadata_versions(sys.modules[__name__], )



def targets_for_version(version: str) -> list[Target]:
    return openriak_discovery.targets_for_version(sys.modules[__name__], version)



def discover_targets(
    versions: Iterable[str] | None = None,
    os_id: str | Iterable[str] | None = None,
    otp: str | None = None,
    download_id: str | None = None,
) -> list[Target]:
    return openriak_discovery.discover_targets(sys.modules[__name__], versions, os_id, otp, download_id)



def base_image_for(target: Target, *, upstream: bool = False) -> str:
    return openriak_discovery.base_image_for(sys.modules[__name__], target, upstream=upstream)



def debian_repository_setup(target: Target) -> str:
    return builders.repositories(sys.modules[__name__], target)


def package_install_script(target: Target) -> str:
    return builders.install(sys.modules[__name__], target)


def create_riak_user_script(target: Target) -> str:
    return openriak_render.create_riak_user_script(sys.modules[__name__], target)



ENTRYPOINT_SCRIPT = (pathlib.Path(__file__).parent / "runtime" / "entrypoint.sh").read_text()


HEALTHCHECK_SCRIPT = (pathlib.Path(__file__).parent / "runtime" / "healthcheck.sh").read_text()


# Shared descriptions keep Dockerfile, Compose, and example.env terminology aligned.
RUNTIME_OPTIONS = {
    "TZ": ("Etc/UTC", "IANA timezone for the process and entrypoint logs, for example Asia/Tokyo."),
    "RIAK_UID": ("", "Optional nonzero UID for riak; empty retains the package UID. Mounted directories are chowned."),
    "RIAK_GID": ("", "Optional nonzero GID for riak; empty retains the package GID. Mounted directories are chowned."),
    "RIAK_LOG_MAX_FILE_SIZE": ("1MB", "Maximum size per OpenRiak logger file; initializes new configurations only."),
    "RIAK_LOG_MAX_FILES": ("10", "Maximum file count per OpenRiak logger handler; initializes new configurations only."),
}
COMPOSE_OPTIONS = {
    "OPENRIAK_CPUS": ("0", "CPU limit per node, for example 2.0; 0 means unrestricted."),
    "OPENRIAK_MEMORY_LIMIT": ("0", "Memory limit per node, for example 4g; 0 means unrestricted."),
    "OPENRIAK_DOCKER_LOG_MAX_SIZE": ("10m", "Maximum size of each Docker JSON log file per node."),
    "OPENRIAK_DOCKER_LOG_MAX_FILES": ("3", "Maximum number of Docker JSON log files retained per node."),
}


def compose_runtime_options() -> str:
    return openriak_render.compose_runtime_options(sys.modules[__name__], )



def compose_resource_options() -> str:
    return openriak_render.compose_resource_options(sys.modules[__name__], )



def image_labels(target: Target) -> dict[str, str]:
    return openriak_render.image_labels(sys.modules[__name__], target)



def render_image_labels(target: Target) -> str:
    return openriak_render.render_image_labels(sys.modules[__name__], target)



SETTING_COMMENTS = {
    **{name: description for name, (_, description) in {**RUNTIME_OPTIONS, **COMPOSE_OPTIONS}.items()},
    "RIAK_NODE_HOST": "DNS hostname used to derive the OpenRiak KV nodename.",
    "RIAK_NODE_NAME": "Explicit nodename; empty derives openriak-kv@<hostname>.",
    "RIAK_DISTRIBUTED_COOKIE": "Initial cookie; existing riak.conf wins and new followers adopt the coordinator cookie.",
    "RIAK_RING_SIZE": "Partition count for a new ring; do not change on an existing cluster.",
    "RIAK_STORAGE_BACKEND": "Storage backend used by OpenRiak KV.",
    "RIAK_ANTI_ENTROPY": "Legacy active anti-entropy mode (passive disables active exchanges).",
    "RIAK_TICTACAAE_ACTIVE": "Enable TicTac active anti-entropy.",
    "RIAK_TICTACAAE_STOREHEADS": "Store object heads in the TicTac anti-entropy store.",
    "RIAK_HTTP_LISTENER": "Container HTTP bind address and port.",
    "RIAK_PB_LISTENER": "Container Protocol Buffers bind address and port.",
    "RIAK_NOFILE_LIMIT": "Requested open-file limit; bounded by container ulimits.",
    "RIAK_INIT_ONLY": "Initialize configuration and directories without starting the daemon when 1.",
    "RIAK_STARTUP_POLL_SECONDS": "Seconds between daemon startup checks.",
    "RIAK_SHUTDOWN_POLL_SECONDS": "Seconds between BEAM shutdown checks.",
    "RIAK_MONITOR_INTERVAL_SECONDS": "Seconds between running-node health checks.",
    "OPENRIAK_CLUSTER_MODE": "Use single-node startup or shared-directory cluster discovery.",
    "OPENRIAK_CLUSTER_CONTROL_DIR": "Container directory shared by cluster discovery participants.",
    "OPENRIAK_CLUSTER_POLL_SECONDS": "Seconds between cluster discovery checks.",
    "OPENRIAK_CLUSTER_WAIT_SECONDS": "Maximum seconds to wait for cluster discovery approval.",
    "role": "Coordinator on exactly one cluster service; empty or omitted means follower.",
    "OPENRIAK_CONTAINER_NAME": "Single-node Docker container name.",
    "OPENRIAK_PB_PORT": "Host port forwarded to container Protocol Buffers port 8087.",
    "OPENRIAK_HTTP_PORT": "Host port forwarded to container HTTP port 8098.",
    "OPENRIAK_CONFIG_PATH": "Host bind-mount directory for /etc/riak configuration.",
    "OPENRIAK_DATA_PATH": "Host bind-mount directory for /var/lib/riak data.",
    "OPENRIAK_LOGS_PATH": "Host bind-mount directory for /var/log/riak logs.",
    "OPENRIAK_CLUSTER_CONTROL_PATH": "Host directory shared by all cluster discovery participants.",
}


def setting_comment(name: str) -> str:
    return openriak_render.setting_comment(sys.modules[__name__], name)



def annotate_artifact(contents: str, kind: str, image: str) -> str:
    return openriak_render.annotate_artifact(sys.modules[__name__], contents, kind, image)



def render_dockerfile(
    target: Target,
    pinned_base_image: str,
    distributed_cookie: str | None = None,
    *,
    _minimal: bool = True,
) -> str:
    return openriak_render.render_dockerfile(sys.modules[__name__], target, pinned_base_image, distributed_cookie, _minimal=_minimal)



def render_single_compose(
    target: Target,
    distributed_cookie: str | None = None,
    publish_ports: bool = True,
) -> str:
    return openriak_render.render_single_compose(sys.modules[__name__], target, distributed_cookie, publish_ports)



def cluster_node_name(target: Target, index: int) -> str:
    return openriak_render.cluster_node_name(sys.modules[__name__], target, index)



def render_cluster_service(
    target: Target,
    index: int,
    distributed_cookie: str,
    publish_ports: bool,
) -> str:
    return openriak_render.render_cluster_service(sys.modules[__name__], target, index, distributed_cookie, publish_ports)



def render_cluster_compose(
    target: Target,
    node_count: int = DEFAULT_CLUSTER_NODES,
    distributed_cookie: str | None = None,
    publish_ports: bool = True,
) -> str:
    return openriak_render.render_cluster_compose(sys.modules[__name__], target, node_count, distributed_cookie, publish_ports)



def render_environment_example(
    target: Target,
    distributed_cookie: str,
    node_count: int = DEFAULT_CLUSTER_NODES,
) -> str:
    return openriak_render.render_environment_example(sys.modules[__name__], target, distributed_cookie, node_count)



def docker_command() -> str:
    executable = shutil.which("docker") or shutil.which("docker.exe")
    if not executable:
        raise DockerToolError("Docker CLI was not found on PATH")
    return executable


def run_logged(
    command: list[str],
    log_path: pathlib.Path,
    *,
    cwd: pathlib.Path | None = None,
    environment: dict[str, str] | None = None,
    check: bool = True,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> subprocess.CompletedProcess[str]:
    return openriak_execution.run_logged(sys.modules[__name__], command, log_path, cwd=cwd, environment=environment, check=check, timeout_seconds=timeout_seconds)



def verify_runtime_options(container: str, target: Target, timeout_seconds: int, log_path: pathlib.Path) -> dict[str, Any]:
    return openriak_testing.verify_runtime_options(sys.modules[__name__], container, target, timeout_seconds, log_path)



def verify_admin_test(container: str, timeout_seconds: int, log_path: pathlib.Path) -> dict[str, Any]:
    return openriak_testing.verify_admin_test(sys.modules[__name__], container, timeout_seconds, log_path)



def digest_from_pull_output(output: str) -> str | None:
    return openriak_execution.digest_from_pull_output(sys.modules[__name__], output)



def resolve_base_image(
    target: Target,
    logs: pathlib.Path,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    *, upstream: bool = False,
) -> tuple[str, str]:
    return openriak_execution.resolve_base_image(sys.modules[__name__], target, logs, timeout_seconds, upstream=upstream)



def set_riak_setting(source: str, key: str, value: str) -> str:
    return openriak_testing.set_riak_setting(sys.modules[__name__], source, key, value)



def configure_test_node(config_path: pathlib.Path, node_name: str) -> None:
    return openriak_testing.configure_test_node(sys.modules[__name__], config_path, node_name)



def effective_riak_settings(config_path: pathlib.Path, keys: Iterable[str]) -> dict[str, str]:
    return openriak_testing.effective_riak_settings(sys.modules[__name__], config_path, keys)



def populated(path: pathlib.Path) -> bool:
    return openriak_testing.populated(sys.modules[__name__], path)



def free_tcp_port() -> int:
    return openriak_testing.free_tcp_port(sys.modules[__name__], )



def remaining_timeout(deadline: float) -> float:
    return openriak_testing.remaining_timeout(sys.modules[__name__], deadline)



def run_before_deadline(command: list[str], deadline: float, **kwargs: Any) -> subprocess.CompletedProcess[str]:
    return openriak_testing.run_before_deadline(sys.modules[__name__], command, deadline, **kwargs)



# Use the package's existing Erlang runtime; no HTTP client package is needed.
# HTTP/1.0 plus Connection: close lets gen_tcp collect the complete response.
HTTP_PROBE_ERLANG = (pathlib.Path(__file__).parent / "runtime" / "http-probe.erl").read_text()
HTTP_PROBE_COMMAND = (pathlib.Path(__file__).parent / "runtime" / "http-probe.sh").read_text()


def container_http_ping(container_name: str, timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS) -> tuple[int, str, int]:
    return openriak_testing.container_http_ping(sys.modules[__name__], container_name, timeout_seconds)



def wait_for_node(
    container_name: str,
    timeout_seconds: int,
    logs: pathlib.Path,
) -> tuple[str, str]:
    return openriak_testing.wait_for_node(sys.modules[__name__], container_name, timeout_seconds, logs)



def wait_for_container_log(
    container_name: str,
    marker: str,
    timeout_seconds: int,
    log_path: pathlib.Path,
) -> str:
    return openriak_testing.wait_for_container_log(sys.modules[__name__], container_name, marker, timeout_seconds, log_path)



def wait_for_container_health(
    container_name: str,
    timeout_seconds: int,
    log_path: pathlib.Path,
) -> str:
    return openriak_testing.wait_for_container_health(sys.modules[__name__], container_name, timeout_seconds, log_path)



def wait_for_cluster(
    container_names: list[str],
    expected_nodenames: list[str],
    timeout_seconds: int,
    log_path: pathlib.Path,
) -> dict[str, Any]:
    return openriak_testing.wait_for_cluster(sys.modules[__name__], container_names, expected_nodenames, timeout_seconds, log_path)



def record_step(report: dict[str, Any], name: str, action: Any) -> Any:
    started = time.monotonic()
    item: dict[str, Any] = {"name": name, "status": "running", "started_at": isoformat()}
    report["steps"].append(item)
    checkpoint = getattr(report, "checkpoint", lambda: None)
    checkpoint()
    try:
        result = action()
    except BaseException as error:
        item.update(
            status="interrupted" if isinstance(error, (KeyboardInterrupt, SystemExit)) else "failed",
            finished_at=isoformat(),
            duration_seconds=round(time.monotonic() - started, 3),
            error=str(error),
        )
        checkpoint()
        raise
    item.update(
        status="passed",
        finished_at=isoformat(),
        duration_seconds=round(time.monotonic() - started, 3),
    )
    checkpoint()
    return result


def artifact_downloads(
    target: Target,
    dockerfile: pathlib.Path,
    compose_single: pathlib.Path,
    compose_cluster: pathlib.Path,
    environment_example: pathlib.Path,
) -> dict[str, Any]:
    return openriak_cache.artifact_downloads(sys.modules[__name__], target, dockerfile, compose_single, compose_cluster, environment_example)



def sync_download_metadata(versions: Iterable[str], timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> None:
    return openriak_cache.sync_download_metadata(sys.modules[__name__], versions, timeout_seconds)



def publish_current_run(target: Target, run_root: pathlib.Path, report: dict[str, Any]) -> None:
    return openriak_cache.publish_current_run(sys.modules[__name__], target, run_root, report)



def initial_report(
    target: Target,
    identifier: str,
    cluster_nodes: int,
    distributed_cookie: str,
) -> dict[str, Any]:
    return openriak_cache.initial_report(sys.modules[__name__], target, identifier, cluster_nodes, distributed_cookie)



def refresh_target(
    target: Target,
    timeout_seconds: int,
    keep_workdir: bool = False,
    cluster_nodes: int = DEFAULT_CLUSTER_NODES,
    progress: Callable[[str], None] | None = None,
    prepared: dict[str, Any] | None = None,
) -> bool:
    return openriak_testing.refresh_target(sys.modules[__name__], target, timeout_seconds, keep_workdir, cluster_nodes, progress, prepared)



def cached_current_reports() -> Iterable[tuple[pathlib.Path, dict[str, Any]]]:
    return openriak_cache.cached_current_reports(sys.modules[__name__], )



def report_artifact_filenames(report: dict[str, Any]) -> tuple[str, ...]:
    return openriak_cache.report_artifact_filenames(sys.modules[__name__], report)



def cache_state(target: Target, cluster_nodes: int = DEFAULT_CLUSTER_NODES) -> tuple[str, str]:
    return openriak_cache.cache_state(sys.modules[__name__], target, cluster_nodes)



def sync_static() -> int:
    return openriak_cache.sync_static(sys.modules[__name__], )



def grouped_targets(targets: list[Target]) -> list[list[Target]]:
    return openriak_discovery.grouped_targets(sys.modules[__name__], targets)



def release_key(target: Target) -> tuple[int, ...]:
    return openriak_discovery.release_key(sys.modules[__name__], target)



def image_aliases(target: Target, all_targets: list[Target]) -> list[str]:
    return openriak_discovery.image_aliases(sys.modules[__name__], target, all_targets)



def render_multiarch_dockerfile(
    targets: list[Target], base_images: dict[str, dict[str, str]], cookie: str, tags: list[str],
) -> str:
    return openriak_render.render_multiarch_dockerfile(sys.modules[__name__], targets, base_images, cookie, tags)



class MultiarchBuilderLifecycle:
    """Restore builder state once per invocation, including interrupted builds."""

    def __init__(self) -> None:
        self.logs: pathlib.Path | None = None
        self.timeout = 0
        self.stop_required = False
        self.lease = None

    def acquire(self):
        if self.lease is None:
            lease = openriak_locks.lock(sys.modules[__name__], f'builder:{MULTIARCH_BUILDER}')
            lease.__enter__()
            self.lease = lease

    def observe(self, inspection: subprocess.CompletedProcess[str], logs: pathlib.Path, timeout: int) -> None:
        if self.logs is not None:
            return
        if inspection.returncode == 0:
            states = re.findall(r"^Status:\s*(\S+)\s*$", inspection.stdout, re.MULTILINE)
            if not states or any(state not in ("running", "stopped") for state in states):
                raise DockerToolError(f"Cannot determine usable node states for builder {MULTIARCH_BUILDER}; inspect it before refresh")
            stopped = all(state == "stopped" for state in states)
            if not stopped and "stopped" in states:
                raise DockerToolError(f"Builder {MULTIARCH_BUILDER} has mixed running/stopped nodes; start it explicitly before refresh")
            if stopped and not re.search(r"^Driver:\s*docker-container\s*$", inspection.stdout, re.MULTILINE):
                raise DockerToolError(f"Cannot temporarily start stopped builder {MULTIARCH_BUILDER}: expected the docker-container driver")
            self.stop_required = stopped
        self.logs = logs
        self.timeout = timeout

    def __enter__(self) -> MultiarchBuilderLifecycle:
        return self

    def __exit__(self, exception_type: Any, exception: Any, traceback: Any) -> None:
        try:
            if self.stop_required:
                print(f"{log_timestamp()} Stopping builder {MULTIARCH_BUILDER} started for this refresh", flush=True)
                run_logged([docker_command(), "buildx", "stop", MULTIARCH_BUILDER],
                           self.logs / "builder.log", timeout_seconds=self.timeout)
        finally:
            if self.lease is not None:
                self.lease.__exit__(exception_type, exception, traceback)
                self.lease = None


def ensure_multiarch_builder(
    logs: pathlib.Path, timeout: int, lifecycle: MultiarchBuilderLifecycle | None = None,
) -> None:
    return openriak_execution.ensure_multiarch_builder(sys.modules[__name__], logs, timeout, lifecycle)



def group_input(targets: list[Target], cluster_nodes: int, tags: list[str]) -> dict[str, Any]:
    return openriak_cache.group_input(sys.modules[__name__], targets, cluster_nodes, tags)



def group_is_passed(targets: list[Target], report: dict[str, Any], inputs: dict[str, Any]) -> bool:
    return openriak_cache.group_is_passed(sys.modules[__name__], targets, report, inputs)



def publish_group(targets: list[Target], report: dict[str, Any], timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> None:
    return openriak_cache.publish_group(sys.modules[__name__], targets, report, timeout_seconds)



def extra_namespace(value: str) -> str:
    if not re.fullmatch(r"[a-z0-9]+(?:[._-][a-z0-9]+)*", value):
        raise argparse.ArgumentTypeError("Use a lowercase namespace such as tiotjp, without a registry URL or slash")
    return value


def namespaced_tags(tags: list[str], namespaces: list[str]) -> list[str]:
    if not tags or any(not re.fullmatch(r"[a-z0-9]+(?:[._-][a-z0-9]+)*/openriak-kv:[a-zA-Z0-9_][a-zA-Z0-9_.-]{0,127}", tag) for tag in tags):
        raise DockerToolError("Image tags must use <namespace>/openriak-kv:<tag>")
    result = list(tags)
    for namespace in namespaces:
        extra_namespace(namespace)
        result.extend(f"{namespace}/openriak-kv:{tag.split(':', 1)[1]}" for tag in tags)
    return list(dict.fromkeys(result))


def approved_group_report(targets: list[Target]) -> dict[str, Any]:
    return openriak_cache.approved_group_report(sys.modules[__name__], targets)



def build_group_images(
    target: Target, platforms: list[str], tags: list[str], context: pathlib.Path,
    history: pathlib.Path, report: dict[str, Any], timeout: int, no_cache: bool = False,
) -> None:
    return openriak_cache.build_group_images(sys.modules[__name__], target, platforms, tags, context, history, report, timeout, no_cache)



def rebuild_approved_group(targets: list[Target], options: argparse.Namespace,
                           builder_lifecycle: MultiarchBuilderLifecycle | None = None) -> bool:
    with openriak_locks.activity(sys.modules[__name__]), openriak_locks.lock(sys.modules[__name__], targets[0].group_directory):
        return openriak_cache.rebuild_approved_group(sys.modules[__name__], targets, options, builder_lifecycle)



def refresh_group(targets: list[Target], options: argparse.Namespace, all_targets: list[Target],
                  builder_lifecycle: MultiarchBuilderLifecycle | None = None) -> bool:
    with openriak_locks.activity(sys.modules[__name__]), openriak_locks.lock(sys.modules[__name__], targets[0].group_directory):
        return openriak_cache.refresh_group(sys.modules[__name__], targets, options, all_targets, builder_lifecycle)


def print_matrix(targets: list[Target], as_json: bool) -> None:
    return openriak_discovery.print_matrix(sys.modules[__name__], targets, as_json)




def print_refresh_header(
    options: argparse.Namespace,
    targets: list[Target],
    started_at: dt.datetime | None = None,
) -> None:
    versions = "all" if options.all else ", ".join(dict.fromkeys(t.version for t in targets))
    os_patterns = [options.os_id] if isinstance(options.os_id, str) else options.os_id or []
    os_selection = ", ".join(os_patterns) or "all"
    if options.os_id or options.download_id:
        architectures = ", ".join(dict.fromkeys(t.architecture for t in targets))
    else:
        architectures = "all"
    separator = "=" * 64
    print(separator)
    print(f"Docker script started at {log_timestamp(started_at)}\nPID:           {os.getpid()}\nLog file:      {os.environ.get('OPENRIAK_DOCKER_LOG_FILE', 'stdout/stderr')}")
    print(f"Version:       {versions}")
    print(f"OS:            {os_selection}")
    print(f"Architecture:  {architectures}")
    print(f"Namespace:     {identity_from_options(options).namespace}")
    print(f"Vendor:        {identity_from_options(options).vendor}")
    print(f"Output:        {getattr(options, 'output', None) or 'docs cache'}")
    print(f"Docs updates:  {'disabled' if getattr(options, 'output', None) or getattr(options, 'do_not_test', False) else 'enabled'}")
    print(f"Timeout:       {options.timeout}s")
    print(f"Cluster nodes: {'from approved files' if getattr(options, 'do_not_test', False) else options.cluster_nodes}")
    print(separator, flush=True)


def label_text(value: str) -> str:
    if not value.strip() or any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise argparse.ArgumentTypeError("Label values must be nonempty, single-line text")
    return value


def label_url(value: str) -> str:
    label_text(value)
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or any(char.isspace() for char in value):
        raise argparse.ArgumentTypeError("Use an absolute HTTP or HTTPS URL")
    return value


def standalone_output(value: str) -> pathlib.Path:
    root = pathlib.Path(value).expanduser().resolve()
    protected = (CACHE_ROOT, MULTIARCH_CACHE_ROOT, STATIC_ROOT, METADATA_ROOT,
                 REPOSITORY_ROOT / "content", REPOSITORY_ROOT / "tools/generated", REPOSITORY_ROOT / ".git")
    for path in protected:
        path = path.resolve()
        if root.is_relative_to(path) or path.is_relative_to(root):
            raise DockerToolError(f"Standalone output must be separate from docs, generated metadata, and test caches: {root}")
    return root


def validate_output_targets(targets: list[Target]) -> None:
    return openriak_discovery.validate_output_targets(sys.modules[__name__], targets)



def identity_from_options(options: argparse.Namespace) -> ImageIdentity:
    defaults = ImageIdentity()
    return ImageIdentity(**{field.name: getattr(options, field.name, None) or getattr(defaults, field.name)
                            for field in dataclasses.fields(ImageIdentity)})


def render_group_assets(targets: list[Target], bases: dict[str, dict[str, str]], cookie: str,
                        tags: list[str], cluster_nodes: int, destination: pathlib.Path) -> None:
    return openriak_render.render_group_assets(sys.modules[__name__], targets, bases, cookie, tags, cluster_nodes, destination)



def generate_group(targets: list[Target], options: argparse.Namespace, all_targets: list[Target]) -> bool:
    with openriak_locks.activity(sys.modules[__name__]), openriak_locks.lock(sys.modules[__name__], targets[0].group_directory):
        return openriak_cache.generate_group(sys.modules[__name__], targets, options, all_targets)



class IndentedProgress:
    """Indent continuation output, including prints split across multiple writes."""
    def __init__(self, stream: Any, width: int):
        self.stream = stream
        self.indent = " " * width
        self.line_start = True

    def write(self, text: str) -> int:
        for part in text.splitlines(keepends=True):
            if self.line_start and part.strip("\r\n"):
                self.stream.write(self.indent)
            self.stream.write(part)
            self.line_start = part.endswith(("\n", "\r"))
        return len(text)

    def flush(self) -> None:
        self.stream.flush()

    def __getattr__(self, name: str) -> Any:
        return getattr(self.stream, name)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subcommands = result.add_subparsers(dest="command", required=True)

    matrix = subcommands.add_parser("matrix", help="List metadata-derived Docker targets without changing files")
    matrix.add_argument("--version", action="append", dest="versions")
    matrix.add_argument("--os-id", action="append", metavar="PATTERN", help="Match metadata OS IDs with case-sensitive wildcard patterns; repeat to match any pattern and quote patterns such as 'oracle*'")
    matrix.add_argument("--otp")
    matrix.add_argument("--download-id")
    matrix.add_argument("--json", action="store_true")

    refresh = subcommands.add_parser(
        "refresh", help="Manually pull, generate, build, test, cache, and publish selected targets"
    )
    selection = refresh.add_mutually_exclusive_group(required=True)
    selection.add_argument("--version", action="append", dest="versions")
    selection.add_argument("--all", action="store_true")
    refresh.add_argument("--os-id", action="append", metavar="PATTERN", help="Match metadata OS IDs with case-sensitive wildcard patterns; repeat to match any pattern and quote patterns such as 'oracle*'")
    refresh.add_argument("--otp")
    refresh.add_argument("--download-id")
    refresh.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="Seconds per operation or wait (default: 1800)")
    refresh.add_argument("--whatif", action="store_true", help="Show what would rebuild or skip and why, without Docker or file changes")
    refresh.add_argument("--cluster-nodes", type=int, default=DEFAULT_CLUSTER_NODES)
    regeneration = refresh.add_mutually_exclusive_group()
    regeneration.add_argument(
        "--force",
        action="store_true",
        help="Regenerate and retest even when a complete cached result exists",
    )
    regeneration.add_argument(
        "--retry-failed",
        action="store_true",
        help="Regenerate failed or incompatible targets while keeping passed caches",
    )
    regeneration.add_argument(
        "--do-not-test", action="store_true",
        help="Rebuild only approved cached files without regeneration or integration tests",
    )
    refresh.add_argument(
        "--extra-namespace", action="append", type=extra_namespace, default=[], metavar="NAMESPACE",
        help="Also apply every built tag under this namespace (repeatable); does not push images",
    )
    refresh.add_argument("--keep-test-workdir", action="store_true")
    refresh.add_argument(
        "--yes",
        action="store_true",
        help="Required with --all because the complete historical matrix is large",
    )

    generate = subcommands.add_parser("generate", help="Render standalone files without building, testing, or publishing docs")
    generation_selection = generate.add_mutually_exclusive_group(required=True)
    generation_selection.add_argument("--version", action="append", dest="versions")
    generation_selection.add_argument("--all", action="store_true")
    generate.add_argument("--os-id", action="append", metavar="PATTERN", help="Match metadata OS IDs with case-sensitive wildcard patterns; repeat to match any pattern and quote patterns such as 'oracle*'")
    generate.add_argument("--otp")
    generate.add_argument("--download-id")
    generate.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="Seconds per operation or wait (default: 1800)")
    generate.add_argument("--cluster-nodes", type=int, default=DEFAULT_CLUSTER_NODES)
    generate.add_argument("--force", action="store_true", help="Pull fresh base digests and regenerate, retaining previous output")
    generate.add_argument("--yes", action="store_true", help="Required with --all")
    generate.set_defaults(do_not_test=False)

    for command in (refresh, generate):
        for field in dataclasses.fields(LifecycleOptions):
            command.add_argument("--" + field.name.replace("_", "-"),
                                 type=int if field.name == "healthcheck_retries" else duration_seconds,
                                 help=f"Generated {field.name.replace('_', ' ')} (default: {field.default}{'' if field.name == 'healthcheck_retries' else 's'})")
        command.add_argument("--nohup", action="store_true", help="Run in the background and print the worker PID and timestamped log path")
        command.add_argument("--vendor", type=label_text, help='Image vendor label (default: "OpenRiak")')
        command.add_argument("--source", type=label_url, help="Image source label (default: https://github.com/OpenRiak/openriak-docs)")
        command.add_argument("--url", type=label_url, help="Image project URL label (default: https://openriak.org)")
        command.add_argument("--namespace", type=extra_namespace, help='Primary image namespace (default: "openriak")')
        command.add_argument("--output", "--output-dir", required=command is generate, metavar="PATH",
                             help="Separate output/cache root; automatically disables all docs publication")
        command.add_argument("--no-docs", action="store_true", help="Explicitly disable docs updates (requires --output for isolation)")

    subcommands.add_parser("sync-static", help="Republish previously passed cache entries without retesting")
    import openriak_push
    openriak_push.configure_parser(subcommands.add_parser("push", help="Push approved OCI images and save detailed Scout CVE reports"))
    import openriak_base
    openriak_base.configure_parser(subcommands.add_parser("base", help="Generate, build/test, or push the reusable patched Debian base"), sys.modules[__name__])
    import openriak_cleanup
    openriak_cleanup.configure_parser(subcommands.add_parser("cleanup", help="Preview or remove generator resources older than a supplied cutoff"))
    import openriak_distributed
    openriak_distributed.configure_parser(subcommands.add_parser("distribute", help="Plan, run and collect builds across machines"), sys.modules[__name__])
    import openriak_inspect
    openriak_inspect.configure_parsers(subcommands, sys.modules[__name__])
    return result


def main(arguments: list[str] | None = None) -> int:
    options = parser().parse_args(arguments)
    try:
        if options.command == "distribute":
            import openriak_distributed
            return openriak_distributed.main(options, sys.modules[__name__], sys.argv[1:] if arguments is None else arguments)
        if options.command in ("doctor", "status", "failures", "cve-diff"):
            import openriak_inspect
            return openriak_inspect.main(options, sys.modules[__name__])
        if options.command == "base":
            import openriak_base
            with openriak_locks.activity(sys.modules[__name__]):
                return openriak_base.main(options, sys.modules[__name__], sys.argv[1:] if arguments is None else arguments)
        if options.command == "push":
            import openriak_push
            with contextlib.nullcontext() if options.whatif else openriak_locks.activity(sys.modules[__name__]):
                return openriak_push.main(options, sys.modules[__name__])
        if options.command == "cleanup":
            import openriak_cleanup
            return openriak_cleanup.main(options, sys.modules[__name__])
        if options.command == "sync-static":
            with openriak_locks.activity(sys.modules[__name__], shared=False):
                print(f"Published {sync_static()} cached Docker target(s).")
            return 0

        versions = options.versions if getattr(options, "versions", None) else None
        targets = discover_targets(
            versions,
            os_id=getattr(options, "os_id", None),
            otp=getattr(options, "otp", None),
            download_id=getattr(options, "download_id", None),
        )
        if not targets:
            raise DockerToolError("No Docker targets matched the requested metadata filters")
        if options.command == "matrix":
            print_matrix(targets, options.json)
            return 0
        if options.all and not options.yes and not getattr(options, "whatif", False):
            raise DockerToolError(f"{options.command} --all requires --yes")
        if options.cluster_nodes < 2 or options.cluster_nodes > 253:
            raise DockerToolError("--cluster-nodes must be between 2 and 253")

        if options.timeout <= 0:
            raise DockerToolError("--timeout must be a positive number of seconds")

        if options.no_docs and not options.output:
            raise DockerToolError("--no-docs requires --output to keep standalone results outside the watched docs cache")
        if options.do_not_test and any(getattr(options, name) is not None for name in ("vendor", "source", "url")):
            raise DockerToolError("--do-not-test rebuilds approved labels unchanged; use generate or refresh to change --vendor/--source/--url")
        lifecycle_values = {}
        for field in dataclasses.fields(LifecycleOptions):
            value = getattr(options, field.name)
            if value is not None:
                if options.do_not_test:
                    raise DockerToolError("--do-not-test rebuilds approved files unchanged; lifecycle options require generate or refresh with tests")
                if value < (0 if field.name == "healthcheck_start_period" else 1):
                    raise DockerToolError(f"--{field.name.replace('_', '-')} must be {'nonnegative' if field.name == 'healthcheck_start_period' else 'positive'}")
                lifecycle_values[field.name] = value
        lifecycle_options = LifecycleOptions(**lifecycle_values)
        identity = identity_from_options(options)
        output_root = standalone_output(options.output) if options.output else None
        all_targets = [dataclasses.replace(t, identity=identity, output_root=output_root, lifecycle_options=lifecycle_options) for t in discover_targets()]
        selected_keys = {(t.version, t.family, t.release, t.otp) for t in targets}
        groups = grouped_targets([t for t in all_targets if (t.version, t.family, t.release, t.otp) in selected_keys])
        validate_output_targets([target for group in groups for target in group])
        if getattr(options, "whatif", False):
            import openriak_whatif
            return openriak_whatif.run(sys.modules[__name__], groups, options, all_targets)
        if options.do_not_test:
            approved_groups = []
            for group in groups:
                path = group[0].group_directory / "report.json"
                if path.is_file() and read_json(path).get("status") == "passed":
                    approved_groups.append(group)
                else:
                    print(f"{log_timestamp()} SKIPPED {group[0].image} (no passed group approval)", flush=True)
            groups = approved_groups
            if not groups:
                raise DockerToolError("No passed groups selected for --do-not-test")
            print("Rebuilding approved cached files; integration tests will not run.", flush=True)
        if options.nohup:
            import openriak_background
            return openriak_background.launch(sys.modules[__name__], options, sys.argv[1:] if arguments is None else arguments)
        print_refresh_header(options, [target for group in groups for target in group])
        failures = 0
        matrix_started = time.monotonic()
        counter_width = len(str(len(groups)))
        with MultiarchBuilderLifecycle() as builder_lifecycle:
            for index, group in enumerate(groups, start=1):
                prefix = f"[{index:0{counter_width}d}/{len(groups)}] "
                print(f"{prefix}{log_timestamp()} {group[0].image} ({', '.join(t.platform for t in group)})", flush=True)
                group_started = time.monotonic()
                with contextlib.redirect_stdout(IndentedProgress(sys.stdout, len(prefix))):
                    try:
                        if options.command == "generate":
                            passed = generate_group(group, options, all_targets)
                        elif options.do_not_test:
                            passed = rebuild_approved_group(group, options, builder_lifecycle)
                        else:
                            passed = refresh_group(group, options, all_targets, builder_lifecycle)
                    except (DockerToolError, minimal.ConfigurationError, OSError, ValueError) as error:
                        print(f"{log_timestamp()} FAILED {group[0].image}: {error}", flush=True)
                        passed = False
                    failures += int(not passed)
                    duration = round(time.monotonic() - group_started)
                    success = ("GENERATED (not tested)" if options.command == "generate" else
                               "BUILT (not retested)" if options.do_not_test else "PASSED")
                    outcome = success if passed else "FAILED"
                    print(f"{log_timestamp()} {outcome} {group[0].image} (duration {duration}s)", flush=True)
        if options.command == "refresh" and not options.do_not_test and output_root is None:
            sync_download_metadata((t.version for t in targets), timeout_seconds=options.timeout)
        print(f"{log_timestamp()} Finished {len(groups)} groups: {failures} failed (duration {round(time.monotonic() - matrix_started)}s)", flush=True)
        return 1 if failures else 0
    except KeyboardInterrupt:
        remote_controller = options.command == "distribute" and options.distributed_command in ("run", "start", "stop", "restart", "monitor", "fetch")
        message = ("Distributed controller stopped; worker builds continue. Deployment state was retained for reconnection." if remote_controller else
                   "Push/scan stopped by operator; any created reports were retained." if options.command == "push" else
                   "Generation stopped by operator; its run record was retained." if options.command == "generate" else
                   "Rebuild stopped by operator; its build record was retained." if getattr(options, "do_not_test", False)
                   else "Refresh stopped by operator; current test cleanup completed.")
        print(message, file=sys.stderr)
        return 130
    except (DockerToolError, minimal.ConfigurationError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    def stop_refresh(signum: int, frame: Any) -> None:
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop_refresh)
    raise SystemExit(main())
