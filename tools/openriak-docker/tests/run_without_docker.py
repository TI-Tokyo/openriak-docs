#!/usr/bin/env python3
"""Compatibility test runner for the extracted runtime tool."""
import os
from pathlib import Path
import sys
root = Path(os.environ.get('OPENRIAK_DOCKER_ROOT', str(Path(__file__).resolve().parents[4] / 'openriak-docker')))
python = root / '.venv/bin/python3'
if not python.exists():
    raise SystemExit('Run python3 scripts/setup.py in the openriak-docker checkout first')
os.execv(str(python), [str(python), str(root / 'tests/run_without_docker.py'), *sys.argv[1:]])
