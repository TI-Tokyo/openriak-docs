"""Testing operations; dependencies are supplied by the public tool facade."""
from __future__ import annotations
from openriak_state import StepReport
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
from openriak_defaults import DEFAULT_TIMEOUT_SECONDS
import openriak_minimal as minimal
DEFAULT_CLUSTER_NODES = 5


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


def refresh_target(tool,
    target: Target,
    timeout_seconds: int,
    keep_workdir: bool = False,
    cluster_nodes: int = DEFAULT_CLUSTER_NODES,
    progress: Callable[[str], None] | None = None,
    prepared: dict[str, Any] | None = None,
) -> bool:
    identifier = tool.run_id()
    run_root = target.cache_directory / "runs" / identifier
    logs = run_root / "logs"
    run_root.mkdir(parents=True, exist_ok=False)
    distributed_cookie = prepared["distributed_cookie"] if prepared else tool.generate_distributed_cookie()
    report = StepReport(tool.initial_report(target, identifier, cluster_nodes, distributed_cookie),
                        lambda value: tool.write_json(run_root / "report.json", value))
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
    docker = tool.docker_command()

    def report_progress(message: str) -> None:
        if progress is not None:
            progress(message)

    try:
        if prepared:
            report["base_image"] = prepared["base_images"][target.platform]
            pinned_base = report["base_image"]["pinned"]
        else:
            report_progress(f"Pulling and pinning base image (timeout {timeout_seconds}s)")
            base, pinned_base = tool.record_step(
                report,
                "pull_and_pin_base_image",
                lambda: tool.resolve_base_image(target, logs, timeout_seconds),
            )
            report["base_image"] = {
                "requested": base,
                "pinned": pinned_base,
                "resolved_at": tool.isoformat(),
            }
        report_progress("Creating Dockerfile, compose YAML files and .env for this run")

        def generate() -> None:
            if prepared:
                for filename in tool.ARTIFACT_FILENAMES:
                    shutil.copy2(target.group_directory / filename, run_root / filename)
                return
            dockerfile.write_text(
                tool.render_dockerfile(target, pinned_base, distributed_cookie),
                encoding="utf-8",
                newline="\n",
            )
            compose_single.write_text(
                tool.render_single_compose(target, distributed_cookie),
                encoding="utf-8",
                newline="\n",
            )
            compose_cluster.write_text(
                tool.render_cluster_compose(target, cluster_nodes, distributed_cookie),
                encoding="utf-8",
                newline="\n",
            )
            environment_example.write_text(
                tool.render_environment_example(target, distributed_cookie, cluster_nodes),
                encoding="utf-8",
                newline="\n",
            )

        tool.record_step(report, "generate_artifacts", generate)

        def validate_compose_artifacts() -> None:
            for compose_path, log_name in (
                (compose_single, "compose-single-config.log"),
                (compose_cluster, "compose-cluster-config.log"),
            ):
                tool.run_logged(
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

        tool.record_step(report, "validate_compose_artifacts", validate_compose_artifacts)
        report_progress(f"Building image (timeout {timeout_seconds}s)")
        tool.record_step(
            report,
            "build_image",
            lambda: tool.run_logged(
                [
                    docker,
                    *( ["buildx", "build", "--builder", tool.MULTIARCH_BUILDER, "--load"] if prepared else ["build"] ),
                    "--platform",
                    target.platform,
                    "--pull=false",
                    # An explicit refresh must rerun package updates even when
                    # the OS tag still resolves to the same base-image digest.
                    "--no-cache",
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
            tool.render_single_compose(target, distributed_cookie, publish_ports=False),
            encoding="utf-8",
            newline="\n",
        )
        compose_cluster_test.write_text(
            tool.render_cluster_compose(
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
                            line = f'      RIAK_DISTRIBUTED_COOKIE: "{tool.generate_distributed_cookie()}"'
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
            OPENRIAK_PB_PORT=str(tool.free_tcp_port()),
            OPENRIAK_HTTP_PORT=str(tool.free_tcp_port()),
            OPENRIAK_MONITOR_INTERVAL_SECONDS="1",
        )
        cluster_container_names = [
            f"{tool.cluster_node_name(target, index)}-t-{test_suffix}"
            for index in range(1, cluster_nodes + 1)
        ]
        cluster_nodenames = [
            f"openriak-kv@{tool.default_node_host(index)}" for index in range(1, cluster_nodes + 1)
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

        existing = tool.run_logged(
            [docker, "container", "inspect", test_container_name],
            logs / "container-name-check.log",
            check=False,
            timeout_seconds=timeout_seconds,
        )
        if existing.returncode == 0:
            raise tool.DockerToolError(
                f"Container name {test_container_name} is already in use; refusing to remove it"
            )

        tool.record_step(
            report,
            "initialize_volumes",
            lambda: tool.run_logged(
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
        if not tool.populated(config_directory) or not data_directory.is_dir() or not log_directory.is_dir():
            raise tool.DockerToolError("Compose initialization did not create config, data, and logs directories")
        report["tests"]["volume_initialization"] = {
            "status": "passed",
            "config_populated": True,
            "data_directory_created": True,
            "logs_directory_created": True,
        }

        config_path = config_directory / "riak.conf"
        tool.record_step(
            report,
            "make_test_config_writable",
            lambda: tool.run_logged(
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
        tool.record_step(
            report,
            "configure_node",
            lambda: tool.configure_test_node(config_path, tool.default_node_host(1)),
        )
        preserved_test_cookie = tool.generate_distributed_cookie()
        if prepared:
            config_path.write_text(tool.set_riak_setting(config_path.read_text(), "distributed_cookie", preserved_test_cookie))
        # An operator-edited setting must survive startup despite a different ENV default.
        config_path.write_text(tool.set_riak_setting(config_path.read_text(), "logger.max_files", "7"))
        preserved_config_hash = tool.sha256_file(config_path)
        expected_settings = {
            "logger.max_file_size": "2MB",
            "logger.max_files": "7",
            "nodename": f"openriak-kv@{tool.default_node_host(1)}",
            "ring_size": "8",
            "storage_backend": "leveled",
            "anti_entropy": "passive",
            "tictacaae_active": "active",
            "tictacaae_storeheads": "enabled",
            "listener.http.internal": "0.0.0.0:8098",
            "listener.protobuf.internal": "0.0.0.0:8087",
        }
        actual_settings = tool.effective_riak_settings(config_path, expected_settings)
        if actual_settings != expected_settings:
            raise tool.DockerToolError(
                f"Generated riak.conf does not contain the requested settings: {actual_settings!r}"
            )
        report["tests"]["configuration"] = {
            "status": "passed",
            "settings": actual_settings,
        }

        compose_started = True
        tool.record_step(
            report,
            "start_compose_node",
            lambda: tool.run_logged(
                compose_command + ["up", "--detach", "--no-build"],
                logs / "compose-up.log",
                cwd=test_directory,
                environment=environment,
                timeout_seconds=timeout_seconds,
            ),
        )
        lifecycle_output = tool.record_step(
            report,
            "wait_for_entrypoint_readiness",
            lambda: tool.wait_for_container_log(
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
            raise tool.DockerToolError(
                f"Container log is missing lifecycle messages: {missing_startup_markers!r}"
            )
        report["tests"]["entrypoint_startup"] = {
            "status": "passed",
            "required_log_messages": startup_markers,
        }
        cli_response, http_response = tool.record_step(
            report,
            "wait_for_cli_and_http",
            lambda: tool.wait_for_node(
                test_container_name,
                timeout_seconds,
                logs,
            ),
        )
        if tool.sha256_file(config_path) != preserved_config_hash:
            raise tool.DockerToolError("Startup changed the existing riak.conf")
        report["tests"]["preserved_configuration"] = {"status": "passed", "sha256": preserved_config_hash}
        report["tests"]["runtime_options"] = tool.record_step(
            report, "verify_runtime_options",
            lambda: tool.verify_runtime_options(test_container_name, target, timeout_seconds, logs / "runtime-options.log"),
        )
        if prepared:
            actual_cookie = tool.effective_riak_settings(config_path, ["distributed_cookie"]).get("distributed_cookie")
            if actual_cookie != preserved_test_cookie:
                raise tool.DockerToolError("Startup replaced the existing distributed cookie")
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
        report["tests"]["admin_test"] = tool.record_step(
            report,
            "single_node_admin_test",
            lambda: tool.verify_admin_test(test_container_name, timeout_seconds, logs / "admin-test.log"),
        )
        health_status = tool.record_step(
            report,
            "wait_for_healthcheck",
            lambda: tool.wait_for_container_health(
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
        if not tool.populated(data_directory) or not tool.populated(log_directory):
            raise tool.DockerToolError("OpenRiak startup did not populate both data and log volumes")
        report["tests"]["populated_volumes"] = {
            "status": "passed",
            "config": sorted(path.name for path in config_directory.iterdir()),
            "data": sorted(path.name for path in data_directory.iterdir()),
            "logs": sorted(path.name for path in log_directory.iterdir()),
        }
        tool.record_step(
            report,
            "graceful_stop",
            lambda: tool.run_logged(
                compose_command + ["stop", "--timeout", str(min(timeout_seconds, target.lifecycle_options.stop_grace_period))],
                logs / "compose-stop.log",
                cwd=test_directory,
                environment=environment,
                timeout_seconds=timeout_seconds,
            ),
        )
        stopped_logs = tool.record_step(
            report,
            "verify_graceful_shutdown_logging",
            lambda: tool.run_logged(
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
            raise tool.DockerToolError(
                f"Container log is missing graceful shutdown messages: {missing_shutdown_markers!r}"
            )
        report["tests"]["graceful_shutdown"] = {
            "status": "passed",
            "signal": "SIGTERM",
            "required_log_messages": shutdown_markers,
        }
        tool.record_step(
            report,
            "remove_single_node_test",
            lambda: tool.run_logged(
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
            existing = tool.run_logged(
                [docker, "container", "inspect", cluster_container_name],
                logs / "cluster-container-name-check.log",
                check=False,
                timeout_seconds=timeout_seconds,
            )
            if existing.returncode == 0:
                raise tool.DockerToolError(
                    f"Container name {cluster_container_name} is already in use; refusing to remove it"
                )

        cluster_started = True
        tool.record_step(
            report,
            "start_compose_cluster",
            lambda: tool.run_logged(
                cluster_command + ["up", "--detach", "--no-build"],
                logs / "cluster-compose-up.log",
                cwd=test_directory,
                environment=environment,
                timeout_seconds=timeout_seconds,
            ),
        )
        cluster_state = tool.record_step(
            report,
            "wait_for_cluster",
            lambda: tool.wait_for_cluster(
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
            container_logs = tool.run_logged(
                [docker, "logs", cluster_container_name],
                logs / f"cluster-node-{index}.log",
                timeout_seconds=timeout_seconds,
            ).stdout
            expected_role = "Coordinator" if index == 1 else "Follower"
            if f"cluster: Role: {expected_role}" not in container_logs:
                raise tool.DockerToolError(
                    f"{cluster_container_name} did not log its {expected_role} role"
                )
            role_logs[cluster_container_name] = expected_role
            tool.wait_for_container_health(
                cluster_container_name,
                timeout_seconds,
                logs / f"cluster-node-{index}-health.log",
            )
            cluster_admin_tests[cluster_container_name] = tool.record_step(
                report,
                f"cluster_node_{index}_admin_test",
                lambda: tool.verify_admin_test(
                    cluster_container_name, timeout_seconds, logs / f"cluster-node-{index}-admin-test.log"
                ),
            )
            report["tests"]["cluster_runtime_options"][cluster_container_name] = tool.record_step(
                report, f"cluster_node_{index}_runtime_options",
                lambda: tool.verify_runtime_options(cluster_container_name, target, timeout_seconds, logs / f"cluster-node-{index}-runtime-options.log"),
            )
            if prepared:
                cookie_result = tool.run_logged(
                    [docker, "exec", cluster_container_name, "cat", "/etc/riak/riak.conf"],
                    logs / f"cluster-node-{index}-configuration.log", timeout_seconds=timeout_seconds,
                ).stdout
                expected_cookie = re.search(r"(?m)^distributed_cookie\s*=\s*(\S+)\s*$", cookie_result)
                if not expected_cookie or expected_cookie.group(1) != distributed_cookie:
                    raise tool.DockerToolError(f"Cluster node {index} did not retain the coordinator cookie")
                if index > 1 and "adopted coordinator cookie before daemon startup" not in container_logs:
                    raise tool.DockerToolError(f"Cluster node {index} did not log cookie adoption before startup")
            cluster_node_directory = test_directory / tool.cluster_node_name(target, index)
            for volume_name in ("config", "data", "logs"):
                if not tool.populated(cluster_node_directory / volume_name):
                    raise tool.DockerToolError(
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
        tool.record_step(
            report,
            "graceful_stop_cluster",
            lambda: tool.run_logged(
                cluster_command + ["stop", "--timeout", str(min(timeout_seconds, target.lifecycle_options.stop_grace_period))],
                logs / "cluster-compose-stop.log",
                cwd=test_directory,
                environment=environment,
                timeout_seconds=timeout_seconds,
            ),
        )
        tool.record_step(
            report,
            "remove_cluster_test",
            lambda: tool.run_logged(
                cluster_command + ["down", "--remove-orphans", "--timeout", str(min(timeout_seconds, target.lifecycle_options.stop_grace_period))],
                logs / "cluster-compose-down.log",
                cwd=test_directory,
                environment=environment,
                timeout_seconds=timeout_seconds,
            ),
        )
        cluster_started = False
        report["artifacts"] = tool.artifact_downloads(
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
                result = tool.run_logged(*args, **kwargs)
                if result.returncode:
                    raise tool.DockerToolError(f"Cleanup command failed: {' '.join(args[0])}; see {args[1]}")
            except (tool.DockerToolError, OSError) as error:
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
        report["finished_at"] = tool.isoformat()
        tool.publish_current_run(target, run_root, report)
    return report["status"] == "passed"
