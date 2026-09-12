#!/usr/bin/env python3
"""Run unit tests, rejecting direct Docker, Skopeo, SSH and SCP calls."""
from pathlib import Path
import subprocess
import unittest


class NoDocker(subprocess.Popen):
    def __init__(self, args, *positional, **keywords):
        command = args[0] if isinstance(args, (list, tuple)) else args.split()[0]
        if Path(str(command)).name in ("docker", "docker.exe", "skopeo", "ssh", "scp"):
            raise AssertionError(f"Unit tests must not contact Docker, registries, or SSH nodes: {args}")
        super().__init__(args, *positional, **keywords)


if __name__ == "__main__":
    subprocess.Popen = NoDocker
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).parent))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
