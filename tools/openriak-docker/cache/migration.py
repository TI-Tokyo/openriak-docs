"""Verified, repeatable relocation of the historical mixed cache layout."""
from pathlib import Path
import json
import os
import shutil

from cache import storage


def moves(repository):
    work = repository / '.work/openriak-docker'
    explicit = {'openriak-docker': 'legacy', 'openriak-docker-multiarch': 'images', 'openriak-docker-bases': 'bases'}
    for source in sorted((repository / 'tools/cache').glob('openriak-docker*')):
        if source.is_dir():
            yield source, work / explicit.get(source.name, 'experiments/' + source.name)
    reviews = repository / 'tools/openriak-docker/reports'
    if reviews.exists():
        yield reviews, repository / 'records/openriak-docker/reviews'
    for source in sorted(repository.glob('openriak-docker-*.json')):
        if source.name.endswith('.remote.json'):
            yield source, work / 'distributed/deployments' / source.name
        else:
            yield source, repository / 'records/openriak-docker/distributed/plans' / source.name
    for source in sorted(repository.glob('openriak-docker-*.results')):
        if source.is_dir():
            yield source, work / 'distributed/results' / source.name
    for source in sorted(repository.glob('openriak-docker-*.bundle.tar.gz')):
        yield source, work / 'distributed/bundles' / source.name


def relocate(source, destination, manifest):
    """Same-filesystem rename preserves all bytes, including large OCI archives."""
    if destination.exists():
        if source.is_file():
            if source.read_bytes() != destination.read_bytes():
                raise ValueError(f'Migration destination differs: {destination}')
            raise ValueError(f'Both migration paths exist; inspect before continuing: {source}, {destination}')
        for child in sorted(source.iterdir()):
            relocate(child, destination / child.name, manifest)
        source.rmdir()
        return
    files = list(source.rglob('*')) if source.is_dir() else [source]
    entries = []
    for path in files:
        if not path.is_file():
            continue
        relative = path.relative_to(source) if source.is_dir() else Path('.')
        stat = path.stat()
        entries.append((relative, stat.st_dev, stat.st_ino, stat.st_size))
    destination.parent.mkdir(parents=True, exist_ok=True)
    source.rename(destination)
    for relative, device, inode, size in entries:
        target = destination / relative if relative != Path('.') else destination
        stat = target.stat()
        if (stat.st_dev, stat.st_ino, stat.st_size) != (device, inode, size):
            raise ValueError(f'Relocation identity check failed: {target}')
    manifest.append({'from': str(source.relative_to(storage.REPOSITORY)),
                     'to': str(destination.relative_to(storage.REPOSITORY)),
                     'files': len(entries), 'bytes': sum(e[3] for e in entries),
                     'verification': 'same device, inode and length after rename'})


def main(options, tool):
    selected = list(moves(tool.REPOSITORY_ROOT))
    for source, destination in selected:
        print(f'{"MOVE" if options.apply else "WOULD MOVE"} {source.relative_to(tool.REPOSITORY_ROOT)} -> {destination.relative_to(tool.REPOSITORY_ROOT)}')
    if not options.apply:
        print('Preview only. Add --apply to migrate; no builds, tests or uploads are started.')
        return 0
    from commands.cleanup import generator_workers, process_table
    if generator_workers(tool, process_table()):
        raise tool.DockerToolError('Stop active generator workers before relocating their files')
    manifest = []
    try:
        for source, destination in selected:
            relocate(source, destination, manifest)
        # Deployment state is local and mutable. Keep its original bytes, then
        # update controller paths; embedded frozen plans remain unchanged.
        replacements = [(str(a), str(b)) for a, b in selected]
        for path in (storage.WORK / 'distributed/deployments').glob('*.remote.json') if replacements else ():
            original = path.read_bytes()
            backup = path.with_suffix('.before-migration.json')
            if not backup.exists():
                storage.atomic(backup, original)
            def rewrite(value):
                if isinstance(value, str):
                    for old, new in replacements:
                        if value == old or value.startswith(old + '/'):
                            return new + value[len(old):]
                if isinstance(value, list):
                    return [rewrite(x) for x in value]
                if isinstance(value, dict):
                    return {k: v if k == 'plan' else rewrite(v) for k, v in value.items()}
                return value
            storage.atomic(path, storage.encoded(rewrite(json.loads(original))))
        storage.capture_tree(include_running=True)
        # Imported worker reports are retained independently of their OCI files.
        for path in (storage.WORK / 'distributed/results').rglob('*.json'):
            if path.name in ('report.json', 'worker.json'):
                storage.put_record(storage.RECORDS, path.relative_to(storage.WORK), path.read_bytes())
    finally:
        receipt = {'schema_version': 1, 'created_at': tool.isoformat(), 'moves': manifest,
                   'raw_payload_retention': 'Local originals preserved; managed archives follow the 90-day cleanup policy'}
        storage.atomic(storage.RECORDS / 'migrations' / (tool.run_id() + '.json'), storage.encoded(receipt))
    print('Migration complete. Durable records and approved files retained; local archives and diagnostics preserved.')
    return 0
