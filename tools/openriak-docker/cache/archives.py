"""Cache archives operations."""
from __future__ import annotations
import argparse
import base64
import contextlib
import dataclasses
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile
import time
from core.defaults import DEFAULT_TIMEOUT_SECONDS
from publishing.cve_storage import write_report


def sha256(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()


def archive_metadata(path, expected_platforms):
    """Read without extraction; verify every content-addressed blob in the tar."""
    documents, sizes = {}, {}
    with tarfile.open(path, 'r:*') as archive:
        seen = set()
        for member in archive:
            name = member.name
            if name in seen:
                raise ValueError(f'Duplicate OCI archive member: {name}')
            seen.add(name)
            if member.isdir():
                continue
            if not member.isfile():
                raise ValueError(f'Non-regular OCI archive member: {name}')
            if name not in ('index.json', 'oci-layout') and not re.fullmatch(r'blobs/sha256/[0-9a-f]{64}', name):
                raise ValueError(f'Unexpected OCI archive member: {name}')
            stream = archive.extractfile(member)
            digest = hashlib.sha256()
            # Manifests/configs are small; layer blobs are hashed but not retained.
            chunks = [] if member.size <= 16 * 1024 * 1024 else None
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
                if chunks is not None:
                    chunks.append(chunk)
            if name.startswith('blobs/') and digest.hexdigest() != name.rsplit('/', 1)[1]:
                raise ValueError(f'OCI blob checksum mismatch: {name}')
            sizes[name] = member.size
            if chunks is not None:
                raw = b''.join(chunks)
                try:
                    documents[name] = json.loads(raw)
                except (ValueError, UnicodeError):
                    pass
    if documents.get('oci-layout', {}).get('imageLayoutVersion') != '1.0.0':
        raise ValueError('Unsupported or missing OCI layout')
    entries = documents.get('index.json', {}).get('manifests', [])
    roots = {item['digest'] for item in entries}
    if len(roots) != 1:
        raise ValueError('OCI archive must contain exactly one image, possibly with multiple tags')

    def blob(descriptor):
        digest = descriptor.get('digest', '')
        if not re.fullmatch(r'sha256:[0-9a-f]{64}', digest):
            raise ValueError(f'Invalid OCI digest: {digest}')
        name = 'blobs/' + digest.replace(':', '/')
        if sizes.get(name) != descriptor.get('size'):
            raise ValueError(f'Missing or incorrectly sized OCI blob: {digest}')
        return documents.get(name)

    root = blob(entries[0])
    if not isinstance(root, dict) or root.get('schemaVersion') != 2:
        raise ValueError('Expected an OCI image manifest or image index')
    media_type = root.get('mediaType', entries[0].get('mediaType'))
    if media_type in ('application/vnd.oci.image.index.v1+json',
                      'application/vnd.docker.distribution.manifest.list.v2+json'):
        if not root.get('manifests'):
            raise ValueError('Image index has no manifests')
        descriptors = root['manifests']
        is_index = True
    elif media_type in ('application/vnd.oci.image.manifest.v1+json',
                        'application/vnd.docker.distribution.manifest.v2+json'):
        # BuildKit can export a single-platform group directly as a manifest.
        # Keep its digest unchanged, and obtain its platform from the config
        # when the outer layout descriptor does not advertise one.
        descriptor = dict(entries[0])
        if not descriptor.get('platform'):
            config = blob(root['config'])
            if not isinstance(config, dict):
                raise ValueError('Missing single-platform image configuration')
            descriptor['platform'] = {k: config[k] for k in ('os', 'architecture', 'variant') if k in config}
        descriptors = [descriptor]
        is_index = False
    else:
        raise ValueError(f'Unsupported image manifest media type: {media_type}')
    platforms, manifests = {}, {}
    for descriptor in descriptors:
        manifest = blob(descriptor)
        if not isinstance(manifest, dict):
            raise ValueError('Missing image manifest')
        config = blob(manifest['config'])
        for layer in manifest['layers']:
            blob(layer)
        manifests[descriptor['digest']] = {'descriptor': descriptor, 'manifest': manifest, 'config': config}
        platform = descriptor.get('platform', {})
        if descriptor.get('annotations', {}).get('vnd.docker.reference.type') == 'attestation-manifest':
            if platform.get('os') != 'unknown':
                raise ValueError('Unexpected attestation platform')
            continue
        key = platform.get('os', '') + '/' + platform.get('architecture', '')
        if key in platforms or key not in expected_platforms:
            raise ValueError(f'Unexpected or duplicate archive platform: {key}')
        if not isinstance(config, dict) or any(config.get(k) != platform.get(k) for k in ('os', 'architecture')):
            raise ValueError(f'Image configuration/platform mismatch: {key}')
        platforms[key] = descriptor
    if set(platforms) != set(expected_platforms):
        raise ValueError('Archive does not contain every approved platform')
    return {'digest': entries[0]['digest'], 'manifest': root, 'index': root if is_index else None,
            'layout_index': documents['index.json'],
            'platforms': platforms, 'manifests': manifests}
