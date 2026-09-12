"""Lossless, compressed Scout payloads beside small per-image reports.

Run `python3 tools/openriak-docker/publishing/cve_storage.py compact PATH...`
to convert completed historical reports without Docker or network access.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix='.' + path.name + '-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, path.stat().st_mode & 0o777 if path.exists() else 0o644)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_output(report_path: Path, reference: dict):
    """Verify a local payload before returning its exact text or parsed JSON."""
    digest = reference.get('sha256', '')
    name = reference.get('path', '')
    if (not re.fullmatch(r'[0-9a-f]{64}', digest)
            or name != f'scout-output/{digest}.gz'
            or reference.get('compression') != 'gzip'
            or reference.get('format') not in ('text', 'json')):
        raise ValueError('Invalid Scout payload reference')
    path = report_path.parent / name
    if not path.resolve().is_relative_to(report_path.parent.resolve()):
        raise ValueError('Scout payload escapes the report directory')
    raw = gzip.decompress(path.read_bytes())
    if len(raw) != reference.get('size_bytes') or hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError(f'Scout payload integrity check failed: {path}')
    text = raw.decode('utf-8')
    return json.loads(text) if reference['format'] == 'json' else text


def store_output(report_path: Path, text: str, format: str) -> dict:
    raw = text.encode('utf-8')
    digest = hashlib.sha256(raw).hexdigest()
    reference = {'path': f'scout-output/{digest}.gz', 'sha256': digest,
                 'size_bytes': len(raw), 'compression': 'gzip', 'format': format}
    path = report_path.parent / reference['path']
    if not path.resolve().is_relative_to(report_path.parent.resolve()):
        raise ValueError('Scout payload escapes the report directory')
    if path.exists():
        if read_output(report_path, {**reference, 'format': 'text'}) != text:
            raise ValueError(f'Conflicting Scout payload: {path}')
    else:
        atomic_write(path, gzip.compress(raw, mtime=0))
    return reference


def compact_report(report: dict, report_path: Path) -> None:
    """Replace large inline fields with references, preserving every attempt.

    Successful parsed data and its raw stdout share one gzip file. If a legacy
    report's parsed data differs from stdout, retain both instead of guessing.
    All sidecars are durable before the caller replaces the report atomically.
    """
    for scan in report.get('scans', {}).values():
        for mode in ('sarif', 'sbom', 'details'):
            output = scan.get(mode, {})
            if 'data' in output:
                data = output['data']
                format = 'text' if mode == 'details' else 'json'
                text = None
                for attempt in reversed(output.get('attempts', [])):
                    candidate = attempt.get('stdout')
                    if candidate is None and attempt.get('stdout_file'):
                        candidate = read_output(report_path, attempt['stdout_file'])
                    if not isinstance(candidate, str):
                        continue
                    try:
                        parsed = candidate if format == 'text' else json.loads(candidate)
                    except ValueError:
                        continue
                    if parsed == data:
                        text = candidate
                        break
                if text is None:
                    text = data if format == 'text' else json.dumps(data, ensure_ascii=False, separators=(',', ':'))
                output['data_file'] = store_output(report_path, text, format)
                del output['data']
            for attempt in output.get('attempts', []):
                # Keep small stderr, timings, commands and errors in the index.
                if attempt.get('stdout'):
                    attempt['stdout_file'] = store_output(report_path, attempt['stdout'], 'text')
                    del attempt['stdout']
    report['schema_version'] = 2


def write_report(path: Path, report: dict) -> None:
    compact_report(report, path)
    atomic_write(path, (json.dumps(report, indent=2, sort_keys=True) + '\n').encode())
    from cache.storage import capture_file
    capture_file(path)


def hydrate_report(path: Path, report: dict | None = None) -> dict:
    """Read either storage format, restoring full fields for audit consumers."""
    result = copy.deepcopy(report) if report is not None else json.loads(path.read_text())
    for scan in result.get('scans', {}).values():
        for mode in ('sarif', 'sbom', 'details'):
            output = scan.get(mode, {})
            if 'data_file' in output:
                output['data'] = read_output(path, output.pop('data_file'))
            for attempt in output.get('attempts', []):
                if 'stdout_file' in attempt:
                    attempt['stdout'] = read_output(path, attempt.pop('stdout_file'))
    return result


def migrate_report(path: Path) -> bool:
    original_bytes = path.read_bytes()
    original = json.loads(original_bytes)
    if original.get('schema_version') == 2:
        return False
    if original.get('status') not in ('complete', 'failed', 'interrupted'):
        raise ValueError(f'Report may still be in use; refusing to compact: {path}')
    converted = copy.deepcopy(original)
    compact_report(converted, path)
    # Verify semantic round-trip, including every failed attempt, before replace.
    restored = hydrate_report(path, converted)
    restored['schema_version'] = original.get('schema_version')
    if restored != original:
        raise ValueError(f'Lossless Scout report verification failed: {path}')
    converted['storage_migration'] = {
        'original_schema_version': original.get('schema_version'),
        'original_report_sha256': hashlib.sha256(original_bytes).hexdigest(),
        'original_size_bytes': len(original_bytes),
    }
    if path.read_bytes() != original_bytes:
        raise ValueError(f'Report changed during compaction; refusing to replace: {path}')
    atomic_write(path, (json.dumps(converted, indent=2, sort_keys=True) + '\n').encode())
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['compact'])
    parser.add_argument('paths', nargs='+', type=Path, help='Report files or directories to search recursively')
    parser.add_argument('--whatif', action='store_true', help='List reports without changing files')
    options = parser.parse_args()
    paths = set()
    for path in options.paths:
        if not path.exists():
            parser.error(f'Path does not exist: {path}')
        paths.update(path.rglob('cve-report.json') if path.is_dir() else [path])
    for path in sorted(paths):
        if options.whatif:
            print(f'CHECK {path} ({path.stat().st_size:,} bytes)')
        else:
            before = path.stat().st_size
            changed = migrate_report(path)
            print(f'{"COMPACTED" if changed else "UNCHANGED"} {path}: {before:,} -> {path.stat().st_size:,} bytes', flush=True)


if __name__ == '__main__':
    main()
