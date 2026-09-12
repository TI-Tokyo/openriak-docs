"""Explicit application services, independent of the executable entry point.

Providers are lazy to avoid import cycles. Commands/workflows receive this object;
unit tests can override individual services without replacing the launcher.
"""
from functools import partial, update_wrapper
from importlib import import_module
from pathlib import Path
import json


class Services:
    def __init__(self):
        self.__file__ = str(Path(__file__).resolve().parents[1] / 'openriak_docker.py')
        self.TOOL_ROOT = Path(self.__file__).parent
        self._providers = json.loads((Path(__file__).with_name('services.json')).read_text())

    def __getattr__(self, name):
        try:
            module, attribute, bind = self._providers[name]
        except KeyError:
            raise AttributeError(name) from None
        provider = import_module(module)
        value = getattr(provider, attribute) if attribute else provider
        return update_wrapper(partial(value, self), value) if bind else value


context = Services()
