import argparse
import contextlib
import io
import dataclasses
import json
import pathlib
import shlex
import subprocess
import tempfile
import unittest
from unittest import mock
from test_openriak_docker import docker_tool as tool


class MultiarchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.targets = tool.discover_targets(["3.4.0", "3.4.1"])
        cls.groups = tool.grouped_targets(cls.targets)
        cls.alpine = next(g for g in cls.groups if g[0].image_tag == "3.4.0-alpine-3.21-otp24")

    def test_groups_cover_packages_once_and_have_architecture_free_tags(self):
        self.assertEqual(sum(map(len, self.groups)), len(self.targets))
        self.assertEqual(len({t.image for t in self.targets}), len(self.targets))
        self.assertEqual({t.platform for t in self.alpine}, {"linux/amd64", "linux/arm64"})
        for group in self.groups:
            self.assertEqual(len({t.image for t in group}), 1)
            self.assertEqual(len({t.cache_directory for t in group}), len(group))
            self.assertEqual(len({t.group_directory for t in group}), 1)
            self.assertTrue(group[0].image.endswith(f"-otp{group[0].otp}"))

    def test_aliases_follow_metadata_highest_otp_release_version_and_alpine(self):
        def aliases(tag):
            group = next(g for g in self.groups if g[0].image_tag == tag)
            return [image.split(":", 1)[1] for image in tool.image_aliases(group[0], self.targets)]
        self.assertEqual(aliases("3.4.0-ubuntu-noble-otp24"), ["3.4.0-ubuntu-noble-otp24"])
        self.assertEqual(aliases("3.4.0-ubuntu-noble-otp26"), ["3.4.0-ubuntu-noble-otp26", "3.4.0-ubuntu-noble", "3.4.0-ubuntu"])
        self.assertEqual(aliases("3.4.0-ubuntu-jammy-otp26"), ["3.4.0-ubuntu-jammy-otp26", "3.4.0-ubuntu-jammy"])
        latest = [g for g in self.groups if "openriak/openriak-kv:latest" in tool.image_aliases(g[0], self.targets)]
        self.assertEqual(len(latest), 1)
        self.assertEqual(latest[0][0].version, "3.4.1")
        self.assertEqual(latest[0][0].family, "alpine")
        self.assertIn("openriak/openriak-kv:3.4.1", tool.image_aliases(latest[0][0], self.targets))

    def test_shared_dockerfile_selects_correct_package_and_keeps_one_runtime(self):
        bases = {t.platform: {"pinned": f"alpine:3.21@sha256:{str(i) * 64}"} for i, t in enumerate(self.alpine, 1)}
        source = tool.render_multiarch_dockerfile(self.alpine, bases, "cookie-test", tool.image_aliases(self.alpine[0], self.targets))
        self.assertNotIn("\nARG TARGETARCH\n", source)
        self.assertIn("FROM package-${TARGETARCH} AS final", source)
        for t in self.alpine:
            arch = t.platform.split('/')[1]
            download = source.split(f"FROM scratch AS download-{arch}\n", 1)[1].split("\nFROM ", 1)[0]
            stage = source.split(f"AS package-{arch}\n", 1)[1].split("OPENRIAK_PACKAGE_INSTALL\n", 1)[0]
            self.assertIn(t.package["url"], download)
            self.assertIn(t.package["checksum"]["value"], download)
            self.assertIn(f"from=download-{arch},target=/opt/openriak-package,ro", stage)
            self.assertNotIn("ADD ", stage)
        self.assertEqual(source.count("COPY <<'OPENRIAK_ENTRYPOINT'"), 1)
        self.assertEqual(source.count('ENV RIAK_DISTRIBUTED_COOKIE="cookie-test"'), 1)
        self.assertNotIn("FROM alpine:latest", source)
        with self.assertRaises(tool.DockerToolError):
            tool.render_multiarch_dockerfile(self.alpine, {t.platform: {"pinned": "alpine:3.21"} for t in self.alpine}, "cookie", [])
        subprocess.run(["sh", "-n"], input=tool.ENTRYPOINT_SCRIPT, text=True, check=True, capture_output=True)

    def test_package_downloads_stay_out_of_runtime_layers(self):
        for group in self.groups:
            bases = {t.platform: {"pinned": "example:1@sha256:" + "a" * 64} for t in group}
            sources = [tool.render_multiarch_dockerfile(group, bases, "cookie", [])]
            sources.extend(tool.render_dockerfile(t, bases[t.platform]["pinned"], "cookie") for t in group)
            for source in sources:
                with self.subTest(image=group[0].image, multiarch="AS final" in source):
                    current_base = None
                    current_stage = None
                    for line in source.splitlines():
                        if line.startswith("FROM "):
                            parts = [part for part in line.split() if not part.startswith("--")]
                            current_base = parts[1]
                            current_stage = parts[-1]
                        if line.startswith("ADD "):
                            self.assertIn("--checksum=sha256:", line)
                            if current_stage.startswith("openssl-build-"):
                                # OpenSSL source archives stay in a discarded compiler stage.
                                self.assertIn(line.rsplit(" ", 1)[-1],
                                              ("/sources/openssl.tar.gz", "/sources/debian.tar.xz"))
                                self.assertFalse(any(t.package["url"] in line for t in group))
                            else:
                                self.assertEqual(current_base, "scratch")
                    installs = source.split("RUN --mount=")[1:]
                    self.assertTrue(installs)
                    for install in installs:
                        install = install.split("OPENRIAK_PACKAGE_INSTALL\n", 1)[0]
                        self.assertIn("type=bind,from=download", install)
                        self.assertIn("target=/opt/openriak-package,ro", install)
                        body = install.split("set -eu\n", 1)[1]
                        copies = [line for line in body.splitlines() if line.startswith("cp /opt/openriak-package/")]
                        if copies:
                            destination = copies[0].split()[-1]
                            self.assertIn(f"rm -f {destination}", body)
                            self.assertLess(body.index(copies[0]), body.index(f"rm -f {destination}"))
                        else:
                            # Minimal installers consume the read-only package mount directly.
                            self.assertIn("rpm --root /openriak-rootfs -Uvh", body)
                            self.assertIn("--nodeps /opt/openriak-package/", body)
                            self.assertNotIn("cp /opt/openriak-package/", body)
                        subprocess.run(["sh", "-n"], input=body, text=True, check=True, capture_output=True)

    def test_package_caches_are_cleaned_inside_install_layer(self):
        for group in self.groups:
            bases = {t.platform: {"pinned": "example:1@sha256:" + "a" * 64} for t in group}
            source = tool.render_multiarch_dockerfile(group, bases, "cookie", [])
            for install in source.split("RUN --mount=")[1:]:
                body = install.split("OPENRIAK_PACKAGE_INSTALL\n", 1)[0]
                family = group[0].operating_system["package_family"]
                with self.subTest(image=group[0].image, family=family):
                    if family == "rpm":
                        root = "/openriak-rootfs" if "rpm --root /openriak-rootfs" in body else ""
                        cleanup = f"rm -rf {root}/var/cache/dnf {root}/var/cache/yum"
                        self.assertIn(cleanup, body)
                        package_install = "rpm --root /openriak-rootfs -Uvh" if root else "rpm -Uvh"
                        self.assertLess(body.index(package_install), body.index(cleanup))
                        self.assertNotIn("rm -rf /var/lib/rpm", body)
                    elif family == "deb":
                        self.assertLess(body.index("apt-get install"), body.index("apt-get clean"))
                        self.assertIn("rm -rf /var/lib/apt/lists/*", body)
                    else:
                        self.assertIn("apk add --no-cache", body)
        # Exercise the generic RPM fallback as well as metadata-backed families.
        rpm_target = next(t for t in self.targets if t.operating_system["package_family"] == "rpm")
        operating_system = dict(rpm_target.operating_system, family="other-rpm")
        fallback = dataclasses.replace(rpm_target, operating_system=operating_system)
        self.assertIn("rm -rf /var/cache/dnf /var/cache/yum /var/cache/zypp", tool.package_install_script(fallback))

    def test_os_update_failure_stops_before_package_installation(self):
        rpm = next(t for t in self.targets if t.operating_system["package_family"] == "rpm")
        fallback = dataclasses.replace(rpm, operating_system=dict(rpm.operating_system, family="other-rpm"))
        for target in [*self.targets, fallback]:
            family = target.operating_system["package_family"]
            managers = {"apk": ["apk"], "deb": ["apt-get"],
                        "rpm": ["dnf", "microdnf", "yum", "zypper"]}[family]
            for manager in managers:
                with self.subTest(os=target.os_id, family=target.family, manager=manager):
                    # Execute the real installer with inert package-manager functions.
                    # A failed update must propagate before install or cleanup runs.
                    stubs = f'''command() {{ test "$1" = -v && test "$2" = {manager}; }}
sed() {{ :; }}
rm() {{ echo UNEXPECTED_CLEANUP; return 92; }}
package_manager() {{
    echo "{manager} $*"
    case " $* " in
        *" install "*|*" add "*) return 91 ;;
        *" upgrade "*|*" dist-upgrade "*) return 19 ;;
        *" update "*)
            if [ {manager} = apt-get ]; then return 0; fi
            return 19 ;;
        *" refresh "*|*" clean expire-cache "*) return 0 ;;
        *) return 93 ;;
    esac
}}
alias {manager}=package_manager
'''
                    # Repository file setup has its own filesystem regression test;
                    # this test isolates package updates and subsequent cleanup.
                    with mock.patch.object(tool, "debian_repository_setup", return_value=""):
                        script = tool.package_install_script(target)
                    result = subprocess.run(["sh", "-c", "set -eu\n" + stubs + script],
                                            text=True, capture_output=True, timeout=5)
                    self.assertEqual(result.returncode, 19, result.stdout + result.stderr)
                    self.assertNotIn("UNEXPECTED_CLEANUP", result.stdout)
                    self.assertNotRegex(result.stdout, r"\s(?:install|add)\s")

    def test_retry_reuses_passed_platform_and_force_retests_all(self):
        options = argparse.Namespace(cluster_nodes=5, force=False, retry_failed=True, timeout=1800, keep_test_workdir=False)
        attempts = []
        platforms = [t.platform for t in self.alpine]
        fail_arm = True
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture), tempfile.TemporaryDirectory() as directory, mock.patch.object(tool, "MULTIARCH_CACHE_ROOT", pathlib.Path(directory)), \
                mock.patch.object(tool, "ensure_multiarch_builder"), mock.patch.object(tool, "publish_group"), \
                mock.patch.object(tool, "docker_command", return_value="docker"), \
                mock.patch.object(tool, "resolve_base_image", return_value=("alpine:3.21", "alpine:3.21@sha256:" + "a" * 64)) as pull:
            def refresh(target, timeout, keep, nodes, progress, prepared):
                attempts.append(target.platform)
                run = target.cache_directory / "runs" / tool.run_id()
                run.mkdir(parents=True)
                for name in tool.ARTIFACT_FILENAMES:
                    (run / name).write_bytes((target.group_directory / name).read_bytes())
                report = tool.initial_report(target, run.name, nodes, prepared["distributed_cookie"])
                report["status"] = "failed" if fail_arm and target.platform == "linux/arm64" else "passed"
                report["finished_at"] = tool.isoformat()
                report["artifacts"] = tool.artifact_downloads(target, *(run / n for n in tool.ARTIFACT_FILENAMES))
                tool.publish_current_run(target, run, report)
                return report["status"] == "passed"
            with mock.patch.object(tool, "refresh_target", side_effect=refresh), mock.patch.object(tool, "run_logged", return_value=mock.Mock(stdout="x86_64", returncode=0)):
                self.assertFalse(tool.refresh_group(self.alpine, options, self.targets))
                self.assertEqual(attempts, platforms)
                self.assertRegex(capture.getvalue(), r'\d{4}-\d\d-\d\d \d\d:\d\d:\d\d   PASSED linux/amd64')
                self.assertIn('FAILED linux/arm64', capture.getvalue())
                self.assertNotIn('PASSED linux/arm64', capture.getvalue())
                capture.seek(0)
                capture.truncate(0)
                fail_arm = False
                self.assertTrue(tool.refresh_group(self.alpine, options, self.targets))
                self.assertIn('PASSED linux/arm64', capture.getvalue())
                self.assertIn('SKIPPED linux/amd64', capture.getvalue())
                self.assertNotIn('PASSED linux/amd64', capture.getvalue())
                self.assertEqual(attempts, platforms + ["linux/arm64"])
                self.assertEqual(pull.call_count, len(platforms))
                self.assertTrue(tool.refresh_group(self.alpine, options, self.targets))
                self.assertEqual(len(attempts), len(platforms) + 1)
                options.force = True
                self.assertTrue(tool.refresh_group(self.alpine, options, self.targets))
                self.assertEqual(len(attempts), len(platforms) * 2 + 1)
                self.assertEqual(pull.call_count, len(platforms) * 2)

    def test_platform_harness_uses_temporary_tag_and_different_follower_cookies(self):
        with tempfile.TemporaryDirectory() as directory, mock.patch.object(tool, "MULTIARCH_CACHE_ROOT", pathlib.Path(directory)):
            target = self.alpine[0]
            root = target.group_directory
            root.mkdir(parents=True)
            cookie = "coordinator-test-cookie"
            bases = {t.platform: {"pinned": "alpine:3.21@sha256:" + "a" * 64} for t in self.alpine}
            (root / "Dockerfile").write_text(tool.render_multiarch_dockerfile(self.alpine, bases, cookie, [target.image]))
            (root / "compose.single.yaml").write_text(tool.render_single_compose(target, cookie))
            (root / "compose.cluster.yaml").write_text(tool.render_cluster_compose(target, distributed_cookie=cookie))
            (root / "example.env").write_text(tool.render_environment_example(target, cookie))
            workdir = pathlib.Path(directory) / "work"
            workdir.mkdir()
            prepared = {"distributed_cookie": cookie, "base_images": bases}
            # Stop before any runtime action by simulating an existing test container.
            with mock.patch.object(tool, "docker_command", return_value="docker"), \
                    mock.patch.object(tool.tempfile, "mkdtemp", return_value=str(workdir)), \
                    mock.patch.object(tool, "free_tcp_port", return_value=18098), \
                    mock.patch.object(tool, "run_logged", return_value=mock.Mock(returncode=0, stdout="")) as run:
                self.assertFalse(tool.refresh_target(target, 1800, keep_workdir=True, prepared=prepared))
            build = next(call.args[0] for call in run.call_args_list if "--tag" in call.args[0])
            temporary_tag = build[build.index("--tag") + 1]
            self.assertTrue(temporary_tag.startswith("openriak/openriak-kv:test-"))
            self.assertNotEqual(temporary_tag, target.image)
            cluster = (workdir / "compose.cluster.test.yaml").read_text()
            self.assertEqual(cluster.count(f"image: {temporary_tag}"), 5)
            self.assertEqual(cluster.count("platform: linux/amd64"), 5)
            cookies = [line.strip() for line in cluster.splitlines() if line.strip().startswith("RIAK_DISTRIBUTED_COOKIE:")]
            self.assertEqual(len(set(cookies)), 5)
            self.assertIn(cookie, cookies[0])
            self.assertIn("OPENRIAK_CLUSTER_WAIT_SECONDS=1800", (workdir / ".env.cluster").read_text())



class CookieTests(unittest.TestCase):
    def cookie_script(self):
        source = tool.ENTRYPOINT_SCRIPT
        helpers = source[source.index("validate_nodename() {"):source.index("atomic_control_file() {")]
        # Real marker parsing and validators, deterministic DNS for isolated shell tests.
        functions = source[source.index("# Read only live settings"):source.index("\nconfigure_timezone\n")]
        functions += source[source.index("existing_cookie=$(configured_cookie)"):source.index('log "configuration: preparing mounted directories"')]
        setter = source[source.index("set_setting() {"):source.index("node_host=${RIAK_NODE_HOST")]
        selection = source[source.index("cluster_mode=${OPENRIAK_CLUSTER_MODE:-single}"):source.index("initialize_setting ring_size")]
        return helpers + '\nnodename_resolves_to_ip() { [ "$2" = "172.25.0.2" ]; }\n' + functions + setter + selection

    def run_cookie(self, config, markers=(), pending=False, role="follower", init=False):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            conf = root / "riak.conf"
            conf.write_text(config)
            if pending:
                (root / ".openriak-cookie-pending").touch()
            for index, (cookie, ip) in enumerate(markers, 1):
                node = f"openriak-kv@node-{index}.cluster"
                suffix = str(index) * 16
                (root / f"{node}-{suffix}-coordinator").write_text(
                    f"nodename={node}\nip={ip}\ncoordinator={node}\nsuffix={suffix}\ncookie={cookie}\n")
            prelude = f'''set -eu
config_dir={shlex.quote(directory)}
control_dir=$config_dir
riak_node_name=openriak-kv@follower.cluster
RIAK_DISTRIBUTED_COOKIE=image-cookie
OPENRIAK_CLUSTER_MODE=cluster
OPENRIAK_CLUSTER_WAIT_SECONDS=0
RIAK_INIT_ONLY={int(init)}
role={role}
log() {{ echo "$*"; }}
clean_owned_control_files() {{ :; }}
'''
            result = subprocess.run(["sh", "-c", prelude + self.cookie_script()], capture_output=True, text=True, timeout=5)
            return result, conf.read_text(), (root / ".openriak-cookie-pending").exists()

    def test_existing_cookie_survives_image_and_coordinator_cookie_changes(self):
        result, config, _ = self.run_cookie("  distributed_cookie  = persisted-cookie  \n", [("other-cookie", "172.25.0.2")])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("  distributed_cookie  = persisted-cookie  \n", config)
        self.assertIn("preserving distributed cookie", result.stdout)
        self.assertNotIn("adopted coordinator cookie", result.stdout)

    def test_new_follower_adopts_coordinator_before_startup(self):
        result, config, pending = self.run_cookie("## distributed_cookie = packaged-cookie\n", [("cluster-cookie", "172.25.0.2")])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("distributed_cookie = cluster-cookie\n", config)
        self.assertIn("adopted coordinator cookie before daemon startup", result.stdout)
        self.assertFalse(pending)
        self.assertLess(tool.ENTRYPOINT_SCRIPT.index("wait_for_coordinator_cookie\nfi"), tool.ENTRYPOINT_SCRIPT.index("if riak_command daemon"))

    def test_interrupted_initialization_does_not_establish_package_cookie(self):
        result, config, pending = self.run_cookie("distributed_cookie = packaged-cookie\n", [("cluster-cookie", "172.25.0.2")], pending=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("distributed_cookie = cluster-cookie\n", config)
        self.assertFalse(pending)

    def test_missing_invalid_or_ambiguous_coordinator_never_starts_new_node(self):
        for markers in ([], [("bad cookie", "172.25.0.2")], [("good", "172.25.0.3")], [("one", "172.25.0.2"), ("two", "172.25.0.2")]):
            with self.subTest(markers=markers):
                result, config, pending = self.run_cookie("##distributed_cookie=packaged\n", markers)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("distributed_cookie = image-cookie", config)
                self.assertTrue(pending)

    def test_coordinator_retains_config_cookie(self):
        result, config, _ = self.run_cookie("distributed_cookie = existing-cluster\n", role="coordinator")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("distributed_cookie = existing-cluster\n", config)

    def test_init_only_follower_leaves_cookie_pending(self):
        result, config, pending = self.run_cookie("distributed_cookie = packaged\n", pending=True, init=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(pending)


if __name__ == "__main__":
    unittest.main()
