"""Testing operations; dependencies are supplied by the public tool facade."""
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

from validation.configuration import verify_runtime_options, verify_admin_test, set_riak_setting, configure_test_node, effective_riak_settings, populated, free_tcp_port
from validation.waits import remaining_timeout, run_before_deadline, container_http_ping, wait_for_node, wait_for_container_log, wait_for_container_health, wait_for_cluster
DEFAULT_CLUSTER_NODES = 5






























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
