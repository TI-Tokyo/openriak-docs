import argparse
import contextlib
import io
import pathlib
import tempfile
import unittest
from unittest import mock
from test_openriak_docker import docker_tool as tool


class ApprovedRebuildTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.patch = mock.patch.object(tool, "MULTIARCH_CACHE_ROOT", pathlib.Path(self.temporary.name))
        self.patch.start()
        self.addCleanup(self.patch.stop)
        all_targets = tool.discover_targets(["3.4.1"])
        self.group = next(g for g in tool.grouped_targets(all_targets) if g[0].image_tag == "3.4.1-alpine-3.21-otp26")
        self.target = self.group[0]
        self.root = self.target.group_directory
        self.root.mkdir(parents=True)
        for filename in tool.ARTIFACT_FILENAMES:
            (self.root / filename).write_text(f"approved {filename}\n")
        artifacts = tool.artifact_downloads(self.target, *(self.root / n for n in tool.ARTIFACT_FILENAMES))
        self.report = {
            "schema_version": 4, "product": "openriak-kv", "version": "3.4.1",
            "status": "passed", "image": self.target.image, "tags": tool.image_aliases(self.target, all_targets),
            "inputs": {"runtime_sha256": "older-approved-renderer"}, "run_id": "approved-run",
            "finished_at": "2026-09-05T23:00:00Z", "platforms": [t.platform for t in self.group],
            "cluster_nodes": 5, "artifacts": artifacts, "platform_results": {},
        }
        for target in self.group:
            proof = tool.initial_report(target, "platform-approval", 5, "approved-cookie")
            proof.update(status="passed", artifacts=artifacts)
            proof["tests"] = {
                "admin_test": {"status": "passed"}, "preserved_cookie": {"status": "passed"},
                "cluster": {"status": "passed", "coordinator_cookie_adoption": "passed"},
                "cluster_admin_test": {f"node{i}": {"status": "passed"} for i in range(1, 6)},
            }
            proof_path = target.cache_directory / "runs" / "platform-approval" / "report.json"
            tool.write_json(proof_path, proof)
            self.report["platform_results"][target.platform] = {
                "status": "passed", "run_id": "platform-approval", "report": str(proof_path.relative_to(self.root)),
            }
        tool.write_json(self.root / "report.json", self.report)
        self.options = argparse.Namespace(extra_namespace=["tiotjp"], timeout=1800)

    def test_rebuild_preserves_approval_and_uses_all_aliases_without_tests(self):
        original = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(tool, "ensure_multiarch_builder"), \
                mock.patch.object(tool, "docker_command", return_value="docker"), \
                mock.patch.object(tool, "run_logged", return_value=mock.Mock(returncode=0, stdout="x86_64")) as run, \
                mock.patch.object(tool, "refresh_target", side_effect=AssertionError("must not test")), \
                mock.patch.object(tool, "resolve_base_image", side_effect=AssertionError("must not refresh digests")), \
                mock.patch.object(tool, "render_multiarch_dockerfile", side_effect=AssertionError("must not regenerate")), \
                mock.patch.object(tool, "sync_download_metadata", side_effect=AssertionError("must not rewrite test metadata")):
            self.assertTrue(tool.rebuild_approved_group(self.group, self.options))
        for path, contents in original.items():
            self.assertEqual(path.read_bytes(), contents)
        output, = self.root.glob('rebuilds/*/report.json')
        report = tool.read_json(output)
        self.assertEqual(report["status"], "built")
        self.assertEqual(report["tests"]["status"], "not_run")
        self.assertEqual(report["approved_run_id"], "approved-run")
        expected = self.report["tags"] + [tag.replace("openriak/openriak-kv:", "tiotjp/openriak-kv:", 1) for tag in self.report["tags"]]
        self.assertEqual(report["build_tags"], expected)
        commands = [call.args[0] for call in run.call_args_list]
        export = next(command for command in commands if "--output" in command)
        local = next(command for command in commands if "--load" in command)
        self.assertIn("--no-cache", export)
        self.assertNotIn("--no-cache", local)
        self.assertIn("linux/amd64,linux/arm64", export)
        self.assertIn("linux/amd64", local)
        for command in (export, local):
            self.assertEqual([command[i + 1] for i, arg in enumerate(command[:-1]) if arg == "--tag"], expected)
            self.assertNotIn("--push", command)
        for filename in tool.ARTIFACT_FILENAMES:
            self.assertEqual((output.parent / filename).read_bytes(), original[self.root / filename])

    def test_tampered_files_are_rejected_before_docker(self):
        (self.root / "Dockerfile").write_text("unapproved change\n")
        with mock.patch.object(tool, "ensure_multiarch_builder") as builder:
            with self.assertRaises(tool.DockerToolError):
                tool.rebuild_approved_group(self.group, self.options)
            builder.assert_not_called()
        self.assertFalse((self.root / "rebuilds").exists())

    def test_missing_or_failed_platform_approval_is_rejected(self):
        result = self.report["platform_results"]["linux/arm64"]
        path = self.root / result["report"]
        proof = tool.read_json(path)
        proof["tests"]["cluster_admin_test"]["node5"]["status"] = "failed"
        tool.write_json(path, proof)
        with self.assertRaises(tool.DockerToolError):
            tool.approved_group_report(self.group)
        path.unlink()
        with self.assertRaises(tool.DockerToolError):
            tool.approved_group_report(self.group)

    def test_build_failure_keeps_passed_report_unchanged(self):
        before = (self.root / "report.json").read_bytes()
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(tool, "ensure_multiarch_builder"), \
                mock.patch.object(tool, "build_group_images", side_effect=tool.DockerToolError("build failed")):
            self.assertFalse(tool.rebuild_approved_group(self.group, self.options))
        self.assertEqual((self.root / "report.json").read_bytes(), before)
        report, = self.root.glob('rebuilds/*/report.json')
        self.assertEqual(tool.read_json(report)["status"], "failed")

    def test_extra_namespaces_are_validated_and_deduplicated(self):
        tags = ["openriak/openriak-kv:3.4.1", "openriak/openriak-kv:latest"]
        self.assertEqual(tool.namespaced_tags(tags, ["tiotjp", "tiotjp", "openriak"]),
                         tags + ["tiotjp/openriak-kv:3.4.1", "tiotjp/openriak-kv:latest"])
        for namespace in ["", "https://tiotjp", "tiotjp/other", "Uppercase", "--push", "name:port"]:
            with self.subTest(namespace=namespace), self.assertRaises(argparse.ArgumentTypeError):
                tool.extra_namespace(namespace)

    def test_cli_skips_unapproved_groups_and_does_not_sync_metadata(self):
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(tool, "discover_targets", return_value=self.group), \
                mock.patch.object(tool, "rebuild_approved_group", return_value=True) as rebuild, \
                mock.patch.object(tool, "refresh_group", side_effect=AssertionError("must not refresh")), \
                mock.patch.object(tool, "sync_download_metadata", side_effect=AssertionError("must not publish")):
            self.assertEqual(tool.main(["refresh", "--all", "--yes", "--do-not-test", "--extra-namespace", "tiotjp"]), 0)
            rebuild.assert_called_once()
            self.report["status"] = "failed"
            tool.write_json(self.root / "report.json", self.report)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(tool.main(["refresh", "--all", "--yes", "--do-not-test"]), 2)
            self.assertEqual(rebuild.call_count, 1)

    def test_do_not_test_conflicts_with_regeneration_flags(self):
        for flag in ("--force", "--retry-failed"):
            with self.subTest(flag=flag), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                tool.parser().parse_args(["refresh", "--version", "3.4.1", "--do-not-test", flag])


if __name__ == "__main__":
    unittest.main()
