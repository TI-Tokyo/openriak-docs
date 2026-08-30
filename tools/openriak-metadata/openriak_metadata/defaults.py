"""Public defaults API plus normalization of shell-escaped RPM values."""
from . import _defaults_impl as _implementation
from ._defaults_impl import *


_original_parse_rpm_vars = _implementation.parse_rpm_vars


def parse_rpm_vars(directory, root):
    values, sources = _original_parse_rpm_vars(directory, root)
    values = {key: value.rstrip("\\") if isinstance(value, str) else value for key, value in values.items()}
    return values, sources


_implementation.parse_rpm_vars = parse_rpm_vars

