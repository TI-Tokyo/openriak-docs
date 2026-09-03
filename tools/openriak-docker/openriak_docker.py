#!/usr/bin/env python3
"""Generate, test, cache, and publish OpenRiak KV Docker configurations."""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Iterable


SCHEMA_VERSION = 1
MINIMUM_OPENRIAK_VERSION = (3, 4, 0)
REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[2]
METADATA_ROOT = REPOSITORY_ROOT / "content" / "openriak-kv" / "metadata"
CACHE_ROOT = REPOSITORY_ROOT / "tools" / "cache" / "openriak-docker"
STATIC_ROOT = REPOSITORY_ROOT / "content" / "static" / "openriak-kv" / "downloads" / "docker"

ARCHITECTURE_PLATFORMS = {
    "x86_64": "linux/amd64",
    "amd64": "linux/amd64",
    "aarch64": "linux/arm64",
    "arm64": "linux/arm64",
    "armhf": "linux/arm/v7",
}

UBUNTU_RELEASES = {
    "lucid": "lucid",
    "precise": "precise",
    "trusty": "trusty",
    "xenial": "xenial",
    "artful": "artful",
    "bionic": "bionic",
    "focal": "focal",
    "jammy": "jammy",
    "noble": "noble",
}

DEBIAN_CODENAMES = {
    "6": "squeeze",
    "7": "wheezy",
    "8": "jessie",
    "9": "stretch",
    "10": "buster",
    "11": "bullseye",
    "12": "bookworm",
}


class DockerToolError(RuntimeError):
    """An expected target, Docker, or test failure."""


@dataclasses.dataclass(frozen=True)
class Target:
    version: str
    operating_system: dict[str, Any]
    download_id: str
    package: dict[str, Any]

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
            [self.version, self.family, self.release, f"otp{self.otp}", self.architecture]
        ).lower()

    @property
    def image(self) -> str:
        return f"openriak/openriak-kv:{self.image_tag}"

    @property
    def node_name(self) -> str:
        return f"openriak-kv-{self.image_tag}-node"

    @property
    def cache_directory(self) -> pathlib.Path:
        return CACHE_ROOT / self.version / self.os_id / self.download_id

    @property
    def static_directory(self) -> pathlib.Path:
        return STATIC_ROOT / self.version / self.image_tag


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def isoformat(value: dt.datetime | None = None) -> str:
    return (value or utc_now()).isoformat(timespec="seconds").replace("+00:00", "Z")


def run_id(value: dt.datetime | None = None) -> str:
    return (value or utc_now()).strftime("%Y%m%dT%H%M%S.%fZ")


def read_json(path: pathlib.Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: pathlib.Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(f"{path.suffix}.tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


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
    return sorted(
        [
            entry.name
            for entry in METADATA_ROOT.iterdir()
            if entry.is_dir()
            and re.fullmatch(r"\d+\.\d+\.\d+", entry.name)
            and semver_key(entry.name) >= MINIMUM_OPENRIAK_VERSION
        ],
        key=semver_key,
    )


def targets_for_version(version: str) -> list[Target]:
    if semver_key(version) < MINIMUM_OPENRIAK_VERSION:
        raise DockerToolError(
            f"OpenRiak KV Docker targets start at 3.4.0; unsupported version: {version}"
        )
    root = METADATA_ROOT / version
    supported_path = root / "supported-os.json"
    downloads_path = root / "downloads.json"
    if not supported_path.is_file() or not downloads_path.is_file():
        return []
    supported = read_json(supported_path)
    downloads = read_json(downloads_path)
    if supported.get("product") != "kv" or downloads.get("product") != "kv":
        raise DockerToolError(f"Mismatched product metadata for OpenRiak KV {version}")
    if supported.get("version") != version or downloads.get("version") != version:
        raise DockerToolError(f"Mismatched version metadata for OpenRiak KV {version}")
    if supported.get("status") != "complete" or downloads.get("status") != "complete":
        return []

    targets: list[Target] = []
    for operating_system in supported.get("operating_systems", []):
        os_id = operating_system["id"]
        for download_id, package in downloads.get("downloads", {}).get(os_id, {}).items():
            checksum = package.get("checksum", {})
            if checksum.get("algorithm") != "sha256" or not re.fullmatch(
                r"[0-9a-f]{64}", str(checksum.get("value", ""))
            ):
                raise DockerToolError(f"Invalid package checksum for {version}/{os_id}/{download_id}")
            targets.append(Target(version, operating_system, download_id, package))
    grouped: dict[str, list[Target]] = {}
    for target in targets:
        grouped.setdefault(target.image, []).append(target)

    unique: list[Target] = []
    for candidates in grouped.values():
        source_path = str(candidates[0].operating_system.get("source", {}).get("path", ""))

        def preference(candidate: Target) -> tuple[Any, ...]:
            package_path = urllib.parse.unquote(urllib.parse.urlparse(candidate.package["url"]).path)
            return (
                int(bool(source_path) and package_path.startswith(source_path)),
                natural_key(candidate.package.get("package_revision")),
                natural_key(candidate.download_id),
            )

        unique.append(max(candidates, key=preference))
    return sorted(unique, key=lambda item: (item.os_id, natural_key(item.otp), item.download_id))


def discover_targets(
    versions: Iterable[str] | None = None,
    os_id: str | None = None,
    otp: str | None = None,
    download_id: str | None = None,
) -> list[Target]:
    selected_versions = list(versions) if versions is not None else metadata_versions()
    targets = [target for version in selected_versions for target in targets_for_version(version)]
    if os_id:
        targets = [target for target in targets if target.os_id == os_id]
    if otp:
        targets = [target for target in targets if target.otp == str(otp)]
    if download_id:
        targets = [target for target in targets if target.download_id == download_id]
    return targets


def base_image_for(target: Target) -> str:
    family = target.family
    release = target.release
    architecture = target.architecture
    if family == "alpine":
        return f"alpine:{release}"
    if family == "amazon-linux":
        return f"amazonlinux:{release}"
    if family == "debian":
        return f"debian:{DEBIAN_CODENAMES.get(release, release)}-slim"
    if family == "fedora":
        return f"fedora:{release}"
    if family == "oracle-linux":
        return f"oraclelinux:{release}-slim"
    if family == "raspbian":
        repository = "arm32v7/debian" if architecture == "armhf" else "arm64v8/debian"
        return f"{repository}:{DEBIAN_CODENAMES.get(release, release)}-slim"
    if family == "rhel":
        return f"registry.access.redhat.com/ubi{release}/ubi:{release}"
    if family == "sles":
        return f"registry.suse.com/suse/sles{release}:{release}"
    if family == "ubuntu":
        return f"ubuntu:{UBUNTU_RELEASES.get(release, release)}"
    raise DockerToolError(f"No base-image mapping for OS family: {family}")


def package_install_script(target: Target) -> str:
    filename = target.package["filename"]
    if not re.fullmatch(r"[A-Za-z0-9_.+-]+", filename):
        raise DockerToolError(f"Unsafe package filename in metadata: {filename}")
    package_path = f"/tmp/{filename}"
    package_family = target.operating_system["package_family"]
    if package_family == "apk":
        return f"""apk add --no-cache bash ca-certificates curl su-exec
apk add --no-cache --allow-untrusted {package_path}
rm -f {package_path}"""
    if package_family == "deb":
        return f"""apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates curl passwd procps {package_path}
rm -rf /var/lib/apt/lists/*
rm -f {package_path}"""
    if package_family == "rpm":
        return f"""if command -v dnf >/dev/null 2>&1
then
    dnf install -y ca-certificates curl procps-ng shadow-utils {package_path}
    dnf clean all
elif command -v microdnf >/dev/null 2>&1
then
    microdnf install -y ca-certificates curl procps-ng shadow-utils {package_path}
    microdnf clean all
elif command -v yum >/dev/null 2>&1
then
    yum install -y ca-certificates curl procps-ng shadow-utils {package_path}
    yum clean all
elif command -v zypper >/dev/null 2>&1
then
    zypper --non-interactive install -y ca-certificates curl procps {package_path}
    zypper clean --all
else
    echo 'No supported RPM package manager found' >&2
    exit 1
fi
rm -f {package_path}"""
    raise DockerToolError(f"Unsupported package family: {package_family}")


def create_riak_user_script(target: Target) -> str:
    if target.operating_system["package_family"] == "apk":
        return """if ! getent group riak >/dev/null 2>&1
then
    addgroup -S riak
fi
if ! id riak >/dev/null 2>&1
then
    adduser -S -D -H -h /var/lib/riak -s /sbin/nologin -G riak riak
fi"""
    return """if ! getent group riak >/dev/null 2>&1
then
    groupadd --system riak
fi
if ! id riak >/dev/null 2>&1
then
    useradd --system --gid riak --home-dir /var/lib/riak --shell /sbin/nologin riak
fi"""


ENTRYPOINT_SCRIPT = """#!/bin/sh
set -eu

config_dir=/etc/riak
data_dir=/var/lib/riak
log_dir=/var/log/riak
defaults_dir=/opt/openriak-defaults/etc-riak

mkdir -p "$config_dir" "$data_dir" "$log_dir" /run/riak
if [ ! -s "$config_dir/riak.conf" ]
then
    cp -a "$defaults_dir/." "$config_dir/"
fi

set_setting() {
    key=$1
    value=$2
    escaped_key=$(printf '%s' "$key" | sed 's/[.[\\*^$()+?{|]/\\\\&/g')
    if grep -Eq "^[[:space:]]*${escaped_key}[[:space:]]*=" "$config_dir/riak.conf"
    then
        sed -i -E "s|^[[:space:]]*${escaped_key}[[:space:]]*=.*$|${key} = ${value}|" "$config_dir/riak.conf"
    else
        printf '\n%s = %s\n' "$key" "$value" >> "$config_dir/riak.conf"
    fi
}

node_host=${RIAK_NODE_HOST:-$(hostname)}
set_setting nodename "${RIAK_NODE_NAME:-riak@$node_host}"
set_setting ring_size "$RIAK_RING_SIZE"
set_setting storage_backend "$RIAK_STORAGE_BACKEND"
set_setting anti_entropy "$RIAK_ANTI_ENTROPY"
set_setting tictacaae_active "$RIAK_TICTACAAE_ACTIVE"
set_setting tictacaae_storeheads "$RIAK_TICTACAAE_STOREHEADS"
set_setting listener.http.internal "$RIAK_HTTP_LISTENER"
set_setting listener.protobuf.internal "$RIAK_PB_LISTENER"

chown -R riak:riak "$config_dir" "$data_dir" "$log_dir" /run/riak
if [ "${RIAK_INIT_ONLY:-0}" = "1" ]
then
    exit 0
fi

ulimit -n "${RIAK_NOFILE_LIMIT:-100000}"
if command -v su-exec >/dev/null 2>&1
then
    exec su-exec riak /usr/sbin/riak console
fi
if command -v runuser >/dev/null 2>&1
then
    exec runuser -u riak -- /usr/sbin/riak console
fi
exec su -s /bin/sh riak -c 'exec /usr/sbin/riak console'
"""


def render_dockerfile(target: Target, pinned_base_image: str) -> str:
    checksum = target.package["checksum"]["value"]
    filename = target.package["filename"]
    package_url = target.package["url"]
    return f"""# syntax=docker/dockerfile:1.7
# Generated and tested by tools/openriak-docker/openriak-docker. Do not edit by hand.
FROM --platform={target.platform} {pinned_base_image}

# -----------------------------------------------------------------------------
# OpenRiak KV default settings
# Override any value with `docker run --env NAME=value` or Compose `environment`.
# -----------------------------------------------------------------------------
ENV RIAK_NODE_HOST=""
ENV RIAK_NODE_NAME=""
ENV RIAK_RING_SIZE="8"
ENV RIAK_STORAGE_BACKEND="leveled"
ENV RIAK_ANTI_ENTROPY="passive"
ENV RIAK_TICTACAAE_ACTIVE="active"
ENV RIAK_TICTACAAE_STOREHEADS="enabled"
ENV RIAK_HTTP_LISTENER="0.0.0.0:8098"
ENV RIAK_PB_LISTENER="0.0.0.0:8087"
ENV RIAK_NOFILE_LIMIT="100000"
ENV RIAK_INIT_ONLY="0"

ADD --checksum=sha256:{checksum} {package_url} /tmp/{filename}
RUN <<'OPENRIAK_PACKAGE_INSTALL'
set -eu
{package_install_script(target)}
OPENRIAK_PACKAGE_INSTALL

RUN <<'OPENRIAK_IMAGE_SETUP'
set -eu
{create_riak_user_script(target)}
test -x /usr/sbin/riak
id riak
mkdir -p /opt/openriak-defaults/etc-riak /var/lib/riak /var/log/riak /run/riak
cp -a /etc/riak/. /opt/openriak-defaults/etc-riak/
chown -R riak:riak /var/lib/riak /var/log/riak /run/riak
OPENRIAK_IMAGE_SETUP

COPY <<'OPENRIAK_ENTRYPOINT' /usr/local/bin/openriak-entrypoint
{ENTRYPOINT_SCRIPT.rstrip()}
OPENRIAK_ENTRYPOINT

RUN chmod 0755 /usr/local/bin/openriak-entrypoint

VOLUME ["/etc/riak"]
VOLUME ["/var/lib/riak"]
VOLUME ["/var/log/riak"]
EXPOSE 8087
EXPOSE 8098
ENTRYPOINT ["/usr/local/bin/openriak-entrypoint"]
"""


def render_compose(target: Target) -> str:
    node = target.node_name
    return f"""# Generated and tested by tools/openriak-docker/openriak-docker. Do not edit by hand.
name: {node}

services:
  node:
    build:
      context: .
      dockerfile: Dockerfile
    image: {target.image}
    container_name: "${{OPENRIAK_CONTAINER_NAME:-{node}}}"
    hostname: {node}
    environment:
      RIAK_NODE_NAME: "${{OPENRIAK_NODE_NAME:-riak@{node}}}"
    ports:
      - "${{OPENRIAK_PB_PORT:-8087}}:8087"
      - "${{OPENRIAK_HTTP_PORT:-8098}}:8098"
    volumes:
      - "./{node}/config:/etc/riak"
      - "./{node}/data:/var/lib/riak"
      - "./{node}/logs:/var/log/riak"
    ulimits:
      nofile:
        soft: 100000
        hard: 100000
    stop_grace_period: 2m
"""


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
) -> subprocess.CompletedProcess[str]:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    started = isoformat()
    result = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    with log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(f"$ {' '.join(command)}\n")
        handle.write(f"started: {started}\nexit_code: {result.returncode}\n")
        handle.write(result.stdout)
        if result.stdout and not result.stdout.endswith("\n"):
            handle.write("\n")
    if check and result.returncode != 0:
        raise DockerToolError(
            f"Command failed with exit code {result.returncode}: {' '.join(command)} (see {log_path})"
        )
    return result


def resolve_base_image(target: Target, logs: pathlib.Path) -> tuple[str, str]:
    docker = docker_command()
    base = base_image_for(target)
    run_logged([docker, "pull", "--platform", target.platform, base], logs / "base-image-pull.log")
    result = run_logged(
        [docker, "image", "inspect", "--format", "{{json .RepoDigests}}", base],
        logs / "base-image-inspect.log",
    )
    try:
        repo_digests = json.loads(result.stdout.strip())
    except json.JSONDecodeError as error:
        raise DockerToolError(f"Docker returned invalid RepoDigests for {base}") from error
    if not repo_digests:
        raise DockerToolError(f"Docker did not return a digest for {base}")
    digest_reference = str(repo_digests[0])
    digest = digest_reference.rsplit("@", 1)[-1]
    repository = base.rsplit(":", 1)[0]
    return base, f"{base}@{digest}" if "@" not in base else f"{repository}@{digest}"


def set_riak_setting(source: str, key: str, value: str) -> str:
    active = re.compile(rf"^[ \t]*{re.escape(key)}[ \t]*=.*$", re.MULTILINE)
    replacement = f"{key} = {value}"
    if active.search(source):
        return active.sub(replacement, source, count=1)
    commented = re.compile(rf"^[ \t]*#+[ \t]*{re.escape(key)}[ \t]*=.*$", re.MULTILINE)
    if commented.search(source):
        return commented.sub(replacement, source, count=1)
    suffix = "" if source.endswith("\n") else "\n"
    return f"{source}{suffix}{replacement}\n"


def configure_test_node(config_path: pathlib.Path, node_name: str) -> None:
    source = config_path.read_text(encoding="utf-8")
    settings = {
        "nodename": f"riak@{node_name}",
        "ring_size": "8",
        "storage_backend": "leveled",
        "anti_entropy": "passive",
        "tictacaae_active": "active",
        "tictacaae_storeheads": "enabled",
        "listener.http.internal": "0.0.0.0:8098",
        "listener.protobuf.internal": "0.0.0.0:8087",
    }
    for key, value in settings.items():
        source = set_riak_setting(source, key, value)
    config_path.write_text(source, encoding="utf-8", newline="\n")


def effective_riak_settings(config_path: pathlib.Path, keys: Iterable[str]) -> dict[str, str]:
    wanted = set(keys)
    values: dict[str, str] = {}
    for line in config_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^[ \t]*([A-Za-z0-9_.]+)[ \t]*=[ \t]*(.*?)[ \t]*$", line)
        if match and match.group(1) in wanted:
            values[match.group(1)] = match.group(2)
    return values


def populated(path: pathlib.Path) -> bool:
    return path.is_dir() and any(path.iterdir())


def free_tcp_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as handle:
        handle.bind(("127.0.0.1", 0))
        return int(handle.getsockname()[1])


def wait_for_node(
    container_name: str,
    http_port: int,
    timeout_seconds: int,
    logs: pathlib.Path,
) -> tuple[str, str]:
    docker = docker_command()
    deadline = time.monotonic() + timeout_seconds
    last_cli = ""
    last_http = ""
    with (logs / "readiness.log").open("w", encoding="utf-8", newline="\n") as log:
        while time.monotonic() < deadline:
            cli = subprocess.run(
                [docker, "exec", container_name, "riak", "ping"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            last_cli = cli.stdout.strip()
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{http_port}/ping", timeout=3) as response:
                    last_http = response.read().decode("utf-8", errors="replace").strip()
                    http_ok = response.status == 200 and last_http == "OK"
            except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
                last_http = str(error)
                http_ok = False
            log.write(
                f"{isoformat()} cli_exit={cli.returncode} cli={last_cli!r} http={last_http!r}\n"
            )
            log.flush()
            if cli.returncode == 0 and last_cli == "pong" and http_ok:
                return last_cli, last_http
            time.sleep(2)
    raise DockerToolError(
        f"OpenRiak node was not ready after {timeout_seconds}s; CLI={last_cli!r}, HTTP={last_http!r}"
    )


def record_step(report: dict[str, Any], name: str, action: Any) -> Any:
    started = time.monotonic()
    item: dict[str, Any] = {"name": name, "status": "running", "started_at": isoformat()}
    report["steps"].append(item)
    try:
        result = action()
    except Exception as error:
        item.update(
            status="failed",
            finished_at=isoformat(),
            duration_seconds=round(time.monotonic() - started, 3),
            error=str(error),
        )
        raise
    item.update(
        status="passed",
        finished_at=isoformat(),
        duration_seconds=round(time.monotonic() - started, 3),
    )
    return result


def artifact_downloads(target: Target, dockerfile: pathlib.Path, compose: pathlib.Path) -> dict[str, Any]:
    base_url = f"downloads/docker/{target.version}/{target.image_tag}"
    return {
        "dockerfile": {
            "filename": "Dockerfile",
            "url": f"{base_url}/Dockerfile",
            "sha256": sha256_file(dockerfile),
        },
        "compose": {
            "filename": "compose.yaml",
            "url": f"{base_url}/compose.yaml",
            "sha256": sha256_file(compose),
        },
    }


def publish_current_run(target: Target, run_root: pathlib.Path, report: dict[str, Any]) -> None:
    current = target.cache_directory
    current.mkdir(parents=True, exist_ok=True)
    for filename in ("Dockerfile", "compose.yaml"):
        source = run_root / filename
        if source.is_file():
            shutil.copy2(source, current / filename)
    write_json(run_root / "report.json", report)
    write_json(current / "report.json", report)

    if report["status"] == "passed":
        target.static_directory.mkdir(parents=True, exist_ok=True)
        shutil.copy2(run_root / "Dockerfile", target.static_directory / "Dockerfile")
        shutil.copy2(run_root / "compose.yaml", target.static_directory / "compose.yaml")
    elif target.static_directory.exists():
        for filename in ("Dockerfile", "compose.yaml"):
            with contextlib.suppress(FileNotFoundError):
                (target.static_directory / filename).unlink()


def initial_report(target: Target, identifier: str) -> dict[str, Any]:
    package = target.package
    return {
        "schema_version": SCHEMA_VERSION,
        "product": "openriak-kv",
        "status": "running",
        "run_id": identifier,
        "started_at": isoformat(),
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
        },
        "package": {
            "filename": package["filename"],
            "format": package["format"],
            "url": package["url"],
            "checksum": package["checksum"],
        },
        "image": target.image,
        "node": target.node_name,
        "metadata_sources": [
            f"content/openriak-kv/metadata/{target.version}/supported-os.json",
            f"content/openriak-kv/metadata/{target.version}/downloads.json",
        ],
        "base_image": None,
        "volumes": {
            "config": {"container": "/etc/riak", "default": f"./{target.node_name}/config"},
            "data": {"container": "/var/lib/riak", "default": f"./{target.node_name}/data"},
            "logs": {"container": "/var/log/riak", "default": f"./{target.node_name}/logs"},
        },
        "ports": {"protobuf": 8087, "http": 8098},
        "steps": [],
        "tests": {},
        "artifacts": {},
        "error": None,
    }


def refresh_target(target: Target, timeout_seconds: int, keep_workdir: bool = False) -> bool:
    identifier = run_id()
    run_root = target.cache_directory / "runs" / identifier
    logs = run_root / "logs"
    run_root.mkdir(parents=True, exist_ok=False)
    report = initial_report(target, identifier)
    dockerfile = run_root / "Dockerfile"
    compose = run_root / "compose.yaml"
    test_directory: pathlib.Path | None = None
    compose_started = False
    environment = os.environ.copy()
    docker = docker_command()

    try:
        base, pinned_base = record_step(
            report, "pull_and_pin_base_image", lambda: resolve_base_image(target, logs)
        )
        report["base_image"] = {
            "requested": base,
            "pinned": pinned_base,
            "resolved_at": isoformat(),
        }

        def generate() -> None:
            dockerfile.write_text(
                render_dockerfile(target, pinned_base),
                encoding="utf-8",
                newline="\n",
            )
            compose.write_text(
                render_compose(target),
                encoding="utf-8",
                newline="\n",
            )

        record_step(report, "generate_artifacts", generate)
        record_step(
            report,
            "build_image",
            lambda: run_logged(
                [
                    docker,
                    "build",
                    "--platform",
                    target.platform,
                    "--pull=false",
                    "--tag",
                    target.image,
                    "--file",
                    str(dockerfile),
                    str(run_root),
                ],
                logs / "image-build.log",
            ),
        )

        test_directory = pathlib.Path(tempfile.mkdtemp(prefix=f"openriak-docker-{target.image_tag}-"))
        shutil.copy2(compose, test_directory / "compose.yaml")
        shutil.copy2(dockerfile, test_directory / "Dockerfile")
        node_directory = test_directory / target.node_name
        test_suffix = identifier[-8:].lower().replace(".", "")
        test_container_name = f"{target.node_name}-t-{test_suffix}"
        environment.update(
            OPENRIAK_CONTAINER_NAME=test_container_name,
            OPENRIAK_PB_PORT=str(free_tcp_port()),
            OPENRIAK_HTTP_PORT=str(free_tcp_port()),
        )
        compose_command = [
            docker,
            "compose",
            "--project-directory",
            str(test_directory),
            "--file",
            str(test_directory / "compose.yaml"),
        ]

        existing = run_logged(
            [docker, "container", "inspect", test_container_name],
            logs / "container-name-check.log",
            check=False,
        )
        if existing.returncode == 0:
            raise DockerToolError(
                f"Container name {test_container_name} is already in use; refusing to remove it"
            )

        record_step(
            report,
            "initialize_volumes",
            lambda: run_logged(
                compose_command + ["run", "--rm", "-e", "RIAK_INIT_ONLY=1", "node"],
                logs / "compose-init.log",
                cwd=test_directory,
                environment=environment,
            ),
        )
        config_directory = node_directory / "config"
        data_directory = node_directory / "data"
        log_directory = node_directory / "logs"
        if not populated(config_directory) or not data_directory.is_dir() or not log_directory.is_dir():
            raise DockerToolError("Compose initialization did not create config, data, and logs directories")
        report["tests"]["volume_initialization"] = {
            "status": "passed",
            "config_populated": True,
            "data_directory_created": True,
            "logs_directory_created": True,
        }

        config_path = config_directory / "riak.conf"
        record_step(
            report,
            "configure_node",
            lambda: configure_test_node(config_path, target.node_name),
        )
        expected_settings = {
            "nodename": f"riak@{target.node_name}",
            "ring_size": "8",
            "storage_backend": "leveled",
            "anti_entropy": "passive",
            "tictacaae_active": "active",
            "tictacaae_storeheads": "enabled",
            "listener.http.internal": "0.0.0.0:8098",
            "listener.protobuf.internal": "0.0.0.0:8087",
        }
        actual_settings = effective_riak_settings(config_path, expected_settings)
        if actual_settings != expected_settings:
            raise DockerToolError(
                f"Generated riak.conf does not contain the requested settings: {actual_settings!r}"
            )
        report["tests"]["configuration"] = {
            "status": "passed",
            "settings": actual_settings,
        }

        record_step(
            report,
            "start_compose_node",
            lambda: run_logged(
                compose_command + ["up", "--detach", "--no-build"],
                logs / "compose-up.log",
                cwd=test_directory,
                environment=environment,
            ),
        )
        compose_started = True
        cli_response, http_response = record_step(
            report,
            "wait_for_cli_and_http",
            lambda: wait_for_node(
                test_container_name,
                int(environment["OPENRIAK_HTTP_PORT"]),
                timeout_seconds,
                logs,
            ),
        )
        report["tests"]["riak_start"] = {"status": "passed"}
        report["tests"]["cli_ping"] = {
            "status": "passed",
            "command": "riak ping",
            "response": cli_response,
        }
        report["tests"]["http_ping"] = {
            "status": "passed",
            "request": "GET /ping",
            "status_code": 200,
            "response": http_response,
        }
        if not populated(data_directory) or not populated(log_directory):
            raise DockerToolError("OpenRiak startup did not populate both data and log volumes")
        report["tests"]["populated_volumes"] = {
            "status": "passed",
            "config": sorted(path.name for path in config_directory.iterdir()),
            "data": sorted(path.name for path in data_directory.iterdir()),
            "logs": sorted(path.name for path in log_directory.iterdir()),
        }
        report["artifacts"] = artifact_downloads(target, dockerfile, compose)
        report["status"] = "passed"
    except Exception as error:
        report["status"] = "failed"
        report["error"] = {"type": type(error).__name__, "message": str(error)}
    finally:
        if test_directory is not None:
            compose_command = [
                docker,
                "compose",
                "--project-directory",
                str(test_directory),
                "--file",
                str(test_directory / "compose.yaml"),
            ]
            if compose_started:
                run_logged(
                    compose_command + ["logs", "--no-color"],
                    logs / "compose-runtime.log",
                    cwd=test_directory,
                    environment=environment,
                    check=False,
                )
                run_logged(
                    compose_command + ["down", "--remove-orphans"],
                    logs / "compose-down.log",
                    cwd=test_directory,
                    environment=environment,
                    check=False,
                )
            if keep_workdir:
                report["test_workdir"] = str(test_directory)
            else:
                shutil.rmtree(test_directory, ignore_errors=True)
        report["finished_at"] = isoformat()
        publish_current_run(target, run_root, report)
    return report["status"] == "passed"


def cached_current_reports() -> Iterable[tuple[pathlib.Path, dict[str, Any]]]:
    if not CACHE_ROOT.exists():
        return []
    reports: list[tuple[pathlib.Path, dict[str, Any]]] = []
    for path in CACHE_ROOT.glob("*/*/*/report.json"):
        try:
            reports.append((path, read_json(path)))
        except (OSError, json.JSONDecodeError):
            continue
    return reports


def sync_static() -> int:
    copied = 0
    for report_path, report in cached_current_reports():
        if report.get("schema_version") != SCHEMA_VERSION or report.get("status") != "passed":
            continue
        target_data = report["target"]
        matches = discover_targets(
            [target_data["version"]],
            os_id=target_data["os_id"],
            download_id=target_data["download_id"],
        )
        if len(matches) != 1:
            raise DockerToolError(f"Cached report no longer matches metadata: {report_path}")
        target = matches[0]
        destination = target.static_directory
        destination.mkdir(parents=True, exist_ok=True)
        for filename in ("Dockerfile", "compose.yaml"):
            source = report_path.parent / filename
            if not source.is_file():
                raise DockerToolError(f"Cached report is missing {source}")
            shutil.copy2(source, destination / filename)
        copied += 1
    return copied


def print_matrix(targets: list[Target], as_json: bool) -> None:
    records = [
        {
            "version": target.version,
            "os_id": target.os_id,
            "otp": target.otp,
            "architecture": target.architecture,
            "download_id": target.download_id,
            "image": target.image,
            "base_image": base_image_for(target),
            "cached": (target.cache_directory / "report.json").is_file(),
        }
        for target in targets
    ]
    if as_json:
        print(json.dumps(records, indent=2))
        return
    for record in records:
        marker = "cached" if record["cached"] else "not cached"
        print(
            f"{record['version']} {record['os_id']} OTP {record['otp']} "
            f"{record['architecture']} ({record['download_id']}; {marker})"
        )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subcommands = result.add_subparsers(dest="command", required=True)

    matrix = subcommands.add_parser("matrix", help="List metadata-derived Docker targets without changing files")
    matrix.add_argument("--version", action="append", dest="versions")
    matrix.add_argument("--os-id")
    matrix.add_argument("--otp")
    matrix.add_argument("--download-id")
    matrix.add_argument("--json", action="store_true")

    refresh = subcommands.add_parser(
        "refresh", help="Manually pull, generate, build, test, cache, and publish selected targets"
    )
    selection = refresh.add_mutually_exclusive_group(required=True)
    selection.add_argument("--version", action="append", dest="versions")
    selection.add_argument("--all", action="store_true")
    refresh.add_argument("--os-id")
    refresh.add_argument("--otp")
    refresh.add_argument("--download-id")
    refresh.add_argument("--timeout", type=int, default=180)
    refresh.add_argument("--keep-test-workdir", action="store_true")
    refresh.add_argument(
        "--yes",
        action="store_true",
        help="Required with --all because the complete historical matrix is large",
    )

    subcommands.add_parser("sync-static", help="Republish previously passed cache entries without retesting")
    return result


def main(arguments: list[str] | None = None) -> int:
    options = parser().parse_args(arguments)
    try:
        if options.command == "sync-static":
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
        if options.all and not options.yes:
            raise DockerToolError("refresh --all requires --yes")

        failures = 0
        for index, target in enumerate(targets, start=1):
            print(f"[{index}/{len(targets)}] Refreshing {target.image}", flush=True)
            passed = refresh_target(target, options.timeout, options.keep_test_workdir)
            print(f"[{index}/{len(targets)}] {'PASSED' if passed else 'FAILED'} {target.image}", flush=True)
            failures += int(not passed)
        return 1 if failures else 0
    except (DockerToolError, OSError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
