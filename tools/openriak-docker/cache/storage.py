"""Durable evidence and approved assets, separate from disposable execution files.

Records are immutable, content-addressed JSON snapshots. Each directory has a
small current.json index mapping logical filenames to snapshots. The execution
layout is materialised from these records; deleting it does not delete evidence.
Standalone output directories are deliberately outside this store.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile

REPOSITORY = Path(__file__).resolve().parents[3]
WORK = REPOSITORY / '.work/openriak-docker'
RECORDS = REPOSITORY / 'records/openriak-docker'
ARTIFACTS = REPOSITORY / 'artifacts/openriak-docker'
KINDS = ('images', 'legacy', 'bases', 'experiments')
DOWNLOAD_FILES = {'Dockerfile', 'compose.single.yaml', 'compose.cluster.yaml', 'example.env', '.env.example', '.dockerignore'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def atomic(path, data):
    from publishing.cve_storage import atomic_write
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_bytes() != data:
        atomic_write(path, data)


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def put_record(root, relative, data, *, source_sha256=None):
    """Retain exact report bytes; only the small current pointer is mutable."""
    relative = Path(relative)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('Record path must remain within its store')
    parent = root / relative.parent
    checksum = digest(data)
    snapshot = Path('history') / (checksum + '.json')
    if (parent / snapshot).exists() and (parent / snapshot).read_bytes() != data:
        raise ValueError(f'Immutable record snapshot changed: {parent / snapshot}')
    atomic(parent / snapshot, data)
    pointer = parent / 'current.json'
    index = json.loads(pointer.read_text()) if pointer.exists() else {'schema_version': 1, 'files': {}}
    index['files'][relative.name] = {'snapshot': str(snapshot), 'sha256': checksum,
                                    'source_sha256': source_sha256 or checksum}
    atomic(pointer, encoded(index))
    return {'snapshot': str((relative.parent / snapshot)), 'sha256': checksum}


def record_entries(root):
    for pointer in sorted(root.rglob('current.json')):
        index = json.loads(pointer.read_text())
        for name, ref in index.get('files', {}).items():
            if (Path(name).name != name or not re.fullmatch(r'[0-9a-f]{64}', ref.get('sha256', ''))
                    or ref['snapshot'] != 'history/' + ref['sha256'] + '.json'):
                raise ValueError(f'Invalid record pointer: {pointer}')
            source = pointer.parent / ref['snapshot']
            if not source.resolve().is_relative_to(root.resolve()):
                raise ValueError(f'Record escapes its store: {source}')
            data = source.read_bytes()
            if digest(data) != ref['sha256']:
                raise ValueError(f'Record integrity check failed: {source}')
            yield pointer.parent.relative_to(root) / name, data


def compact_security(path, value):
    """Self-contained Scout findings for Git; full original payloads stay in work.

    Preserve SARIF rules, scores, affected/fixed versions and package URLs,
    approval, registry digests, scan status and command provenance. Large raw
    stdout/SBOM payloads remain referenced by their original hashes and paths.
    """
    from publishing.cve_storage import read_output
    result = json.loads(json.dumps(value))
    for scan in result.get('scans', {}).values():
        sarif = scan.get('sarif', {})
        if sarif.get('data_file'):
            sarif['data'] = read_output(path, sarif['data_file'])
            sarif['raw_data_file'] = sarif.pop('data_file')
        data = sarif.get('data')
        runs = data.get('runs', []) if isinstance(data, dict) else []
        for run in runs if isinstance(runs, list) else []:
            if not isinstance(run, dict) or (run.get('results') is not None and not isinstance(run['results'], list)):
                continue  # Retain malformed evidence as malformed, never clean.
            # Scout repeats a result for every filesystem occurrence. The raw
            # payload retains every location/message; the durable CVE evidence
            # needs one entry per rule and retains the original occurrence count.
            findings = {}
            for finding in run.get('results') or []:
                entry = {k: finding[k] for k in ('ruleId', 'ruleIndex', 'kind', 'level') if k in finding}
                key = json.dumps(entry, sort_keys=True)
                if key not in findings:
                    findings[key] = dict(entry, occurrences=0)
                findings[key]['occurrences'] += finding.get('occurrences', 1)
            run['results'] = list(findings.values())
        sarif['normalization'] = 'Unique rule results with occurrence counts; original locations and messages retained in raw payload'
    from cache.retention import ARCHIVE_RETENTION_DAYS
    result['raw_evidence'] = {'retention': 'local-age-based', 'retention_days': ARCHIVE_RETENTION_DAYS,
                              'work_report': str(path.relative_to(WORK))}
    return result


def capture_file(path, *, include_running=False):
    path = Path(path).absolute()
    try:
        relative = path.relative_to(WORK)
    except ValueError:
        return  # An explicitly requested standalone output stays standalone.
    if not relative.parts or relative.parts[0] not in KINDS or path.suffix != '.json':
        return
    if 'scout-output' in relative.parts:
        return
    data = path.read_bytes()
    value = json.loads(data)
    if isinstance(value, dict) and value.get('status') == 'running' and not include_running:
        return
    source_checksum = digest(data)
    pointer = RECORDS / relative.parent / 'current.json'
    previous = json.loads(pointer.read_text()).get('files', {}).get(path.name, {}) if pointer.exists() else {}
    if previous.get('source_sha256') != source_checksum:
        if path.name == 'cve-report.json':
            data = encoded(compact_security(path, value))
        put_record(RECORDS, relative, data, source_sha256=source_checksum)
    # Only approved source files become durable download artifacts. Keep exact
    # historical copies as well so approvals remain independently reviewable.
    if path.name == 'report.json' and isinstance(value, dict) and value.get('status') == 'passed':
        for filename in DOWNLOAD_FILES:
            source = path.parent / filename
            if source.is_file():
                data = source.read_bytes()
                expected = value.get('dockerfile_sha256') if filename == 'Dockerfile' else None
                expected = next((a.get('sha256') for a in value.get('artifacts', {}).values()
                                 if a.get('filename') == filename), expected)
                if expected and digest(data) == expected:
                    atomic(ARTIFACTS / relative.parent / filename, data)


def capture_tree(root=None, *, include_running=False):
    root = root or WORK
    for kind in KINDS:
        for path in sorted((root / kind).rglob('*.json')):
            capture_file(path, include_running=include_running)


def capture_distributed_results(root):
    root = Path(root).resolve()
    if not root.is_relative_to(WORK / 'distributed/results'):
        return
    for path in root.rglob('*.json'):
        if path.name in ('report.json', 'worker.json'):
            put_record(RECORDS, path.relative_to(WORK), path.read_bytes())


def restore(destination=None):
    """Recreate only missing execution files; never overwrite a live worker."""
    destination = destination or WORK
    for relative, data in record_entries(RECORDS):
        if relative.parts[0] not in KINDS:
            continue
        target = destination / relative
        if not target.exists():
            atomic(target, data)
    if ARTIFACTS.exists():
        for source in ARTIFACTS.rglob('*'):
            if source.is_file() and source.name in DOWNLOAD_FILES:
                target = destination / source.relative_to(ARTIFACTS)
                if not target.exists():
                    atomic(target, source.read_bytes())


@contextlib.contextmanager
def session(tool, options):
    """Read-only commands use a temporary view, without changing repo files."""
    if (getattr(options, 'output', None) or getattr(options, 'cache_root', None)
            or tool.MULTIARCH_CACHE_ROOT != WORK / 'images'):
        yield
        return
    readonly = getattr(options, 'whatif', False) or options.command in ('matrix', 'doctor', 'status', 'failures', 'cve-diff')
    if options.command in ('matrix', 'doctor', 'cve-diff', 'cleanup', 'distribute', 'generate', 'migrate-storage') or getattr(options, 'nohup', False):
        yield
        return
    if not readonly:
        restore()
        try:
            yield
        finally:
            capture_tree()
        return
    with tempfile.TemporaryDirectory(prefix='openriak-record-view-') as directory:
        view = Path(directory)
        restore(view)
        # Existing work includes newer incomplete reports and optional archives.
        # Hard links keep OCI containment checks valid without copying gigabytes.
        for kind in KINDS:
            for source in (WORK / kind).rglob('*'):
                if source.is_file() and not source.is_symlink():
                    target = view / source.relative_to(WORK)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if target.exists():
                        target.unlink()
                    try:
                        os.link(source, target)
                    except OSError:
                        if source.name.endswith('.oci.tar'):
                            continue  # Push will report the unavailable archive.
                        shutil.copy2(source, target)
        original = tool.CACHE_ROOT, tool.MULTIARCH_CACHE_ROOT
        tool.CACHE_ROOT, tool.MULTIARCH_CACHE_ROOT = view / 'legacy', view / 'images'
        tool._record_view_root = view
        base_cache = getattr(options, 'cache_root', None)
        if options.command == 'base':
            options.cache_root = view / 'bases'
        try:
            yield
        finally:
            tool.CACHE_ROOT, tool.MULTIARCH_CACHE_ROOT = original
            del tool._record_view_root
            if options.command == 'base':
                options.cache_root = base_cache
