import importlib.util
import pathlib
import sys
import tempfile
import unittest


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
        self.assertIn("HEALTHCHECK --interval=10s", source)
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

    def test_partial_single_compose_start_is_marked_for_cleanup(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        marked = source.index("        compose_started = True\n        record_step(\n            report,\n            \"start_compose_node\"")
        started = source.index('compose_command + ["up", "--detach", "--no-build"]', marked)
        self.assertLess(marked, started)


if __name__ == "__main__":
    unittest.main()
