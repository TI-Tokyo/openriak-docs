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
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.parse
from typing import Any, Iterable


SCHEMA_VERSION = 3
MINIMUM_OPENRIAK_VERSION = (3, 4, 0)
REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[2]
METADATA_ROOT = REPOSITORY_ROOT / "content" / "openriak-kv" / "metadata"
CACHE_ROOT = REPOSITORY_ROOT / "tools" / "cache" / "openriak-docker"
STATIC_ROOT = REPOSITORY_ROOT / "content" / "static" / "openriak-kv" / "downloads" / "docker"
DEFAULT_CLUSTER_NODES = 5
CONTROL_DIRECTORY = "/var/lib/openriak-cluster-control"
ARTIFACT_FILENAMES = (
    "Dockerfile",
    "compose.single.yaml",
    "compose.cluster.yaml",
    ".env.example",
)

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
control_dir=${OPENRIAK_CLUSTER_CONTROL_DIR:-/var/lib/openriak-cluster-control}

log() {
    printf '%s [openriak-entrypoint] %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$*"
}

one_line() {
    tr '\n' ' ' | sed 's/[[:space:]][[:space:]]*/ /g; s/[[:space:]]$//'
}

riak_command() {
    if command -v su-exec >/dev/null 2>&1
    then
        su-exec riak /usr/sbin/riak "$@"
        return
    fi
    if command -v runuser >/dev/null 2>&1
    then
        runuser -u riak -- /usr/sbin/riak "$@"
        return
    fi
    su -s /bin/sh riak -c "/usr/sbin/riak $*"
}

riak_admin_command() {
    admin_vmargs=
    for admin_vmargs_candidate in "$data_dir"/generated.conf/vm.*.args
    do
        [ -r "$admin_vmargs_candidate" ] || continue
        admin_vmargs=$admin_vmargs_candidate
    done
    if [ -z "$admin_vmargs" ]
    then
        log "cluster: generated VM arguments are not available for riak-admin"
        return 1
    fi
    if command -v su-exec >/dev/null 2>&1
    then
        VMARGS_PATH="$admin_vmargs" su-exec riak /usr/lib/riak/bin/riak-admin "$@"
        return
    fi
    if command -v runuser >/dev/null 2>&1
    then
        VMARGS_PATH="$admin_vmargs" runuser -u riak -- /usr/lib/riak/bin/riak-admin "$@"
        return
    fi
    su -s /bin/sh riak -c "VMARGS_PATH='$admin_vmargs' /usr/lib/riak/bin/riak-admin $*"
}

log_cluster_command_output() {
    command_name=$1
    command_output=$2
    printf '%s\n' "$command_output" | while IFS= read -r command_line
    do
        log "cluster: ${command_name}: ${command_line}"
    done
}

join_output_is_successful() {
    printf '%s\n' "$1" | grep -Eq 'Success: staged join request|already (a )?member'
}

plan_output_is_successful() {
    printf '%s\n' "$1" | grep -Eq 'Staged Changes|To commit these changes'
}

commit_output_is_successful() {
    printf '%s\n' "$1" | grep -Eiq 'cluster changes committed'
}

beam_running() {
    pgrep -x beam.smp >/dev/null 2>&1
}

ping_works() {
    ping_output=$(riak_command ping 2>&1 || true)
    ping_value=$(printf '%s' "$ping_output" | tr -d '\\r\\n')
    [ "$ping_value" = "pong" ]
}

validate_nodename() {
    printf '%s\n' "$1" | grep -Eq '^openriak-kv@[A-Za-z0-9][A-Za-z0-9._:-]*$'
}

validate_ipv4() {
    printf '%s\n' "$1" | awk -F. '
        NF != 4 { exit 1 }
        {
            for (octet = 1; octet <= 4; octet += 1) {
                if ($octet !~ /^[0-9]+$/ || $octet < 0 || $octet > 255) exit 1
            }
        }
    '
}

current_node_ipv4() {
    node_ip_candidates=$(hostname -i 2>/dev/null || true)
    if [ -z "$node_ip_candidates" ]
    then
        node_ip_candidates=$(getent hosts "$(hostname)" 2>/dev/null | awk '{print $1}' || true)
    fi
    for node_ip_candidate in $node_ip_candidates
    do
        case "$node_ip_candidate" in
            127.*|*:* )
                continue
                ;;
        esac
        if validate_ipv4 "$node_ip_candidate"
        then
            printf '%s\n' "$node_ip_candidate"
            return 0
        fi
    done
    return 1
}

nodename_resolves_to_ip() {
    resolution_node=$1
    resolution_ip=$2
    resolution_host=${resolution_node#*@}
    getent hosts "$resolution_host" 2>/dev/null | awk -v expected="$resolution_ip" '
        $1 == expected { found = 1 }
        END { exit(found ? 0 : 1) }
    '
}

control_value() {
    control_file=$1
    control_key=$2
    sed -n "s/^${control_key}=//p" "$control_file" | sed -n '1p'
}

atomic_control_file() {
    control_path=$1
    control_node=$2
    control_ip=$3
    control_coordinator=$4
    control_suffix=$5
    control_temporary="${control_path}.tmp.$$"
    printf 'nodename=%s\nip=%s\ncoordinator=%s\nsuffix=%s\n' \
        "$control_node" \
        "$control_ip" \
        "$control_coordinator" \
        "$control_suffix" > "$control_temporary"
    mv -f "$control_temporary" "$control_path"
}

clean_owned_control_files() {
    for owned_file in "$control_dir/${riak_node_name}-"*
    do
        [ -e "$owned_file" ] || continue
        rm -f "$owned_file"
        log "cluster: removed stale owned control file $(basename "$owned_file")"
    done
}

cluster_member() {
    member_output=$(riak_command admin member-status 2>&1 || true)
    member_count=$(printf '%s\n' "$member_output" | grep -Ec '^[[:space:]]*(valid|joining|leaving|exiting|down)[[:space:]]' || true)
    [ "$member_count" -gt 1 ]
}

wait_for_ring() {
    ring_attempt=0
    log "cluster: waiting for the ring to become ready"
    while :
    do
        ring_attempt=$((ring_attempt + 1))
        ring_output=$(riak_command admin ringready 2>&1 || true)
        if printf '%s\n' "$ring_output" | grep -Eq '(^|[[:space:]])TRUE([[:space:]]|$)'
        then
            ring_summary=$(printf '%s' "$ring_output" | one_line)
            log "cluster: ring is ready (${ring_summary})"
            return
        fi
        ring_summary=$(printf '%s' "$ring_output" | one_line)
        log "cluster: waiting for ring readiness (attempt ${ring_attempt}, status=${ring_summary:-no-response})"
        sleep "${RIAK_STARTUP_POLL_SECONDS:-1}"
    done
}

wait_for_transfers() {
    transfer_attempt=0
    log "startup: waiting for Riak transfers to complete"
    while :
    do
        transfer_attempt=$((transfer_attempt + 1))
        transfers_output=$(riak_command admin transfers 2>&1 || true)
        if printf '%s\n' "$transfers_output" | grep -Eq 'No transfers (active|in progress)'
        then
            transfers_summary=$(printf '%s' "$transfers_output" | one_line)
            log "startup: transfers complete (${transfers_summary})"
            return
        fi
        transfers_summary=$(printf '%s' "$transfers_output" | one_line)
        log "startup: waiting for transfers (attempt ${transfer_attempt}, transfers=${transfers_summary:-no-response})"
        sleep "${RIAK_STARTUP_POLL_SECONDS:-1}"
    done
}

cluster_failure_exists() {
    failure_suffix=$1
    for failure_file in "$control_dir/"*-"${failure_suffix}"-failed
    do
        [ -e "$failure_file" ] || continue
        return 0
    done
    return 1
}

stop_with_error() {
    failure_message=$1
    log "cluster: failure: ${failure_message}"
    if beam_running
    then
        riak_command stop || true
        while beam_running
        do
            log "cluster: waiting for BEAM to stop after failure"
            sleep "${RIAK_SHUTDOWN_POLL_SECONDS:-1}"
        done
    fi
    exit 1
}

publish_failure() {
    failure_suffix=$1
    failure_message=$2
    failure_coordinator=${3:-}
    atomic_control_file \
        "$control_dir/${riak_node_name}-${failure_suffix}-failed" \
        "$riak_node_name" \
        "$node_ip" \
        "$failure_coordinator" \
        "$failure_suffix"
    stop_with_error "$failure_message"
}

monitor_node() {
    log "startup: OpenRiak is ready"
    while :
    do
        log "monitor: sleeping for ${RIAK_MONITOR_INTERVAL_SECONDS:-10}s"
        sleep "${RIAK_MONITOR_INTERVAL_SECONDS:-10}"
        if beam_running && ping_works
        then
            log "monitor: BEAM is running and riak ping returned pong"
        else
            log "monitor: OpenRiak stopped responding; container is exiting"
            exit 1
        fi
    done
}

shutdown() {
    shutdown_signal=$1
    trap - HUP INT TERM
    log "shutdown: received ${shutdown_signal}"
    if beam_running
    then
        log "shutdown: requesting OpenRiak stop"
        if riak_command stop
        then
            log "shutdown: OpenRiak accepted the stop request"
        else
            log "shutdown: OpenRiak stop command returned an error"
        fi
    else
        log "shutdown: BEAM is already stopped"
    fi
    shutdown_attempt=0
    while beam_running
    do
        shutdown_attempt=$((shutdown_attempt + 1))
        log "shutdown: waiting for BEAM to stop (attempt ${shutdown_attempt})"
        sleep "${RIAK_SHUTDOWN_POLL_SECONDS:-1}"
    done
    log "shutdown: BEAM stopped; container is exiting"
    exit 0
}

trap 'shutdown SIGHUP' HUP
trap 'shutdown SIGINT' INT
trap 'shutdown SIGTERM' TERM

log "configuration: preparing mounted directories"
mkdir -p "$config_dir" "$data_dir" "$log_dir" /run/riak
if [ ! -s "$config_dir/riak.conf" ]
then
    log "configuration: seeding /etc/riak from packaged defaults"
    cp -a "$defaults_dir/." "$config_dir/"
else
    log "configuration: using existing /etc/riak/riak.conf"
fi

set_setting() {
    key=$1
    value=$2
    escaped_key=$(printf '%s' "$key" | sed 's/[.[\\*^$()+?{|]/\\\\&/g')
    if grep -Eq "^[[:space:]]*${escaped_key}[[:space:]]*=" "$config_dir/riak.conf"
    then
        sed -i -E "s|^[[:space:]]*${escaped_key}[[:space:]]*=.*$|${key} = ${value}|" "$config_dir/riak.conf"
    elif grep -Eq "^[[:space:]]*##[[:space:]]*${escaped_key}[[:space:]]*=" "$config_dir/riak.conf"
    then
        sed -i -E "s|^[[:space:]]*##[[:space:]]*${escaped_key}[[:space:]]*=.*$|${key} = ${value}|" "$config_dir/riak.conf"
    else
        printf '\n%s = %s\n' "$key" "$value" >> "$config_dir/riak.conf"
    fi
    log "configuration: ${key} = ${value}"
}

node_host=${RIAK_NODE_HOST:-$(hostname)}
riak_node_name=${RIAK_NODE_NAME:-openriak-kv@$node_host}
if ! validate_nodename "$riak_node_name"
then
    log "configuration: invalid RIAK_NODE_NAME: ${riak_node_name}"
    exit 1
fi
node_ip=$(current_node_ipv4 || true)
if [ -n "$node_ip" ]
then
    log "configuration: current Docker IPv4 address = ${node_ip}"
else
    log "configuration: no non-loopback Docker IPv4 address is currently available"
fi
if ! printf '%s\n' "$RIAK_DISTRIBUTED_COOKIE" | grep -Eq '^[A-Za-z0-9_-]+$'
then
    log "configuration: RIAK_DISTRIBUTED_COOKIE must contain only letters, numbers, underscores, and hyphens"
    exit 1
fi
set_setting nodename "$riak_node_name"
set_setting distributed_cookie "$RIAK_DISTRIBUTED_COOKIE"
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
    log "initialization: volume setup complete; RIAK_INIT_ONLY requested"
    exit 0
fi

ulimit -n "${RIAK_NOFILE_LIMIT:-100000}"
log "startup: validating configuration and generating VM arguments"
if chkconfig_output=$(riak_command chkconfig 2>&1)
then
    chkconfig_summary=$(printf '%s' "$chkconfig_output" | one_line)
    log "startup: configuration is valid (${chkconfig_summary})"
else
    chkconfig_summary=$(printf '%s' "$chkconfig_output" | one_line)
    log "startup: configuration validation failed (${chkconfig_summary:-no-response})"
    exit 1
fi
log "startup: starting OpenRiak as a daemon"
if riak_command daemon
then
    log "startup: daemon command completed"
else
    log "startup: daemon command failed"
    exit 1
fi

startup_attempt=0
log "startup: waiting for BEAM and riak ping"
while :
do
    startup_attempt=$((startup_attempt + 1))
    beam_status=stopped
    if beam_running
    then
        beam_status=running
    fi
    ping_output=$(riak_command ping 2>&1 || true)
    ping_value=$(printf '%s' "$ping_output" | tr -d '\\r\\n')
    if [ "$beam_status" = "running" ] && [ "$ping_value" = "pong" ]
    then
        log "startup: BEAM is running and riak ping returned pong"
        break
    fi
    ping_summary=$(printf '%s' "$ping_output" | one_line)
    log "startup: waiting for BEAM/ping (attempt ${startup_attempt}, beam=${beam_status}, ping=${ping_summary:-no-response})"
    sleep "${RIAK_STARTUP_POLL_SECONDS:-1}"
done

service_attempt=0
log "startup: waiting for the riak_kv service"
while :
do
    service_attempt=$((service_attempt + 1))
    services_output=$(riak_command admin services 2>&1 || true)
    if printf '%s\n' "$services_output" | grep -Fq 'riak_kv'
    then
        services_summary=$(printf '%s' "$services_output" | one_line)
        log "startup: riak_kv service is up (${services_summary})"
        break
    fi
    services_summary=$(printf '%s' "$services_output" | one_line)
    log "startup: waiting for riak_kv (attempt ${service_attempt}, services=${services_summary:-no-response})"
    sleep "${RIAK_STARTUP_POLL_SECONDS:-1}"
done

wait_for_transfers

cluster_mode=${OPENRIAK_CLUSTER_MODE:-single}
if [ "$cluster_mode" = "single" ]
then
    monitor_node
fi
if [ "$cluster_mode" != "cluster" ]
then
    log "cluster: invalid OPENRIAK_CLUSTER_MODE: ${cluster_mode}"
    exit 1
fi
if [ -z "$node_ip" ]
then
    stop_with_error "a non-loopback Docker IPv4 address is required in cluster mode"
fi

mkdir -p "$control_dir"
role_value=${role:-follower}
if [ -z "$role_value" ]
then
    role_value=follower
fi

run_follower() {
    log "cluster: Role: Follower"
    clean_owned_control_files
    if cluster_member
    then
        log "cluster: existing multi-node membership detected"
        wait_for_ring
        wait_for_transfers
        monitor_node
    fi

    cluster_waited=0
    cluster_poll=${OPENRIAK_CLUSTER_POLL_SECONDS:-1}
    cluster_timeout=${OPENRIAK_CLUSTER_WAIT_SECONDS:-300}
    while :
    do
        for coordinator_file in "$control_dir/"*-coordinator
        do
            [ -e "$coordinator_file" ] || continue
            coordinator_node=$(control_value "$coordinator_file" nodename)
            coordinator_ip=$(control_value "$coordinator_file" ip)
            advertised_coordinator=$(control_value "$coordinator_file" coordinator)
            coordinator_suffix=$(control_value "$coordinator_file" suffix)
            if ! validate_nodename "$coordinator_node"
            then
                log "cluster: ignoring invalid coordinator file $(basename "$coordinator_file")"
                continue
            fi
            if ! validate_ipv4 "$coordinator_ip"
            then
                log "cluster: ignoring coordinator file with invalid IPv4 address $(basename "$coordinator_file")"
                continue
            fi
            if [ "$advertised_coordinator" != "$coordinator_node" ]
            then
                log "cluster: ignoring coordinator file whose coordinator field does not match its nodename"
                continue
            fi
            if ! printf '%s\n' "$coordinator_suffix" | grep -Eq '^[0-9a-f]{16}$'
            then
                log "cluster: ignoring coordinator file with invalid suffix $(basename "$coordinator_file")"
                continue
            fi
            expected_coordinator="$control_dir/${coordinator_node}-${coordinator_suffix}-coordinator"
            if [ "$coordinator_file" != "$expected_coordinator" ]
            then
                log "cluster: ignoring coordinator file whose contents do not match its name"
                continue
            fi
            if ! nodename_resolves_to_ip "$coordinator_node" "$coordinator_ip"
            then
                log "cluster: coordinator ${coordinator_node} does not currently resolve to advertised IPv4 ${coordinator_ip}; retrying"
                continue
            fi
            if cluster_failure_exists "$coordinator_suffix"
            then
                continue
            fi
            ready_file="$control_dir/${riak_node_name}-${coordinator_suffix}-ready"
            approved_file="$control_dir/${riak_node_name}-${coordinator_suffix}-approved"
            joined_file="$control_dir/${riak_node_name}-${coordinator_suffix}-joined"
            complete_file="$control_dir/${riak_node_name}-${coordinator_suffix}-complete"
            if [ ! -e "$ready_file" ] && [ ! -e "$approved_file" ] && [ ! -e "$joined_file" ] && [ ! -e "$complete_file" ]
            then
                atomic_control_file \
                    "$ready_file" \
                    "$riak_node_name" \
                    "$node_ip" \
                    "$coordinator_node" \
                    "$coordinator_suffix"
                log "cluster: announced ${riak_node_name} at ${node_ip} to coordinator ${coordinator_node} (${coordinator_suffix})"
            fi
        done

        approval_count=0
        selected_approval=
        for approved_candidate in "$control_dir/${riak_node_name}-"*-approved
        do
            [ -e "$approved_candidate" ] || continue
            approval_count=$((approval_count + 1))
            selected_approval=$approved_candidate
        done
        if [ "$approval_count" -gt 1 ]
        then
            log "cluster: conflicting coordinator approvals detected; clearing follower state and retrying"
            clean_owned_control_files
            sleep "$cluster_poll"
            continue
        fi
        if [ "$approval_count" -eq 1 ]
        then
            approved_node=$(control_value "$selected_approval" nodename)
            approved_ip=$(control_value "$selected_approval" ip)
            coordinator_node=$(control_value "$selected_approval" coordinator)
            coordinator_suffix=$(control_value "$selected_approval" suffix)
            coordinator_file="$control_dir/${coordinator_node}-${coordinator_suffix}-coordinator"
            if [ "$approved_node" != "$riak_node_name" ] \
                || [ "$approved_ip" != "$node_ip" ] \
                || [ ! -e "$coordinator_file" ] \
                || ! validate_nodename "$coordinator_node"
            then
                log "cluster: approval no longer has a valid coordinator; clearing follower state"
                clean_owned_control_files
                sleep "$cluster_poll"
                continue
            fi
            log "cluster: join approved by ${coordinator_node} (${coordinator_suffix})"
            if join_output=$(riak_admin_command cluster join "$coordinator_node" 2>&1)
            then
                log_cluster_command_output "join" "$join_output"
                if join_output_is_successful "$join_output"
                then
                    joined_file="$control_dir/${riak_node_name}-${coordinator_suffix}-joined"
                    mv -f "$selected_approval" "$joined_file"
                    log "cluster: join request accepted; waiting for plan and commit"
                    while :
                    do
                        if cluster_failure_exists "$coordinator_suffix"
                        then
                            stop_with_error "another node reported a failure for ${coordinator_suffix}"
                        fi
                        if cluster_member
                        then
                            wait_for_ring
                            wait_for_transfers
                            log "cluster: waiting for coordinator completion confirmation"
                            while [ ! -e "$complete_file" ]
                            do
                                if cluster_failure_exists "$coordinator_suffix"
                                then
                                    stop_with_error "another node reported a failure for ${coordinator_suffix}"
                                fi
                                if [ ! -e "$coordinator_file" ]
                                then
                                    publish_failure \
                                        "$coordinator_suffix" \
                                        "coordinator marker disappeared before completion" \
                                        "$coordinator_node"
                                fi
                                sleep "$cluster_poll"
                            done
                            log "cluster: coordinator confirmed completion for ${riak_node_name}"
                            rm -f "$control_dir/${riak_node_name}-"*
                            log "cluster: follower joined ${coordinator_node} successfully"
                            monitor_node
                        fi
                        sleep "$cluster_poll"
                    done
                fi
            else
                log_cluster_command_output "join" "$join_output"
            fi
            publish_failure "$coordinator_suffix" "cluster join was not accepted for ${coordinator_node}"
        fi

        cluster_waited=$((cluster_waited + cluster_poll))
        if [ "$cluster_waited" -ge "$cluster_timeout" ]
        then
            atomic_control_file \
                "$control_dir/${riak_node_name}-startup-failed" \
                "$riak_node_name" \
                "$node_ip" \
                "" \
                startup
            stop_with_error "no coordinator approved this follower within ${cluster_timeout}s"
        fi
        log "cluster: follower waiting for coordinator approval (${cluster_waited}s/${cluster_timeout}s)"
        sleep "$cluster_poll"
    done
}

run_coordinator() {
    log "cluster: Role: Coordinator"
    for stale_file in "$control_dir/"*-coordinator
    do
        [ -e "$stale_file" ] || continue
        rm -f "$stale_file"
        log "cluster: removed stale coordinator file $(basename "$stale_file")"
    done
    for stale_state in "$control_dir/"*-ready "$control_dir/"*-approved "$control_dir/"*-joined "$control_dir/"*-complete "$control_dir/"*-failed
    do
        [ -e "$stale_state" ] || continue
        rm -f "$stale_state"
        log "cluster: removed stale cluster state $(basename "$stale_state")"
    done
    coordinator_suffix=$(od -An -N8 -tx1 /dev/urandom | tr -d ' \\n')
    coordinator_file="$control_dir/${riak_node_name}-${coordinator_suffix}-coordinator"
    atomic_control_file \
        "$coordinator_file" \
        "$riak_node_name" \
        "$node_ip" \
        "$riak_node_name" \
        "$coordinator_suffix"
    log "cluster: published coordinator ${riak_node_name} at ${node_ip} in $(basename "$coordinator_file")"

    if cluster_member
    then
        log "cluster: existing multi-node membership detected"
        wait_for_ring
        wait_for_transfers
    fi

    cluster_poll=${OPENRIAK_CLUSTER_POLL_SECONDS:-1}
    while :
    do
        for failure_file in "$control_dir/"*-failed
        do
            [ -e "$failure_file" ] || continue
            atomic_control_file \
                "$control_dir/${riak_node_name}-${coordinator_suffix}-failed" \
                "$riak_node_name" \
                "$node_ip" \
                "$riak_node_name" \
                "$coordinator_suffix"
            stop_with_error "cluster participant reported failure in $(basename "$failure_file")"
        done

        for ready_file in "$control_dir/"*-"${coordinator_suffix}"-ready
        do
            [ -e "$ready_file" ] || continue
            follower_node=$(control_value "$ready_file" nodename)
            follower_ip=$(control_value "$ready_file" ip)
            requested_coordinator=$(control_value "$ready_file" coordinator)
            requested_suffix=$(control_value "$ready_file" suffix)
            expected_ready="$control_dir/${follower_node}-${coordinator_suffix}-ready"
            if ! validate_nodename "$follower_node" \
                || ! validate_ipv4 "$follower_ip" \
                || [ "$requested_coordinator" != "$riak_node_name" ] \
                || [ "$requested_suffix" != "$coordinator_suffix" ] \
                || [ "$ready_file" != "$expected_ready" ]
            then
                log "cluster: rejecting malformed readiness file $(basename "$ready_file")"
                rm -f "$ready_file"
                continue
            fi
            if ! nodename_resolves_to_ip "$follower_node" "$follower_ip"
            then
                log "cluster: waiting for ${follower_node} to resolve to advertised IPv4 ${follower_ip}"
                continue
            fi
            approved_file=${ready_file%-ready}-approved
            mv -f "$ready_file" "$approved_file"
            log "cluster: approved follower ${follower_node} at ${follower_ip}"
        done

        joined_count=0
        for joined_file in "$control_dir/"*-"${coordinator_suffix}"-joined
        do
            [ -e "$joined_file" ] || continue
            joined_count=$((joined_count + 1))
        done
        pending_count=0
        for pending_file in "$control_dir/"*-"${coordinator_suffix}"-ready "$control_dir/"*-"${coordinator_suffix}"-approved
        do
            [ -e "$pending_file" ] || continue
            pending_count=$((pending_count + 1))
        done
        if [ "$joined_count" -gt 0 ] && [ "$pending_count" -gt 0 ]
        then
            log "cluster: waiting for ${pending_count} approved or ready node(s) before planning ${joined_count} joined node(s)"
        fi
        if [ "$joined_count" -gt 0 ] && [ "$pending_count" -eq 0 ]
        then
            log "cluster: planning a batch of ${joined_count} joined node(s)"
            if plan_output=$(riak_admin_command cluster plan 2>&1)
            then
                log_cluster_command_output "plan" "$plan_output"
                if ! plan_output_is_successful "$plan_output"
                then
                    publish_failure "$coordinator_suffix" "cluster plan was not accepted"
                fi
            else
                log_cluster_command_output "plan" "$plan_output"
                publish_failure "$coordinator_suffix" "cluster plan command failed"
            fi
            log "cluster: committing the planned membership changes"
            if commit_output=$(riak_admin_command cluster commit 2>&1)
            then
                log_cluster_command_output "commit" "$commit_output"
                if ! commit_output_is_successful "$commit_output"
                then
                    publish_failure "$coordinator_suffix" "cluster commit was not accepted"
                fi
            else
                log_cluster_command_output "commit" "$commit_output"
                publish_failure "$coordinator_suffix" "cluster commit command failed"
            fi
            wait_for_ring
            wait_for_transfers
            for joined_file in "$control_dir/"*-"${coordinator_suffix}"-joined
            do
                [ -e "$joined_file" ] || continue
                complete_file=${joined_file%-joined}-complete
                mv -f "$joined_file" "$complete_file"
                log "cluster: completed follower $(basename "${complete_file%-complete}")"
            done
        fi

        if beam_running && ping_works
        then
            log "monitor: Coordinator is healthy; sleeping for ${cluster_poll}s"
        else
            atomic_control_file \
                "$control_dir/${riak_node_name}-${coordinator_suffix}-failed" \
                "$riak_node_name" \
                "$node_ip" \
                "$riak_node_name" \
                "$coordinator_suffix"
            stop_with_error "coordinator health check failed"
        fi
        sleep "$cluster_poll"
    done
}

case "$role_value" in
    coordinator)
        run_coordinator
        ;;
    follower)
        run_follower
        ;;
    *)
        log "cluster: invalid role value: ${role_value}"
        exit 1
        ;;
esac
"""


HEALTHCHECK_SCRIPT = """#!/bin/sh
set -eu

if ! pgrep -x beam.smp >/dev/null 2>&1
then
    echo "OpenRiak healthcheck failed: beam.smp is not running"
    exit 1
fi

ping_output=$(/usr/sbin/riak ping 2>/dev/null || true)
if [ "$ping_output" != "pong" ]
then
    echo "OpenRiak healthcheck failed: riak ping did not return pong"
    exit 1
fi

echo "OpenRiak healthcheck passed: BEAM is running and riak ping returned pong"
"""


def render_dockerfile(
    target: Target,
    pinned_base_image: str,
    distributed_cookie: str | None = None,
) -> str:
    distributed_cookie = distributed_cookie or generate_distributed_cookie()
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
ENV RIAK_DISTRIBUTED_COOKIE="{distributed_cookie}"
ENV RIAK_RING_SIZE="8"
ENV RIAK_STORAGE_BACKEND="leveled"
ENV RIAK_ANTI_ENTROPY="passive"
ENV RIAK_TICTACAAE_ACTIVE="active"
ENV RIAK_TICTACAAE_STOREHEADS="enabled"
ENV RIAK_HTTP_LISTENER="0.0.0.0:8098"
ENV RIAK_PB_LISTENER="0.0.0.0:8087"
ENV RIAK_NOFILE_LIMIT="100000"
ENV RIAK_INIT_ONLY="0"
ENV RIAK_STARTUP_POLL_SECONDS="1"
ENV RIAK_SHUTDOWN_POLL_SECONDS="1"
ENV RIAK_MONITOR_INTERVAL_SECONDS="10"
ENV OPENRIAK_CLUSTER_MODE="single"
ENV OPENRIAK_CLUSTER_CONTROL_DIR="/var/lib/openriak-cluster-control"
ENV OPENRIAK_CLUSTER_POLL_SECONDS="1"
ENV OPENRIAK_CLUSTER_WAIT_SECONDS="300"
ENV role=""

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
mkdir -p /opt/openriak-defaults/etc-riak /var/lib/riak /var/log/riak /run/riak /usr/lib/riak/log
cp -a /etc/riak/. /opt/openriak-defaults/etc-riak/
chown -R riak:riak /var/lib/riak /var/log/riak /run/riak /usr/lib/riak/log
OPENRIAK_IMAGE_SETUP

COPY <<'OPENRIAK_ENTRYPOINT' /usr/local/bin/openriak-entrypoint
{ENTRYPOINT_SCRIPT.rstrip()}
OPENRIAK_ENTRYPOINT

COPY <<'OPENRIAK_HEALTHCHECK' /usr/local/bin/openriak-healthcheck
{HEALTHCHECK_SCRIPT.rstrip()}
OPENRIAK_HEALTHCHECK

RUN <<'OPENRIAK_SCRIPT_SETUP'
set -eu
chmod 0755 /usr/local/bin/openriak-entrypoint
chmod 0755 /usr/local/bin/openriak-healthcheck
OPENRIAK_SCRIPT_SETUP

VOLUME ["/etc/riak"]
VOLUME ["/var/lib/riak"]
VOLUME ["/var/log/riak"]
EXPOSE 8087
EXPOSE 8098
HEALTHCHECK --interval=10s --timeout=10s --start-period=60s --retries=3 CMD ["/usr/local/bin/openriak-healthcheck"]
STOPSIGNAL SIGTERM
ENTRYPOINT ["/usr/local/bin/openriak-entrypoint"]
"""


def render_single_compose(
    target: Target,
    distributed_cookie: str | None = None,
    publish_ports: bool = True,
) -> str:
    distributed_cookie = distributed_cookie or generate_distributed_cookie()
    node = target.node_name
    host = default_node_host(1)
    ports = f'''    ports:
      - "${{OPENRIAK_PB_PORT:-8087}}:8087"
      - "${{OPENRIAK_HTTP_PORT:-8098}}:8098"
''' if publish_ports else ""
    return f"""# Generated and tested by tools/openriak-docker/openriak-docker. Do not edit by hand.
name: {node}

services:
  node:
    build:
      context: .
      dockerfile: ./Dockerfile
    image: {target.image}
    container_name: "${{OPENRIAK_CONTAINER_NAME:-{node}}}"
    hostname: "${{OPENRIAK_NODE_1_HOST:-{host}}}"
    environment:
      RIAK_NODE_HOST: "${{OPENRIAK_NODE_1_HOST:-{host}}}"
      RIAK_DISTRIBUTED_COOKIE: "${{OPENRIAK_DISTRIBUTED_COOKIE:-{distributed_cookie}}}"
      RIAK_MONITOR_INTERVAL_SECONDS: "${{OPENRIAK_MONITOR_INTERVAL_SECONDS:-10}}"
{ports}    volumes:
      - "${{OPENRIAK_CONFIG_PATH:-./{node}/config}}:/etc/riak"
      - "${{OPENRIAK_DATA_PATH:-./{node}/data}}:/var/lib/riak"
      - "${{OPENRIAK_LOGS_PATH:-./{node}/logs}}:/var/log/riak"
    networks:
      openriak:
        aliases:
          - "${{OPENRIAK_NODE_1_HOST:-{host}}}"
    ulimits:
      nofile:
        soft: 100000
        hard: 100000
    stop_grace_period: 2m

networks:
  openriak:
    driver: bridge
"""


def cluster_node_name(target: Target, index: int) -> str:
    return f"{target.node_name}-{index}"


def render_cluster_service(
    target: Target,
    index: int,
    distributed_cookie: str,
    publish_ports: bool,
) -> str:
    node = cluster_node_name(target, index)
    host = default_node_host(index)
    port_prefix = 18000 + (index - 1) * 100
    role_line = "      role: coordinator\n" if index == 1 else ""
    ports = f'''    ports:
      - "${{OPENRIAK_NODE_{index}_PB_PORT:-{port_prefix + 87}}}:8087"
      - "${{OPENRIAK_NODE_{index}_HTTP_PORT:-{port_prefix + 98}}}:8098"
''' if publish_ports else ""
    return f"""  node{index}:
    build:
      context: .
      dockerfile: ./Dockerfile
    image: {target.image}
    container_name: "${{OPENRIAK_NODE_{index}_CONTAINER_NAME:-{node}}}"
    hostname: "${{OPENRIAK_NODE_{index}_HOST:-{host}}}"
    environment:
      OPENRIAK_CLUSTER_MODE: cluster
{role_line}      RIAK_NODE_HOST: "${{OPENRIAK_NODE_{index}_HOST:-{host}}}"
      RIAK_DISTRIBUTED_COOKIE: "${{OPENRIAK_DISTRIBUTED_COOKIE:-{distributed_cookie}}}"
      RIAK_MONITOR_INTERVAL_SECONDS: "${{OPENRIAK_MONITOR_INTERVAL_SECONDS:-10}}"
      OPENRIAK_CLUSTER_POLL_SECONDS: "${{OPENRIAK_CLUSTER_POLL_SECONDS:-1}}"
      OPENRIAK_CLUSTER_WAIT_SECONDS: "${{OPENRIAK_CLUSTER_WAIT_SECONDS:-300}}"
{ports}    volumes:
      - "${{OPENRIAK_NODE_{index}_CONFIG_PATH:-./{node}/config}}:/etc/riak"
      - "${{OPENRIAK_NODE_{index}_DATA_PATH:-./{node}/data}}:/var/lib/riak"
      - "${{OPENRIAK_NODE_{index}_LOGS_PATH:-./{node}/logs}}:/var/log/riak"
      - "${{OPENRIAK_CLUSTER_CONTROL_PATH:-./{target.node_name}-cluster-control}}:{CONTROL_DIRECTORY}"
    networks:
      openriak:
        aliases:
          - "${{OPENRIAK_NODE_{index}_HOST:-{host}}}"
    ulimits:
      nofile:
        soft: 100000
        hard: 100000
    stop_grace_period: 2m
"""


def render_cluster_compose(
    target: Target,
    node_count: int = DEFAULT_CLUSTER_NODES,
    distributed_cookie: str | None = None,
    publish_ports: bool = True,
) -> str:
    if node_count < 2 or node_count > 253:
        raise DockerToolError("Cluster Compose generation supports between 2 and 253 nodes")
    distributed_cookie = distributed_cookie or generate_distributed_cookie()
    services = "\n".join(
        render_cluster_service(target, index, distributed_cookie, publish_ports).rstrip()
        for index in range(1, node_count + 1)
    )
    return f"""# Generated and tested by tools/openriak-docker/openriak-docker. Do not edit by hand.
# Set role=coordinator on exactly one service. An omitted or empty role is a follower.
name: {target.node_name}-cluster

services:
{services}

networks:
  openriak:
    driver: bridge
"""


def render_environment_example(
    target: Target,
    distributed_cookie: str,
    node_count: int = DEFAULT_CLUSTER_NODES,
) -> str:
    lines = [
        "# Copy this file to .env before running either Compose file.",
        "# All values below match the generated defaults and may be edited.",
        "# Every member of one cluster must use the same distributed cookie.",
        f"OPENRIAK_DISTRIBUTED_COOKIE={distributed_cookie}",
        "OPENRIAK_MONITOR_INTERVAL_SECONDS=10",
        "OPENRIAK_CLUSTER_POLL_SECONDS=1",
        "OPENRIAK_CLUSTER_WAIT_SECONDS=300",
        "",
        "# Single-node container, ports, and bind-mount source paths.",
        f"OPENRIAK_CONTAINER_NAME={target.node_name}",
        "OPENRIAK_PB_PORT=8087",
        "OPENRIAK_HTTP_PORT=8098",
        f"OPENRIAK_CONFIG_PATH=./{target.node_name}/config",
        f"OPENRIAK_DATA_PATH=./{target.node_name}/data",
        f"OPENRIAK_LOGS_PATH=./{target.node_name}/logs",
        "",
        "# Cluster-wide shared control-directory source path.",
        f"OPENRIAK_CLUSTER_CONTROL_PATH=./{target.node_name}-cluster-control",
        "",
        "# Cluster node identities, ports, and bind-mount source paths.",
    ]
    for index in range(1, node_count + 1):
        node = cluster_node_name(target, index)
        port_prefix = 18000 + (index - 1) * 100
        lines.extend(
            [
                f"OPENRIAK_NODE_{index}_HOST={default_node_host(index)}",
                f"OPENRIAK_NODE_{index}_CONTAINER_NAME={node}",
                f"OPENRIAK_NODE_{index}_PB_PORT={port_prefix + 87}",
                f"OPENRIAK_NODE_{index}_HTTP_PORT={port_prefix + 98}",
                f"OPENRIAK_NODE_{index}_CONFIG_PATH=./{node}/config",
                f"OPENRIAK_NODE_{index}_DATA_PATH=./{node}/data",
                f"OPENRIAK_NODE_{index}_LOGS_PATH=./{node}/logs",
                "",
            ]
        )
    return "\n".join(lines)


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


def digest_from_pull_output(output: str) -> str | None:
    match = re.search(
        r"^Digest:[ \t]*(sha256:[0-9a-f]{64})[ \t]*$",
        output,
        re.MULTILINE,
    )
    return match.group(1) if match else None


def resolve_base_image(target: Target, logs: pathlib.Path) -> tuple[str, str]:
    docker = docker_command()
    base = base_image_for(target)
    pull_result = run_logged(
        [docker, "pull", "--platform", target.platform, base],
        logs / "base-image-pull.log",
    )
    result = run_logged(
        [docker, "image", "inspect", "--format", "{{json .RepoDigests}}", base],
        logs / "base-image-inspect.log",
    )
    try:
        repo_digests = json.loads(result.stdout.strip())
    except json.JSONDecodeError as error:
        raise DockerToolError(f"Docker returned invalid RepoDigests for {base}") from error
    if repo_digests:
        digest_reference = str(repo_digests[0])
        digest = digest_reference.rsplit("@", 1)[-1]
    else:
        digest = digest_from_pull_output(pull_result.stdout)
        if digest is None:
            raise DockerToolError(f"Docker did not return a digest for {base}")
    repository = base.rsplit(":", 1)[0]
    return base, f"{base}@{digest}" if "@" not in base else f"{repository}@{digest}"


def set_riak_setting(source: str, key: str, value: str) -> str:
    active = re.compile(rf"^[ \t]*{re.escape(key)}[ \t]*=.*$", re.MULTILINE)
    replacement = f"{key} = {value}"
    if active.search(source):
        return active.sub(replacement, source, count=1)
    commented = re.compile(rf"^[ \t]*##[ \t]*{re.escape(key)}[ \t]*=.*$", re.MULTILINE)
    if commented.search(source):
        return commented.sub(replacement, source, count=1)
    suffix = "" if source.endswith("\n") else "\n"
    return f"{source}{suffix}{replacement}\n"


def configure_test_node(config_path: pathlib.Path, node_name: str) -> None:
    source = config_path.read_text(encoding="utf-8")
    settings = {
        "nodename": f"openriak-kv@{node_name}",
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


def container_http_ping(container_name: str) -> tuple[int, str, int]:
    docker = docker_command()
    result = subprocess.run(
        [
            docker,
            "exec",
            container_name,
            "curl",
            "--silent",
            "--show-error",
            "--output",
            "-",
            "--write-out",
            "\\n%{http_code}",
            "http://127.0.0.1:8098/ping",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    body, separator, status = result.stdout.strip().rpartition("\n")
    status_code = int(status) if separator and status.isdigit() else 0
    return result.returncode, body if separator else result.stdout.strip(), status_code


def wait_for_node(
    container_name: str,
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
            http_exit, last_http, http_status = container_http_ping(container_name)
            http_ok = http_exit == 0 and http_status == 200 and last_http == "OK"
            log.write(
                f"{isoformat()} cli_exit={cli.returncode} cli={last_cli!r} "
                f"http_exit={http_exit} http_status={http_status} http={last_http!r}\n"
            )
            log.flush()
            if cli.returncode == 0 and last_cli == "pong" and http_ok:
                return last_cli, last_http
            time.sleep(2)
    raise DockerToolError(
        f"OpenRiak node was not ready after {timeout_seconds}s; CLI={last_cli!r}, HTTP={last_http!r}"
    )


def wait_for_container_log(
    container_name: str,
    marker: str,
    timeout_seconds: int,
    log_path: pathlib.Path,
) -> str:
    docker = docker_command()
    deadline = time.monotonic() + timeout_seconds
    last_output = ""
    with log_path.open("w", encoding="utf-8", newline="\n") as log:
        while time.monotonic() < deadline:
            result = subprocess.run(
                [docker, "logs", container_name],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            last_output = result.stdout
            found = result.returncode == 0 and marker in last_output
            log.write(f"{isoformat()} exit={result.returncode} marker_found={found}\n")
            log.flush()
            if found:
                return last_output
            time.sleep(1)
    raise DockerToolError(
        f"Container log did not contain {marker!r} after {timeout_seconds}s"
    )


def wait_for_container_health(
    container_name: str,
    timeout_seconds: int,
    log_path: pathlib.Path,
) -> str:
    docker = docker_command()
    deadline = time.monotonic() + timeout_seconds
    last_status = "unknown"
    with log_path.open("w", encoding="utf-8", newline="\n") as log:
        while time.monotonic() < deadline:
            result = subprocess.run(
                [
                    docker,
                    "container",
                    "inspect",
                    "--format",
                    "{{if .State.Health}}{{.State.Health.Status}}{{else}}missing{{end}}",
                    container_name,
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            last_status = result.stdout.strip()
            log.write(
                f"{isoformat()} exit={result.returncode} health={last_status!r}\n"
            )
            log.flush()
            if result.returncode == 0 and last_status == "healthy":
                return last_status
            time.sleep(1)
    raise DockerToolError(
        f"Container healthcheck did not become healthy after {timeout_seconds}s; status={last_status!r}"
    )


def wait_for_cluster(
    container_names: list[str],
    expected_nodenames: list[str],
    timeout_seconds: int,
    log_path: pathlib.Path,
) -> dict[str, Any]:
    docker = docker_command()
    deadline = time.monotonic() + timeout_seconds
    last_state: dict[str, Any] = {}
    status_line = re.compile(
        r"^[ \t]*(?:valid|joining|leaving|exiting|down)[ \t]", re.MULTILINE
    )
    with log_path.open("w", encoding="utf-8", newline="\n") as log:
        while time.monotonic() < deadline:
            all_ready = True
            state: dict[str, Any] = {}
            for container_name in container_names:
                commands = {
                    "members": ["riak", "admin", "member-status"],
                    "ring": ["riak", "admin", "ringready"],
                    "transfers": ["riak", "admin", "transfers"],
                    "ping": ["riak", "ping"],
                }
                outputs: dict[str, dict[str, Any]] = {}
                for name, arguments in commands.items():
                    result = subprocess.run(
                        [docker, "exec", container_name, *arguments],
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        encoding="utf-8",
                        errors="replace",
                        check=False,
                    )
                    outputs[name] = {
                        "exit": result.returncode,
                        "output": result.stdout.strip(),
                    }
                http_exit, http_body, http_status = container_http_ping(container_name)
                http_ok = http_exit == 0 and http_status == 200 and http_body == "OK"
                members_output = outputs["members"]["output"]
                node_ready = (
                    outputs["members"]["exit"] == 0
                    and len(status_line.findall(members_output)) == len(expected_nodenames)
                    and all(nodename in members_output for nodename in expected_nodenames)
                    and outputs["ring"]["exit"] == 0
                    and re.search(r"(^|\s)TRUE(\s|$)", outputs["ring"]["output"])
                    and outputs["transfers"]["exit"] == 0
                    and re.search(
                        r"No transfers (?:active|in progress)",
                        outputs["transfers"]["output"],
                    )
                    and outputs["ping"]["exit"] == 0
                    and outputs["ping"]["output"] == "pong"
                    and http_ok
                )
                state[container_name] = {
                    "ready": bool(node_ready),
                    "members": members_output,
                    "ring": outputs["ring"]["output"],
                    "transfers": outputs["transfers"]["output"],
                    "ping": outputs["ping"]["output"],
                    "http": http_body,
                }
                all_ready = all_ready and bool(node_ready)
            last_state = state
            log.write(f"{isoformat()} {json.dumps(state, sort_keys=True)}\n")
            log.flush()
            if all_ready:
                return state
            time.sleep(2)
    raise DockerToolError(
        f"OpenRiak cluster was not ready after {timeout_seconds}s; last state={last_state!r}"
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


def artifact_downloads(
    target: Target,
    dockerfile: pathlib.Path,
    compose_single: pathlib.Path,
    compose_cluster: pathlib.Path,
    environment_example: pathlib.Path,
) -> dict[str, Any]:
    base_url = f"downloads/docker/{target.version}/{target.image_tag}"
    return {
        "dockerfile": {
            "filename": "Dockerfile",
            "url": f"{base_url}/Dockerfile",
            "sha256": sha256_file(dockerfile),
        },
        "compose_single": {
            "filename": "compose.single.yaml",
            "url": f"{base_url}/compose.single.yaml",
            "sha256": sha256_file(compose_single),
        },
        "compose_cluster": {
            "filename": "compose.cluster.yaml",
            "url": f"{base_url}/compose.cluster.yaml",
            "sha256": sha256_file(compose_cluster),
        },
        "environment_example": {
            "filename": ".env.example",
            "url": f"{base_url}/.env.example",
            "sha256": sha256_file(environment_example),
        },
    }


def publish_current_run(target: Target, run_root: pathlib.Path, report: dict[str, Any]) -> None:
    current = target.cache_directory
    current.mkdir(parents=True, exist_ok=True)
    for filename in ARTIFACT_FILENAMES:
        source = run_root / filename
        if source.is_file():
            shutil.copy2(source, current / filename)
    with contextlib.suppress(FileNotFoundError):
        (current / "compose.yaml").unlink()
    write_json(run_root / "report.json", report)
    write_json(current / "report.json", report)

    if report["status"] == "passed":
        target.static_directory.mkdir(parents=True, exist_ok=True)
        for filename in ARTIFACT_FILENAMES:
            shutil.copy2(run_root / filename, target.static_directory / filename)
        with contextlib.suppress(FileNotFoundError):
            (target.static_directory / "compose.yaml").unlink()
    elif target.static_directory.exists():
        for filename in ARTIFACT_FILENAMES:
            with contextlib.suppress(FileNotFoundError):
                (target.static_directory / filename).unlink()


def initial_report(
    target: Target,
    identifier: str,
    cluster_nodes: int,
    distributed_cookie: str,
) -> dict[str, Any]:
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
        "generation": {
            "cluster_nodes": cluster_nodes,
            "distributed_cookie": distributed_cookie,
        },
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
        "network": {
            "address_assignment": "docker",
            "node_host": default_node_host(1),
            "riak_node_name": f"openriak-kv@{default_node_host(1)}",
        },
        "ports": {"protobuf": 8087, "http": 8098},
        "steps": [],
        "tests": {},
        "artifacts": {},
        "error": None,
    }


def refresh_target(
    target: Target,
    timeout_seconds: int,
    keep_workdir: bool = False,
    cluster_nodes: int = DEFAULT_CLUSTER_NODES,
) -> bool:
    identifier = run_id()
    run_root = target.cache_directory / "runs" / identifier
    logs = run_root / "logs"
    run_root.mkdir(parents=True, exist_ok=False)
    distributed_cookie = generate_distributed_cookie()
    report = initial_report(target, identifier, cluster_nodes, distributed_cookie)
    dockerfile = run_root / "Dockerfile"
    compose_single = run_root / "compose.single.yaml"
    compose_cluster = run_root / "compose.cluster.yaml"
    environment_example = run_root / ".env.example"
    test_directory: pathlib.Path | None = None
    compose_started = False
    cluster_started = False
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
                render_dockerfile(target, pinned_base, distributed_cookie),
                encoding="utf-8",
                newline="\n",
            )
            compose_single.write_text(
                render_single_compose(target, distributed_cookie),
                encoding="utf-8",
                newline="\n",
            )
            compose_cluster.write_text(
                render_cluster_compose(target, cluster_nodes, distributed_cookie),
                encoding="utf-8",
                newline="\n",
            )
            environment_example.write_text(
                render_environment_example(target, distributed_cookie, cluster_nodes),
                encoding="utf-8",
                newline="\n",
            )

        record_step(report, "generate_artifacts", generate)

        def validate_compose_artifacts() -> None:
            for compose_path, log_name in (
                (compose_single, "compose-single-config.log"),
                (compose_cluster, "compose-cluster-config.log"),
            ):
                run_logged(
                    [
                        docker,
                        "compose",
                        "--project-directory",
                        str(run_root),
                        "--file",
                        str(compose_path),
                        "config",
                        "--quiet",
                    ],
                    logs / log_name,
                )

        record_step(report, "validate_compose_artifacts", validate_compose_artifacts)
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
        compose_single_test = test_directory / "compose.single.test.yaml"
        compose_cluster_test = test_directory / "compose.cluster.test.yaml"
        compose_single_test.write_text(
            render_single_compose(target, distributed_cookie, publish_ports=False),
            encoding="utf-8",
            newline="\n",
        )
        compose_cluster_test.write_text(
            render_cluster_compose(
                target,
                cluster_nodes,
                distributed_cookie,
                publish_ports=False,
            ),
            encoding="utf-8",
            newline="\n",
        )
        shutil.copy2(dockerfile, test_directory / "Dockerfile")
        shutil.copy2(environment_example, test_directory / ".env.example")
        node_directory = test_directory / target.node_name
        test_suffix = identifier[-8:].lower().replace(".", "")
        test_container_name = f"{target.node_name}-t-{test_suffix}"
        environment.update(
            OPENRIAK_CONTAINER_NAME=test_container_name,
            OPENRIAK_PB_PORT=str(free_tcp_port()),
            OPENRIAK_HTTP_PORT=str(free_tcp_port()),
            OPENRIAK_MONITOR_INTERVAL_SECONDS="1",
        )
        cluster_container_names = [
            f"{cluster_node_name(target, index)}-t-{test_suffix}"
            for index in range(1, cluster_nodes + 1)
        ]
        cluster_nodenames = [
            f"openriak-kv@{default_node_host(index)}" for index in range(1, cluster_nodes + 1)
        ]
        cluster_pb_ports = [18087 + (index - 1) * 100 for index in range(1, cluster_nodes + 1)]
        cluster_http_ports = [18098 + (index - 1) * 100 for index in range(1, cluster_nodes + 1)]
        cluster_environment_lines = [
            "OPENRIAK_CLUSTER_POLL_SECONDS=1",
            "OPENRIAK_CLUSTER_WAIT_SECONDS=300",
        ]
        for index in range(1, cluster_nodes + 1):
            cluster_environment_lines.extend(
                [
                    f"OPENRIAK_NODE_{index}_CONTAINER_NAME={cluster_container_names[index - 1]}",
                    f"OPENRIAK_NODE_{index}_PB_PORT={cluster_pb_ports[index - 1]}",
                    f"OPENRIAK_NODE_{index}_HTTP_PORT={cluster_http_ports[index - 1]}",
                ]
            )
        single_environment = test_directory / ".env.single"
        single_environment.write_text(
            "\n".join(
                [
                    f"OPENRIAK_CONTAINER_NAME={environment['OPENRIAK_CONTAINER_NAME']}",
                    f"OPENRIAK_PB_PORT={environment['OPENRIAK_PB_PORT']}",
                    f"OPENRIAK_HTTP_PORT={environment['OPENRIAK_HTTP_PORT']}",
                    "OPENRIAK_MONITOR_INTERVAL_SECONDS=1",
                    "",
                ]
            ),
            encoding="utf-8",
            newline="\n",
        )
        cluster_environment = test_directory / ".env.cluster"
        cluster_environment.write_text(
            "\n".join(["OPENRIAK_MONITOR_INTERVAL_SECONDS=1", *cluster_environment_lines, ""]),
            encoding="utf-8",
            newline="\n",
        )
        compose_command = [
            docker,
            "compose",
            "--env-file",
            str(single_environment),
            "--project-directory",
            str(test_directory),
            "--file",
            str(compose_single_test),
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
            "make_test_config_writable",
            lambda: run_logged(
                compose_command
                + [
                    "run",
                    "--rm",
                    "--entrypoint",
                    "chmod",
                    "node",
                    "0666",
                    "/etc/riak/riak.conf",
                ],
                logs / "compose-config-permissions.log",
                cwd=test_directory,
                environment=environment,
            ),
        )
        record_step(
            report,
            "configure_node",
            lambda: configure_test_node(config_path, default_node_host(1)),
        )
        expected_settings = {
            "nodename": f"openriak-kv@{default_node_host(1)}",
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

        compose_started = True
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
        lifecycle_output = record_step(
            report,
            "wait_for_entrypoint_readiness",
            lambda: wait_for_container_log(
                test_container_name,
                "monitor: BEAM is running",
                timeout_seconds,
                logs / "entrypoint-readiness.log",
            ),
        )
        startup_markers = [
            "startup: starting OpenRiak as a daemon",
            "startup: BEAM is running and riak ping returned pong",
            "startup: riak_kv service is up",
            "startup: transfers complete",
            "startup: OpenRiak is ready",
            "monitor: BEAM is running",
        ]
        missing_startup_markers = [
            marker for marker in startup_markers if marker not in lifecycle_output
        ]
        if missing_startup_markers:
            raise DockerToolError(
                f"Container log is missing lifecycle messages: {missing_startup_markers!r}"
            )
        report["tests"]["entrypoint_startup"] = {
            "status": "passed",
            "required_log_messages": startup_markers,
        }
        cli_response, http_response = record_step(
            report,
            "wait_for_cli_and_http",
            lambda: wait_for_node(
                test_container_name,
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
        health_status = record_step(
            report,
            "wait_for_healthcheck",
            lambda: wait_for_container_health(
                test_container_name,
                timeout_seconds,
                logs / "healthcheck.log",
            ),
        )
        report["tests"]["healthcheck"] = {
            "status": "passed",
            "docker_status": health_status,
            "checks": ["beam.smp", "riak ping == pong"],
        }
        if not populated(data_directory) or not populated(log_directory):
            raise DockerToolError("OpenRiak startup did not populate both data and log volumes")
        report["tests"]["populated_volumes"] = {
            "status": "passed",
            "config": sorted(path.name for path in config_directory.iterdir()),
            "data": sorted(path.name for path in data_directory.iterdir()),
            "logs": sorted(path.name for path in log_directory.iterdir()),
        }
        record_step(
            report,
            "graceful_stop",
            lambda: run_logged(
                compose_command + ["stop", "--timeout", "120"],
                logs / "compose-stop.log",
                cwd=test_directory,
                environment=environment,
            ),
        )
        stopped_logs = record_step(
            report,
            "verify_graceful_shutdown_logging",
            lambda: run_logged(
                [docker, "logs", test_container_name],
                logs / "graceful-shutdown.log",
            ).stdout,
        )
        shutdown_markers = [
            "shutdown: received SIGTERM",
            "shutdown: requesting OpenRiak stop",
            "shutdown: BEAM stopped; container is exiting",
        ]
        missing_shutdown_markers = [
            marker for marker in shutdown_markers if marker not in stopped_logs
        ]
        if missing_shutdown_markers:
            raise DockerToolError(
                f"Container log is missing graceful shutdown messages: {missing_shutdown_markers!r}"
            )
        report["tests"]["graceful_shutdown"] = {
            "status": "passed",
            "signal": "SIGTERM",
            "required_log_messages": shutdown_markers,
        }
        record_step(
            report,
            "remove_single_node_test",
            lambda: run_logged(
                compose_command + ["down", "--remove-orphans"],
                logs / "compose-down.log",
                cwd=test_directory,
                environment=environment,
            ),
        )
        compose_started = False

        cluster_command = [
            docker,
            "compose",
            "--env-file",
            str(cluster_environment),
            "--project-directory",
            str(test_directory),
            "--file",
            str(compose_cluster_test),
        ]
        for cluster_container_name in cluster_container_names:
            existing = run_logged(
                [docker, "container", "inspect", cluster_container_name],
                logs / "cluster-container-name-check.log",
                check=False,
            )
            if existing.returncode == 0:
                raise DockerToolError(
                    f"Container name {cluster_container_name} is already in use; refusing to remove it"
                )

        cluster_started = True
        record_step(
            report,
            "start_compose_cluster",
            lambda: run_logged(
                cluster_command + ["up", "--detach", "--no-build"],
                logs / "cluster-compose-up.log",
                cwd=test_directory,
                environment=environment,
            ),
        )
        cluster_state = record_step(
            report,
            "wait_for_cluster",
            lambda: wait_for_cluster(
                cluster_container_names,
                cluster_nodenames,
                max(timeout_seconds, 300),
                logs / "cluster-readiness.log",
            ),
        )
        role_logs: dict[str, str] = {}
        for index, cluster_container_name in enumerate(cluster_container_names, start=1):
            container_logs = run_logged(
                [docker, "logs", cluster_container_name],
                logs / f"cluster-node-{index}.log",
            ).stdout
            expected_role = "Coordinator" if index == 1 else "Follower"
            if f"cluster: Role: {expected_role}" not in container_logs:
                raise DockerToolError(
                    f"{cluster_container_name} did not log its {expected_role} role"
                )
            role_logs[cluster_container_name] = expected_role
            wait_for_container_health(
                cluster_container_name,
                timeout_seconds,
                logs / f"cluster-node-{index}-health.log",
            )
            cluster_node_directory = test_directory / cluster_node_name(target, index)
            for volume_name in ("config", "data", "logs"):
                if not populated(cluster_node_directory / volume_name):
                    raise DockerToolError(
                        f"Cluster node {index} did not populate its {volume_name} volume"
                    )
        report["tests"]["cluster"] = {
            "status": "passed",
            "node_count": cluster_nodes,
            "members": cluster_nodenames,
            "roles": role_logs,
            "checks": [
                "same member set",
                "ring ready",
                "transfers complete",
                "riak ping == pong",
                "HTTP 200/OK",
                "Docker healthcheck healthy",
                "config/data/log volumes populated",
            ],
            "state": cluster_state,
        }
        record_step(
            report,
            "graceful_stop_cluster",
            lambda: run_logged(
                cluster_command + ["stop", "--timeout", "120"],
                logs / "cluster-compose-stop.log",
                cwd=test_directory,
                environment=environment,
            ),
        )
        record_step(
            report,
            "remove_cluster_test",
            lambda: run_logged(
                cluster_command + ["down", "--remove-orphans"],
                logs / "cluster-compose-down.log",
                cwd=test_directory,
                environment=environment,
            ),
        )
        cluster_started = False
        report["artifacts"] = artifact_downloads(
            target, dockerfile, compose_single, compose_cluster, environment_example
        )
        report["status"] = "passed"
    except Exception as error:
        report["status"] = "failed"
        report["error"] = {"type": type(error).__name__, "message": str(error)}
    finally:
        if test_directory is not None:
            compose_command = [
                docker,
                "compose",
                "--env-file",
                str(test_directory / ".env.single"),
                "--project-directory",
                str(test_directory),
                "--file",
                str(test_directory / "compose.single.test.yaml"),
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
            if cluster_started:
                cluster_command = [
                    docker,
                    "compose",
                    "--env-file",
                    str(test_directory / ".env.cluster"),
                    "--project-directory",
                    str(test_directory),
                    "--file",
                    str(test_directory / "compose.cluster.test.yaml"),
                ]
                run_logged(
                    cluster_command + ["logs", "--no-color"],
                    logs / "cluster-compose-runtime.log",
                    cwd=test_directory,
                    environment=environment,
                    check=False,
                )
                run_logged(
                    cluster_command + ["down", "--remove-orphans"],
                    logs / "cluster-compose-down.log",
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


def cache_state(target: Target, cluster_nodes: int = DEFAULT_CLUSTER_NODES) -> tuple[str, str]:
    report_path = target.cache_directory / "report.json"
    expected_paths = [target.cache_directory / filename for filename in ARTIFACT_FILENAMES]
    present = [path for path in [report_path, *expected_paths] if path.exists()]
    if not present:
        return "missing", ""
    missing = [path.name for path in [report_path, *expected_paths] if not path.is_file()]
    if missing:
        return "invalid", f"missing files: {', '.join(missing)}"
    try:
        report = read_json(report_path)
    except (OSError, json.JSONDecodeError) as error:
        return "invalid", f"unreadable report: {error}"
    if report.get("schema_version") != SCHEMA_VERSION:
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
        "environment_example": ".env.example",
    }
    for key, filename in artifact_names.items():
        artifact = report.get("artifacts", {}).get(key, {})
        path = target.cache_directory / filename
        if artifact.get("filename") != filename or artifact.get("sha256") != sha256_file(path):
            return "invalid", f"artifact metadata does not match {filename}"
    return "valid", ""


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
        for filename in ARTIFACT_FILENAMES:
            source = report_path.parent / filename
            if not source.is_file():
                raise DockerToolError(f"Cached report is missing {source}")
            shutil.copy2(source, destination / filename)
        with contextlib.suppress(FileNotFoundError):
            (destination / "compose.yaml").unlink()
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
            "cached": cache_state(target)[0] == "valid",
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
    refresh.add_argument("--cluster-nodes", type=int, default=DEFAULT_CLUSTER_NODES)
    refresh.add_argument(
        "--force",
        action="store_true",
        help="Regenerate and retest even when a complete cached result exists",
    )
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
        if options.cluster_nodes < 2 or options.cluster_nodes > 253:
            raise DockerToolError("--cluster-nodes must be between 2 and 253")

        failures = 0
        for index, target in enumerate(targets, start=1):
            state, reason = cache_state(target, options.cluster_nodes)
            if state == "valid" and not options.force:
                print(f"[{index}/{len(targets)}] SKIPPED {target.image} (complete cache exists)")
                continue
            if state == "invalid" and not options.force:
                raise DockerToolError(
                    f"Incomplete or incompatible cache for {target.image}: {reason}; use --force to regenerate"
                )
            print(f"[{index}/{len(targets)}] Refreshing {target.image}", flush=True)
            passed = refresh_target(
                target,
                options.timeout,
                options.keep_test_workdir,
                options.cluster_nodes,
            )
            print(f"[{index}/{len(targets)}] {'PASSED' if passed else 'FAILED'} {target.image}", flush=True)
            failures += int(not passed)
        return 1 if failures else 0
    except (DockerToolError, OSError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
