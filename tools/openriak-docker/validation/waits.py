"""Validation waits operations."""
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


def remaining_timeout(tool, deadline: float) -> float:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise tool.DockerToolError("Docker readiness wait reached its timeout")
    return remaining


def run_before_deadline(tool, command: list[str], deadline: float, **kwargs: Any) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, timeout=tool.remaining_timeout(deadline), **kwargs)
    except subprocess.TimeoutExpired as error:
        raise tool.DockerToolError(f"Docker readiness command exceeded the wait timeout: {' '.join(command)}") from error


def container_http_ping(tool, container_name: str, timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS) -> tuple[int, str, int]:
    deadline = time.monotonic() + timeout_seconds
    result = tool.run_before_deadline(
        [tool.docker_command(), "exec", container_name, "sh", "-c", tool.HTTP_PROBE_COMMAND,
         "openriak-http-probe", tool.HTTP_PROBE_ERLANG, str(max(1, int(timeout_seconds * 1000)))],
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


def wait_for_node(tool,
    container_name: str,
    timeout_seconds: int,
    logs: pathlib.Path,
) -> tuple[str, str]:
    docker = tool.docker_command()
    deadline = time.monotonic() + timeout_seconds
    last_cli = ""
    last_http = ""
    with (logs / "readiness.log").open("w", encoding="utf-8", newline="\n") as log:
        while time.monotonic() < deadline:
            cli = tool.run_before_deadline(
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
            if cli.returncode:
                state = tool.run_before_deadline(
                    [docker, "container", "inspect", "--format",
                     "{{.State.Running}} {{.State.ExitCode}}", container_name],
                    deadline=deadline, text=True, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, encoding="utf-8", errors="replace", check=False,
                )
                state_parts = state.stdout.strip().split()
                if state.returncode == 0 and state_parts and state_parts[0] == "false":
                    exit_code = state_parts[1] if len(state_parts) > 1 else "unknown"
                    log.write(f"{tool.isoformat()} exited={exit_code} cli={last_cli!r}\n")
                    raise tool.DockerToolError(
                        f"Container {container_name!r} exited with code {exit_code} "
                        f"before CLI/HTTP readiness; CLI={last_cli!r}"
                    )
            http_exit, last_http, http_status = tool.container_http_ping(container_name, tool.remaining_timeout(deadline))
            http_ok = http_exit == 0 and http_status == 200 and last_http == "OK"
            log.write(
                f"{tool.isoformat()} cli_exit={cli.returncode} cli={last_cli!r} "
                f"http_exit={http_exit} http_status={http_status} http={last_http!r}\n"
            )
            log.flush()
            if cli.returncode == 0 and last_cli == "pong" and http_ok:
                return last_cli, last_http
            time.sleep(min(2, max(0, deadline - time.monotonic())))
    raise tool.DockerToolError(
        f"OpenRiak node was not ready after {timeout_seconds}s; CLI={last_cli!r}, HTTP={last_http!r}"
    )


def wait_for_container_log(tool,
    container_name: str,
    marker: str,
    timeout_seconds: int,
    log_path: pathlib.Path,
) -> str:
    docker = tool.docker_command()
    deadline = time.monotonic() + timeout_seconds
    last_output = ""
    with log_path.open("w", encoding="utf-8", newline="\n") as log:
        while time.monotonic() < deadline:
            result = tool.run_before_deadline(
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
            state = tool.run_before_deadline(
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
                f"{tool.isoformat()} logs_exit={result.returncode} marker_found={found} "
                f"inspect_exit={state.returncode} state={state_output!r}\n"
            )
            log.flush()
            if state.returncode == 0 and not running:
                exit_code = state_parts[1] if len(state_parts) >= 2 else "unknown"
                output_tail = "\n".join(last_output.strip().splitlines()[-20:]) or "<empty>"
                raise tool.DockerToolError(
                    f"Container {container_name!r} exited with code {exit_code} before "
                    f"its log contained {marker!r}; last log output:\n{output_tail}"
                )
            if found and running:
                return last_output
            time.sleep(min(1, max(0, deadline - time.monotonic())))
    raise tool.DockerToolError(
        f"Container log did not contain {marker!r} after {timeout_seconds}s"
    )


def wait_for_container_health(tool,
    container_name: str,
    timeout_seconds: int,
    log_path: pathlib.Path,
) -> str:
    docker = tool.docker_command()
    deadline = time.monotonic() + timeout_seconds
    last_status = "unknown"
    with log_path.open("w", encoding="utf-8", newline="\n") as log:
        while time.monotonic() < deadline:
            result = tool.run_before_deadline(
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
                f"{tool.isoformat()} exit={result.returncode} health={last_status!r}\n"
            )
            log.flush()
            if result.returncode == 0 and last_status == "healthy":
                return last_status
            time.sleep(min(1, max(0, deadline - time.monotonic())))
    raise tool.DockerToolError(
        f"Container healthcheck did not become healthy after {timeout_seconds}s; status={last_status!r}"
    )


def wait_for_cluster(tool,
    container_names: list[str],
    expected_nodenames: list[str],
    timeout_seconds: int,
    log_path: pathlib.Path,
) -> dict[str, Any]:
    docker = tool.docker_command()
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
                running = tool.run_before_deadline(
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
                    log.write(f"{tool.isoformat()} {json.dumps(state, sort_keys=True)}\n")
                    log.flush()
                    raise tool.DockerToolError(
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
                    result = tool.run_before_deadline(
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
                http_exit, http_body, http_status = tool.container_http_ping(container_name, tool.remaining_timeout(deadline))
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
            log.write(f"{tool.isoformat()} {json.dumps(state, sort_keys=True)}\n")
            log.flush()
            if all_ready:
                return state
            time.sleep(min(2, max(0, deadline - time.monotonic())))
    raise tool.DockerToolError(
        f"OpenRiak cluster was not ready after {timeout_seconds}s; last state={last_state!r}"
    )
