from __future__ import annotations
import pathlib
import re
import shutil
import subprocess
from typing import Any
import core.locks as openriak_locks
from core.context import context


def docker_command() -> str:
    executable = shutil.which('docker') or shutil.which('docker.exe')
    if not executable:
        raise context.DockerToolError('Docker CLI was not found on PATH')
    return executable


class MultiarchBuilderLifecycle:
    """Restore builder state once per invocation, including interrupted builds."""

    def __init__(self) -> None:
        self.logs: pathlib.Path | None = None
        self.timeout = 0
        self.stop_required = False
        self.lease = None

    def acquire(self):
        if self.lease is None:
            lease = openriak_locks.lock(context, f'builder:{context.MULTIARCH_BUILDER}')
            lease.__enter__()
            self.lease = lease

    def observe(self, inspection: subprocess.CompletedProcess[str], logs: pathlib.Path, timeout: int) -> None:
        if self.logs is not None:
            return
        if inspection.returncode == 0:
            states = re.findall('^Status:\\s*(\\S+)\\s*$', inspection.stdout, re.MULTILINE)
            if not states or any((state not in ('running', 'stopped') for state in states)):
                raise context.DockerToolError(f'Cannot determine usable node states for builder {context.MULTIARCH_BUILDER}; inspect it before refresh')
            stopped = all((state == 'stopped' for state in states))
            if not stopped and 'stopped' in states:
                raise context.DockerToolError(f'Builder {context.MULTIARCH_BUILDER} has mixed running/stopped nodes; start it explicitly before refresh')
            if stopped and (not re.search('^Driver:\\s*docker-container\\s*$', inspection.stdout, re.MULTILINE)):
                raise context.DockerToolError(f'Cannot temporarily start stopped builder {context.MULTIARCH_BUILDER}: expected the docker-container driver')
            self.stop_required = stopped
        self.logs = logs
        self.timeout = timeout

    def __enter__(self) -> MultiarchBuilderLifecycle:
        return self

    def __exit__(self, exception_type: Any, exception: Any, traceback: Any) -> None:
        try:
            if self.stop_required:
                print(f'{context.log_timestamp()} Stopping builder {context.MULTIARCH_BUILDER} started for this refresh', flush=True)
                context.run_logged([context.docker_command(), 'buildx', 'stop', context.MULTIARCH_BUILDER], self.logs / 'builder.log', timeout_seconds=self.timeout)
        finally:
            if self.lease is not None:
                self.lease.__exit__(exception_type, exception, traceback)
                self.lease = None
