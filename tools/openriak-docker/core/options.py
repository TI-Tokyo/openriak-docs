from __future__ import annotations
import argparse
import dataclasses
import pathlib
import re
import secrets
import urllib.parse
from typing import Any
from core.context import context


def duration_seconds(value: str) -> int:
    match = re.fullmatch('([0-9]+)([smh]?)', value)
    if not match:
        raise argparse.ArgumentTypeError('Use whole seconds or a duration such as 30s, 2m, or 1h')
    return int(match[1]) * {'': 1, 's': 1, 'm': 60, 'h': 3600}[match[2]]


def generate_distributed_cookie() -> str:
    """Return a Docker-target-specific, shell-safe Erlang distribution cookie."""
    return f'openriak-{secrets.token_hex(16)}'


def semver_key(version: str) -> tuple[int, ...]:
    match = re.fullmatch('(\\d+)\\.(\\d+)\\.(\\d+)', version)
    if not match:
        raise context.DockerToolError(f'Invalid OpenRiak KV version directory: {version}')
    return tuple((int(item) for item in match.groups()))


def natural_key(value: Any) -> tuple[tuple[int, Any], ...]:
    return tuple(((0, int(part)) if part.isdigit() else (1, part.lower()) for part in re.split('([0-9]+)', str(value or ''))))


def extra_namespace(value: str) -> str:
    if not re.fullmatch('[a-z0-9]+(?:[._-][a-z0-9]+)*', value):
        raise argparse.ArgumentTypeError('Use a lowercase namespace such as tiotjp, without a registry URL or slash')
    return value


def namespaced_tags(tags: list[str], namespaces: list[str]) -> list[str]:
    if not tags or any((not re.fullmatch('[a-z0-9]+(?:[._-][a-z0-9]+)*/openriak-kv:[a-zA-Z0-9_][a-zA-Z0-9_.-]{0,127}', tag) for tag in tags)):
        raise context.DockerToolError('Image tags must use <namespace>/openriak-kv:<tag>')
    result = list(tags)
    for namespace in namespaces:
        context.extra_namespace(namespace)
        result.extend((f"{namespace}/openriak-kv:{tag.split(':', 1)[1]}" for tag in tags))
    return list(dict.fromkeys(result))


def label_text(value: str) -> str:
    if not value.strip() or any((ord(char) < 32 or ord(char) == 127 for char in value)):
        raise argparse.ArgumentTypeError('Label values must be nonempty, single-line text')
    return value


def label_url(value: str) -> str:
    context.label_text(value)
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in {'http', 'https'} or not parsed.netloc or any((char.isspace() for char in value)):
        raise argparse.ArgumentTypeError('Use an absolute HTTP or HTTPS URL')
    return value


def standalone_output(value: str) -> pathlib.Path:
    root = pathlib.Path(value).expanduser().resolve()
    protected = (context.CACHE_ROOT, context.MULTIARCH_CACHE_ROOT, context.STATIC_ROOT, context.METADATA_ROOT, context.REPOSITORY_ROOT / 'content', context.REPOSITORY_ROOT / 'tools/generated', context.REPOSITORY_ROOT / '.git', context.REPOSITORY_ROOT / 'records', context.REPOSITORY_ROOT / 'artifacts')
    for path in protected:
        path = path.resolve()
        if root.is_relative_to(path) or path.is_relative_to(root):
            raise context.DockerToolError(f'Standalone output must be separate from docs, generated metadata, and test caches: {root}')
    return root


def identity_from_options(options: argparse.Namespace) -> context.ImageIdentity:
    defaults = context.ImageIdentity()
    return context.ImageIdentity(**{field.name: getattr(options, field.name, None) or getattr(defaults, field.name) for field in dataclasses.fields(context.ImageIdentity)})
