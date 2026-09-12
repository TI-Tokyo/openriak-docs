"""Standalone worker checks, executed locally or sent through SSH as Python.

Only the explicit repair actions install emulation or create a persistent temp
directory. Probes use uniquely named containers and disposable scratch folders.
"""
import contextlib
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tempfile
import time


class CommandError(RuntimeError):
    """A failed Docker command, distinct from a host-side bind verification."""


def command(arguments, timeout):
    result = subprocess.run(arguments, stdin=subprocess.DEVNULL, capture_output=True,
                            text=True, timeout=timeout)
    if result.returncode:
        raise CommandError((result.stderr or result.stdout or f'exit {result.returncode}')[-2000:].strip())
    return result.stdout.strip()


def container(arguments, timeout):
    name = 'openriak-worker-check-' + secrets.token_hex(12)
    try:
        return command(['docker', 'run', '--rm', '--name', name, *arguments], timeout)
    finally:
        # A timed-out Docker client can leave its container running. Remove only
        # this probe; a successful --rm run has already removed it.
        with contextlib.suppress(RuntimeError, subprocess.TimeoutExpired, OSError):
            command(['docker', 'rm', '--force', name], min(timeout, 10))


def temporary_root(request):
    configured = request.get('tmpdir')
    if configured:
        root = Path(configured).expanduser()
        if not root.is_absolute():
            raise ValueError('Worker TMPDIR must be absolute or beneath ~/')
        if not root.is_dir() or not os.access(root, os.W_OK | os.X_OK):
            raise ValueError(f'Worker TMPDIR is not writable: {root}')
        return str(root)
    return tempfile.gettempdir()


def check(request):
    timeout = request['timeout']
    action = request['action']
    if action == 'prerequisites':
        for program in ('docker', 'nohup', 'ps', 'cp', 'tail'):
            if not shutil.which(program):
                raise RuntimeError(f'Worker requires {program} on PATH')
        folder = Path(request['workdir']).expanduser()
        if not folder.is_absolute():
            raise ValueError('Working directory must be absolute or beneath ~/')
        existing = folder
        while not existing.exists():
            existing = existing.parent
        if not existing.is_dir() or not os.access(existing, os.W_OK | os.X_OK):
            raise RuntimeError(f'Working directory is not writable: {existing}')
        deadline = time.monotonic() + timeout
        info = json.loads(command(['docker', 'info', '--format', '{{json .}}'], timeout))
        for arguments in (['docker', 'buildx', 'version'], ['docker', 'compose', 'version']):
            command(arguments, max(0.1, deadline - time.monotonic()))
        architecture = {'x86_64': 'amd64', 'aarch64': 'arm64'}.get(info['Architecture'], info['Architecture'])
        return {'ok': True, 'platform': 'linux/' + architecture,
                'docker_root': info.get('DockerRootDir'),
                'repair_tmpdir': str(Path.home() / 'openriak-builds' / 'tmp')}
    if action == 'arm64':
        try:
            output = container(['--platform', 'linux/arm64', request['image'], 'uname', '-m'], timeout)
        except RuntimeError as error:
            return {'ok': False, 'error': str(error),
                    'repairable': 'exec format error' in str(error).lower()}
        return {'ok': output == 'aarch64', 'error': f'Expected aarch64, got {output!r}',
                'repairable': False}
    if action == 'install-arm64':
        container(['--privileged', request['binfmt_image'], '--install', 'arm64'], timeout)
        return {'ok': True}
    if action == 'create-tmpdir':
        root = Path(request['tmpdir']).expanduser()
        # The approved repair uses an ordinary directory in this worker's home,
        # where Snap Docker's home interface can access it.
        if (not root.is_absolute() or root == Path.home()
                or not root.is_relative_to(Path.home())
                or any(part.startswith('.') for part in root.relative_to(Path.home()).parts)
                or any(p.is_symlink() for p in [root, *root.parents])):
            raise ValueError('Repair TMPDIR must be a non-hidden, non-symlink directory beneath the worker home')
        root.mkdir(parents=True, exist_ok=True)
        return {'ok': True, 'tmpdir': temporary_root(request)}
    if action == 'bind':
        try:
            root = temporary_root(request)
            with tempfile.TemporaryDirectory(prefix='openriak-bind-check-', dir=root) as directory:
                token = secrets.token_hex(16)
                folder = Path(directory)
                (folder / 'from-host').write_text(token)
                output = container(['--platform', request['platform'],
                    '--mount', f'type=bind,source={directory},target=/check', request['image'],
                    'sh', '-c', 'cat /check/from-host\nprintf "%s" "$1" > /check/from-container',
                    'sh', token], timeout)
                if output != token or (folder / 'from-container').read_text() != token:
                    raise RuntimeError('Host and container see different temporary files')
            return {'ok': True, 'tmpdir': root}
        except CommandError as error:
            return {'ok': False, 'error': str(error),
                    'repairable': any(term in str(error).lower() for term in ('/check/', 'mount'))}
        except (OSError, ValueError, RuntimeError) as error:
            return {'ok': False, 'error': str(error), 'repairable': True}
    raise ValueError('Unknown worker check action')


if __name__ == '__main__':
    try:
        print(json.dumps(check(json.loads(sys.argv[1]))))
    except Exception as error:
        print(json.dumps({'ok': False, 'error': str(error), 'repairable': False}))
