import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from openriak_metadata.source import SourceResolver


class SourceCheckoutTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="metadata-source-test-")
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.upstream = self.directory / "upstream"
        self.git("init", "--quiet", "--initial-branch=main", str(self.upstream))
        self.git("-C", str(self.upstream), "config", "user.name", "Source test")
        self.git("-C", str(self.upstream), "config", "user.email", "test@example.invalid")
        self.resolver = SourceResolver(self.directory / "cache")
        self.addCleanup(self.resolver.close)

    @staticmethod
    def git(*args):
        return subprocess.run(
            ["git", *args], check=True, capture_output=True, text=True,
        ).stdout.strip()

    def commit(self, content):
        (self.upstream / "setting.txt").write_text(content, encoding="utf-8")
        self.git("-C", str(self.upstream), "add", "setting.txt")
        self.git("-C", str(self.upstream), "commit", "--quiet", "-m", content)
        return self.git("-C", str(self.upstream), "rev-parse", "HEAD")

    def assert_checkout(self, ref, expected_commit, expected_content):
        path, commit = self.resolver._checkout(str(self.upstream), ref, "dependency")
        self.assertEqual(commit, expected_commit)
        self.assertEqual(self.git("-C", str(path), "rev-parse", "HEAD"), expected_commit)
        self.assertEqual((path / "setting.txt").read_text("utf-8"), expected_content)

    def test_pinned_commit_behind_shallow_boundary(self):
        old_commit = self.commit("old settings")
        current_commit = self.commit("current settings")
        self.assert_checkout("main", current_commit, "current settings")

        # The exact fetch reaches an older commit outside the shallow history
        # advertised by the cache's branch, so cloning alone can omit it.
        self.assert_checkout(old_commit, old_commit, "old settings")

    def test_moving_branch_with_stale_cache_ref(self):
        old_commit = self.commit("old settings")
        self.assert_checkout("main", old_commit, "old settings")
        new_commit = self.commit("new settings")

        # The cache's branch still points at the first commit; the next exact
        # fetch records the new tip in FETCH_HEAD only.
        self.assert_checkout("main", new_commit, "new settings")

    def test_cached_immutable_commit_needs_no_upstream(self):
        commit = self.commit("pinned settings")
        self.assert_checkout(commit, commit, "pinned settings")
        self.upstream.rename(self.directory / "offline-upstream")
        self.upstream.mkdir()  # Keep the local-path spelling stable, but no Git repository.
        self.assert_checkout(commit, commit, "pinned settings")

    def test_duplicate_dependency_ref_resolved_once_per_snapshot(self):
        dependency = self.directory / 'dependency'
        self.git('init', '--quiet', '--initial-branch=main', str(dependency))
        self.git('-C', str(dependency), 'config', 'user.name', 'Source test')
        self.git('-C', str(dependency), 'config', 'user.email', 'test@example.invalid')
        self.git('-C', str(dependency), 'commit', '--quiet', '--allow-empty', '-m', 'dependency')
        (self.upstream / 'rebar.lock').write_text(
            '[{first, {git, "' + dependency.as_uri() + '", {branch, "main"}}, 0},'
            '{second, {git, "' + dependency.as_uri() + '", {branch, "main"}}, 0}].')
        self.git('-C', str(self.upstream), 'add', 'rebar.lock')
        self.commit('root')
        with patch.object(self.resolver, '_checkout', wraps=self.resolver._checkout) as checkout:
            root, repositories, warnings = self.resolver.resolve(str(self.upstream), 'main')
        self.assertEqual(checkout.call_count, 2)
        self.assertEqual(len(repositories), 2)
        self.assertEqual(warnings, [])
        # Release-only discovery must not inspect a dependency's development graph.
        with patch('openriak_metadata._source_impl.parse_rebar_config_dependencies',
                   side_effect=AssertionError('unexpected development dependency traversal')):
            (dependency / 'rebar.config').write_text('{deps, []}.')
            self.git('-C', str(dependency), 'add', 'rebar.config')
            self.git('-C', str(dependency), 'commit', '--quiet', '-m', 'development config')
            _, locked, warnings = self.resolver.resolve(str(self.upstream), 'main', recursive=False)
        self.assertEqual(len(locked), 2)
        self.assertEqual(warnings, [])


if __name__ == "__main__":
    unittest.main()
