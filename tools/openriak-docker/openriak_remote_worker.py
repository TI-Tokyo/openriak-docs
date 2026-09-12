"""Small Linux control helper sent through SSH; it needs only the standard library.

Each deployment owns an isolated directory. Never replace a source tree used by a
running worker. Persist launch intent before spawning, so a lost SSH connection
cannot silently cause a second build on a retry.
"""
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import shutil
import subprocess
import sys
import tarfile
import tempfile


def read(path):
    return json.loads(path.read_text())


def write(path, data):
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.control-')
    try:
        with os.fdopen(fd, 'w') as handle:
            json.dump(data, handle)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(temporary)


def checksum(path):
    result = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def start_ticks(pid):
    try:
        # comm may itself contain spaces or parentheses; field 22 follows it.
        return Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[19]
    except (FileNotFoundError, ProcessLookupError):
        return None


def status(root):
    launch_path = root / 'launch.json'
    if not launch_path.exists():
        return {'status': 'staged', 'remote_dir': str(root)}
    launch = read(launch_path)
    pid = launch.get('pid')
    if not pid:
        return dict(launch, status='unknown', error='Launch was interrupted before its PID was saved; inspect this node before retrying')
    if not isinstance(pid, int) or pid < 1:
        raise ValueError('Invalid saved PID')
    process = subprocess.run(['ps', '-p', str(pid), '-o', 'stat=', '-o', 'args='],
                             capture_output=True, text=True, timeout=15)
    if process.returncode not in (0, 1):
        raise RuntimeError('ps failed: ' + process.stderr.strip())
    fields = process.stdout.strip().split(maxsplit=1)
    alive = bool(fields and not fields[0].startswith('Z') and launch.get('start_ticks')
                 and start_ticks(pid) == launch['start_ticks'])
    receipt_path = root / 'results' / 'worker.json'
    receipt = read(receipt_path) if receipt_path.exists() else None
    if receipt and (receipt.get('plan_id'), receipt.get('worker')) != (launch['plan_id'], launch['worker']):
        raise ValueError('Worker receipt does not belong to this launch')
    if receipt and receipt.get('pid', pid) != pid:
        return dict(launch, status='unknown', error='Worker receipt belongs to a different process; inspect any manual restart before fetching')
    if alive:
        state = 'running'
    elif receipt and receipt.get('status') in ('complete', 'failed', 'interrupted'):
        state = receipt['status']
    else:
        state = 'interrupted'
    return dict(launch, status=state, process=process.stdout.strip(), receipt=receipt)


def extract(root, request):
    source = root / 'source'
    marker = root / 'source.json'
    if source.exists():
        if not marker.exists() or read(marker)['sha256'] != request['sha256']:
            raise ValueError('Existing worker source differs from the staged bundle')
        return
    bundle = root / ('bundle-' + request['sha256'] + '.tar.gz')
    if checksum(bundle) != request['sha256']:
        raise ValueError('Staged bundle checksum mismatch')
    with tempfile.TemporaryDirectory(prefix='.source-', dir=root) as directory:
        stage = Path(directory)
        with tarfile.open(bundle) as archive:
            names = set()
            for member in archive.getmembers():
                path = stage / member.name
                if (not path.resolve().is_relative_to(stage) or not member.isfile()
                        or member.name in names or member.name.startswith('/')):
                    raise ValueError('Unsafe or duplicate worker bundle entry')
                names.add(member.name)
                path.parent.mkdir(parents=True, exist_ok=True)
                with archive.extractfile(member) as incoming, path.open('xb') as outgoing:
                    shutil.copyfileobj(incoming, outgoing)
                path.chmod(0o755 if member.mode & 0o111 else 0o644)
        plan = read(stage / 'plan.json')
        identity = {k: v for k, v in plan.items() if k != 'id'}
        calculated = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        if plan['id'] != request['plan_id'] or plan['id'] != calculated:
            raise ValueError('Staged plan checksum mismatch')
        for prefix, manifest in [('tools/openriak-docker', plan['sources']),
                                 ('content/openriak-kv/metadata', plan['metadata'])]:
            for name, value in manifest.items():
                path = stage / prefix / name
                if not path.resolve().is_relative_to(stage) or checksum(path) != value:
                    raise ValueError('Staged source or metadata checksum mismatch')
        os.replace(stage, source)
    write(marker, {'sha256': request['sha256']})


def control(request):
    raw_root = Path(request['remote_dir']).expanduser()
    if not raw_root.is_absolute():
        raise ValueError('Remote directory must be absolute or beneath ~/')
    if any(path.is_symlink() for path in [raw_root, *raw_root.parents]):
        raise ValueError('Remote working directory must not traverse symlinks')
    root = raw_root.resolve()
    if request['action'] in ('status', 'stop') and not root.exists():
        return {'status': 'staged', 'remote_dir': str(root)}
    root.mkdir(parents=True, exist_ok=True)
    with (root / 'control.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        owner = {'plan_id': request['plan_id'], 'worker': request['worker']}
        marker = root / 'owner.json'
        if marker.exists() and read(marker) != owner:
            raise ValueError('Remote folder belongs to another assignment')
        if not marker.exists():
            write(marker, owner)
        if request['action'] == 'prepare':
            return {'remote_dir': str(root)}
        if request['action'] == 'status':
            return status(root)
        if request['action'] == 'stop':
            current = status(root)
            if current['status'] != 'running':
                return current
            # Bind the signal to the exact process, never a recycled numeric PID.
            try:
                descriptor = os.pidfd_open(current['pid'])
            except ProcessLookupError:
                return status(root)
            try:
                if start_ticks(current['pid']) != current['start_ticks']:
                    raise ValueError('Worker PID changed; refusing to send a signal')
                signal.pidfd_send_signal(descriptor, signal.SIGTERM)
            finally:
                os.close(descriptor)
            return dict(status(root), stop_requested=True)
        retry = request['action'] == 'restart'
        if request['action'] not in ('start', 'restart'):
            raise ValueError('Unknown remote operation')
        if retry:
            current = status(root)
            if current.get('restart_id') == request['restart_id']:
                return current
            if current['status'] not in ('complete', 'failed', 'interrupted'):
                raise ValueError('Worker must be stopped before restarting its queue')
            if not re.fullmatch(r'[A-Za-z0-9_.-]+', request['restart_id']):
                raise ValueError('Invalid restart identifier')
        elif (root / 'launch.json').exists():
            return status(root)
        if not shutil.which('nohup'):
            raise ValueError('nohup is not installed on this node')
        if not retry:
            extract(root, request)
        source = root / 'source'
        results = root / 'results'
        results.mkdir(exist_ok=True)
        environment = os.environ.copy()
        if request.get('tmpdir'):
            temporary = Path(request['tmpdir']).expanduser()
            if not temporary.is_absolute() or not temporary.is_dir() or not os.access(temporary, os.W_OK | os.X_OK):
                raise ValueError(f'Configured worker TMPDIR is not writable: {temporary}; rerun check-nodes')
            environment['TMPDIR'] = str(temporary)
        launch = dict(owner, status='launching', remote_dir=str(root),
                      log=str(root / 'worker.log'), results=str(results))
        if retry:
            # Keep the frozen plan/source and group caches. Archive controller
            # records before the new runner replaces the current receipt.
            history = root / 'attempts' / request['restart_id']
            history.mkdir(parents=True, exist_ok=True)
            for filename in ('launch.json', 'results/worker.json'):
                original = root / filename
                saved = history / Path(filename).name
                if original.exists() and not saved.exists():
                    shutil.copy2(original, saved)
            runner = history / 'retry.py'
            source_text = request['runner']
            if hashlib.sha256(source_text.encode()).hexdigest() != request['runner_sha256']:
                raise ValueError('Retry runner checksum mismatch')
            if runner.exists() and runner.read_text() != source_text:
                raise ValueError('Retry runner changed during reconnection')
            runner.write_text(source_text)
            # status() must not mistake the previous receipt for a receipt from
            # the new PID while its interpreter is still starting up.
            (results / 'worker.json').unlink(missing_ok=True)
            launch['restart_id'] = request['restart_id']
        write(root / 'launch.json', launch)
        command = (['nohup', sys.executable, '-u', str(runner), '--source', str(source)] if retry else
                   ['nohup', sys.executable, '-u', str(source / 'tools/openriak-docker/openriak_docker.py'),
                    'distribute', 'worker', '--plan', str(source / 'plan.json')])
        command.extend(['--worker', str(request['worker']), '--output', str(results)])
        with (root / 'worker.log').open('ab') as log:
            process = subprocess.Popen(command, cwd=source, stdin=subprocess.DEVNULL,
                                       stdout=log, stderr=subprocess.STDOUT,
                                       start_new_session=True, close_fds=True, env=environment)
        launch.update(pid=process.pid, start_ticks=start_ticks(process.pid), status='running')
        write(root / 'launch.json', launch)
        return launch


if __name__ == '__main__':
    try:
        print(json.dumps(control(json.loads(sys.argv[1]))))
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
