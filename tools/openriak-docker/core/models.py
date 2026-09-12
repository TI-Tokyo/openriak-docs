from __future__ import annotations
import dataclasses
import pathlib
import re
from typing import Any
from core.context import context


class DockerToolError(RuntimeError):
    """An expected target, Docker, or test failure."""


@dataclasses.dataclass(frozen=True)
class ImageIdentity:
    vendor: str = 'OpenRiak'
    source: str = 'https://github.com/OpenRiak/openriak-docs'
    url: str = 'https://openriak.org'
    namespace: str = 'openriak'


@dataclasses.dataclass(frozen=True)
class LifecycleOptions:
    healthcheck_interval: int = 10
    healthcheck_timeout: int = 60
    healthcheck_start_period: int = 120
    healthcheck_retries: int = 3
    stop_grace_period: int = 120


@dataclasses.dataclass(frozen=True)
class Target:
    version: str
    operating_system: dict[str, Any]
    download_id: str
    package: dict[str, Any]
    grouped: bool = False
    identity: context.ImageIdentity = dataclasses.field(default_factory=context.ImageIdentity)
    output_root: pathlib.Path | None = None
    lifecycle_options: context.LifecycleOptions = dataclasses.field(default_factory=context.LifecycleOptions)

    @property
    def os_id(self) -> str:
        return str(self.operating_system['id'])

    @property
    def family(self) -> str:
        return str(self.operating_system['family'])

    @property
    def release(self) -> str:
        return str(self.operating_system['release'])

    @property
    def architecture(self) -> str:
        return str(self.package['architecture'])

    @property
    def otp(self) -> str:
        raw = self.package.get('otp')
        if raw is not None and str(raw):
            return str(raw)
        explicit = re.search('(?:^|[-_.])OTP([0-9]+(?:\\.[0-9]+)?)(?:[-_.]|$)', self.package['filename'], re.I)
        if explicit:
            return explicit.group(1)
        alpine = re.match(f'^riak-{re.escape(self.version)}\\.([0-9]+)-r[0-9]+\\.apk$', self.package['filename'], re.I)
        if alpine:
            return alpine.group(1)
        raise context.DockerToolError(f'Unable to infer OTP version for {self.version}/{self.os_id}/{self.download_id}')

    @property
    def platform(self) -> str:
        try:
            return context.ARCHITECTURE_PLATFORMS[self.architecture]
        except KeyError as error:
            raise context.DockerToolError(f'Unsupported Docker architecture: {self.architecture}') from error

    @property
    def image_tag(self) -> str:
        return '-'.join([self.version, self.family, self.release, f'otp{self.otp}'] + ([] if self.grouped else [self.architecture])).lower()

    @property
    def image(self) -> str:
        return f'{self.identity.namespace}/openriak-kv:{self.image_tag}'

    @property
    def node_name(self) -> str:
        return f'openriak-kv-{self.image_tag}-node'

    @property
    def cache_directory(self) -> pathlib.Path:
        if self.grouped:
            return self.group_directory / 'platforms' / self.platform.replace('/', '-')
        return (self.output_root or context.CACHE_ROOT) / self.version / self.os_id / self.download_id

    @property
    def group_directory(self) -> pathlib.Path:
        return (self.output_root or context.MULTIARCH_CACHE_ROOT) / self.version / self.image_tag

    @property
    def static_directory(self) -> pathlib.Path:
        return context.STATIC_ROOT / self.version / self.image_tag


def default_node_host(index: int) -> str:
    if index < 1 or index > 253:
        raise context.DockerToolError('OpenRiak node indexes must be between 1 and 253')
    return f'node-{index:02d}.cluster-a.openriak'
