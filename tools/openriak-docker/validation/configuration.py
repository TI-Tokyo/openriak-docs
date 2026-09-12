"""Validation configuration operations."""
from __future__ import annotations
from core.state import StepReport
import http.client
import io
import json
import os
import pathlib
import re
import shutil
import socket
import subprocess
import tempfile
import time
from typing import Any, Callable, Iterable
from core.defaults import DEFAULT_TIMEOUT_SECONDS
import images.minimal as minimal


def verify_runtime_options(tool, container: str, target: Target, timeout_seconds: int, log_path: pathlib.Path) -> dict[str, Any]:
    docker = tool.docker_command()
    output = tool.run_logged(
        [docker, "exec", container, "sh", "-c",
         "date +%z\nid -u riak\nid -g riak\nstat -c '%u:%g' /etc/riak /var/lib/riak /var/log/riak"],
        log_path, timeout_seconds=timeout_seconds,
    ).stdout.splitlines()
    if output != ["+0900", "19001", "19002", "19001:19002", "19001:19002", "19001:19002"]:
        raise tool.DockerToolError(f"Timezone or UID/GID checks failed for {container}: {output!r}")
    inspection = json.loads(tool.run_logged(
        [docker, "container", "inspect", container], log_path, timeout_seconds=timeout_seconds,
    ).stdout)[0]
    labels = inspection["Config"].get("Labels", {})
    if any(labels.get(key) != value for key, value in tool.image_labels(target).items()):
        raise tool.DockerToolError(f"Image identification labels do not match {container}")
    logging = inspection["HostConfig"]["LogConfig"]
    if (logging.get("Type") != "json-file" or logging.get("Config", {}).get("max-size") != "10m"
            or logging.get("Config", {}).get("max-file") != "3"):
        raise tool.DockerToolError(f"Docker log rotation is not configured for {container}")
    result = {"status": "passed", "timezone": "Asia/Tokyo", "uid": 19001, "gid": 19002,
              "labels": labels, "docker_logging": logging}
    minimal_check = minimal.runtime_check(target)
    if minimal_check:
        tool.run_logged([docker, "exec", container, "sh", "-ec", minimal_check],
                   log_path, timeout_seconds=timeout_seconds)
        result["runtime_filesystem"] = {"status": "passed", **minimal.configuration(target)}
    if target.family in {"suse", "sles"}:
        tool.run_logged([docker, "exec", container, "sh", "-ec", """test ! -e /usr/bin/container-suseconnect
if rpm -q container-suseconnect >/dev/null 2>&1
then
    echo 'Unexpected SUSE registration helper in runtime image' >&2
    exit 1
fi"""], log_path, timeout_seconds=timeout_seconds)
        result["dependencies"] = {"container-suseconnect": "absent"}
    if target.family == "alpine":
        # Assert the final runtime image is curl-free while retaining coreutils.
        tool.run_logged([docker, "exec", container, "sh", "-ec", """if command -v curl >/dev/null 2>&1
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


def verify_admin_test(tool, container: str, timeout_seconds: int, log_path: pathlib.Path) -> dict[str, Any]:
    result = tool.run_logged(
        [tool.docker_command(), "exec", container, "riak", "admin", "test"],
        log_path,
        timeout_seconds=timeout_seconds,
    )
    if not re.search(r"Successfully completed [1-9][0-9]* read/write cycles? to ", result.stdout):
        raise tool.DockerToolError(f"riak admin test did not confirm a read/write cycle (see {log_path})")
    return {
        "status": "passed",
        "command": "riak admin test",
        "response": result.stdout.strip(),
    }


def set_riak_setting(tool, source: str, key: str, value: str) -> str:
    active = re.compile(rf"^[ \t]*{re.escape(key)}[ \t]*=.*$", re.MULTILINE)
    replacement = f"{key} = {value}"
    if active.search(source):
        return active.sub(replacement, source, count=1)
    commented = re.compile(rf"^[ \t]*##[ \t]*{re.escape(key)}[ \t]*=.*$", re.MULTILINE)
    if commented.search(source):
        return commented.sub(replacement, source, count=1)
    suffix = "" if source.endswith("\n") else "\n"
    return f"{source}{suffix}{replacement}\n"


def configure_test_node(tool, config_path: pathlib.Path, node_name: str) -> None:
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
        source = tool.set_riak_setting(source, key, value)
    config_path.write_text(source, encoding="utf-8", newline="\n")


def effective_riak_settings(tool, config_path: pathlib.Path, keys: Iterable[str]) -> dict[str, str]:
    wanted = set(keys)
    values: dict[str, str] = {}
    for line in config_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^[ \t]*([A-Za-z0-9_.]+)[ \t]*=[ \t]*(.*?)[ \t]*$", line)
        if match and match.group(1) in wanted:
            values[match.group(1)] = match.group(2)
    return values


def populated(tool, path: pathlib.Path) -> bool:
    return path.is_dir() and any(path.iterdir())


def free_tcp_port(tool, ) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as handle:
        handle.bind(("127.0.0.1", 0))
        return int(handle.getsockname()[1])
