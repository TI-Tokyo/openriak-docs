"""Cutoff-based cleanup for this repository's OpenRiak KV Docker generator."""
from __future__ import annotations

import core.locks as openriak_locks
import contextlib
import argparse
import datetime as dt
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import time

from core.defaults import DEFAULT_TIMEOUT_SECONDS


def timestamp(value: str) -> dt.datetime:
    # Docker emits nanoseconds; Python 3.10 accepts at most six fractional digits.
    value = re.sub(r'(\.\d{6})\d+(?=Z|[+-]\d\d:\d\d$)', r'\1', value)
    parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('The cutoff must include a timezone, for example 2026-09-06T15:30:00+09:00')
    return parsed


def cutoff_argument(value: str) -> dt.datetime:
    try:
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d+)?)?', value):
            # A naive datetime is interpreted in the machine's local timezone,
            # including the local UTC offset applicable to that date.
            return dt.datetime.fromisoformat(value).astimezone()
        return timestamp(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            'Use YYYY-MM-DD, YYYY-MM-DDThh:mm:ss, or an ISO timestamp with a UTC offset'
        ) from error


def configure_parser(parser):
    parser.add_argument('--before', type=cutoff_argument, metavar='DATE_OR_TIMESTAMP',
                        help='Keep activity at or after this cutoff; dates mean local midnight, times without an offset are local (default: now)')
    parser.add_argument('--remove-all', action='store_true',
                        help='Also remove older local caches, images and build cache; stop older workers (retained records/downloads are protected)')
    parser.add_argument('--remove-downloads', action='store_true', help='With --remove-all, also remove selected published downloads and their metadata')
    parser.add_argument('--remove-records', action='store_true', help='With --remove-all --remove-downloads, also delete the selected durable evidence and approved source files')
    parser.add_argument('--clear-archives', action='store_true', help='Remove all local Scout payloads, diagnostic logs, OCI archives and archived bundles regardless of age; still requires --delete')
    parser.add_argument('--delete', action='store_true', help='Apply cleanup; otherwise only show a preview')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT_SECONDS, help='Seconds per Docker operation or worker shutdown wait (default: 1800)')


def read_report(path):
    return json.loads(path.read_text())


def report_time(report):
    values = [timestamp(report[key]) for key in ('started_at', 'finished_at', 'tested_at', 'testedAt') if report.get(key)]
    return max(values) if values else None


def tree_is_old(path, cutoff):
    if path.is_symlink() or not path.exists():
        return False
    for item in [path, *path.rglob('*')] if path.is_dir() else [path]:
        if item.is_symlink() or item.stat().st_mtime >= cutoff.timestamp():
            return False
        if item.name == 'report.json' and item.is_file():
            when = report_time(read_report(item))
            if when is None or when >= cutoff:
                return False
    return True


def contained(path, parents):
    return any(path == parent or parent in path.parents for parent in parents)


def cache_records(tool):
    roots = (tool.CACHE_ROOT, tool.MULTIARCH_CACHE_ROOT)
    records = [(p, read_report(p)) for root in roots for p in root.rglob('report.json')]
    current = [(p, report) for p, report in records
               if not {'runs', 'rebuilds'}.intersection(p.relative_to(next(root for root in roots if root in p.parents)).parts)]
    return records, current


def file_plan(tool, cutoff, remove_all=False, remove_downloads=False):
    records, current = cache_records(tool)
    trees, files, protected = set(), set(), set()
    recent_images, recent_downloads = set(), set()
    if remove_all and remove_downloads:
        for path in (tool.REPOSITORY_ROOT / 'tools/generated/openriak-kv/data/versions').glob('*.json'):
            for entry in read_report(path).get('dockerImages', []):
                when = report_time(entry)
                if when is None or when >= cutoff:
                    recent_images.add(entry.get('image'))
                    url = entry.get('dockerfile', {}).get('url', '')
                    if url.startswith('downloads/docker/'):
                        recent_downloads.add((tool.STATIC_ROOT / url[len('downloads/docker/'):]).parent)
    if remove_all:
        for path, report in sorted(current, key=lambda pair: len(pair[0].parts)):
            if 'pushes' in path.parts:
                # Raw evidence follows the separate 90-day archive policy.
                continue
            if report.get('image') not in recent_images and not contained(path, trees) and tree_is_old(path.parent, cutoff):
                trees.add(path.parent)
    for path, report in current:
        if contained(path, trees):
            continue
        if report.get('run_id'):
            protected.add(path.parent / 'runs' / report['run_id'])
        if report.get('oci_archive'):
            protected.add((path.parent / report['oci_archive']).parent)
        for platform in report.get('platform_results', {}).values():
            if platform.get('report'):
                protected.add((path.parent / platform['report']).parent)
    for path, report in records:
        run = path.parent
        if run.parent.name not in ('runs', 'rebuilds') or run in protected or contained(run, trees):
            continue
        try:
            started = dt.datetime.strptime(run.name, '%Y%m%dT%H%M%S.%fZ').replace(tzinfo=dt.timezone.utc)
        except ValueError:
            continue
        if started >= cutoff or not tree_is_old(run, cutoff):
            continue
        if not remove_all and report.get('status') in ('running', None):
            continue
        if remove_all:
            trees.add(run)
        else:
            files.update(p for p in run.rglob('*') if p.is_file() and p.suffix != '.json')
    if remove_all and remove_downloads:
        retained_downloads = recent_downloads
        for path, report in current:
            if not contained(path, trees) and report.get('status') == 'passed':
                for artifact in report.get('artifacts', {}).values():
                    url = artifact.get('url', '')
                    if url.startswith('downloads/docker/'):
                        retained_downloads.add((tool.STATIC_ROOT / url[len('downloads/docker/'):]).parent)
        for directory in tool.STATIC_ROOT.glob('*/*'):
            if directory.is_dir() and directory not in retained_downloads and tree_is_old(directory, cutoff):
                trees.add(directory)
    # Paths under a selected parent need no separate deletion.
    trees = {p for p in trees if not contained(p, trees - {p})}
    return sorted(trees), sorted(p for p in files if not contained(p, trees))


def metadata_plan(tool, trees):
    """Only Docker entries are removed; package metadata remains authoritative."""
    removed_images = set()
    _, current = cache_records(tool)
    for path, report in current:
        if contained(path, trees) and report.get('image'):
            removed_images.add(report['image'])
    changes = []
    for path in (tool.REPOSITORY_ROOT / 'tools/generated/openriak-kv/data/versions').glob('*.json'):
        data = read_report(path)
        entries = data.get('dockerImages', [])
        def removing(entry):
            url = entry.get('dockerfile', {}).get('url', '')
            published = tool.STATIC_ROOT / url[len('downloads/docker/'):] if url.startswith('downloads/docker/') else None
            return entry.get('image') in removed_images or (published is not None and contained(published, trees))
        kept = [entry for entry in entries if not removing(entry)]
        if kept != entries:
            data['dockerImages'] = kept
            changes.append((path, data, len(entries) - len(kept)))
    return changes


def check_write_access(tool, trees, files, changes):
    """Check directory permissions before any stop, prune, or deletion action."""
    directories = {path.parent for path in files}
    directories.update(path.parent for path, _, _ in changes)
    for tree in trees:
        directories.update([tree.parent, tree])
        directories.update(path for path in tree.rglob('*') if path.is_dir())
    for directory in sorted(directories):
        if not os.access(directory, os.W_OK | os.X_OK):
            owner = directory.stat()
            raise tool.DockerToolError(
                f'Cleanup cannot write to directory: {directory.absolute()} '
                f'(owner UID {owner.st_uid}, GID {owner.st_gid}). '
                'Restore ownership of cache files created by earlier sudo runs, then retry.'
            )


def remove_tree(path):
    def onerror(function, failed_path, exception_info):
        error = exception_info[1]
        if isinstance(error, OSError):
            # rmtree uses dir_fd internally, so error.filename can be only
            # "report.json". The callback receives the full failing path.
            raise OSError(error.errno, error.strerror, str(Path(failed_path).absolute())) from error
        raise error
    shutil.rmtree(path, onerror=onerror)


def process_table(proc=Path('/proc')):
    boot = int(next(line.split()[1] for line in (proc / 'stat').read_text().splitlines() if line.startswith('btime ')))
    ticks = os.sysconf('SC_CLK_TCK')
    processes = {}
    for directory in proc.iterdir():
        if not directory.name.isdigit():
            continue
        try:
            fields = (directory / 'stat').read_text().rsplit(')', 1)[1].split()
            if fields[0] == 'Z':
                continue
            args = (directory / 'cmdline').read_bytes().decode().rstrip('\0').split('\0')
            processes[int(directory.name)] = {
                'ppid': int(fields[1]), 'token': fields[19], 'args': args,
                'started': dt.datetime.fromtimestamp(boot + int(fields[19]) / ticks, dt.timezone.utc),
            }
        except (FileNotFoundError, ProcessLookupError, PermissionError):
            continue
    return processes


def generator_workers(tool, processes, proc=Path('/proc')):
    script = tool.REPOSITORY_ROOT / 'tools/openriak-docker/openriak_docker.py'
    workers = {}
    for pid, info in processes.items():
        if pid == os.getpid():
            continue
        for index, argument in enumerate(info['args'][:-1]):
            command = info['args'][index + 1]
            subcommand = info['args'][index + 2] if len(info['args']) > index + 2 else ''
            mutating = command in ('refresh', 'generate', 'sync-static', 'push', 'base') or (command == 'distribute' and subcommand in ('run', 'worker', 'collect'))
            if Path(argument).name != script.name or not mutating:
                continue
            candidate = Path(argument)
            if not candidate.is_absolute():
                candidate = (proc / str(pid) / 'cwd').resolve(strict=True) / candidate
            if candidate.resolve() == script.resolve():
                workers[pid] = info
    return workers


def stop_workers(tool, workers, timeout):
    if not workers:
        return
    processes = process_table()
    descendants = {pid for pid, info in workers.items() if processes.get(pid, {}).get('token') == info['token']}
    while True:
        expanded = descendants | {pid for pid, info in processes.items() if info['ppid'] in descendants}
        if expanded == descendants:
            break
        descendants = expanded
    # Record start tokens to avoid signalling a recycled PID.
    selected = {pid: processes[pid] for pid in descendants if pid in processes}
    for pid in [*workers, *(p for p in selected if p not in workers)]:
        current = process_table().get(pid)
        expected = workers.get(pid, selected.get(pid))
        if current and expected and current['token'] == expected['token']:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
    deadline = time.monotonic() + timeout
    while True:
        current = process_table()
        alive = [pid for pid, info in selected.items() if current.get(pid, {}).get('token') == info['token']]
        if not alive:
            return
        if time.monotonic() >= deadline:
            raise tool.DockerToolError(f'Workers did not stop within {timeout}s; leaving files and Docker cache intact: {alive}')
        time.sleep(0.5)


def docker_run(tool, *args, check=True, timeout=DEFAULT_TIMEOUT_SECONDS):
    try:
        result = subprocess.run([tool.docker_command(), *args], text=True, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        raise tool.DockerToolError(f'Docker cleanup command timed out after {timeout}s: {" ".join(args)}') from error
    if check and result.returncode:
        raise tool.DockerToolError(f'Docker cleanup command failed: {" ".join(args)}: {result.stderr.strip()}')
    return result


def inspect_all(tool, kind, timeout=DEFAULT_TIMEOUT_SECONDS):
    arguments = ('ps', '--all', '--quiet', '--no-trunc') if kind == 'container' else ('image', 'ls', '--quiet', '--no-trunc')
    ids = sorted(set(docker_run(tool, *arguments, timeout=timeout).stdout.split()))
    return json.loads(docker_run(tool, kind, 'inspect', *ids, timeout=timeout).stdout) if ids else []


def docker_plan(tool, cutoff, timeout=DEFAULT_TIMEOUT_SECONDS):
    records, _ = cache_records(tool)
    known, recent = set(), set()
    for path, report in records:
        tags = set(report.get('tags', [])) | set(report.get('build_tags', []))
        if report.get('image'):
            tags.add(report['image'])
        known.update(tags)
        when = report_time(report)
        if (when and when >= cutoff) or path.stat().st_mtime >= cutoff.timestamp():
            recent.update(tags)
    containers = inspect_all(tool, 'container', timeout=timeout)
    images = inspect_all(tool, 'image', timeout=timeout)
    removals = []
    for container in containers:
        labels = container.get('Config', {}).get('Labels') or {}
        config_files = labels.get('com.docker.compose.project.config_files', '').split(',')
        harness = any(re.fullmatch(r'/(?:[^/]+/)*openriak-docker-[^/]+/compose\.(single|cluster)\.test\.yaml', p) for p in config_files)
        if harness and timestamp(container['Created']) < cutoff:
            removals.append(container)
    retained_ids = {c['Image'] for c in containers if c not in removals}
    tags = []
    dangling = []
    for image in images:
        if timestamp(image['Created']) >= cutoff or image['Id'] in retained_ids:
            continue
        labels = image.get('Config', {}).get('Labels') or {}
        canonical = labels.get('org.openriak.image.tag')
        names = image.get('RepoTags') or []
        if canonical in recent or any(tag in recent for tag in names):
            continue
        tags.extend(tag for tag in names
                    if re.fullmatch(r'[a-z0-9._-]+/openriak-kv:[^\s]+', tag)
                    and (tag in known or (canonical in known and tag.startswith(canonical.split(':', 1)[0] + ':test-'))))
        if not names and canonical in known:
            dangling.append(image['Id'])
    networks = [json.loads(line) for line in docker_run(tool, 'network', 'ls', '--format', '{{json .}}', timeout=timeout).stdout.splitlines() if line.strip()]
    projects = {c.get('Config', {}).get('Labels', {}).get('com.docker.compose.project') for c in removals}
    network_ids = []
    for network in networks:
        inspected = json.loads(docker_run(tool, 'network', 'inspect', network['ID'], timeout=timeout).stdout)[0]
        if (inspected.get('Labels') or {}).get('com.docker.compose.project') in projects - {None}:
            if not set(inspected.get('Containers') or {}) - {c['Id'] for c in removals}:
                network_ids.append(inspected['Id'])
    builder = docker_run(tool, 'buildx', 'ls', '--format', '{{.Name}}', timeout=timeout).stdout.splitlines()
    return removals, sorted(set(tags + dangling)), network_ids, tool.MULTIARCH_BUILDER in builder


def prune_builder_cache(tool, cutoff, timeout=DEFAULT_TIMEOUT_SECONDS):
    with openriak_locks.lock(tool, f'builder:{tool.MULTIARCH_BUILDER}'):
        return _prune_builder_cache(tool, cutoff, timeout)


def _prune_builder_cache(tool, cutoff, timeout=DEFAULT_TIMEOUT_SECONDS):
    builder = tool.MULTIARCH_BUILDER
    inspection = docker_run(tool, 'buildx', 'inspect', builder, timeout=timeout).stdout
    states = re.findall(r'^Status:\s*(\S+)\s*$', inspection, re.MULTILINE)
    if not states or any(state not in ('running', 'stopped') for state in states):
        raise tool.DockerToolError(f'Cannot determine usable node states for builder {builder}; inspect it before cleanup')
    stopped = all(state == 'stopped' for state in states)
    if not stopped and 'stopped' in states:
        raise tool.DockerToolError(f'Builder {builder} has mixed running/stopped nodes; start it explicitly before cleanup')
    if stopped and not re.search(r'^Driver:\s*docker-container\s*$', inspection, re.MULTILINE):
        raise tool.DockerToolError(f'Cannot temporarily start stopped builder {builder}: expected the docker-container driver')
    try:
        if stopped:
            print(f'{tool.log_timestamp()} Starting stopped builder {builder} temporarily for cache cleanup', flush=True)
            docker_run(tool, 'buildx', 'inspect', builder, '--bootstrap', timeout=timeout)
        # Booting can take time; compute the relative filter immediately before
        # pruning so the original absolute cutoff remains the boundary.
        seconds = max(0, math.ceil((dt.datetime.now(dt.timezone.utc) - cutoff).total_seconds()))
        result = docker_run(tool, 'buildx', 'prune', '--builder', builder,
                           '--all', '--force', '--filter', f'until={seconds}s', timeout=timeout)
        print(result.stdout, end='')
    finally:
        if stopped:
            print(f'{tool.log_timestamp()} Restoring stopped state of builder {builder}', flush=True)
            docker_run(tool, 'buildx', 'stop', builder, timeout=timeout)


def main(options, tool):
    now = dt.datetime.now().astimezone()
    cutoff = options.before if options.before is not None else now
    print(f'Cleanup cutoff (--before): {cutoff.isoformat(timespec="microseconds")}', flush=True)
    if cutoff > now:
        raise tool.DockerToolError('--before cannot be in the future')
    if options.timeout <= 0:
        raise tool.DockerToolError('--timeout must be positive')
    from cache.retention import ARCHIVE_RETENTION_DAYS, archive_selection, merge_archive_selection
    clear_archives = getattr(options, 'clear_archives', False)
    archive_cutoff = min(cutoff, now - dt.timedelta(days=ARCHIVE_RETENTION_DAYS))
    print('Archive retention: clear all local archives (age and --before ignored)' if clear_archives else
          f'Archive retention: {ARCHIVE_RETENTION_DAYS} days; removing before {archive_cutoff.isoformat(timespec="microseconds")}', flush=True)
    remove_downloads = getattr(options, 'remove_downloads', False)
    remove_records = getattr(options, 'remove_records', False)
    if (remove_downloads and not options.remove_all) or (remove_records and not (options.remove_all and remove_downloads)):
        raise tool.DockerToolError('--remove-downloads requires --remove-all; --remove-records also requires --remove-downloads')
    def selection():
        trees, files = file_plan(tool, cutoff, options.remove_all, remove_downloads)
        removable, retained = archive_selection(tool.REPOSITORY_ROOT / '.work/openriak-docker',
                                                 archive_cutoff, clear=clear_archives)
        trees, files = merge_archive_selection(trees, files, removable, retained)
        if remove_records:
            work = tool.REPOSITORY_ROOT / '.work/openriak-docker'
            for tree in list(trees):
                if tree.is_relative_to(work):
                    relative = tree.relative_to(work)
                    for folder in ('records', 'artifacts'):
                        retained = tool.REPOSITORY_ROOT / folder / 'openriak-docker' / relative
                        if retained.exists():
                            trees.append(retained)
        return sorted(set(trees)), files
    trees, files = selection()
    changes = metadata_plan(tool, trees) if remove_downloads else []
    if options.delete:
        check_write_access(tool, trees, files, changes)
    workers, newer = {}, {}
    if options.remove_all:
        all_workers = generator_workers(tool, process_table())
        workers = {pid: info for pid, info in all_workers.items() if info['started'] < cutoff}
        newer = {pid: info for pid, info in all_workers.items() if info['started'] >= cutoff}
        for pid, info in workers.items():
            print(f'Worker to stop: PID {pid}, started {info["started"].isoformat()}')
        if newer:
            print(f'Keeping workers started since the cutoff: {sorted(newer)}')
            if options.delete:
                raise tool.DockerToolError('A newer generator worker is active; wait for it to finish before --remove-all --delete to avoid concurrent metadata/cache writes')
        # Verify Docker access before stopping any work.
        docker_run(tool, 'info', '--format', '{{.ID}}', timeout=options.timeout)
        if options.delete:
            stop_workers(tool, workers, options.timeout)
            if generator_workers(tool, process_table()):
                raise tool.DockerToolError('A generator worker is still active; no files or Docker cache removed')
    if options.remove_all and options.delete:
        # Graceful worker shutdown can update reports and create new logs.
        trees, files = selection()
        changes = metadata_plan(tool, trees) if remove_downloads else []
        check_write_access(tool, trees, files, changes)
    resources = docker_plan(tool, cutoff, timeout=options.timeout) if options.remove_all else ([], [], [], False)
    size = sum(p.stat().st_size for p in files)
    size += sum(f.stat().st_size for p in trees for f in p.rglob('*') if f.is_file())
    verb = 'WILL DELETE' if options.delete else 'WOULD DELETE'
    for path in trees:
        print(f'{verb} directory: {path.relative_to(tool.REPOSITORY_ROOT)}')
    for parent in sorted({p.parent for p in files}):
        print(f'{verb} old diagnostic files under: {parent.relative_to(tool.REPOSITORY_ROOT)}')
    for path, data, count in changes:
        print(f'{verb} {count} Docker metadata entries: {path.name}')
    containers, images, networks, builder = resources
    for container in containers:
        print(f'{verb} test container: {container["Name"]}')
    for image in images:
        print(f'{verb} image tag/ID: {image}')
    for network in networks:
        print(f'{verb} harness network: {network}')
    if builder:
        print(f'{verb} unused build cache last used before {cutoff.isoformat()} in {tool.MULTIARCH_BUILDER}')
    print(f'{len(trees)} directories and {len(files)} diagnostic files: {size / 1024**3:.2f} GiB (excluding Docker storage)')
    if not options.delete:
        print('Preview only; nothing stopped or deleted. Add --delete to apply.')
        return 0
    with openriak_locks.activity(tool, shared=False), (openriak_locks.lock(tool, f'builder:{tool.MULTIARCH_BUILDER}') if options.remove_all else contextlib.nullcontext()):
        fresh_trees, fresh_files = selection()
        if fresh_trees != trees or fresh_files != files:
            raise tool.DockerToolError('Cleanup selection changed while acquiring its lock; rerun cleanup')
        changes = metadata_plan(tool, trees) if remove_downloads else []
        if options.remove_all:
            containers, images, networks, builder = docker_plan(tool, cutoff, timeout=options.timeout)
        for container in containers:
            if container.get('State', {}).get('Running'):
                docker_run(tool, 'stop', '--time', str(options.timeout), container['Id'], timeout=options.timeout)
            docker_run(tool, 'container', 'rm', container['Id'], timeout=options.timeout)
        for network in networks:
            docker_run(tool, 'network', 'rm', network, timeout=options.timeout)
        # Never force image deletion: other containers/repositories may share layers.
        for image in images:
            docker_run(tool, 'image', 'rm', image, timeout=options.timeout)
        if builder:
            _prune_builder_cache(tool, cutoff, timeout=options.timeout)
        for path in files:
            path.unlink()
        for path in trees:
            remove_tree(path)
        for path, data, count in changes:
            temporary = path.with_name(f'{path.name}.{os.getpid()}.cleanup.tmp')
            temporary.write_text(json.dumps(data, indent=2) + '\n')
            temporary.replace(path)
        print('Cleanup complete.')
        return 0
