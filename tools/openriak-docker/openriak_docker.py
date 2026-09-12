#!/usr/bin/env python3
"""Command-line entry point for OpenRiak KV Docker tooling."""
import signal
from cli import main

if __name__ == '__main__':
    def stop(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, stop)
    raise SystemExit(main())
