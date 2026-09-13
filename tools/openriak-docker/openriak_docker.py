#!/usr/bin/env python3
"""Compatibility launcher for the separate openriak-docker repository."""
import os
from pathlib import Path
import sys
root = Path(os.environ.get('OPENRIAK_DOCKER_ROOT', str(Path(__file__).resolve().parents[3] / 'openriak-docker')))
launcher = root / 'openriak-docker'
if not launcher.is_file():
    raise SystemExit('Clone openriak-docker beside openriak-docs or set OPENRIAK_DOCKER_ROOT')
os.execv(str(launcher), [str(launcher), *sys.argv[1:]])
