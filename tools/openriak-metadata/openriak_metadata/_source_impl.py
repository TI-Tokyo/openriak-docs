from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from .erlang import TermParser, tuple_values


@dataclass
class Repository:
    name: str
    repository: str
    commit: str
    dependency_depth: int
    path: Path


class SourceError(RuntimeError):
    pass


class SourceResolver:
    def __init__(self, cache_dir: Path, refresh: bool = False, keep_workdir: bool = False) -> None:
        self.cache_dir = cache_dir
        self.refresh = refresh
        self.keep_workdir = keep_workdir
        self.workdir = Path(tempfile.mkdtemp(prefix="openriak-metadata-"))
        (cache_dir / "git").mkdir(parents=True, exist_ok=True)

    def close(self) -> None:
        if not self.keep_workdir:
            shutil.rmtree(self.workdir, ignore_errors=True)

    def resolve(self, repository: str, tag: str) -> tuple[Repository, list[Repository], list[str]]:
        url = _repository_url(repository)
        root_path, commit = self._checkout(url, tag, "root")
        root = Repository(_repo_name(url), repository, commit, 0, root_path)
        repositories = [root]
        warnings: list[str] = []
        lock = root_path / "rebar.lock"
        dependencies = parse_rebar_lock(lock.read_text("utf-8", errors="replace")) if lock.exists() else []
        if not dependencies:
            config = root_path / "rebar.config"
            if config.exists():
                dependencies = parse_rebar_config_dependencies(config.read_text("utf-8", errors="replace"))
                warnings.append("rebar.lock was unavailable or empty; dependencies were resolved from static rebar.config declarations.")
        seen = {(url, commit)}
        queue = [(name, dep_url, ref, 1) for name, dep_url, ref in dependencies]
        while queue:
            name, dep_url, ref, depth = queue.pop(0)
            try:
                path, sha = self._checkout(dep_url, ref, f"dep-{len(repositories):04d}-{name}")
            except Exception as exc:
                warnings.append(f"Could not resolve dependency {name} at {ref}: {exc}")
                continue
            identity = (_repository_url(dep_url), sha)
            if identity in seen:
                shutil.rmtree(path, ignore_errors=True)
                continue
            seen.add(identity)
            repo = Repository(name, dep_url, sha, depth, path)
            repositories.append(repo)
            child_lock = path / "rebar.lock"
            child_deps = parse_rebar_lock(child_lock.read_text("utf-8", errors="replace")) if child_lock.exists() else []
            if not child_deps:
                child_config = path / "rebar.config"
                if child_config.exists():
                    child_deps = parse_rebar_config_dependencies(child_config.read_text("utf-8", errors="replace"))
            queue.extend((n, u, r, depth + 1) for n, u, r in child_deps)
        return root, repositories, warnings

    def _checkout(self, repository: str, ref: str, name: str) -> tuple[Path, str]:
        canonical = _repository_url(repository)
        cache_name = hashlib.sha256(canonical.encode()).hexdigest()[:24] + ".git"
        bare = self.cache_dir / "git" / cache_name
        if not bare.exists():
            self._git("clone", "--bare", canonical, str(bare))
        elif self.refresh:
            self._git("-C", str(bare), "fetch", "--prune", "origin")
        # Fetching the exact ref prevents a stale cache from selecting a moving branch.
        self._git("-C", str(bare), "fetch", "--force", "--depth", "1", "origin", ref)
        commit = self._git("-C", str(bare), "rev-parse", "FETCH_HEAD").strip()
        destination = self.workdir / name
        self._git("clone", "--quiet", "--no-checkout", str(bare), str(destination))
        self._git("-C", str(destination), "checkout", "--quiet", "--detach", commit)
        return destination, commit

    @staticmethod
    def _git(*args: str) -> str:
        process = subprocess.run(["git", *args], capture_output=True, text=True, timeout=120)
        if process.returncode:
            raise SourceError(process.stderr.strip() or "git failed")
        return process.stdout


def _repository_url(repository: str) -> str:
    if repository.startswith("git@github.com:"):
        repository = "github.com/" + repository.split(":", 1)[1]
    if not repository.startswith(("http://", "https://", "file://")) and not os.path.exists(repository):
        repository = "https://" + repository
    if repository.startswith("http") and not repository.endswith(".git"):
        repository += ".git"
    return repository


def _repo_name(repository: str) -> str:
    return Path(urlparse(repository).path).stem


def parse_rebar_lock(text: str) -> list[tuple[str, str, str]]:
    # Locked git entries are deliberately parsed as balanced Erlang terms first.
    normalized = re.sub(r"<<(\"(?:\\.|[^\"])*\")>>", r"\1", text)
    try:
        terms = TermParser(normalized).parse_all()
    except Exception:
        return []
    found: list[tuple[str, str, str]] = []
    for term, _ in terms:
        _walk_dependency_terms(term, found)
    return _dedupe_dependencies(found)


def parse_rebar_config_dependencies(text: str) -> list[tuple[str, str, str]]:
    normalized = re.sub(r"<<(\"(?:\\.|[^\"])*\")>>", r"\1", text)
    try:
        terms = TermParser(normalized).parse_all()
    except Exception:
        return []
    found: list[tuple[str, str, str]] = []
    for term, _ in terms:
        _walk_dependency_terms(term, found)
    return _dedupe_dependencies(found)


def _walk_dependency_terms(value, found: list[tuple[str, str, str]]) -> None:
    values = tuple_values(value)
    if values:
        # Lock/config forms include {Name, {git, URL, {ref|tag, Revision}}, ...}.
        if len(values) >= 2 and isinstance(values[0], str):
            git = tuple_values(values[1])
            if git and len(git) >= 3 and git[0] == "git" and isinstance(git[1], str):
                revision = tuple_values(git[2])
                if revision and len(revision) >= 2 and revision[0] in ("ref", "tag", "branch"):
                    found.append((values[0], git[1], str(revision[1])))
        for child in values:
            _walk_dependency_terms(child, found)
    elif isinstance(value, list):
        for child in value:
            _walk_dependency_terms(child, found)


def _dedupe_dependencies(items: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    result, seen = [], set()
    for item in items:
        identity = (_repository_url(item[1]), item[2])
        if identity not in seen:
            seen.add(identity); result.append(item)
    return result


def is_erlang_repository(path: Path) -> bool:
    return ((path / "rebar.config").exists() or (path / "rebar.config.script").exists()
            or any(path.glob("src/*.erl")) or any(path.glob("apps/*/src/*.erl"))
            or any(path.rglob("*.app.src")) or any(path.glob("priv/*.schema")))
