"""Execution operations; dependencies are supplied by the public tool facade."""
from __future__ import annotations
import contextlib
import json
import os
import pathlib
import re
import signal
import shlex
import subprocess
from core.defaults import DEFAULT_TIMEOUT_SECONDS
DEFAULT_CLUSTER_NODES = 5


def run_logged(tool, command, log_path, *, cwd=None, environment=None, check=True,
               timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """Write child output directly to disk while retaining the command result API."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    started = tool.isoformat()
    with log_path.open('a+', encoding='utf-8', errors='replace', newline='\n') as handle:
        handle.write(f"$ {shlex.join(str(x) for x in command)}\nstarted: {started}\n")
        handle.flush()
        output_start = handle.tell()
        process = subprocess.Popen(command, cwd=cwd, env=environment, stdout=handle,
                                   stderr=subprocess.STDOUT, start_new_session=True)
        timed_out = False
        try:
            process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            with contextlib.suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        except BaseException:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=min(timeout_seconds, 10))
            except subprocess.TimeoutExpired:
                with contextlib.suppress(ProcessLookupError):
                    os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            handle.write('\nexit_code: interrupted\n')
            handle.flush()
            raise
        handle.seek(output_start)
        output = handle.read()
        handle.seek(0, 2)
        handle.write(f"\ntimeout_seconds: {timeout_seconds}\nexit_code: {'timeout' if timed_out else process.returncode}\n")
        handle.flush()
    if timed_out:
        raise tool.DockerToolError(f"Command timed out after {timeout_seconds}s: {shlex.join(command)} (see {log_path})")
    result = subprocess.CompletedProcess(command, process.returncode, output)
    if check and result.returncode:
        failure_lines = [line.strip() for line in output.splitlines() if 'ERROR:' in line or 'error:' in line]
        summary = failure_lines[-1] if failure_lines else output.strip()[-300:]
        raise tool.DockerToolError(f"Command failed with exit code {result.returncode}: {shlex.join(command)} (see {log_path}): {summary}")
    return result


def digest_from_pull_output(tool, output: str) -> str | None:
    match = re.search(
        r"^Digest:[ \t]*(sha256:[0-9a-f]{64})[ \t]*$",
        output,
        re.MULTILINE,
    )
    return match.group(1) if match else None


def resolve_base_image(tool,
    target: Target,
    logs: pathlib.Path,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    *, upstream: bool = False,
) -> tuple[str, str]:
    docker = tool.docker_command()
    base = tool.base_image_for(target, upstream=upstream)
    pull_result = tool.run_logged(
        [docker, "pull", "--platform", target.platform, base],
        logs / "base-image-pull.log",
        timeout_seconds=timeout_seconds,
    )
    result = tool.run_logged(
        [docker, "image", "inspect", "--format", "{{json .RepoDigests}}", base],
        logs / "base-image-inspect.log",
        timeout_seconds=timeout_seconds,
    )
    try:
        repo_digests = json.loads(result.stdout.strip())
    except json.JSONDecodeError as error:
        raise tool.DockerToolError(f"Docker returned invalid RepoDigests for {base}") from error
    if repo_digests:
        digest_reference = str(repo_digests[0])
        digest = digest_reference.rsplit("@", 1)[-1]
    else:
        digest = tool.digest_from_pull_output(pull_result.stdout)
        if digest is None:
            raise tool.DockerToolError(f"Docker did not return a digest for {base}")
    repository = base.rsplit(":", 1)[0]
    return base, f"{base}@{digest}" if "@" not in base else f"{repository}@{digest}"


def ensure_multiarch_builder(tool,
    logs: pathlib.Path, timeout: int, lifecycle: MultiarchBuilderLifecycle | None = None,
) -> None:
    if lifecycle is not None:
        lifecycle.acquire()
    docker = tool.docker_command()
    inspected = tool.run_logged([docker, "buildx", "inspect", tool.MULTIARCH_BUILDER], logs / "builder.log", check=False, timeout_seconds=timeout)
    if lifecycle is not None:
        lifecycle.observe(inspected, logs, timeout)
    if inspected.returncode:
        tool.run_logged([docker, "buildx", "create", "--name", tool.MULTIARCH_BUILDER, "--driver", "docker-container"], logs / "builder.log", timeout_seconds=timeout)
        if lifecycle is not None:
            lifecycle.stop_required = True
    tool.run_logged([docker, "buildx", "inspect", tool.MULTIARCH_BUILDER, "--bootstrap"], logs / "builder.log", timeout_seconds=timeout)
