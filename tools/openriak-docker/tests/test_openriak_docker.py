import contextlib
import importlib.util
import io
import pathlib
import sys
import tempfile
import unittest
from unittest import mock


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "openriak_docker.py"
SPEC = importlib.util.spec_from_file_location("openriak_docker", MODULE_PATH)
docker_tool = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = docker_tool
SPEC.loader.exec_module(docker_tool)


class OpenRiakDockerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        matches = docker_tool.discover_targets(
            ["3.4.0"],
            os_id="alpine-3.21-x86_64",
            download_id="otp24-x86_64-r1",
        )
        assert len(matches) == 1
        cls.target = matches[0]

    def test_metadata_selects_expected_initial_target(self):
        self.assertEqual(self.target.otp, "24")
        self.assertEqual(self.target.architecture, "x86_64")
        self.assertEqual(self.target.platform, "linux/amd64")
        self.assertEqual(
            self.target.image,
            "openriak/openriak-kv:3.4.0-alpine-3.21-otp24-x86_64",
        )
        self.assertEqual(
            self.target.package["checksum"]["value"],
            "140f1decb585e5855990c140b58afcb2ba3629e5dc65fffab8d0eaaa0621cc69",
        )

    def test_dockerfile_is_pinned_and_self_contained(self):
        digest = "sha256:" + "a" * 64
        cookie = "openriak-0123456789abcdef0123456789abcdef"
        source = docker_tool.render_dockerfile(
            self.target, f"alpine:3.21@{digest}", cookie
        )
        self.assertIn(f"FROM --platform=linux/amd64 alpine:3.21@{digest}", source)
        self.assertNotIn("latest", source.lower())
        self.assertNotIn("\r", source)
        self.assertIn("ADD --checksum=sha256:140f1d", source)
        self.assertIn(
            "apk add --no-cache bash ca-certificates coreutils curl su-exec",
            source,
        )
        self.assertIn("adduser -S -D -H", source)
        self.assertIn("/usr/lib/riak/log", source)
        self.assertIn("# OpenRiak KV default settings", source)
        self.assertIn('ENV RIAK_RING_SIZE="8"', source)
        self.assertIn(f'ENV RIAK_DISTRIBUTED_COOKIE="{cookie}"', source)
        self.assertIn('ENV RIAK_STORAGE_BACKEND="leveled"', source)
        self.assertIn('ENV RIAK_TICTACAAE_ACTIVE="active"', source)
        self.assertIn('ENV RIAK_TICTACAAE_STOREHEADS="enabled"', source)
        self.assertIn('ENV RIAK_MONITOR_INTERVAL_SECONDS="10"', source)
        self.assertIn('ENV OPENRIAK_CLUSTER_MODE="single"', source)
        self.assertIn('ENV OPENRIAK_CLUSTER_WAIT_SECONDS="300"', source)
        self.assertIn('ENV role=""', source)
        self.assertIn('VOLUME ["/etc/riak"]', source)
        self.assertIn('VOLUME ["/var/lib/riak"]', source)
        self.assertIn('VOLUME ["/var/log/riak"]', source)
        self.assertIn("ENTRYPOINT", source)
        self.assertIn("COPY <<'OPENRIAK_ENTRYPOINT'", source)
        self.assertIn("COPY <<'OPENRIAK_HEALTHCHECK'", source)
        self.assertIn("riak_command daemon", source)
        self.assertIn("riak_command chkconfig", source)
        self.assertIn('log "startup: configuration is valid', source)
        self.assertIn("riak_command admin services", source)
        self.assertIn("riak_command admin transfers", source)
        self.assertIn("riak_command stop", source)
        self.assertIn("pgrep -x beam.smp", source)
        self.assertIn(
            "HEALTHCHECK --interval=10s --timeout=60s --start-period=120s --retries=3",
            source,
        )
        self.assertIn("STOPSIGNAL SIGTERM", source)
        self.assertIn('log "startup: OpenRiak is ready"', source)
        self.assertIn('log "monitor: BEAM is running and riak ping returned pong"', source)
        self.assertIn('log "cluster: Role: Coordinator"', source)
        self.assertIn('log "cluster: Role: Follower"', source)
        self.assertIn('riak_admin_command cluster join "$coordinator_node"', source)
        self.assertIn("riak_admin_command cluster plan", source)
        self.assertIn("riak_admin_command cluster commit", source)
        self.assertIn('pending_file in "$control_dir/"*-"${coordinator_suffix}"-ready', source)
        self.assertIn('[ "$pending_count" -eq 0 ]', source)
        self.assertIn('while [ ! -e "$complete_file" ]', source)
        self.assertIn("cluster: coordinator confirmed completion", source)
        self.assertIn("plan_output_is_successful", source)
        self.assertIn("commit_output_is_successful", source)
        self.assertIn("current_node_ipv4", source)
        self.assertIn("nodename_resolves_to_ip", source)
        self.assertIn('$1 == expected || $1 == "::ffff:" expected', source)
        self.assertIn('set_setting distributed_cookie "$RIAK_DISTRIBUTED_COOKIE"', source)
        self.assertIn('log "configuration: ${key} = ${value}"', source)
        self.assertIn("for (octet = 1; octet <= 4; octet += 1)", source)
        self.assertIn("nodename=%s", source)
        self.assertIn("ip=%s", source)
        self.assertIn("coordinator=%s", source)
        self.assertIn("suffix=%s", source)
        self.assertIn("*-coordinator", source)
        self.assertIn("-approved", source)
        self.assertNotIn("/usr/sbin/riak console", source)
        for line in source.splitlines():
            if line.startswith("RUN "):
                self.assertNotIn(" && ", line)
                self.assertNotIn("; ", line)

    def test_compose_has_requested_identity_ports_volumes_and_network(self):
        cookie = "openriak-0123456789abcdef0123456789abcdef"
        source = docker_tool.render_single_compose(self.target, cookie)
        node = "openriak-kv-3.4.0-alpine-3.21-otp24-x86_64-node"
        host = "node-01.cluster-a.openriak"
        self.assertIn("build:\n      context: .\n      dockerfile: ./Dockerfile", source)
        self.assertIn(f'container_name: "${{OPENRIAK_CONTAINER_NAME:-{node}}}"', source)
        self.assertIn(f'hostname: "${{OPENRIAK_NODE_1_HOST:-{host}}}"', source)
        self.assertIn(f'RIAK_NODE_HOST: "${{OPENRIAK_NODE_1_HOST:-{host}}}"', source)
        self.assertIn(f'RIAK_DISTRIBUTED_COOKIE: "${{OPENRIAK_DISTRIBUTED_COOKIE:-{cookie}}}"', source)
        self.assertIn(
            'RIAK_MONITOR_INTERVAL_SECONDS: "${OPENRIAK_MONITOR_INTERVAL_SECONDS:-10}"',
            source,
        )
        self.assertIn('"${OPENRIAK_PB_PORT:-8087}:8087"', source)
        self.assertIn('"${OPENRIAK_HTTP_PORT:-8098}:8098"', source)
        self.assertIn(f'"${{OPENRIAK_CONFIG_PATH:-./{node}/config}}:/etc/riak"', source)
        self.assertIn(f'"${{OPENRIAK_DATA_PATH:-./{node}/data}}:/var/lib/riak"', source)
        self.assertIn(f'"${{OPENRIAK_LOGS_PATH:-./{node}/logs}}:/var/log/riak"', source)
        self.assertIn(f'aliases:\n          - "${{OPENRIAK_NODE_1_HOST:-{host}}}"', source)
        self.assertNotIn("ipv4_address", source)
        self.assertNotIn("ipam", source)

    def test_cluster_compose_has_five_nodes_one_coordinator_and_shared_control(self):
        cookie = "openriak-0123456789abcdef0123456789abcdef"
        source = docker_tool.render_cluster_compose(self.target, distributed_cookie=cookie)
        for index in range(1, 6):
            node = f"{self.target.node_name}-{index}"
            host = f"node-{index:02d}.cluster-a.openriak"
            self.assertIn(f"  node{index}:", source)
            self.assertIn(f'hostname: "${{OPENRIAK_NODE_{index}_HOST:-{host}}}"', source)
            self.assertIn(
                f'RIAK_NODE_HOST: "${{OPENRIAK_NODE_{index}_HOST:-{host}}}"',
                source,
            )
            self.assertIn(
                f'aliases:\n          - "${{OPENRIAK_NODE_{index}_HOST:-{host}}}"',
                source,
            )
            self.assertIn(f'"${{OPENRIAK_NODE_{index}_CONFIG_PATH:-./{node}/config}}:/etc/riak"', source)
            self.assertIn(f'"${{OPENRIAK_NODE_{index}_DATA_PATH:-./{node}/data}}:/var/lib/riak"', source)
            self.assertIn(f'"${{OPENRIAK_NODE_{index}_LOGS_PATH:-./{node}/logs}}:/var/log/riak"', source)
        self.assertEqual(source.count(f'RIAK_DISTRIBUTED_COOKIE: "${{OPENRIAK_DISTRIBUTED_COOKIE:-{cookie}}}"'), 5)
        self.assertEqual(source.count("      role: coordinator"), 1)
        self.assertEqual(source.count("      OPENRIAK_CLUSTER_MODE: cluster"), 5)
        self.assertEqual(
            source.count(
                f'"${{OPENRIAK_CLUSTER_CONTROL_PATH:-./{self.target.node_name}-cluster-control}}:'
                f'{docker_tool.CONTROL_DIRECTORY}"'
            ),
            5,
        )
        self.assertNotIn("configured-node-count", source)
        self.assertNotIn("ipv4_address", source)
        self.assertNotIn("OPENRIAK_NETWORK_SUBNET", source)

    def test_cluster_node_count_is_generator_control_not_runtime_configuration(self):
        source = docker_tool.render_cluster_compose(self.target, 3)
        self.assertIn("  node3:", source)
        self.assertNotIn("  node4:", source)
        self.assertEqual(source.count("      role: coordinator"), 1)
        with self.assertRaisesRegex(docker_tool.DockerToolError, "between 2 and 253"):
            docker_tool.render_cluster_compose(self.target, 1)

    def test_runtime_compose_can_disable_host_port_publication(self):
        cookie = "openriak-0123456789abcdef0123456789abcdef"
        single = docker_tool.render_single_compose(
            self.target,
            cookie,
            publish_ports=False,
        )
        cluster = docker_tool.render_cluster_compose(
            self.target,
            distributed_cookie=cookie,
            publish_ports=False,
        )
        self.assertNotIn("    ports:", single)
        self.assertNotIn("    ports:", cluster)
        self.assertIn("EXPOSE 8087", docker_tool.render_dockerfile(self.target, "alpine:3.21", cookie))
        self.assertIn("EXPOSE 8098", docker_tool.render_dockerfile(self.target, "alpine:3.21", cookie))

    def test_configure_node_sets_all_test_values(self):
        source = """nodename = riak@127.0.0.1
## ring_size = 64
storage_backend = bitcask
anti_entropy = active
tictacaae_active = passive
tictacaae_storeheads = disabled
listener.http.internal = 127.0.0.1:8098
listener.protobuf.internal = 127.0.0.1:8087
"""
        with tempfile.TemporaryDirectory() as directory:
            config = pathlib.Path(directory) / "riak.conf"
            config.write_text(source, encoding="utf-8")
            docker_tool.configure_test_node(config, self.target.node_name)
            values = docker_tool.effective_riak_settings(
                config,
                [
                    "nodename",
                    "ring_size",
                    "storage_backend",
                    "anti_entropy",
                    "tictacaae_active",
                    "tictacaae_storeheads",
                    "listener.http.internal",
                    "listener.protobuf.internal",
                ],
            )
        self.assertEqual(values["nodename"], f"openriak-kv@{self.target.node_name}")
        self.assertEqual(values["ring_size"], "8")
        self.assertEqual(values["storage_backend"], "leveled")
        self.assertEqual(values["anti_entropy"], "passive")
        self.assertEqual(values["tictacaae_active"], "active")
        self.assertEqual(values["tictacaae_storeheads"], "enabled")
        self.assertEqual(values["listener.http.internal"], "0.0.0.0:8098")
        self.assertEqual(values["listener.protobuf.internal"], "0.0.0.0:8087")

    def test_commented_setting_replacement_ignores_whitespace(self):
        source = "    ##          ring_size  =        64         \n"
        updated = docker_tool.set_riak_setting(source, "ring_size", "8")
        self.assertEqual(updated, "ring_size = 8\n")

    def test_single_hash_comment_is_not_treated_as_disabled_setting(self):
        source = "# ring_size = documentation\n"
        updated = docker_tool.set_riak_setting(source, "ring_size", "8")
        self.assertEqual(
            updated,
            "# ring_size = documentation\nring_size = 8\n",
        )

    def test_base_image_uses_release_tag(self):
        self.assertEqual(docker_tool.base_image_for(self.target), "alpine:3.21")

    def test_admin_command_uses_installed_package_layout(self):
        source = docker_tool.ENTRYPOINT_SCRIPT
        function = source[source.index("riak_admin_command() {"):source.index("log_cluster_command_output() {")]
        for layout in ("lib64", "lib", "missing"):
            with self.subTest(layout=layout), tempfile.TemporaryDirectory() as directory:
                root = pathlib.Path(directory)
                vmargs = root / "generated.conf" / "vm.test.args"
                vmargs.parent.mkdir()
                vmargs.touch()
                executable = root / layout / "riak/bin/riak-admin"
                if layout != "missing":
                    executable.parent.mkdir(parents=True)
                    executable.write_text('#!/bin/sh\nprintf "%s\\n" "$VMARGS_PATH" "$@"\n')
                    executable.chmod(0o755)
                script = function.replace("/usr/lib64/", f"{root}/lib64/").replace("/usr/lib/", f"{root}/lib/")
                script += '\nlog() { printf "%s\\n" "$*"; }\n'
                launcher = root / "su-exec"
                launcher.write_text('#!/bin/sh\nshift\nexec "$@"\n')
                launcher.chmod(0o755)
                script += f"PATH='{root}':$PATH\n"
                script += f"data_dir='{root}'\nriak_admin_command cluster join openriak-kv@node-01.cluster-a.openriak\n"
                result = docker_tool.subprocess.run(
                    ["/bin/sh", "-eu", "-c", script], capture_output=True, text=True,
                )
                if layout == "missing":
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("packaged riak-admin executable is not available", result.stdout)
                else:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout.splitlines(), [
                        str(vmargs), "cluster", "join", "openriak-kv@node-01.cluster-a.openriak",
                    ])

    def test_rhel_base_images_use_current_release_specific_tags(self):
        rhel_targets = {
            target.release: target
            for target in docker_tool.discover_targets()
            if target.family == "rhel"
        }
        self.assertEqual(
            docker_tool.base_image_for(rhel_targets["8"]),
            "registry.access.redhat.com/ubi8/ubi:8.10",
        )
        self.assertEqual(
            docker_tool.base_image_for(rhel_targets["9"]),
            "registry.access.redhat.com/ubi9/ubi:9.8",
        )

    def test_amazon_linux_keeps_existing_curl_and_uses_bundled_escript(self):
        target = next(
            target
            for target in docker_tool.discover_targets()
            if target.family == "amazon-linux"
        )
        script = docker_tool.package_install_script(target)
        self.assertIn("if ! command -v curl", script)
        self.assertNotIn("dnf install -y ca-certificates curl ", script)
        self.assertIn("rpm -Uvh --replacepkgs --nodeps", script)
        self.assertIn("/usr/lib64/riak/erts-*/bin/escript", script)
        self.assertIn("test -x /usr/bin/escript", script)

    def test_rhel_keeps_existing_curl_minimal(self):
        target = next(
            target
            for target in docker_tool.discover_targets()
            if target.family == "rhel"
        )
        script = docker_tool.package_install_script(target)
        self.assertIn("if ! command -v curl", script)
        self.assertNotIn("dnf install -y ca-certificates curl ", script)

    def test_microdnf_installs_dependencies_before_local_rpm(self):
        target = next(
            target
            for target in docker_tool.discover_targets()
            if target.family == "oracle-linux"
        )
        script = docker_tool.package_install_script(target)
        self.assertIn("microdnf install -y dnf", script)
        self.assertIn(
            "dnf install -y bash ca-certificates glibc hostname libgcc libstdc++",
            script,
        )
        self.assertIn("shadow-utils sudo util-linux zlib", script)
        self.assertIn(
            f"rpm -Uvh --replacepkgs --nodeps /tmp/{target.package['filename']}",
            script,
        )

    def test_pull_output_digest_pattern_supports_containerd_image_store(self):
        output = "Digest: sha256:" + "b" * 64 + "\nStatus: Downloaded newer image\n"
        self.assertEqual(
            docker_tool.digest_from_pull_output(output),
            "sha256:" + "b" * 64,
        )
        self.assertIsNone(docker_tool.digest_from_pull_output("Status: up to date\n"))

    def test_cookie_and_environment_example_are_generated(self):
        first = docker_tool.generate_distributed_cookie()
        second = docker_tool.generate_distributed_cookie()
        self.assertRegex(first, r"^openriak-[0-9a-f]{32}$")
        self.assertNotEqual(first, second)
        source = docker_tool.render_environment_example(self.target, first)
        self.assertIn(f"OPENRIAK_DISTRIBUTED_COOKIE={first}", source)
        self.assertIn("OPENRIAK_NODE_1_HOST=node-01.cluster-a.openriak", source)
        self.assertIn("OPENRIAK_NODE_5_HOST=node-05.cluster-a.openriak", source)
        self.assertIn("OPENRIAK_CONFIG_PATH=./", source)
        self.assertIn("OPENRIAK_NODE_1_CONFIG_PATH=./", source)

    def test_complete_metadata_matrix_is_discoverable(self):
        targets = docker_tool.discover_targets()
        self.assertGreater(len(targets), 20)
        self.assertTrue(
            all(
                docker_tool.semver_key(target.version)
                >= docker_tool.MINIMUM_OPENRIAK_VERSION
                for target in targets
            )
        )
        self.assertTrue(all(target.otp for target in targets))
        self.assertTrue(all(target.platform.startswith("linux/") for target in targets))
        self.assertTrue(all("latest" not in docker_tool.base_image_for(target) for target in targets))
        self.assertEqual(len({target.image for target in targets}), len(targets))

    def test_rejects_pre_openriak_versions(self):
        with self.assertRaisesRegex(
            docker_tool.DockerToolError,
            "OpenRiak KV Docker targets start at 3.4.0",
        ):
            docker_tool.discover_targets(["3.3.9"])

    def test_refresh_parser_has_cache_and_cluster_controls(self):
        options = docker_tool.parser().parse_args(
            [
                "refresh",
                "--version",
                "3.4.0",
                "--cluster-nodes",
                "7",
                "--force",
            ]
        )
        self.assertEqual(options.cluster_nodes, 7)
        self.assertTrue(options.force)

        retry_options = docker_tool.parser().parse_args(
            [
                "refresh",
                "--version",
                "3.4.0",
                "--retry-failed",
            ]
        )
        self.assertTrue(retry_options.retry_failed)
        self.assertFalse(retry_options.force)

    def test_refresh_log_header_and_skipped_target_are_timestamped(self):
        output = io.StringIO()
        with mock.patch.object(
            docker_tool, "discover_targets", return_value=[self.target]
        ), mock.patch.object(
            docker_tool, "cache_state", return_value=("valid", "")
        ), mock.patch.object(
            docker_tool, "log_timestamp", return_value="2026-09-05 11:01:22"
        ), contextlib.redirect_stdout(output):
            exit_code = docker_tool.main(["refresh", "--version", "3.4.0"])
        source = output.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("Docker script started at 2026-09-05 11:01:22", source)
        self.assertIn("Version:       3.4.0", source)
        self.assertIn("OS:            all", source)
        self.assertIn("Architecture:  all", source)
        self.assertIn("Timeout:       180s", source)
        self.assertIn("Cluster nodes: 5", source)
        self.assertIn(
            f"[1/1] 2026-09-05 11:01:22 SKIPPED {self.target.image} "
            "(complete cache exists)",
            source,
        )

    def test_refresh_target_has_timestamped_phase_progress_hooks(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        self.assertIn('report_progress(f"Pulling and pinning base image (timeout ', source)
        self.assertIn(
            'report_progress("Creating Dockerfile, compose YAML files and .env for this run")',
            source,
        )
        self.assertIn('report_progress(f"Building image (timeout ', source)
        self.assertIn('report_progress(f"Testing single node (timeout ', source)
        self.assertIn('f"Testing {cluster_nodes}-node cluster (timeout ', source)

    def test_run_logged_records_and_reports_command_timeout(self):
        command = ["docker", "build", "."]
        timeout = docker_tool.subprocess.TimeoutExpired(
            command,
            1800,
            output="partial build output\n",
        )
        with tempfile.TemporaryDirectory() as directory:
            log_path = pathlib.Path(directory) / "build.log"
            with mock.patch.object(
                docker_tool.subprocess,
                "run",
                side_effect=timeout,
            ):
                with self.assertRaisesRegex(
                    docker_tool.DockerToolError,
                    "timed out after 1800s",
                ):
                    docker_tool.run_logged(
                        command,
                        log_path,
                        timeout_seconds=1800,
                    )
            log = log_path.read_text(encoding="utf-8")
            self.assertIn("timeout_seconds: 1800", log)
            self.assertIn("exit_code: timeout", log)
            self.assertIn("partial build output", log)

    def test_partial_single_compose_start_is_marked_for_cleanup(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        marked = source.index("        compose_started = True\n        record_step(\n            report,\n            \"start_compose_node\"")
        started = source.index('compose_command + ["up", "--detach", "--no-build"]', marked)
        self.assertLess(marked, started)

    def test_container_log_wait_fails_immediately_when_container_exits(self):
        log_result = docker_tool.subprocess.CompletedProcess(
            args=["docker", "logs", "failed-node"],
            returncode=0,
            stdout="startup: configuration validation failed\n",
        )
        state_result = docker_tool.subprocess.CompletedProcess(
            args=["docker", "container", "inspect", "failed-node"],
            returncode=0,
            stdout="false 1\n",
        )
        with tempfile.TemporaryDirectory() as directory:
            log_path = pathlib.Path(directory) / "readiness.log"
            with mock.patch.object(
                docker_tool, "docker_command", return_value="/usr/bin/docker"
            ), mock.patch.object(
                docker_tool.subprocess,
                "run",
                side_effect=[log_result, state_result],
            ) as run:
                with self.assertRaisesRegex(
                    docker_tool.DockerToolError,
                    "exited with code 1",
                ):
                    docker_tool.wait_for_container_log(
                        "failed-node",
                        "monitor: BEAM is running",
                        1800,
                        log_path,
                    )
            self.assertEqual(run.call_count, 2)
            self.assertIn("state='false 1'", log_path.read_text(encoding="utf-8"))

    def test_cluster_wait_fails_immediately_when_a_container_exits(self):
        state_result = docker_tool.subprocess.CompletedProcess(
            args=["docker", "container", "inspect", "failed-node"],
            returncode=0,
            stdout="false 7\n",
        )
        with tempfile.TemporaryDirectory() as directory:
            log_path = pathlib.Path(directory) / "cluster-readiness.log"
            with mock.patch.object(
                docker_tool, "docker_command", return_value="/usr/bin/docker"
            ), mock.patch.object(
                docker_tool.subprocess,
                "run",
                return_value=state_result,
            ) as run:
                with self.assertRaisesRegex(
                    docker_tool.DockerToolError,
                    "stopped before the cluster became ready",
                ):
                    docker_tool.wait_for_cluster(
                        ["failed-node"],
                        ["openriak-kv@failed-node"],
                        1800,
                        log_path,
                    )
            self.assertEqual(run.call_count, 1)
            self.assertIn('"running": "false 7"', log_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
