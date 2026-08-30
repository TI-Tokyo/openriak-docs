"""Public source-resolution API with collision-safe disposable checkout names."""
from pathlib import Path

from ._source_impl import *
from ._source_impl import SourceResolver as _SourceResolver


class SourceResolver(_SourceResolver):
    def _checkout(self, repository: str, ref: str, name: str):
        candidate = name
        counter = 2
        while (self.workdir / candidate).exists():
            candidate = f"{name}-{counter}"
            counter += 1
        return super()._checkout(repository, ref, candidate)

