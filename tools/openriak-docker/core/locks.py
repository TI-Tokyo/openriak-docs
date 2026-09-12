"""Process-scoped advisory locks; lock files are never deleted while in use."""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import socket
import tempfile


@contextmanager
def lock(tool, key, *, shared=False):
    root = Path(tempfile.gettempdir()) / f'openriak-docker-locks-{os.getuid()}'
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    path = root / (hashlib.sha256(str(key).encode()).hexdigest() + '.lock')
    with path.open('a+') as handle:
        try:
            fcntl.flock(handle, (fcntl.LOCK_SH if shared else fcntl.LOCK_EX) | fcntl.LOCK_NB)
        except BlockingIOError as error:
            handle.seek(0)
            raise tool.DockerToolError(f'Resource is in use: {key}; owner: {handle.read().strip() or "another worker"}') from error
        try:
            if not shared:
                handle.seek(0); handle.truncate()
                json.dump({'pid': os.getpid(), 'host': socket.gethostname(), 'started_at': tool.isoformat(), 'resource': str(key)}, handle)
                handle.flush()
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def activity(tool, *, shared=True):
    return lock(tool, f'activity:{tool.REPOSITORY_ROOT.resolve()}', shared=shared)
