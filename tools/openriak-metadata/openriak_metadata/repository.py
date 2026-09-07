"""Install fully staged package metadata without changing other repository files."""
import os
from pathlib import Path
import shutil
import tempfile


FILENAMES = ('supported-os.json', 'downloads.json')


def install_packages(stage: Path, repository: Path, product: str, versions: list[str]) -> int:
    root = repository / 'content' / f'openriak-{product}' / 'metadata'
    prepared = Path(tempfile.mkdtemp(prefix='.package-metadata-update-', dir=root))
    pending, changed = [], []
    retain_recovery = False
    try:
        # Prepare all replacements and backups on the destination filesystem.
        # Network work and validation have already completed for every version.
        for version in versions:
            directory = root / version
            if directory.is_symlink():
                raise ValueError(f'Refusing to replace metadata through a symlink: {directory}')
            directory.mkdir(exist_ok=True)
            if not os.access(directory, os.W_OK | os.X_OK):
                raise PermissionError(f'Cannot update metadata directory: {directory}')
            for filename in FILENAMES:
                source = stage / product / version / filename
                target = directory / filename
                if target.is_symlink():
                    raise ValueError(f'Refusing to replace a metadata symlink: {target}')
                if target.is_file() and target.read_bytes() == source.read_bytes():
                    continue
                replacement = prepared / f'{version}-{filename}.new'
                backup = prepared / f'{version}-{filename}.previous' if target.exists() else None
                shutil.copy2(source, replacement)
                if backup is not None:
                    shutil.copy2(target, backup)
                pending.append((target, replacement, backup))
        try:
            for target, replacement, backup in pending:
                changed.append((target, backup))
                os.replace(replacement, target)
        except BaseException as error:
            try:
                for target, backup in reversed(changed):
                    if backup is None:
                        target.unlink(missing_ok=True)
                    else:
                        os.replace(backup, target)
            except OSError as recovery_error:
                retain_recovery = True
                raise OSError(f'Installation failed ({error}); rollback failed ({recovery_error}); recovery files retained in {prepared}') from recovery_error
            raise
        return len(changed)
    finally:
        if not retain_recovery:
            shutil.rmtree(prepared)
