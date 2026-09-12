"""Age-based retention for local archives, independent of durable approvals."""
import datetime as dt
import json
from pathlib import Path

ARCHIVE_RETENTION_DAYS = 90


def is_archive(relative):
    """Only generator-owned diagnostics and archive files, never approved sources."""
    return (bool({'pushes', 'scout-output', 'logs', 'migration-prototypes'}.intersection(relative.parts))
            or (bool({'runs', 'rebuilds'}.intersection(relative.parts)) and relative.suffix != '.json')
            or '.oci.tar' in relative.name
            or relative.suffix == '.log'
            or relative.name == 'cve-report.json'
            or relative.name.endswith(('scout.json', 'sarif.json', 'sbom.json'))
            or ('distributed' in relative.parts and relative.name.endswith('.bundle.tar.gz')))


def archive_selection(work, cutoff, *, clear=False):
    """Return removable and retained files; exact cutoff timestamps are retained.

    Use the newest file or ancestor-run timestamp, so old build files belonging
    to a recently completed run remain available. No symlinks are followed.
    Ordinary retention preserves running records. Explicit clearing is performed
    under cleanup's exclusive activity lock, which excludes active generators.
    """
    work = Path(work)
    if not work.exists() or work.is_symlink():
        return set(), set()
    metadata = {}

    def run_state(directory):
        if directory in metadata:
            return metadata[directory]
        newest, running = 0, False
        if directory != work:
            newest, running = run_state(directory.parent)
        own_timestamp = None
        for filename in ('report.json', 'worker.json', 'cve-report.json'):
            report = directory / filename
            if not report.is_file() or report.is_symlink():
                continue
            own_timestamp = max(own_timestamp or 0, report.stat().st_mtime)
            try:
                data = json.loads(report.read_text())
                running |= data.get('status') == 'running'
                for key in ('started_at', 'finished_at', 'tested_at', 'testedAt'):
                    if data.get(key):
                        value = dt.datetime.fromisoformat(data[key].replace('Z', '+00:00'))
                        if value.tzinfo is None:
                            raise ValueError('Unqualified report timestamp')
                        own_timestamp = max(own_timestamp, value.timestamp())
            except (ValueError, OSError, AttributeError, TypeError):
                # Unreadable/incomplete evidence is not automatically expired.
                running = True
        if own_timestamp is not None:
            newest = own_timestamp
        metadata[directory] = newest, running
        return newest, running

    removable, retained = set(), set()
    for path in work.rglob('*'):
        if not path.is_file() or path.is_symlink() or not is_archive(path.relative_to(work)):
            continue
        if any(parent.is_symlink() for parent in path.parents if parent != work and work in parent.parents):
            continue
        newest, running = run_state(path.parent)
        old = max(path.stat().st_mtime, newest) < cutoff.timestamp()
        (removable if clear or (old and not running) else retained).add(path)
    return removable, retained


def merge_archive_selection(trees, files, removable, retained):
    """A parent-directory deletion must not bypass the archive retention rule."""
    trees = [tree for tree in trees if not any(tree in path.parents for path in retained)]
    files = (set(files) - retained) | removable
    files = {path for path in files if not any(tree in path.parents for tree in trees)}
    return sorted(set(trees)), sorted(files)
