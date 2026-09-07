#!/usr/bin/env python3
"""Generate, test, cache, and publish OpenRiak KV Docker configurations."""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime as dt
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

    operating_systems = list(supported.get("operating_systems", []))
    alias_rules = read_json(OS_ALIASES_PATH)
    native_families = {item["family"] for item in operating_systems}
    native_ids = {item["id"] for item in operating_systems}
    for source in supported.get("operating_systems", []):
        if source["family"] != alias_rules["source_family"]:
            continue
        for alias in alias_rules["aliases"]:
            if alias.get("docker") is False:
                continue
            if alias.get("nativeFamily", alias["family"]) in native_families:
                continue
            release = alias.get("modernReleases", alias.get("releases", {})).get(str(source["release"]))
            alias_release = release["id"] if release else source["release"]
            alias_id = f"{alias['family']}-{alias_release}-{source['architecture']}"
            if alias_id in native_ids:
                continue
            operating_systems.append({
                **source,
                "id": alias_id,
                "family": alias["family"],
                "release": alias_release,
                "display_name": f"{alias.get('name', alias['family'])} {release['version'] if release else alias_release}",
                "alias_of": source["id"],
            })

    targets: list[Target] = []
    for operating_system in operating_systems:
        os_id = operating_system["id"]
        package_os_id = operating_system.get("alias_of", os_id)
        for download_id, package in downloads.get("downloads", {}).get(package_os_id, {}).items():
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
    try:
        config = read_json(BASE_IMAGES_PATH)
        if config.get("schema_version") != 1:
            raise ValueError("unsupported schema_version")
        families = config["families"]
        family = target.family
        visited = set()
        while True:
            if family in visited:
                raise ValueError(f"cyclic family alias: {family}")
            visited.add(family)
            entry = families[family]
            if "alias" not in entry:
                break
            family = entry["alias"]
        release = target.release
        for old, new in entry.get("release_replacements", {}).items():
            release = release.lower().replace(old, new)
        if "release_map" in entry:
            mapping = config["release_maps"][entry["release_map"]]
            if entry.get("require_release_mapping") and release not in mapping:
                raise ValueError(f"No release-specific image mapping for {target.family} {target.release}")
            release = mapping.get(release, release)
        major = release.split(".")[0]
        for rule in entry["rules"]:
            if "architectures" in rule and target.architecture not in rule["architectures"]:
                continue
            if "minimum_major" in rule and int(major) < rule["minimum_major"]:
                continue
            image = rule["image"].format(release=release, os_release=target.release,
                                         major=major, architecture=target.architecture)
            # A release tag is mandatory; refresh resolves its immutable digest.
            if not re.fullmatch(r"[a-z0-9][a-z0-9./:_-]*:[A-Za-z0-9_][A-Za-z0-9_.-]*", image) or image.rsplit(":", 1)[1].lower() == "latest":
                raise ValueError(f"Expected a release-specific base image tag, got {image!r}")
            return image
        raise ValueError(f"No base-image rule matches architecture {target.architecture}")
    except (KeyError, TypeError, ValueError, AttributeError, OSError) as error:
        raise DockerToolError(f"Invalid base-image configuration {BASE_IMAGES_PATH} for {target.family} {target.release}: {error}") from error


def package_install_script(target: Target) -> str:
    filename = target.package["filename"]
    if not re.fullmatch(r"[A-Za-z0-9_.+-]+", filename):
        raise DockerToolError(f"Unsafe package filename in metadata: {filename}")
    package_path = f"/tmp/{filename}"
    package_family = target.operating_system["package_family"]
    if package_family == "apk":
        return f"""# Update installed OS packages from this release's configured repositories.
apk upgrade --no-cache
apk add --no-cache bash ca-certificates coreutils su-exec shadow tzdata
apk add --no-cache --allow-untrusted {package_path}
rm -f {package_path}"""
    if package_family == "deb":
        return f"""# Update installed OS packages from this release's configured repositories.
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y --no-install-recommends
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates passwd procps tzdata {package_path}
apt-get clean
rm -rf /var/lib/apt/lists/*
rm -f {package_path}"""
    if package_family == "rpm":
        if target.family in {"amazon-linux", "oracle-linux", "rhel", "rocky", "centos", "fedora", "suse", "sles"}:
            repository_setup = ""
            if target.family == "centos" and target.release == "8":
                repository_setup = r"""# CentOS Stream 8 repositories were moved to the release archive.
sed -i 's|^mirrorlist=|#mirrorlist=|' /etc/yum.repos.d/CentOS-Stream-*.repo
sed -i 's|^#baseurl=http://mirror.centos.org/\$contentdir/\$stream/|baseurl=https://vault.centos.org/8-stream/|' /etc/yum.repos.d/CentOS-Stream-*.repo
"""
            dependencies = (
                "bash ca-certificates glibc hostname libgcc libstdc++ ncurses-libs "
                "openssl-libs pam procps-ng shadow-utils sudo util-linux zlib tzdata"
            )
            suse_openssl = "libopenssl3" if target.operating_system.get("alias_of", "").startswith("rhel-9-") else "libopenssl1_1"
            return f"""{repository_setup}# Update installed OS packages before installing the OpenRiak KV package.
if command -v dnf >/dev/null 2>&1
then
    dnf upgrade --refresh -y
    dnf install -y {dependencies}
    dnf clean all
elif command -v microdnf >/dev/null 2>&1
then
    microdnf upgrade --refresh -y
    microdnf install -y dnf
    dnf install -y {dependencies}
    dnf clean all
elif command -v yum >/dev/null 2>&1
then
    yum clean expire-cache
    yum update -y
    yum install -y {dependencies}
    yum clean all
elif command -v zypper >/dev/null 2>&1
then
    zypper --non-interactive refresh
    zypper --non-interactive update --no-recommends
    zypper --non-interactive install --no-recommends bash ca-certificates gawk glibc hostname libgcc_s1 libstdc++6 libncurses6 {suse_openssl} pam procps shadow sudo util-linux libz1 timezone
    zypper clean --all
else
    echo 'No supported RPM package manager found' >&2
    exit 1
fi
# These RPMs bundle their matching OTP runtime, including escript, but their
# generated dependency metadata requires /usr/bin/escript outside the payload.
rpm -Uvh --replacepkgs --nodeps {package_path}
if [ ! -e /usr/bin/escript ]
then
    for bundled_escript in /usr/lib64/riak/erts-*/bin/escript /usr/lib/riak/erts-*/bin/escript
    do
        if [ -x "$bundled_escript" ]
        then
            ln -s "$bundled_escript" /usr/bin/escript
            break
        fi
    done
fi
test -x /usr/bin/escript
# Check the bundled runtime and its OpenSSL NIF before starting integration tests.
for bundled_erl in /usr/lib64/riak/erts-*/bin/erl /usr/lib/riak/erts-*/bin/erl
do
    if [ -x "$bundled_erl" ]
    then
        runtime_root=${{bundled_erl%/erts-*}}
        "$bundled_erl" +S 2:2 -boot "$runtime_root/bin/no_dot_erlang" -pa "$runtime_root"/lib/crypto-*/ebin -noshell -eval 'crypto:strong_rand_bytes(1), halt().'
        break
    fi
done
# Clear caches from every package manager used in this installation layer.
# In particular, dnf clean all does not clear microdnf's /var/cache/yum.
rm -rf /var/cache/dnf /var/cache/yum /var/cache/zypp
rm -f {package_path}"""
        return f"""# Update installed OS packages before installing the OpenRiak KV package.
if command -v dnf >/dev/null 2>&1
then
    dnf upgrade --refresh -y
    dnf install -y ca-certificates procps-ng shadow-utils tzdata {package_path}
    dnf clean all
elif command -v microdnf >/dev/null 2>&1
then
    microdnf upgrade --refresh -y
    microdnf install -y ca-certificates procps-ng shadow-utils tzdata {package_path}
    microdnf clean all
elif command -v yum >/dev/null 2>&1
then
    yum clean expire-cache
    yum update -y
    yum install -y ca-certificates procps-ng shadow-utils tzdata {package_path}
    yum clean all
elif command -v zypper >/dev/null 2>&1
then
    zypper --non-interactive refresh
    zypper --non-interactive update --no-recommends
    zypper --non-interactive install -y ca-certificates procps timezone {package_path}
    zypper clean --all
else
    echo 'No supported RPM package manager found' >&2
    exit 1
fi
# Clear caches from every package manager used in this installation layer.
# In particular, dnf clean all does not clear microdnf's /var/cache/yum.
rm -rf /var/cache/dnf /var/cache/yum /var/cache/zypp
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
export RUNNER_LOG_DIR="$log_dir" # Keep daemon logs in the mounted directory owned by the runtime UID.
log() {
    printf '%s [openriak-entrypoint] %s\n' "$(date +'%Y-%m-%dT%H:%M:%S%:z')" "$*"
}

one_line() {
    tr '\n' ' ' | sed 's/[[:space:]][[:space:]]*/ /g; s/[[:space:]]$//'
}

configure_timezone() {
    TZ=${TZ:-Etc/UTC}
    case "$TZ" in
        /*|*..*|*[!A-Za-z0-9_+/-]*|'')
            log "configuration: invalid timezone: $TZ"
            exit 1
            ;;
    esac
    if [ ! -f "/usr/share/zoneinfo/$TZ" ]
    then
        log "configuration: unknown timezone: $TZ"
        exit 1
    fi
    export TZ
    log "configuration: timezone = $TZ"
}

configure_identity() {
    requested_uid=${RIAK_UID:-$(id -u riak)}
    requested_gid=${RIAK_GID:-$(id -g riak)}
    for identity in "$requested_uid" "$requested_gid"
    do
        if ! printf '%s\\n' "$identity" | grep -Eq '^[1-9][0-9]{0,9}$' || [ "$identity" -ge 4294967295 ]
        then
            log "configuration: UID/GID must be a nonzero numeric ID below 4294967295"
            exit 1
        fi
    done
    uid_owner=$(getent passwd "$requested_uid" | cut -d: -f1 || true)
    gid_owner=$(getent group "$requested_gid" | cut -d: -f1 || true)
    if [ -n "$uid_owner" ] && [ "$uid_owner" != "riak" ]
    then
        log "configuration: requested UID belongs to $uid_owner"
        exit 1
    fi
    if [ -n "$gid_owner" ] && [ "$gid_owner" != "riak" ]
    then
        log "configuration: requested GID belongs to $gid_owner"
        exit 1
    fi
    if [ "$(id -g riak)" != "$requested_gid" ]
    then
        groupmod -g "$requested_gid" riak
        usermod -g "$requested_gid" riak
    fi
    if [ "$(id -u riak)" != "$requested_uid" ]
    then
        usermod -u "$requested_uid" riak
    fi
    log "configuration: riak UID/GID = $requested_uid/$requested_gid"
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
    admin_command=
    for admin_candidate in /usr/lib64/riak/bin/riak-admin /usr/lib/riak/bin/riak-admin
    do
        [ -x "$admin_candidate" ] || continue
        admin_command=$admin_candidate
        break
    done
    if [ -z "$admin_command" ]
    then
        log "cluster: packaged riak-admin executable is not available"
        return 1
    fi
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
        VMARGS_PATH="$admin_vmargs" su-exec riak "$admin_command" "$@"
        return
    fi
    if command -v runuser >/dev/null 2>&1
    then
        VMARGS_PATH="$admin_vmargs" runuser -u riak -- "$admin_command" "$@"
        return
    fi
    su -s /bin/sh riak -c "VMARGS_PATH='$admin_vmargs' '$admin_command' $*"
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
    for beam_pid in $(pgrep -x beam.smp 2>/dev/null)
    do
        beam_stat=$(cat "/proc/$beam_pid/stat" 2>/dev/null) || continue
        beam_stat=${beam_stat##*) }
        case "$beam_stat" in
            Z*|X*) continue ;;
        esac
        return 0
    done
    return 1
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
        $1 == expected || $1 == "::ffff:" expected { found = 1 }
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
    case "$control_path" in
        *-coordinator)
            printf 'cookie=%s\\n' "$RIAK_DISTRIBUTED_COOKIE" >> "$control_temporary"
            ;;
    esac
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

# Read only live settings; a disabled ## setting is not an established cookie.
configured_cookie() {
    [ -s "$config_dir/riak.conf" ] || return 0
    awk -F= '
        /^[[:space:]]*distributed_cookie[[:space:]]*=/ {
            sub(/^[^=]*=[[:space:]]*/, "")
            sub(/[[:space:]]*$/, "")
            print
            exit
        }
    ' "$config_dir/riak.conf"
}

validate_cookie() {
    printf '%s\\n' "$1" | grep -Eq '^[A-Za-z0-9_.@+-]+$'
}

coordinator_cookie() {
    marker=$1
    marker_node=$(control_value "$marker" nodename)
    marker_ip=$(control_value "$marker" ip)
    marker_suffix=$(control_value "$marker" suffix)
    marker_owner=$(control_value "$marker" coordinator)
    marker_cookie=$(control_value "$marker" cookie)
    validate_nodename "$marker_node" || return 1
    validate_ipv4 "$marker_ip" || return 1
    validate_cookie "$marker_cookie" || return 1
    [ "$marker_owner" = "$marker_node" ] || return 1
    printf '%s\\n' "$marker_suffix" | grep -Eq '^[0-9a-f]{16}$' || return 1
    [ "$marker" = "$control_dir/${marker_node}-${marker_suffix}-coordinator" ] || return 1
    nodename_resolves_to_ip "$marker_node" "$marker_ip" || return 1
    printf '%s\\n' "$marker_cookie"
}

wait_for_coordinator_cookie() {
    cookie_waited=0
    cookie_timeout=${OPENRIAK_CLUSTER_WAIT_SECONDS:-300}
    cookie_poll=${OPENRIAK_CLUSTER_POLL_SECONDS:-1}
    while :
    do
        cookie_count=0
        selected_cookie=
        for marker in "$control_dir/"*-coordinator
        do
            [ -f "$marker" ] || continue
            if candidate_cookie=$(coordinator_cookie "$marker")
            then
                cookie_count=$((cookie_count + 1))
                selected_cookie=$candidate_cookie
            fi
        done
        if [ "$cookie_count" -eq 1 ]
        then
            RIAK_DISTRIBUTED_COOKIE=$selected_cookie
            export RIAK_DISTRIBUTED_COOKIE
            log "configuration: adopted coordinator cookie before daemon startup"
            return
        fi
        if [ "$cookie_count" -gt 1 ]
        then
            log "configuration: multiple valid coordinators; refusing ambiguous cookie"
            exit 1
        fi
        if [ "$cookie_waited" -ge "$cookie_timeout" ]
        then
            log "configuration: timed out waiting for a valid coordinator cookie"
            exit 1
        fi
        log "configuration: waiting for coordinator cookie before daemon startup"
        sleep "$cookie_poll"
        cookie_waited=$((cookie_waited + cookie_poll))
    done
}

configure_timezone
configure_identity

existing_cookie=$(configured_cookie)
if [ -e "$config_dir/.openriak-cookie-pending" ]
then
    existing_cookie=
fi
initialize_config=0
log "configuration: preparing mounted directories"
mkdir -p "$config_dir" "$data_dir" "$log_dir" /run/riak
if [ ! -s "$config_dir/riak.conf" ]
then
    log "configuration: seeding /etc/riak from packaged defaults"
    touch "$config_dir/.openriak-cookie-pending"
    touch "$config_dir/.openriak-config-pending"
    cp -a "$defaults_dir/." "$config_dir/"
else
    log "configuration: using existing /etc/riak/riak.conf"
fi

if [ -e "$config_dir/.openriak-config-pending" ]
then
    initialize_config=1
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

# Existing configuration, including intentionally disabled settings, is authoritative.
initialize_setting() {
    if [ "${initialize_config:-0}" = "1" ]
    then
        set_setting "$1" "$2"
    else
        log "configuration: preserving $1 from existing riak.conf"
    fi
}

configured_nodename() {
    awk '
        /^[[:space:]]*nodename[[:space:]]*=/ {
            sub(/^[^=]*=[[:space:]]*/, "")
            sub(/[[:space:]]*$/, "")
            print
            exit
        }
    ' "$config_dir/riak.conf"
}

node_host=${RIAK_NODE_HOST:-$(hostname)}
riak_node_name=${RIAK_NODE_NAME:-openriak-kv@$node_host}
if [ "$initialize_config" = "0" ]
then
    saved_nodename=$(configured_nodename)
    if [ -z "$saved_nodename" ]
    then
        log "configuration: existing riak.conf requires a live nodename setting"
        exit 1
    fi
    riak_node_name=$saved_nodename
fi
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
cluster_mode=${OPENRIAK_CLUSTER_MODE:-single}
role_value=${role:-follower}
case "$cluster_mode:$role_value" in
    single:*|cluster:coordinator|cluster:follower) ;;
    *) log "configuration: invalid cluster mode or role"; exit 1 ;;
esac
if [ "$cluster_mode" = "cluster" ]
then
    mkdir -p "$control_dir"
    if [ "$role_value" = "coordinator" ]
    then
        # Remove old coordinator sessions before any new cookie is advertised.
        for stale_file in "$control_dir/"*-coordinator "$control_dir/"*-ready "$control_dir/"*-approved "$control_dir/"*-joined "$control_dir/"*-complete "$control_dir/"*-failed
        do
            [ -e "$stale_file" ] || continue
            rm -f "$stale_file"
        done
    else
        clean_owned_control_files
    fi
fi
if [ -n "$existing_cookie" ]
then
    RIAK_DISTRIBUTED_COOKIE=$existing_cookie
    export RIAK_DISTRIBUTED_COOKIE
    log "configuration: preserving distributed cookie from existing riak.conf"
elif [ "$cluster_mode" = "cluster" ] && [ "$role_value" = "follower" ] && [ "${RIAK_INIT_ONLY:-0}" != "1" ]
then
    touch "$config_dir/.openriak-cookie-pending"
    wait_for_coordinator_cookie
fi
if ! validate_cookie "$RIAK_DISTRIBUTED_COOKIE"
then
    log "configuration: invalid distributed cookie"
    exit 1
fi
initialize_setting nodename "$riak_node_name"
if [ -z "$existing_cookie" ]
then
    set_setting distributed_cookie "$RIAK_DISTRIBUTED_COOKIE"
fi
if [ "$cluster_mode" != "cluster" ] || [ "$role_value" = "coordinator" ] || [ "${RIAK_INIT_ONLY:-0}" != "1" ]
then
    rm -f "$config_dir/.openriak-cookie-pending"
fi
log "configuration: effective distributed cookie = ${RIAK_DISTRIBUTED_COOKIE}"
initialize_setting ring_size "$RIAK_RING_SIZE"
initialize_setting storage_backend "$RIAK_STORAGE_BACKEND"
initialize_setting anti_entropy "$RIAK_ANTI_ENTROPY"
initialize_setting tictacaae_active "$RIAK_TICTACAAE_ACTIVE"
initialize_setting tictacaae_storeheads "$RIAK_TICTACAAE_STOREHEADS"
initialize_setting listener.http.internal "$RIAK_HTTP_LISTENER"
initialize_setting listener.protobuf.internal "$RIAK_PB_LISTENER"

initialize_setting logger.max_file_size "${RIAK_LOG_MAX_FILE_SIZE:-1MB}"
initialize_setting logger.max_files "${RIAK_LOG_MAX_FILES:-10}"
rm -f "$config_dir/.openriak-config-pending"

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
    if ! beam_running
    then
        log "startup: BEAM exited while waiting for the riak_kv service"
        tail -n 80 /var/log/riak/console.log 2>/dev/null || true
        exit 1
    fi
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
            if [ "$(control_value "$coordinator_file" cookie)" != "$RIAK_DISTRIBUTED_COOKIE" ]
            then
                log "cluster: coordinator cookie differs from preserved node cookie; refusing join"
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
    return "".join(f'      {name}: "${{{name}:-{default}}}"\n' for name, (default, _) in RUNTIME_OPTIONS.items())


def compose_resource_options() -> str:
    return '''    # Optional per-node resource limits; zero leaves the resource unrestricted.
    cpus: "${OPENRIAK_CPUS:-0}"
    mem_limit: "${OPENRIAK_MEMORY_LIMIT:-0}"
    # Rotate Docker stdout/stderr logs separately from OpenRiak KV file logs.
    logging:
      driver: json-file
      options:
        max-size: "${OPENRIAK_DOCKER_LOG_MAX_SIZE:-10m}"
        max-file: "${OPENRIAK_DOCKER_LOG_MAX_FILES:-3}"
'''


def image_labels(target: Target) -> dict[str, str]:
    return {
        "org.opencontainers.image.title": "OpenRiak KV",
        "org.opencontainers.image.description": "Package-backed OpenRiak KV with single-node and cluster startup support",
        "org.opencontainers.image.version": target.version,
        "org.opencontainers.image.vendor": target.identity.vendor,
        "org.opencontainers.image.url": target.identity.url,
        "org.opencontainers.image.source": target.identity.source,
        "org.openriak.otp.version": target.otp,
        "org.openriak.os.name": target.family,
        "org.openriak.os.release": target.release,
        "org.openriak.os.version": str(target.operating_system.get("release_version") or target.release),
        "org.openriak.image.tag": target.image,
    }


def render_image_labels(target: Target) -> str:
    lines = []
    for key, value in image_labels(target).items():
        quoted = json.dumps(value).replace("$", r"\$")
        lines.append(f"LABEL {key}={quoted}")
    return "\n".join(lines)


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
    canonical = re.sub(r"^OPENRIAK_NODE_\d+_", "OPENRIAK_", name)
    if canonical == "OPENRIAK_HOST":
        canonical = "RIAK_NODE_HOST"
    if canonical == "OPENRIAK_CONTAINER_NAME" and "_NODE_" in name:
        return "Docker container name for this cluster node."
    if canonical not in SETTING_COMMENTS and canonical.startswith("OPENRIAK_"):
        canonical = canonical.replace("OPENRIAK_", "RIAK_", 1)
    return SETTING_COMMENTS[canonical]


def annotate_artifact(contents: str, kind: str, image: str) -> str:
    """Add documentation only, preserving every executable/configuration line."""
    notice = [
        "# Created by TI Tokyo, www.tiot.jp, for the OpenRiak project at https://openriak.org",
        "# WARNING: Edit only if you understand the effect of your changes.",
        f"# Original image tag: {image}",
    ]
    lines = contents.splitlines()
    lines = [line for line in lines if not line.startswith("# Generated and tested by tools/openriak-docker/")]
    insertion = 1 if lines and lines[0].startswith("# syntax=") else 0
    lines[insertion:insertion] = notice
    output = []
    for line in lines:
        match = None
        if kind == "Dockerfile":
            match = re.match(r"ENV ([A-Za-z_][A-Za-z_0-9]*)=", line)
        elif kind == "example.env":
            match = re.match(r"([A-Za-z_][A-Za-z_0-9]*)=", line)
        else:
            match = re.match(r"      ((?:RIAK_|OPENRIAK_)[A-Z_0-9]+|role|TZ):", line)
        if match:
            indent = line[:len(line) - len(line.lstrip())]
            output.append(f"{indent}# {setting_comment(match[1])}")
        output.append(line)
    return "\n".join(output) + "\n"


def render_dockerfile(
    target: Target,
    pinned_base_image: str,
    distributed_cookie: str | None = None,
) -> str:
    distributed_cookie = distributed_cookie or generate_distributed_cookie()
    checksum = target.package["checksum"]["value"]
    filename = target.package["filename"]
    package_url = target.package["url"]
    runtime_defaults = "\n".join(f"ENV {name}={json.dumps(default)}" for name, (default, _) in RUNTIME_OPTIONS.items())
    return annotate_artifact(f"""# syntax=docker/dockerfile:1.7
# Generated and tested by tools/openriak-docker/openriak-docker. Do not edit by hand.
# Download and verify in a separate stage; its layers are not in the final image.
FROM scratch AS download
ADD --checksum=sha256:{checksum} {package_url} /{filename}

FROM --platform={target.platform} {pinned_base_image}

{render_image_labels(target)}

# -----------------------------------------------------------------------------
# OpenRiak KV default settings
# Environment settings initialize new configurations; existing riak.conf is preserved.
# -----------------------------------------------------------------------------
{runtime_defaults}
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

RUN --mount=type=bind,from=download,target=/opt/openriak-package,ro <<'OPENRIAK_PACKAGE_INSTALL'
set -eu
# Copy, install, and remove in this one layer; only the installed files persist.
cp /opt/openriak-package/{filename} /tmp/{filename}
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
# Health probe interval, maximum duration, startup allowance, and failure threshold.
HEALTHCHECK --interval={target.lifecycle_options.healthcheck_interval}s --timeout={target.lifecycle_options.healthcheck_timeout}s --start-period={target.lifecycle_options.healthcheck_start_period}s --retries={target.lifecycle_options.healthcheck_retries} CMD ["/usr/local/bin/openriak-healthcheck"]
STOPSIGNAL SIGTERM
ENTRYPOINT ["/usr/local/bin/openriak-entrypoint"]
""", "Dockerfile", target.image)


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
    return annotate_artifact(f"""# Generated and tested by tools/openriak-docker/openriak-docker. Do not edit by hand.
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
{compose_runtime_options()}      RIAK_NODE_HOST: "${{OPENRIAK_NODE_1_HOST:-{host}}}"
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
{compose_resource_options()}    # Time allowed for graceful OpenRiak KV shutdown before Docker sends SIGKILL.
    stop_grace_period: {target.lifecycle_options.stop_grace_period}s

networks:
  openriak:
    driver: bridge
""", "compose.single.yaml", target.image)


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
{compose_runtime_options()}      OPENRIAK_CLUSTER_MODE: cluster
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
{compose_resource_options()}    # Time allowed for graceful OpenRiak KV shutdown before Docker sends SIGKILL.
    stop_grace_period: {target.lifecycle_options.stop_grace_period}s
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
    return annotate_artifact(f"""# Generated and tested by tools/openriak-docker/openriak-docker. Do not edit by hand.
# Set role=coordinator on exactly one service. An omitted or empty role is a follower.
name: {target.node_name}-cluster

services:
{services}

networks:
  openriak:
    driver: bridge
""", "compose.cluster.yaml", target.image)


def render_environment_example(
    target: Target,
    distributed_cookie: str,
    node_count: int = DEFAULT_CLUSTER_NODES,
) -> str:
    lines = [
        "# Copy this file to .env before running either Compose file.",
        "# All values below match the generated defaults and may be edited.",
        "# Every member of one cluster must use the same distributed cookie.",
        *(f"{name}={default}" for name, (default, _) in {**RUNTIME_OPTIONS, **COMPOSE_OPTIONS}.items()),
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
    return annotate_artifact("\n".join(lines), "example.env", target.image)


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
    log_path.parent.mkdir(parents=True, exist_ok=True)
    started = isoformat()
    try:
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
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as error:
        output = error.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        with log_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(f"$ {' '.join(command)}\n")
            handle.write(f"started: {started}\n")
            handle.write(f"timeout_seconds: {timeout_seconds}\nexit_code: timeout\n")
            handle.write(output)
            if output and not output.endswith("\n"):
                handle.write("\n")
        raise DockerToolError(
            f"Command timed out after {timeout_seconds}s: {' '.join(command)} "
            f"(see {log_path})"
        ) from error
    with log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(f"$ {' '.join(command)}\n")
        handle.write(f"started: {started}\nexit_code: {result.returncode}\n")
        handle.write(result.stdout)
        if result.stdout and not result.stdout.endswith("\n"):
            handle.write("\n")
    if check and result.returncode != 0:
        failure_lines = [line.strip() for line in result.stdout.splitlines() if "ERROR:" in line or "error:" in line]
        summary = failure_lines[-1] if failure_lines else result.stdout.strip()[-300:]
        raise DockerToolError(
            f"Command failed with exit code {result.returncode}: {' '.join(command)} "
            f"(see {log_path}): {summary}"
        )
    return result


def verify_runtime_options(container: str, target: Target, timeout_seconds: int, log_path: pathlib.Path) -> dict[str, Any]:
    docker = docker_command()
    output = run_logged(
        [docker, "exec", container, "sh", "-c",
         "date +%z\nid -u riak\nid -g riak\nstat -c '%u:%g' /etc/riak /var/lib/riak /var/log/riak"],
        log_path, timeout_seconds=timeout_seconds,
    ).stdout.splitlines()
    if output != ["+0900", "19001", "19002", "19001:19002", "19001:19002", "19001:19002"]:
        raise DockerToolError(f"Timezone or UID/GID checks failed for {container}: {output!r}")
    inspection = json.loads(run_logged(
        [docker, "container", "inspect", container], log_path, timeout_seconds=timeout_seconds,
    ).stdout)[0]
    labels = inspection["Config"].get("Labels", {})
    if any(labels.get(key) != value for key, value in image_labels(target).items()):
        raise DockerToolError(f"Image identification labels do not match {container}")
    logging = inspection["HostConfig"]["LogConfig"]
    if (logging.get("Type") != "json-file" or logging.get("Config", {}).get("max-size") != "10m"
            or logging.get("Config", {}).get("max-file") != "3"):
        raise DockerToolError(f"Docker log rotation is not configured for {container}")
    result = {"status": "passed", "timezone": "Asia/Tokyo", "uid": 19001, "gid": 19002,
              "labels": labels, "docker_logging": logging}
    if target.family == "alpine":
        # Assert the final runtime image is curl-free while retaining coreutils.
        run_logged([docker, "exec", container, "sh", "-ec", """if command -v curl >/dev/null 2>&1
then
    echo 'Unexpected curl executable in Alpine image' >&2
    exit 1
fi
for package in curl libcurl
do
    if apk info -e "$package" >/dev/null 2>&1
    then
        echo "Unexpected $package package in Alpine image" >&2
        exit 1
    fi
done
for library in /usr/lib/libcurl.so*
do
    test ! -e "$library"
done
apk info -e coreutils
"""], log_path, timeout_seconds=timeout_seconds)
        result["dependencies"] = {"curl": "absent", "libcurl": "absent", "coreutils": "installed"}
    return result


def verify_admin_test(container: str, timeout_seconds: int, log_path: pathlib.Path) -> dict[str, Any]:
    result = run_logged(
        [docker_command(), "exec", container, "riak", "admin", "test"],
        log_path,
        timeout_seconds=timeout_seconds,
    )
    if not re.search(r"Successfully completed [1-9][0-9]* read/write cycles? to ", result.stdout):
        raise DockerToolError(f"riak admin test did not confirm a read/write cycle (see {log_path})")
    return {
        "status": "passed",
        "command": "riak admin test",
        "response": result.stdout.strip(),
    }


def digest_from_pull_output(output: str) -> str | None:
    match = re.search(
        r"^Digest:[ \t]*(sha256:[0-9a-f]{64})[ \t]*$",
        output,
        re.MULTILINE,
    )
    return match.group(1) if match else None


def resolve_base_image(
    target: Target,
    logs: pathlib.Path,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> tuple[str, str]:
    docker = docker_command()
    base = base_image_for(target)
    pull_result = run_logged(
        [docker, "pull", "--platform", target.platform, base],
        logs / "base-image-pull.log",
        timeout_seconds=timeout_seconds,
    )
    result = run_logged(
        [docker, "image", "inspect", "--format", "{{json .RepoDigests}}", base],
        logs / "base-image-inspect.log",
        timeout_seconds=timeout_seconds,
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


def remaining_timeout(deadline: float) -> float:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise DockerToolError("Docker readiness wait reached its timeout")
    return remaining


def run_before_deadline(command: list[str], deadline: float, **kwargs: Any) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, timeout=remaining_timeout(deadline), **kwargs)
    except subprocess.TimeoutExpired as error:
        raise DockerToolError(f"Docker readiness command exceeded the wait timeout: {' '.join(command)}") from error


# Use the package's existing Erlang runtime; no HTTP client package is needed.
# HTTP/1.0 plus Connection: close lets gen_tcp collect the complete response.
HTTP_PROBE_ERLANG = r"""
Timeout = list_to_integer(os:getenv("OPENRIAK_HTTP_PROBE_TIMEOUT_MS")),
case gen_tcp:connect({127,0,0,1}, 8098, [binary, {active,false}], Timeout) of
    {ok, Socket} ->
        ok = gen_tcp:send(Socket, <<"GET /ping HTTP/1.0\r\nHost: localhost\r\nConnection: close\r\n\r\n">>),
        Receive = fun Again() ->
            case gen_tcp:recv(Socket, 0, Timeout) of
                {ok, Data} -> ok = file:write(standard_io, Data), Again();
                {error, closed} -> halt(0);
                {error, Reason} -> io:format(standard_error, "HTTP receive failed: ~p~n", [Reason]), halt(1)
            end
        end,
        Receive();
    {error, Reason} ->
        io:format(standard_error, "HTTP connect failed: ~p~n", [Reason]), halt(1)
end.
"""
HTTP_PROBE_COMMAND = """set -eu
export OPENRIAK_HTTP_PROBE_TIMEOUT_MS="$2"
for bundled_erl in /usr/lib64/riak/erts-*/bin/erl /usr/lib/riak/erts-*/bin/erl
do
    if [ -x "$bundled_erl" ]
    then
        runtime_root=${bundled_erl%/erts-*}
        exec "$bundled_erl" +S 1:1 +SDcpu 1 +SDio 1 +A 1 -boot "$runtime_root/bin/no_dot_erlang" -noshell -eval "$1"
    fi
done
echo 'Bundled Erlang runtime not found for HTTP probe' >&2
exit 1
"""


def container_http_ping(container_name: str, timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS) -> tuple[int, str, int]:
    deadline = time.monotonic() + timeout_seconds
    result = run_before_deadline(
        [docker_command(), "exec", container_name, "sh", "-c", HTTP_PROBE_COMMAND,
         "openriak-http-probe", HTTP_PROBE_ERLANG, str(max(1, int(timeout_seconds * 1000)))],
        deadline=deadline,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        return result.returncode, result.stderr.decode("utf-8", errors="replace").strip(), 0

    class ProbeSocket:
        def makefile(self, mode: str) -> io.BytesIO:
            return io.BytesIO(result.stdout)

    try:
        with http.client.HTTPResponse(ProbeSocket()) as response:
            response.begin()
            return 0, response.read().decode("utf-8", errors="replace").strip(), response.status
    except (http.client.HTTPException, ValueError, OSError) as error:
        return 1, f"Invalid HTTP probe response: {error}", 0


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
            cli = run_before_deadline(
                [docker, "exec", container_name, "riak", "ping"],
                deadline=deadline,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            last_cli = cli.stdout.strip()
            http_exit, last_http, http_status = container_http_ping(container_name, remaining_timeout(deadline))
            http_ok = http_exit == 0 and http_status == 200 and last_http == "OK"
            log.write(
                f"{isoformat()} cli_exit={cli.returncode} cli={last_cli!r} "
                f"http_exit={http_exit} http_status={http_status} http={last_http!r}\n"
            )
            log.flush()
            if cli.returncode == 0 and last_cli == "pong" and http_ok:
                return last_cli, last_http
            time.sleep(min(2, max(0, deadline - time.monotonic())))
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
            result = run_before_deadline(
                [docker, "logs", container_name],
                deadline=deadline,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            last_output = result.stdout
            found = result.returncode == 0 and marker in last_output
            state = run_before_deadline(
                [
                    docker,
                    "container",
                    "inspect",
                    "--format",
                    "{{.State.Running}} {{.State.ExitCode}}",
                    container_name,
                ],
                deadline=deadline,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            state_output = state.stdout.strip()
            state_parts = state_output.split()
            running = (
                state.returncode == 0
                and len(state_parts) >= 1
                and state_parts[0] == "true"
            )
            log.write(
                f"{isoformat()} logs_exit={result.returncode} marker_found={found} "
                f"inspect_exit={state.returncode} state={state_output!r}\n"
            )
            log.flush()
            if state.returncode == 0 and not running:
                exit_code = state_parts[1] if len(state_parts) >= 2 else "unknown"
                output_tail = "\n".join(last_output.strip().splitlines()[-20:]) or "<empty>"
                raise DockerToolError(
                    f"Container {container_name!r} exited with code {exit_code} before "
                    f"its log contained {marker!r}; last log output:\n{output_tail}"
                )
            if found and running:
                return last_output
            time.sleep(min(1, max(0, deadline - time.monotonic())))
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
            result = run_before_deadline(
                [
                    docker,
                    "container",
                    "inspect",
                    "--format",
                    "{{if .State.Health}}{{.State.Health.Status}}{{else}}missing{{end}}",
                    container_name,
                ],
                deadline=deadline,
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
            time.sleep(min(1, max(0, deadline - time.monotonic())))
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
                running = run_before_deadline(
                    [
                        docker,
                        "container",
                        "inspect",
                        "--format",
                        "{{.State.Running}} {{.State.ExitCode}}",
                        container_name,
                    ],
                    deadline=deadline,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    encoding="utf-8",
                    errors="replace",
                    check=False,
                )
                running_state = running.stdout.strip()
                if running.returncode != 0 or not running_state.startswith("true "):
                    state[container_name] = {
                        "ready": False,
                        "running": running_state,
                    }
                    last_state = state
                    log.write(f"{isoformat()} {json.dumps(state, sort_keys=True)}\n")
                    log.flush()
                    raise DockerToolError(
                        f"OpenRiak cluster container {container_name!r} stopped "
                        f"before the cluster became ready; state={running_state!r}"
                    )
                commands = {
                    "members": ["riak", "admin", "member-status"],
                    "ring": ["riak", "admin", "ringready"],
                    "transfers": ["riak", "admin", "transfers"],
                    "ping": ["riak", "ping"],
                }
                outputs: dict[str, dict[str, Any]] = {}
                for name, arguments in commands.items():
                    result = run_before_deadline(
                        [docker, "exec", container_name, *arguments],
                        deadline=deadline,
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
                http_exit, http_body, http_status = container_http_ping(container_name, remaining_timeout(deadline))
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
            time.sleep(min(2, max(0, deadline - time.monotonic())))
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
    base_url = "." if target.output_root is not None else f"downloads/docker/{target.version}/{target.image_tag}"
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
            "filename": "example.env",
            "url": f"{base_url}/example.env",
            "sha256": sha256_file(environment_example),
        },
    }


def sync_download_metadata(versions: Iterable[str], timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> None:
    versions = sorted(set(versions), key=semver_key)
    if not versions:
        return
    node = shutil.which("node")
    if not node:
        raise DockerToolError("Node.js is required to update Docker download metadata; install Node.js and run sync-static")
    command = [node, str(REPOSITORY_ROOT / "tools/scripts/sync-product-metadata.js"), "--docker-only"]
    for version in versions:
        command.extend(["--include-version", f"openriak-kv={version}"])
    try:
        result = subprocess.run(command, cwd=REPOSITORY_ROOT, text=True, capture_output=True, timeout=timeout_seconds)
    except subprocess.TimeoutExpired as error:
        raise DockerToolError(f"Docker download metadata update timed out after {timeout_seconds}s; cached test results are retained") from error
    if result.returncode:
        raise DockerToolError(f"Could not update Docker download metadata: {result.stderr.strip()}; cached test results are retained")
    print("".join(f"{log_timestamp()} {line}\n" for line in result.stdout.splitlines() if line.strip()), end="", flush=True)


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

    if target.grouped or target.output_root is not None:
        return

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
    sync_download_metadata([target.version])


def initial_report(
    target: Target,
    identifier: str,
    cluster_nodes: int,
    distributed_cookie: str,
) -> dict[str, Any]:
    package = target.package
    return {
        "schema_version": MULTIARCH_SCHEMA_VERSION if target.grouped else SCHEMA_VERSION,
        "identity": dataclasses.asdict(target.identity),
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
            *([str(OS_ALIASES_PATH.relative_to(REPOSITORY_ROOT))]
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
    progress: Callable[[str], None] | None = None,
    prepared: dict[str, Any] | None = None,
) -> bool:
    identifier = run_id()
    run_root = target.cache_directory / "runs" / identifier
    logs = run_root / "logs"
    run_root.mkdir(parents=True, exist_ok=False)
    distributed_cookie = prepared["distributed_cookie"] if prepared else generate_distributed_cookie()
    report = initial_report(target, identifier, cluster_nodes, distributed_cookie)
    build_image_tag = (f"{target.identity.namespace}/openriak-kv:test-{target.image_tag}-{target.platform.replace('/', '-')}-{identifier.lower()}"
                       if prepared else target.image)
    dockerfile = run_root / "Dockerfile"
    compose_single = run_root / "compose.single.yaml"
    compose_cluster = run_root / "compose.cluster.yaml"
    environment_example = run_root / "example.env"
    test_directory: pathlib.Path | None = None
    compose_started = False
    cluster_started = False
    # Test containers must never inherit operator bind paths, identities, or cookies.
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith(("OPENRIAK_", "RIAK_")) and key not in {"role", "TZ"}}
    docker = docker_command()

    def report_progress(message: str) -> None:
        if progress is not None:
            progress(message)

    try:
        if prepared:
            report["base_image"] = prepared["base_images"][target.platform]
            pinned_base = report["base_image"]["pinned"]
        else:
            report_progress(f"Pulling and pinning base image (timeout {timeout_seconds}s)")
            base, pinned_base = record_step(
                report,
                "pull_and_pin_base_image",
                lambda: resolve_base_image(target, logs, timeout_seconds),
            )
            report["base_image"] = {
                "requested": base,
                "pinned": pinned_base,
                "resolved_at": isoformat(),
            }
        report_progress("Creating Dockerfile, compose YAML files and .env for this run")

        def generate() -> None:
            if prepared:
                for filename in ARTIFACT_FILENAMES:
                    shutil.copy2(target.group_directory / filename, run_root / filename)
                return
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
                    timeout_seconds=timeout_seconds,
                )

        record_step(report, "validate_compose_artifacts", validate_compose_artifacts)
        report_progress(f"Building image (timeout {timeout_seconds}s)")
        record_step(
            report,
            "build_image",
            lambda: run_logged(
                [
                    docker,
                    *( ["buildx", "build", "--builder", MULTIARCH_BUILDER, "--load"] if prepared else ["build"] ),
                    "--platform",
                    target.platform,
                    "--pull=false",
                    "--tag",
                    build_image_tag,
                    "--file",
                    str(dockerfile),
                    str(run_root),
                ],
                logs / "image-build.log",
                timeout_seconds=timeout_seconds,
            ),
        )

        report_progress(f"Testing single node (timeout {timeout_seconds}s)")
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
        if prepared:
            for compose_test in (compose_single_test, compose_cluster_test):
                text = compose_test.read_text()
                text = text.replace(f"    image: {target.image}\n", f"    image: {build_image_tag}\n    platform: {target.platform}\n")
                if compose_test == compose_cluster_test:
                    service_index = 0
                    lines = []
                    for line in text.splitlines():
                        match = re.match(r"  node([0-9]+):", line)
                        if match:
                            service_index = int(match.group(1))
                        if service_index > 1 and line.startswith("      RIAK_DISTRIBUTED_COOKIE:"):
                            line = f'      RIAK_DISTRIBUTED_COOKIE: "{generate_distributed_cookie()}"'
                        lines.append(line)
                    text = "\n".join(lines) + "\n"
                compose_test.write_text(text)
        shutil.copy2(dockerfile, test_directory / "Dockerfile")
        shutil.copy2(environment_example, test_directory / "example.env")
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
        runtime_test_environment = [
            "TZ=Asia/Tokyo", "RIAK_UID=19001", "RIAK_GID=19002",
            "RIAK_LOG_MAX_FILE_SIZE=2MB", "RIAK_LOG_MAX_FILES=4",
        ]
        cluster_environment_lines = [
            *runtime_test_environment,
            "OPENRIAK_CLUSTER_POLL_SECONDS=1",
            f"OPENRIAK_CLUSTER_WAIT_SECONDS={timeout_seconds}",
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
                    *runtime_test_environment,
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
            timeout_seconds=timeout_seconds,
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
                timeout_seconds=timeout_seconds,
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
                timeout_seconds=timeout_seconds,
            ),
        )
        record_step(
            report,
            "configure_node",
            lambda: configure_test_node(config_path, default_node_host(1)),
        )
        preserved_test_cookie = generate_distributed_cookie()
        if prepared:
            config_path.write_text(set_riak_setting(config_path.read_text(), "distributed_cookie", preserved_test_cookie))
        # An operator-edited setting must survive startup despite a different ENV default.
        config_path.write_text(set_riak_setting(config_path.read_text(), "logger.max_files", "7"))
        preserved_config_hash = sha256_file(config_path)
        expected_settings = {
            "logger.max_file_size": "2MB",
            "logger.max_files": "7",
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
                timeout_seconds=timeout_seconds,
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
        if sha256_file(config_path) != preserved_config_hash:
            raise DockerToolError("Startup changed the existing riak.conf")
        report["tests"]["preserved_configuration"] = {"status": "passed", "sha256": preserved_config_hash}
        report["tests"]["runtime_options"] = record_step(
            report, "verify_runtime_options",
            lambda: verify_runtime_options(test_container_name, target, timeout_seconds, logs / "runtime-options.log"),
        )
        if prepared:
            actual_cookie = effective_riak_settings(config_path, ["distributed_cookie"]).get("distributed_cookie")
            if actual_cookie != preserved_test_cookie:
                raise DockerToolError("Startup replaced the existing distributed cookie")
            report["tests"]["preserved_cookie"] = {"status": "passed", "configuration_cookie": actual_cookie}
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
        report["tests"]["admin_test"] = record_step(
            report,
            "single_node_admin_test",
            lambda: verify_admin_test(test_container_name, timeout_seconds, logs / "admin-test.log"),
        )
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
                compose_command + ["stop", "--timeout", str(min(timeout_seconds, target.lifecycle_options.stop_grace_period))],
                logs / "compose-stop.log",
                cwd=test_directory,
                environment=environment,
                timeout_seconds=timeout_seconds,
            ),
        )
        stopped_logs = record_step(
            report,
            "verify_graceful_shutdown_logging",
            lambda: run_logged(
                [docker, "logs", test_container_name],
                logs / "graceful-shutdown.log",
                timeout_seconds=timeout_seconds,
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
                compose_command + ["down", "--remove-orphans", "--timeout", str(min(timeout_seconds, target.lifecycle_options.stop_grace_period))],
                logs / "compose-down.log",
                cwd=test_directory,
                environment=environment,
                timeout_seconds=timeout_seconds,
            ),
        )
        compose_started = False

        report_progress(
            f"Testing {cluster_nodes}-node cluster (timeout {timeout_seconds}s)"
        )
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
                timeout_seconds=timeout_seconds,
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
                timeout_seconds=timeout_seconds,
            ),
        )
        cluster_state = record_step(
            report,
            "wait_for_cluster",
            lambda: wait_for_cluster(
                cluster_container_names,
                cluster_nodenames,
                timeout_seconds,
                logs / "cluster-readiness.log",
            ),
        )
        cluster_admin_tests: dict[str, Any] = {}
        report["tests"]["cluster_admin_test"] = cluster_admin_tests
        report["tests"]["cluster_runtime_options"] = {}
        role_logs: dict[str, str] = {}
        for index, cluster_container_name in enumerate(cluster_container_names, start=1):
            container_logs = run_logged(
                [docker, "logs", cluster_container_name],
                logs / f"cluster-node-{index}.log",
                timeout_seconds=timeout_seconds,
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
            cluster_admin_tests[cluster_container_name] = record_step(
                report,
                f"cluster_node_{index}_admin_test",
                lambda: verify_admin_test(
                    cluster_container_name, timeout_seconds, logs / f"cluster-node-{index}-admin-test.log"
                ),
            )
            report["tests"]["cluster_runtime_options"][cluster_container_name] = record_step(
                report, f"cluster_node_{index}_runtime_options",
                lambda: verify_runtime_options(cluster_container_name, target, timeout_seconds, logs / f"cluster-node-{index}-runtime-options.log"),
            )
            if prepared:
                cookie_result = run_logged(
                    [docker, "exec", cluster_container_name, "cat", "/etc/riak/riak.conf"],
                    logs / f"cluster-node-{index}-configuration.log", timeout_seconds=timeout_seconds,
                ).stdout
                expected_cookie = re.search(r"(?m)^distributed_cookie\s*=\s*(\S+)\s*$", cookie_result)
                if not expected_cookie or expected_cookie.group(1) != distributed_cookie:
                    raise DockerToolError(f"Cluster node {index} did not retain the coordinator cookie")
                if index > 1 and "adopted coordinator cookie before daemon startup" not in container_logs:
                    raise DockerToolError(f"Cluster node {index} did not log cookie adoption before startup")
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
                "riak admin test read/write cycle",
                "Docker healthcheck healthy",
                "config/data/log volumes populated",
            ],
            "state": cluster_state,
            "coordinator_cookie_adoption": "passed" if prepared else "not tested",
        }
        record_step(
            report,
            "graceful_stop_cluster",
            lambda: run_logged(
                cluster_command + ["stop", "--timeout", str(min(timeout_seconds, target.lifecycle_options.stop_grace_period))],
                logs / "cluster-compose-stop.log",
                cwd=test_directory,
                environment=environment,
                timeout_seconds=timeout_seconds,
            ),
        )
        record_step(
            report,
            "remove_cluster_test",
            lambda: run_logged(
                cluster_command + ["down", "--remove-orphans", "--timeout", str(min(timeout_seconds, target.lifecycle_options.stop_grace_period))],
                logs / "cluster-compose-down.log",
                cwd=test_directory,
                environment=environment,
                timeout_seconds=timeout_seconds,
            ),
        )
        cluster_started = False
        report["artifacts"] = artifact_downloads(
            target, dockerfile, compose_single, compose_cluster, environment_example
        )
        report["status"] = "passed"
    except KeyboardInterrupt:
        report["status"] = "interrupted"
        report["error"] = {"type": "KeyboardInterrupt", "message": "Refresh stopped by operator"}
        raise
    except Exception as error:
        report["status"] = "failed"
        report["error"] = {"type": type(error).__name__, "message": str(error)}
        report_progress(f"FAILED {target.platform}: {error}")
    finally:
        def cleanup_command(*args: Any, **kwargs: Any) -> None:
            try:
                result = run_logged(*args, **kwargs)
                if result.returncode:
                    raise DockerToolError(f"Cleanup command failed: {' '.join(args[0])}; see {args[1]}")
            except (DockerToolError, OSError) as error:
                report.setdefault("cleanup_errors", []).append(str(error))
                if report["status"] != "interrupted":
                    report["status"] = "failed"
                report_progress(f"Cleanup failed: {error}")

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
                cleanup_command(
                    compose_command + ["logs", "--no-color"],
                    logs / "compose-runtime.log",
                    cwd=test_directory,
                    environment=environment,
                    check=False,
                    timeout_seconds=timeout_seconds,
                )
                cleanup_command(
                    compose_command + ["down", "--remove-orphans", "--timeout", str(min(timeout_seconds, target.lifecycle_options.stop_grace_period))],
                    logs / "compose-down.log",
                    cwd=test_directory,
                    environment=environment,
                    check=False,
                    timeout_seconds=timeout_seconds,
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
                cleanup_command(
                    cluster_command + ["logs", "--no-color"],
                    logs / "cluster-compose-runtime.log",
                    cwd=test_directory,
                    environment=environment,
                    check=False,
                    timeout_seconds=timeout_seconds,
                )
                cleanup_command(
                    cluster_command + ["down", "--remove-orphans", "--timeout", str(min(timeout_seconds, target.lifecycle_options.stop_grace_period))],
                    logs / "cluster-compose-down.log",
                    cwd=test_directory,
                    environment=environment,
                    check=False,
                    timeout_seconds=timeout_seconds,
                )
            for node_logs in test_directory.glob("*/logs"):
                if node_logs.is_dir():
                    shutil.copytree(node_logs, logs / "riak-runtime" / node_logs.parent.name, dirs_exist_ok=True)
            if keep_workdir or report.get("cleanup_errors"):
                report["test_workdir"] = str(test_directory)
            else:
                shutil.rmtree(test_directory, ignore_errors=True)
        if prepared:
            cleanup_command([docker, "image", "rm", build_image_tag], logs / "remove-test-image.log",
                            check=False, timeout_seconds=timeout_seconds)
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


def report_artifact_filenames(report: dict[str, Any]) -> tuple[str, ...]:
    environment = report.get("artifacts", {}).get("environment_example", {}).get("filename")
    return (*ARTIFACT_FILENAMES[:3], ".env.example" if environment == ".env.example" else "example.env")


def cache_state(target: Target, cluster_nodes: int = DEFAULT_CLUSTER_NODES) -> tuple[str, str]:
    report_path = target.cache_directory / "report.json"
    try:
        report = read_json(report_path) if report_path.exists() else {}
    except (OSError, json.JSONDecodeError) as error:
        return "invalid", f"unreadable report: {error}"
    expected_paths = [target.cache_directory / filename for filename in report_artifact_filenames(report)]
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
    if report.get("schema_version") != (MULTIARCH_SCHEMA_VERSION if target.grouped else SCHEMA_VERSION):
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
        "environment_example": report_artifact_filenames(report)[-1],
    }
    for key, filename in artifact_names.items():
        artifact = report.get("artifacts", {}).get(key, {})
        path = target.cache_directory / filename
        if artifact.get("filename") != filename or artifact.get("sha256") != sha256_file(path):
            return "invalid", f"artifact metadata does not match {filename}"
    return "valid", ""


def sync_static() -> int:
    copied = 0
    versions = set()
    for report_path, report in cached_current_reports():
        versions.add(report["target"]["version"])
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
        for filename in report_artifact_filenames(report):
            source = report_path.parent / filename
            if not source.is_file():
                raise DockerToolError(f"Cached report is missing {source}")
            shutil.copy2(source, destination / filename)
        with contextlib.suppress(FileNotFoundError):
            (destination / "compose.yaml").unlink()
        copied += 1
    for group in grouped_targets(discover_targets()):
        report_path = group[0].group_directory / "report.json"
        if report_path.is_file():
            report = read_json(report_path)
            if report.get("status") == "passed":
                identity = ImageIdentity(**report.get("identity", {}))
                publish_group([dataclasses.replace(t, identity=identity) for t in group], report)
                copied += 1
    sync_download_metadata(versions)
    return copied


def grouped_targets(targets: list[Target]) -> list[list[Target]]:
    groups: dict[str, dict[str, Target]] = {}
    for original in targets:
        target = dataclasses.replace(original, grouped=True)
        platforms = groups.setdefault(target.image, {})
        if target.platform in platforms and platforms[target.platform].package != target.package:
            raise DockerToolError(f"Ambiguous packages for {target.image} {target.platform}")
        platforms[target.platform] = target
    return [list(sorted(platforms.values(), key=lambda t: t.platform)) for _, platforms in sorted(groups.items())]


def release_key(target: Target) -> tuple[int, ...]:
    release = str(target.operating_system.get("release_version", target.release))
    numbers = tuple(int(part) for part in re.findall(r"\d+", release))
    if not numbers:
        raise DockerToolError(f"Metadata needs release_version to order {target.family} {release}")
    return numbers


def image_aliases(target: Target, all_targets: list[Target]) -> list[str]:
    """Aliases are selected from metadata, never from whichever build finishes last."""
    target = dataclasses.replace(target, grouped=True)
    tags = [target.image]
    peers = [t for t in all_targets if t.version == target.version and t.family == target.family]
    same_release = [t for t in peers if t.release == target.release]
    otp_key = lambda t: tuple(int(n) for n in t.otp.split("."))
    if otp_key(target) != max(map(otp_key, same_release)):
        return tags
    prefix = f"{target.identity.namespace}/openriak-kv:{target.version}"
    tags.append(f"{prefix}-{target.family}-{target.release}")
    if release_key(target) != max(map(release_key, peers)):
        return tags
    tags.append(f"{prefix}-{target.family}")
    if target.family == "alpine":
        tags.append(prefix)
        if semver_key(target.version) == max(semver_key(t.version) for t in all_targets):
            tags.append(f"{target.identity.namespace}/openriak-kv:latest")
    return tags


def render_multiarch_dockerfile(
    targets: list[Target], base_images: dict[str, dict[str, str]], cookie: str, tags: list[str],
) -> str:
    if not targets or len({(t.version, t.family, t.release, t.otp) for t in targets}) != 1:
        raise DockerToolError("A shared Dockerfile requires one version, OS release, and OTP")
    if len({t.platform.split("/")[1] for t in targets}) != len(targets):
        raise DockerToolError("Multiple variants of the same TARGETARCH require separate image groups")
    stages = []
    for target in sorted(targets, key=lambda t: t.platform):
        stage = target.platform.split("/")[1]
        pinned = base_images[target.platform]["pinned"]
        if not re.search(r"@sha256:[0-9a-f]{64}$", pinned):
            raise DockerToolError(f"Unpinned base image for {target.platform}")
        checksum = target.package["checksum"]["value"]
        stages.append(f'''# {target.platform}: official package and immutable OS release base.
# Download layers stay outside the final image; the install only mounts them.
FROM scratch AS download-{stage}
ADD --checksum=sha256:{checksum} {target.package['url']} /{target.package['filename']}

FROM --platform={target.platform} {pinned} AS package-{stage}
RUN --mount=type=bind,from=download-{stage},target=/opt/openriak-package,ro <<'OPENRIAK_PACKAGE_INSTALL'
set -eu
# Copy, install, and remove in this one layer; only the installed files persist.
cp /opt/openriak-package/{target.package['filename']} /tmp/{target.package['filename']}
{package_install_script(target)}
OPENRIAK_PACKAGE_INSTALL
''')
    reference = render_dockerfile(targets[0], base_images[targets[0].platform]["pinned"], cookie)
    defaults = reference[reference.index("# -----------------------------------------------------------------------------"):reference.index("RUN --mount=")]
    runtime = reference[reference.index("RUN <<'OPENRIAK_IMAGE_SETUP'"):]
    header = annotate_artifact("# syntax=docker/dockerfile:1.7\n", "Dockerfile", targets[0].image)
    header += "# Supported platforms: " + ", ".join(t.platform for t in targets) + "\n"
    header += "# Image tags: " + ", ".join(tags) + "\n"
    header += "# BuildKit supplies TARGETARCH from --platform in the global scope.\n# Do not redeclare ARG TARGETARCH here: that clears its automatic value.\n\n"
    return header + "\n".join(stages) + '\nFROM package-${TARGETARCH} AS final\n\n' + render_image_labels(targets[0]) + '\n\n' + defaults + runtime


class MultiarchBuilderLifecycle:
    """Restore builder state once per invocation, including interrupted builds."""

    def __init__(self) -> None:
        self.logs: pathlib.Path | None = None
        self.timeout = 0
        self.stop_required = False

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
        if self.stop_required:
            print(f"{log_timestamp()} Stopping builder {MULTIARCH_BUILDER} started for this refresh", flush=True)
            run_logged([docker_command(), "buildx", "stop", MULTIARCH_BUILDER],
                       self.logs / "builder.log", timeout_seconds=self.timeout)


def ensure_multiarch_builder(
    logs: pathlib.Path, timeout: int, lifecycle: MultiarchBuilderLifecycle | None = None,
) -> None:
    docker = docker_command()
    inspected = run_logged([docker, "buildx", "inspect", MULTIARCH_BUILDER], logs / "builder.log", check=False, timeout_seconds=timeout)
    if lifecycle is not None:
        lifecycle.observe(inspected, logs, timeout)
    if inspected.returncode:
        run_logged([docker, "buildx", "create", "--name", MULTIARCH_BUILDER, "--driver", "docker-container"], logs / "builder.log", timeout_seconds=timeout)
        if lifecycle is not None:
            lifecycle.stop_required = True
    run_logged([docker, "buildx", "inspect", MULTIARCH_BUILDER, "--bootstrap"], logs / "builder.log", timeout_seconds=timeout)


def group_input(targets: list[Target], cluster_nodes: int, tags: list[str]) -> dict[str, Any]:
    return {
        "schema_version": MULTIARCH_SCHEMA_VERSION,
        "identity": dataclasses.asdict(targets[0].identity),
        "lifecycle_options": dataclasses.asdict(targets[0].lifecycle_options),
        "labels": image_labels(targets[0]),
        "runtime_options": {k: list(v) for k, v in RUNTIME_OPTIONS.items()},
        "compose_options": {k: list(v) for k, v in COMPOSE_OPTIONS.items()},
        "cluster_nodes": cluster_nodes,
        "tags": tags,
        "packages": {t.platform: {"url": t.package["url"], "checksum": t.package["checksum"], "base": base_image_for(t)} for t in targets},
        "runtime_sha256": hashlib.sha256((ENTRYPOINT_SCRIPT + HEALTHCHECK_SCRIPT).encode()).hexdigest(),
        "renderer_sha256": hashlib.sha256("\n".join(inspect.getsource(fn) for fn in (
            render_multiarch_dockerfile, render_dockerfile, render_single_compose,
            render_cluster_compose, render_cluster_service, render_environment_example,
            package_install_script, create_riak_user_script, render_image_labels, render_group_assets,
            compose_runtime_options, compose_resource_options, annotate_artifact, setting_comment,
        )).encode()).hexdigest(),
    }


def group_is_passed(targets: list[Target], report: dict[str, Any], inputs: dict[str, Any]) -> bool:
    if report.get("status") != "passed" or report.get("inputs") != inputs:
        return False
    if set(report.get("platform_results", {})) != {t.platform for t in targets}:
        return False
    if any(result.get("status") != "passed" for result in report["platform_results"].values()):
        return False
    root = targets[0].group_directory
    for artifact in report.get("artifacts", {}).values():
        path = root / artifact["filename"]
        if not path.is_file() or sha256_file(path) != artifact["sha256"]:
            return False
    return len(report.get("artifacts", {})) == len(ARTIFACT_FILENAMES)


def publish_group(targets: list[Target], report: dict[str, Any], timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> None:
    if report.get("status") != "passed":
        return
    target = targets[0]
    if target.output_root is not None:
        return
    target.static_directory.mkdir(parents=True, exist_ok=True)
    for artifact in report["artifacts"].values():
        source = target.group_directory / artifact["filename"]
        if sha256_file(source) != artifact["sha256"]:
            raise DockerToolError(f"Grouped artifact checksum mismatch: {source}")
        shutil.copy2(source, target.static_directory / source.name)
    sync_download_metadata([target.version], timeout_seconds=timeout_seconds)


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
    """Validate recorded approval of saved bytes, independently of today's renderer."""
    target = targets[0]
    root = target.group_directory
    path = root / "report.json"
    if not path.is_file():
        raise DockerToolError(f"No approved cache for {target.image}")
    report = read_json(path)
    if (report.get("schema_version") != MULTIARCH_SCHEMA_VERSION
            or report.get("product") != "openriak-kv" or report.get("version") != target.version
            or report.get("image") != target.image or report.get("status") != "passed"
            or set(report.get("platforms", [])) != {t.platform for t in targets}
            or not group_is_passed(targets, report, report.get("inputs", {}))):
        raise DockerToolError(f"No complete, unchanged approval for {target.image}")
    namespaced_tags(report.get("tags", []), [])
    if target.image not in report["tags"]:
        raise DockerToolError(f"Approval is missing the primary image tag: {target.image}")
    keys = ("dockerfile", "compose_single", "compose_cluster", "environment_example")
    for key, filename in zip(keys, ARTIFACT_FILENAMES):
        artifact = report.get("artifacts", {}).get(key, {})
        if artifact.get("filename") != filename or sha256_file(root / filename) != artifact.get("sha256"):
            raise DockerToolError(f"Approved artifact is missing or changed: {root / filename}")
    for platform in report["platforms"]:
        result = report["platform_results"][platform]
        proof_path = (root / result.get("report", "")).resolve()
        if not proof_path.is_relative_to(root.resolve()) or not proof_path.is_file():
            raise DockerToolError(f"Missing platform approval for {target.image} {platform}")
        proof = read_json(proof_path)
        tests = proof.get("tests", {})
        cluster_tests = tests.get("cluster_admin_test", {})
        if (proof.get("schema_version") != MULTIARCH_SCHEMA_VERSION
                or proof.get("product") != "openriak-kv" or proof.get("status") != "passed"
                or proof.get("image") != target.image or proof.get("run_id") != result.get("run_id")
                or proof.get("target", {}).get("docker_platform") != platform
                or tests.get("admin_test", {}).get("status") != "passed"
                or tests.get("preserved_cookie", {}).get("status") != "passed"
                or tests.get("cluster", {}).get("status") != "passed"
                or tests.get("cluster", {}).get("coordinator_cookie_adoption") != "passed"
                or len(cluster_tests) != report.get("cluster_nodes")
                or any(test.get("status") != "passed" for test in cluster_tests.values())):
            raise DockerToolError(f"Incomplete platform approval for {target.image} {platform}")
        for key in keys:
            if proof.get("artifacts", {}).get(key, {}).get("sha256") != report["artifacts"][key]["sha256"]:
                raise DockerToolError(f"Platform approval does not cover current {key}: {target.image} {platform}")
    return report


def build_group_images(
    target: Target, platforms: list[str], tags: list[str], context: pathlib.Path,
    history: pathlib.Path, report: dict[str, Any], timeout: int, no_cache: bool = False,
) -> None:
    docker = docker_command()
    logs = history / "logs"
    tag_args = [part for tag in tags for part in ("--tag", tag)]
    print(f"{log_timestamp()}   Exporting OCI image for {', '.join(platforms)} with {len(tags)} tag(s)", flush=True)
    record_step(report, "export_oci_image", lambda: run_logged(
        [docker, "buildx", "build", "--builder", MULTIARCH_BUILDER, "--platform", ",".join(platforms),
         "--pull=false", *(["--no-cache"] if no_cache else []), *tag_args,
         "--output", f"type=oci,dest={history / 'image.oci.tar'}", str(context)],
        logs / "image-export.log", timeout_seconds=timeout))
    report["oci_archive"] = str((history / "image.oci.tar").relative_to(target.group_directory))
    report["build_tags"] = tags
    host_arch = run_logged([docker, "info", "--format", "{{.Architecture}}"], logs / "host-platform.log", timeout_seconds=timeout).stdout.strip()
    host_platform = ARCHITECTURE_PLATFORMS.get(host_arch)
    if host_platform in platforms:
        # Reuse the just-built layers while loading the host image and every alias.
        record_step(report, "load_local_tags", lambda: run_logged(
            [docker, "buildx", "build", "--builder", MULTIARCH_BUILDER, "--platform", host_platform,
             "--pull=false", "--load", *tag_args, str(context)],
            logs / "local-tags.log", timeout_seconds=timeout))
        report["local_tags_platform"] = host_platform
    else:
        print(f"{log_timestamp()}   No {host_arch} package in this group; all tags are in the OCI archive", flush=True)


def rebuild_approved_group(targets: list[Target], options: argparse.Namespace,
                           builder_lifecycle: MultiarchBuilderLifecycle | None = None) -> bool:
    target = targets[0]
    root = target.group_directory
    approval = approved_group_report(targets)
    tags = namespaced_tags(approval["tags"], options.extra_namespace)
    history = root / "rebuilds" / run_id()
    history.mkdir(parents=True, exist_ok=False)
    report = {
        "schema_version": 1, "operation": "rebuild_without_tests", "status": "running",
        "image": target.image, "build_tags": tags, "platforms": approval["platforms"],
        "started_at": isoformat(), "finished_at": None, "steps": [], "error": None,
        "tests": {"status": "not_run"}, "approved_run_id": approval["run_id"],
        "approved_artifacts": approval["artifacts"],
    }
    write_json(history / "report.json", report)
    write_json(history / "approval.json", approval)
    try:
        # Snapshot approved inputs so another refresh cannot change them during a build.
        for artifact in approval["artifacts"].values():
            destination = history / artifact["filename"]
            shutil.copy2(root / artifact["filename"], destination)
            if sha256_file(destination) != artifact["sha256"]:
                raise DockerToolError(f"Approved file changed during rebuild preparation: {destination.name}")
        (history / ".dockerignore").write_text("*\n")
        ensure_multiarch_builder(history / "logs", options.timeout, builder_lifecycle)
        build_group_images(target, approval["platforms"], tags, history, history, report, options.timeout, no_cache=True)
        report["status"] = "built"
    except KeyboardInterrupt:
        report["status"] = "interrupted"
        report["error"] = "Stopped by operator"
        raise
    except (DockerToolError, OSError) as error:
        report["status"] = "failed"
        report["error"] = str(error)
        print(f"{log_timestamp()}   FAILED: {error}", flush=True)
    finally:
        report["finished_at"] = isoformat()
        write_json(history / "report.json", report)
    return report["status"] == "built"


def refresh_group(targets: list[Target], options: argparse.Namespace, all_targets: list[Target],
                  builder_lifecycle: MultiarchBuilderLifecycle | None = None) -> bool:
    target = targets[0]
    root = target.group_directory
    tags = image_aliases(target, all_targets)
    inputs = group_input(targets, options.cluster_nodes, tags)
    report_path = root / "report.json"
    report = read_json(report_path) if report_path.is_file() else {}
    if group_is_passed(targets, report, inputs) and not options.force:
        print(f"{log_timestamp()} SKIPPED {target.image} (all platforms passed)", flush=True)
        publish_group(targets, report, timeout_seconds=options.timeout)
        return True
    if report and not (options.force or options.retry_failed):
        raise DockerToolError(f"Incomplete or incompatible group {target.image}; use --retry-failed or --force")
    identifier = run_id()
    history = root / "runs" / identifier
    logs = history / "logs"
    history.mkdir(parents=True, exist_ok=False)
    reusable = (
        report.get("inputs") == inputs and not options.force
        and set(report.get("base_images", {})) == {t.platform for t in targets}
        and bool(report.get("distributed_cookie"))
        and all((root / name).is_file() and sha256_file(root / name) == report.get("generated_artifacts", {}).get(name)
                for name in ARTIFACT_FILENAMES)
    )
    previous = report
    report = {
        "schema_version": MULTIARCH_SCHEMA_VERSION, "product": "openriak-kv",
        "status": "running", "image": target.image, "tags": tags,
        "identity": dataclasses.asdict(target.identity),
        "run_id": identifier, "started_at": isoformat(), "finished_at": None,
        "inputs": inputs, "platforms": [t.platform for t in targets],
        "targets": [{"os_id": t.os_id, "download_id": t.download_id, "architecture": t.architecture} for t in targets],
        "version": target.version, "os_family": target.family, "os_release": target.release,
        "os_name": target.operating_system["display_name"], "otp": target.otp,
        "node": target.node_name, "cluster_nodes": options.cluster_nodes,
        "steps": [], "platform_results": {}, "artifacts": {}, "error": None,
    }
    write_json(report_path, report)
    try:
        if reusable:
            report["base_images"] = previous["base_images"]
            report["distributed_cookie"] = previous["distributed_cookie"]
        else:
            report["base_images"] = {}
            report["distributed_cookie"] = generate_distributed_cookie()
            for platform_target in targets:
                print(f"{log_timestamp()}   Pulling {base_image_for(platform_target)} for {platform_target.platform}", flush=True)
                base, pinned = resolve_base_image(platform_target, logs / platform_target.platform.replace("/", "-"), options.timeout)
                report["base_images"][platform_target.platform] = {"requested": base, "pinned": pinned, "resolved_at": isoformat()}
            cookie = report["distributed_cookie"]
            render_group_assets(targets, report["base_images"], cookie, tags, options.cluster_nodes, root)
        report["generated_artifacts"] = {name: sha256_file(root / name) for name in ARTIFACT_FILENAMES}
        for name in ARTIFACT_FILENAMES:
            shutil.copy2(root / name, history / name)
        write_json(report_path, report)
        (root / ".dockerignore").write_text("*\n")
        ensure_multiarch_builder(logs, options.timeout, builder_lifecycle)
        for platform_target in targets:
            state, _ = cache_state(platform_target, options.cluster_nodes)
            matches = state == "valid" and all(sha256_file(platform_target.cache_directory / name) == sha256_file(root / name) for name in ARTIFACT_FILENAMES)
            if matches and not options.force:
                print(f"{log_timestamp()}   SKIPPED {platform_target.platform} (same shared files passed)", flush=True)
                passed = True
            else:
                print(f"{log_timestamp()}   Testing {platform_target.platform} (timeout {options.timeout}s per phase)", flush=True)
                passed = refresh_target(platform_target, options.timeout, options.keep_test_workdir, options.cluster_nodes,
                    lambda message: print(f"{log_timestamp()}     {message}", flush=True), prepared=report)
                print(f"{log_timestamp()}   {'PASSED' if passed else 'FAILED'} {platform_target.platform}", flush=True)
            platform_report = read_json(platform_target.cache_directory / "report.json")
            report["platform_results"][platform_target.platform] = {
                "status": "passed" if passed else "failed", "run_id": platform_report["run_id"],
                "finished_at": platform_report["finished_at"],
                "report": str((platform_target.cache_directory / "runs" / platform_report["run_id"] / "report.json").relative_to(root)),
                "artifacts": platform_report["artifacts"],
            }
            write_json(report_path, report)
        if not all(result["status"] == "passed" for result in report["platform_results"].values()):
            raise DockerToolError("One or more architecture tests failed; shared downloads will not be published")
        build_group_images(target, report["platforms"],
            namespaced_tags(tags, getattr(options, "extra_namespace", [])), root, history, report, options.timeout)
        report["artifacts"] = artifact_downloads(target, *(root / name for name in ARTIFACT_FILENAMES))
        report["status"] = "passed"
    except KeyboardInterrupt:
        report["status"] = "interrupted"
        report["error"] = "Stopped by operator"
        raise
    except (DockerToolError, OSError) as error:
        report["status"] = "failed"
        report["error"] = str(error)
        print(f"{log_timestamp()}   FAILED: {error}", flush=True)
    finally:
        report["finished_at"] = isoformat()
        write_json(report_path, report)
        write_json(history / "report.json", report)
    publish_group(targets, report, timeout_seconds=options.timeout)
    return report["status"] == "passed"

def print_matrix(targets: list[Target], as_json: bool) -> None:
    all_targets = discover_targets()
    selected = {(t.version, t.family, t.release, t.otp) for t in targets}
    groups = grouped_targets([t for t in all_targets if (t.version, t.family, t.release, t.otp) in selected])
    records = []
    for group in groups:
        target = group[0]
        tags = image_aliases(target, all_targets)
        path = target.group_directory / "report.json"
        report = read_json(path) if path.is_file() else {}
        records.append({
            "version": target.version, "os_family": target.family, "os_release": target.release,
            "otp": target.otp, "image": target.image, "tags": tags,
            "platforms": [t.platform for t in group],
            "packages": [{"os_id": t.os_id, "download_id": t.download_id, "platform": t.platform,
                          "url": t.package["url"]} for t in group],
            "cached": group_is_passed(group, report, group_input(group, DEFAULT_CLUSTER_NODES, tags)),
        })
    if as_json:
        print(json.dumps(records, indent=2))
        return
    for record in records:
        marker = "cached" if record["cached"] else "not cached"
        print(f"{record['image']} ({', '.join(record['platforms'])}; {marker})")



def print_refresh_header(
    options: argparse.Namespace,
    targets: list[Target],
    started_at: dt.datetime | None = None,
) -> None:
    versions = "all" if options.all else ", ".join(dict.fromkeys(t.version for t in targets))
    os_selection = options.os_id or "all"
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
    for target in targets:
        if target.output_root is None:
            continue
        paths = [target.group_directory, target.cache_directory,
                 target.group_directory / "runs", target.group_directory / "rebuilds",
                 target.cache_directory / "runs"]
        for directory in (target.group_directory, target.cache_directory):
            paths.extend(directory / name for name in (*ARTIFACT_FILENAMES, "report.json", ".dockerignore"))
        for path in paths:
            if not path.resolve().is_relative_to(target.output_root.resolve()):
                raise DockerToolError(f"Standalone output contains a path or symlink outside its root: {path}")


def identity_from_options(options: argparse.Namespace) -> ImageIdentity:
    defaults = ImageIdentity()
    return ImageIdentity(**{field.name: getattr(options, field.name, None) or getattr(defaults, field.name)
                            for field in dataclasses.fields(ImageIdentity)})


def render_group_assets(targets: list[Target], bases: dict[str, dict[str, str]], cookie: str,
                        tags: list[str], cluster_nodes: int, destination: pathlib.Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    target = targets[0]
    (destination / "Dockerfile").write_text(render_multiarch_dockerfile(targets, bases, cookie, tags))
    (destination / "compose.single.yaml").write_text(render_single_compose(target, cookie))
    (destination / "compose.cluster.yaml").write_text(render_cluster_compose(target, cluster_nodes, cookie))
    (destination / "example.env").write_text(render_environment_example(target, cookie, cluster_nodes))


def generate_group(targets: list[Target], options: argparse.Namespace, all_targets: list[Target]) -> bool:
    """Render standalone files; no build, test approval, or docs publication."""
    target = targets[0]
    if target.output_root is None:
        raise DockerToolError("generate requires a standalone --output path")
    root = target.group_directory
    tags = image_aliases(target, all_targets)
    inputs = group_input(targets, options.cluster_nodes, tags)
    report_path = root / "report.json"
    previous = read_json(report_path) if report_path.is_file() else {}
    if previous and not options.force:
        valid = (previous.get("status") in {"generated", "passed"} and previous.get("inputs") == inputs
                 and len(previous.get("generated_artifacts", {})) == len(ARTIFACT_FILENAMES)
                 and all((root / name).is_file() and sha256_file(root / name) == previous["generated_artifacts"].get(name)
                         for name in ARTIFACT_FILENAMES))
        if valid:
            print(f"{log_timestamp()} SKIPPED {target.image} (unchanged files already exist)", flush=True)
            return True
        raise DockerToolError(f"Output already contains changed or incompatible files; use --force: {root}")
    if not previous and not options.force and any((root / name).exists() for name in ARTIFACT_FILENAMES):
        raise DockerToolError(f"Output contains files without a generation report; use --force: {root}")
    history = root / "runs" / run_id()
    history.mkdir(parents=True, exist_ok=False)
    # Keep any previous current files, including operator edits, before replacement.
    for filename in (*ARTIFACT_FILENAMES, "report.json"):
        if (root / filename).is_file():
            (history / "previous").mkdir(exist_ok=True)
            shutil.copy2(root / filename, history / "previous" / filename)
    report = {
        "schema_version": MULTIARCH_SCHEMA_VERSION, "product": "openriak-kv", "operation": "generate",
        "status": "running", "tests": {"status": "not_run"}, "run_id": history.name,
        "image": target.image, "tags": tags, "identity": dataclasses.asdict(target.identity),
        "version": target.version, "cluster_nodes": options.cluster_nodes, "inputs": inputs,
        "platforms": [t.platform for t in targets], "base_images": {}, "artifacts": {},
        "started_at": isoformat(), "finished_at": None, "steps": [], "error": None,
    }
    try:
        for platform_target in targets:
            requested = base_image_for(platform_target)
            base = None
            if not options.force:
                docs_target = dataclasses.replace(platform_target, identity=ImageIdentity(), output_root=None)
                docs_report_path = docs_target.group_directory / "report.json"
                cached = [previous]
                if docs_report_path.is_file():
                    cached.append(read_json(docs_report_path))
                for candidate in cached:
                    value = candidate.get("base_images", {}).get(platform_target.platform, {})
                    if (value.get("requested") == requested
                            and re.fullmatch(re.escape(requested) + r"@sha256:[0-9a-f]{64}", value.get("pinned", ""))):
                        base = dict(value)
                        print(f"{log_timestamp()}   Reusing recorded base digest for {requested} ({platform_target.platform})", flush=True)
                        break
            if base is None:
                print(f"{log_timestamp()}   Pulling and pinning {requested} for {platform_target.platform}", flush=True)
                requested, pinned = resolve_base_image(platform_target, history / "logs" / platform_target.platform.replace("/", "-"), options.timeout)
                base = {"requested": requested, "pinned": pinned, "resolved_at": isoformat()}
            report["base_images"][platform_target.platform] = base
        report["distributed_cookie"] = generate_distributed_cookie()
        render_group_assets(targets, report["base_images"], report["distributed_cookie"], tags,
                            options.cluster_nodes, history)
        for filename in ARTIFACT_FILENAMES:
            shutil.copy2(history / filename, root / filename)
        (root / ".dockerignore").write_text("*\n")
        report["generated_artifacts"] = {name: sha256_file(root / name) for name in ARTIFACT_FILENAMES}
        report["artifacts"] = artifact_downloads(target, *(root / name for name in ARTIFACT_FILENAMES))
        report["status"] = "generated"
    except KeyboardInterrupt:
        report["status"] = "interrupted"
        report["error"] = "Stopped by operator"
        raise
    except (DockerToolError, OSError) as error:
        report["status"] = "failed"
        report["error"] = str(error)
        print(f"{log_timestamp()} FAILED: {error}", flush=True)
    finally:
        report["finished_at"] = isoformat()
        write_json(history / "report.json", report)
        write_json(report_path, report)
    return report["status"] == "generated"


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
    generate.add_argument("--os-id")
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
    import openriak_cleanup
    openriak_cleanup.configure_parser(subcommands.add_parser("cleanup", help="Preview or remove generator resources older than a supplied cutoff"))
    return result


def main(arguments: list[str] | None = None) -> int:
    options = parser().parse_args(arguments)
    try:
        if options.command == "cleanup":
            import openriak_cleanup
            return openriak_cleanup.main(options, sys.modules[__name__])
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
                    except (DockerToolError, OSError, json.JSONDecodeError) as error:
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
        message = ("Generation stopped by operator; its run record was retained." if options.command == "generate" else
                   "Rebuild stopped by operator; its build record was retained." if getattr(options, "do_not_test", False)
                   else "Refresh stopped by operator; current test cleanup completed.")
        print(message, file=sys.stderr)
        return 130
    except (DockerToolError, OSError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    def stop_refresh(signum: int, frame: Any) -> None:
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop_refresh)
    raise SystemExit(main())
