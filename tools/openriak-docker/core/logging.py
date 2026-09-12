from __future__ import annotations
import argparse
import datetime as dt
import os
from typing import Any
from core.context import context


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def isoformat(value: dt.datetime | None=None) -> str:
    return (value or context.utc_now()).isoformat(timespec='seconds').replace('+00:00', 'Z')


def log_timestamp(value: dt.datetime | None=None) -> str:
    return (value or dt.datetime.now().astimezone()).strftime('%Y-%m-%d %H:%M:%S')


def run_id(value: dt.datetime | None=None) -> str:
    return (value or context.utc_now()).strftime('%Y%m%dT%H%M%S.%fZ')


def print_refresh_header(options: argparse.Namespace, targets: list[Target], started_at: dt.datetime | None=None) -> None:
    versions = 'all' if options.all else ', '.join(dict.fromkeys((t.version for t in targets)))
    os_patterns = [options.os_id] if isinstance(options.os_id, str) else options.os_id or []
    os_selection = ', '.join(os_patterns) or 'all'
    if options.os_id or options.download_id:
        architectures = ', '.join(dict.fromkeys((t.architecture for t in targets)))
    else:
        architectures = 'all'
    separator = '=' * 64
    print(separator)
    print(f"Docker script started at {context.log_timestamp(started_at)}\nPID:           {os.getpid()}\nLog file:      {os.environ.get('OPENRIAK_DOCKER_LOG_FILE', 'stdout/stderr')}")
    print(f'Version:       {versions}')
    print(f'OS:            {os_selection}')
    print(f'Architecture:  {architectures}')
    print(f'Namespace:     {context.identity_from_options(options).namespace}')
    print(f'Vendor:        {context.identity_from_options(options).vendor}')
    print(f"Output:        {getattr(options, 'output', None) or 'docs cache'}")
    print(f"Docs updates:  {('disabled' if getattr(options, 'output', None) or getattr(options, 'do_not_test', False) else 'enabled')}")
    print(f'Timeout:       {options.timeout}s')
    print(f"Cluster nodes: {('from approved files' if getattr(options, 'do_not_test', False) else options.cluster_nodes)}")
    print(separator, flush=True)


class IndentedProgress:
    """Indent continuation output, including prints split across multiple writes."""

    def __init__(self, stream: Any, width: int):
        self.stream = stream
        self.indent = ' ' * width
        self.line_start = True

    def write(self, text: str) -> int:
        for part in text.splitlines(keepends=True):
            if self.line_start and part.strip('\r\n'):
                self.stream.write(self.indent)
            self.stream.write(part)
            self.line_start = part.endswith(('\n', '\r'))
        return len(text)

    def flush(self) -> None:
        self.stream.flush()

    def __getattr__(self, name: str) -> Any:
        return getattr(self.stream, name)
