"""Publish approved OpenRiak KV OCI archives, then scan immutable registry images.

This module never builds images or modifies approvals or documentation. Skopeo
copies all platforms (including attestations) and preserves manifest digests.
Docker Scout supplies unfiltered SARIF, SBOM, and detailed CVE/EPSS output.
"""
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

from openriak_defaults import DEFAULT_TIMEOUT_SECONDS
from openriak_cve_storage import write_report


def configure_parser(parser):
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument('--version', action='append', dest='versions')
    selection.add_argument('--all', action='store_true')
    parser.add_argument('--yes', action='store_true', help='Required with --all, except --whatif')
    parser.add_argument('--os-id', help='Select an OS group, including all its architectures')
    parser.add_argument('--otp')
    parser.add_argument('--namespace', help='Filter approvals by their recorded primary namespace')
    parser.add_argument('--extra-namespace', action='append', default=[], help='Add every approved alias under this namespace (repeatable)')
    parser.add_argument('--cache-root', type=Path, help='Existing cache/output directory (default: tools/cache/openriak-docker-multiarch)')
    parser.add_argument('--reports-dir', type=Path, help='Report parent directory (default: CACHE_ROOT/pushes)')
    parser.add_argument('--wait-seconds', type=float, default=5, help='Wait once after all uploads before scanning (default: 5)')
    parser.add_argument('--scan-retries', type=int, default=3, help='Additional attempts after a failed Scout command (default: 3)')
    parser.add_argument('--scan-retry-delay', type=float, default=5, help='Seconds between failed Scout attempts (default: 5)')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT_SECONDS, help='Seconds per external command (default: 1800)')
    parser.add_argument('--whatif', action='store_true', help='Validate approvals/archives and show tags without network access or writes')


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


def make_plan(options, tool):
    root = (options.cache_root or tool.MULTIARCH_CACHE_ROOT).expanduser().resolve()
    selected = tool.discover_targets(options.versions, os_id=options.os_id, otp=options.otp)
    keys = {(t.version, t.family, t.release, t.otp) for t in selected}
    groups = tool.grouped_targets([dataclasses.replace(t, output_root=root) for t in tool.discover_targets(options.versions)
                                  if (t.version, t.family, t.release, t.otp) in keys])
    plans, skipped, blocked, tag_owners = [], [], [], {}
    for group in groups:
        target = group[0]
        report_path = target.group_directory / 'report.json'
        if not report_path.is_file():
            skipped.append({'image': target.image_tag, 'reason': 'No current report'})
            continue
        try:
            report = tool.read_json(report_path)
            if report.get('status') != 'passed':
                skipped.append({'image': report.get('image', target.image_tag), 'reason': f"Status is {report.get('status')!r}"})
                continue
            namespace = report['image'].split('/', 1)[0]
            tool.extra_namespace(namespace)
            if options.namespace and options.namespace != namespace:
                continue
            identity = tool.ImageIdentity(**report.get('identity', {'namespace': namespace}))
            group = [dataclasses.replace(t, identity=identity) for t in group]
            approval = tool.approved_group_report(group)
            root_group = target.group_directory.resolve()
            history = root_group / 'runs' / approval['run_id']
            if not history.resolve().is_relative_to(root_group):
                raise ValueError('Approval run path escapes cache')
            if tool.read_json(history / 'report.json') != approval:
                raise ValueError('Current report differs from its saved run report')
            if not any(s.get('name') == 'export_oci_image' and s.get('status') == 'passed' for s in approval.get('steps', [])):
                raise ValueError('Approval has no successful OCI export')
            path = (root_group / approval['oci_archive']).resolve()
            if path != (history / 'image.oci.tar').resolve() or not path.is_relative_to(root_group):
                raise ValueError('Archive must belong to the approved test run')
            for artifact in approval['artifacts'].values():
                if tool.sha256_file(history / artifact['filename']) != artifact['sha256']:
                    raise ValueError('Run artifact differs from its approval')
            tags = tool.namespaced_tags(approval.get('build_tags') or approval['tags'], options.extra_namespace)
            if not set(approval['tags']).issubset(tags):
                raise ValueError('Export is missing approved tags')
            archive = archive_metadata(path, approval['platforms'])
            source_tag = approval['image'].split(':', 1)[1]
            if not any(d.get('annotations', {}).get('org.opencontainers.image.ref.name') == source_tag
                       for d in archive['layout_index']['manifests']):
                raise ValueError('OCI archive is missing its approved primary tag reference')
            for tag in tags:
                if tag in tag_owners:
                    raise ValueError(f'Tag {tag} is also claimed by {tag_owners[tag]}')
            for tag in tags:
                tag_owners[tag] = approval['image']
            proofs = {platform: tool.read_json(root_group / item['report'])
                      for platform, item in approval['platform_results'].items()}
            plans.append({'image': approval['image'], 'version': target.version, 'image_tag': target.image_tag,
                          'approval_path': str(report_path), 'approval_sha256': tool.sha256_file(report_path),
                          'approval': approval, 'platform_approvals': proofs, 'tags': tags,
                          'archive_path': str(path), 'archive_sha256': tool.sha256_file(path),
                          'archive_size': path.stat().st_size, 'archive': archive})
        except (tool.DockerToolError, argparse.ArgumentTypeError, OSError, ValueError, KeyError, TypeError, AttributeError, tarfile.TarError) as error:
            blocked.append({'image': target.image_tag, 'reason': str(error)})
    return root, plans, skipped, blocked


@contextlib.contextmanager
def docker_auth(options, tool):
    """Bridge Docker's global credsStore (unsupported by Skopeo) without logging secrets."""
    config_path = Path(os.environ.get('DOCKER_CONFIG', str(Path.home() / '.docker'))) / 'config.json'
    config = tool.read_json(config_path) if config_path.is_file() else {}
    keys = ('https://index.docker.io/v1/', 'docker.io', 'index.docker.io', 'registry-1.docker.io')
    helpers = config.get('credHelpers', {})
    helper = next((helpers[k] for k in keys if k in helpers), config.get('credsStore'))
    auth = next((config.get('auths', {})[k] for k in keys if k in config.get('auths', {})), {})
    if helper:
        if not re.fullmatch(r'[A-Za-z0-9_.-]+', helper):
            raise tool.DockerToolError('Invalid Docker credential helper name')
        # The helper protocol sends the server on stdin and returns JSON. Keep
        # this separate from execute(): its stdout must never enter a report.
        try:
            response = subprocess.run(['docker-credential-' + helper, 'get'],
                                      input=b'https://index.docker.io/v1/\n', stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE, timeout=options.timeout, check=False)
            if response.returncode != 0:
                raise ValueError('Helper failed')
            credentials = json.loads(response.stdout)
            username, secret = credentials['Username'], credentials['Secret']
            if not isinstance(username, str) or not isinstance(secret, str) or not secret:
                raise ValueError('Invalid credentials')
        except (OSError, subprocess.TimeoutExpired, ValueError, KeyError, TypeError):
            raise tool.DockerToolError('Cannot read Docker Hub credentials from the configured helper; run docker login in this environment') from None
        auth = ({'auth': base64.b64encode(b':').decode(), 'identitytoken': secret} if username == '<token>' else
                {'auth': base64.b64encode(f'{username}:{secret}'.encode()).decode()})
    if not auth.get('auth') and not auth.get('identitytoken'):
        raise tool.DockerToolError('No Docker Hub credentials found; run docker login first')
    with tempfile.TemporaryDirectory(prefix='openriak-push-auth-') as directory:
        path = Path(directory) / 'auth.json'
        with open(path, 'x', encoding='utf-8', opener=lambda p, flags: os.open(p, flags, 0o600)) as handle:
            json.dump({'auths': {'docker.io': auth}}, handle)
        yield ['--authfile', str(path)]


def execute(command, timeout):
    """Retain complete tool output; never pass credentials on the command line."""
    started = time.monotonic()
    record = {'command': command, 'started_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              'exit_code': None, 'stdout': '', 'stderr': '', 'error': None}
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=False)
        record.update(exit_code=result.returncode, stdout=result.stdout.decode('utf-8', 'replace'),
                      stderr=result.stderr.decode('utf-8', 'replace'))
    except subprocess.TimeoutExpired as error:
        record.update(error=f'Command timed out after {timeout}s',
                      stdout=(error.stdout or b'').decode('utf-8', 'replace'),
                      stderr=(error.stderr or b'').decode('utf-8', 'replace'))
    except OSError as error:
        record['error'] = str(error)
    record['finished_at'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    record['duration_seconds'] = round(time.monotonic() - started, 3)
    return record


def registry_manifest(tag, options, report, label):
    result = execute([options.skopeo, 'inspect', '--raw', *options.auth_args, 'docker://docker.io/' + tag], options.timeout)
    report[label] = result
    if result['exit_code'] != 0:
        return None
    try:
        manifest = json.loads(result['stdout'])
        if not isinstance(manifest, dict) or manifest.get('schemaVersion') != 2:
            raise ValueError('Invalid registry manifest')
    except ValueError as error:
        result['error'] = str(error)
        return None
    result['digest'] = sha256(result['stdout'].encode())
    result['manifest'] = manifest
    return result['digest']


def push_tags(plan, report, options, tool, save):
    path = Path(plan['archive_path'])
    if tool.sha256_file(Path(plan['approval_path'])) != plan['approval_sha256'] or tool.sha256_file(path) != plan['archive_sha256']:
        raise ValueError('Approval or OCI archive changed after preflight; run push again')
    expected = plan['archive']['digest']
    # BuildKit archives have one layout entry per alias; select the primary one.
    source_tag = plan['approval']['image'].split(':', 1)[1]
    source = f'oci-archive:{path}:{source_tag}'
    for tag in plan['tags']:
        state = {'tag': tag, 'expected_digest': expected, 'status': 'running', 'verified': False}
        report['pushes'].append(state)
        save()
        print(f'{tool.log_timestamp()}   Pushing {tag}', flush=True)
        before = registry_manifest(tag, options, state, 'before')
        if before == expected:
            state.update(status='already_present', verified=True, registry_digest=before)
        else:
            state['copy'] = execute([options.skopeo, 'copy', '--all', '--preserve-digests', *options.auth_args,
                                     source, 'docker://docker.io/' + tag], options.timeout)
            save()
            after = registry_manifest(tag, options, state, 'after')
            state.update(verified=after == expected, registry_digest=after,
                         status=('pushed' if state['copy']['exit_code'] == 0 else 'verified_after_copy_error')
                         if after == expected else 'failed')
        print(f"{tool.log_timestamp()}   {state['status'].upper()} {tag}", flush=True)
        save()


def collect_scout(reference, platform, mode, options, record, save):
    """Retry failures, never interpret a missing/malformed report as zero CVEs."""
    if mode == 'sarif':
        args = ['cves', '--format', 'sarif', '--epss']
    elif mode == 'sbom':
        args = ['sbom', '--format', 'json']
    else:
        args = ['cves', '--details', '--epss']
    output = {'status': 'running', 'attempts': []}
    record[mode] = output
    for attempt in range(options.scan_retries + 1):
        result = execute([options.docker, 'scout', *args, '--platform', platform, reference], options.timeout)
        output['attempts'].append(result)
        if result['exit_code'] == 0:
            try:
                data = result['stdout'] if mode == 'details' else json.loads(result['stdout'])
                if mode == 'sarif' and (not isinstance(data, dict) or data.get('version') != '2.1.0'
                                        or not data.get('runs') or any(not isinstance(r, dict) or not r.get('tool', {}).get('driver')
                                            or not isinstance(r.get('results') or [], list) for r in data['runs'])):
                    raise ValueError('Scout returned invalid/incomplete SARIF')
                if mode == 'sbom' and (not isinstance(data, dict) or not data):
                    raise ValueError('Scout returned an empty/invalid SBOM')
                if mode == 'details' and not data.strip():
                    raise ValueError('Scout returned empty details')
                output.update(status='complete', data=data)
                save()
                return data
            except (ValueError, TypeError, AttributeError) as error:
                result['error'] = str(error)
        save()
        if attempt < options.scan_retries:
            time.sleep(options.scan_retry_delay)
    output['status'] = 'failed'
    save()


def scan_image(plan, report, options, tool, save):
    verified = [p for p in report['pushes'] if p.get('verified')]
    if not verified:
        report['scan_status'] = 'not_scanned_no_verified_push'
        save()
        return
    repository = verified[0]['tag'].split(':', 1)[0]
    for platform, descriptor in plan['archive']['platforms'].items():
        # Use each immutable platform digest, never a mutable tag or local image.
        reference = f"registry://docker.io/{repository}@{descriptor['digest']}"
        record = {'platform': platform, 'manifest_digest': descriptor['digest'], 'reference': reference,
                  'started_at': tool.isoformat(), 'status': 'running'}
        report['scans'][platform] = record
        save()
        print(f'{tool.log_timestamp()}   Scanning {plan["image"]} {platform} {descriptor["digest"]}', flush=True)
        for mode in ('sarif', 'sbom', 'details'):
            data = collect_scout(reference, platform, mode, options, record, save)
            if mode == 'sarif' and record[mode]['status'] == 'complete':
                runs = data['runs']
                record['finding_count'] = sum(len(r.get('results') or []) for r in runs)
                record['cve_ids'] = sorted({r.get('ruleId', '') for run in runs for r in (run.get('results') or []) if r.get('ruleId')})
        record['status'] = 'complete' if all(record[m]['status'] == 'complete' for m in ('sarif', 'sbom', 'details')) else 'failed'
        record['finished_at'] = tool.isoformat()
        save()
    report['scan_status'] = 'complete' if all(s['status'] == 'complete' for s in report['scans'].values()) else 'failed'
    save()


def main(options, tool):
    if options.all and not options.yes and not options.whatif:
        raise tool.DockerToolError('push --all requires --yes')
    if options.timeout <= 0 or options.scan_retries < 0 or any(not math.isfinite(n) or n < 0 for n in (options.wait_seconds, options.scan_retry_delay)):
        raise tool.DockerToolError('Timeout must be positive; wait/retry settings must be finite and nonnegative')
    for namespace in [*options.extra_namespace, *([options.namespace] if options.namespace else [])]:
        try:
            tool.extra_namespace(namespace)
        except argparse.ArgumentTypeError as error:
            raise tool.DockerToolError(str(error)) from error
    root, plans, skipped, blocked = make_plan(options, tool)
    for item in skipped:
        print(f"{tool.log_timestamp()} SKIPPED {item['image']}: {item['reason']}", flush=True)
    for item in blocked:
        print(f"{tool.log_timestamp()} BLOCKED {item['image']}: {item['reason']}", flush=True)
    for plan in plans:
        print(f"{tool.log_timestamp()} {'WOULD PUSH' if options.whatif else 'SELECTED'} {plan['image']} ({', '.join(plan['archive']['platforms'])})", flush=True)
        print(f"  Digest: {plan['archive']['digest']}\n  Tags: {', '.join(plan['tags'])}", flush=True)
    if blocked:
        raise tool.DockerToolError('Preflight failed; nothing was pushed. Resolve the blocked approvals/archives first.')
    if not plans:
        raise tool.DockerToolError('No passed images with approved OCI archives selected')
    if options.whatif:
        print(f'Would wait {options.wait_seconds:g}s after all uploads, then scan every platform by digest. Registry state was not queried.')
        return 0
    options.skopeo = shutil.which('skopeo')
    if not options.skopeo:
        raise tool.DockerToolError('Skopeo is required to preserve all architectures. On Ubuntu: sudo apt-get install skopeo')
    options.docker = tool.docker_command()
    versions = {name: execute(command, options.timeout) for name, command in
                [('skopeo', [options.skopeo, '--version']), ('scout', [options.docker, 'scout', 'version'])]}
    if any(r['exit_code'] != 0 for r in versions.values()):
        raise tool.DockerToolError('Skopeo and Docker Scout must be installed and runnable before any upload')
    copy_help = execute([options.skopeo, 'copy', '--help'], options.timeout)
    if copy_help['exit_code'] != 0 or '--preserve-digests' not in copy_help['stdout']:
        raise tool.DockerToolError('Installed Skopeo is too old or its copy command is unavailable. '
                                  'Install a current Skopeo with copy --preserve-digests support '
                                  '(https://github.com/containers/skopeo/blob/main/install.md). '
                                  'Nothing was pushed.')
    directory = (options.reports_dir or root / 'pushes').expanduser().resolve() / tool.run_id()
    directory.mkdir(parents=True, exist_ok=False)
    summary = {'schema_version': 1, 'operation': 'push_and_scan', 'product': 'openriak-kv',
               'started_at': tool.isoformat(), 'finished_at': None, 'pid': os.getpid(), 'status': 'running',
               'settings': {'wait_seconds': options.wait_seconds, 'scan_retries': options.scan_retries,
                            'scan_retry_delay': options.scan_retry_delay, 'timeout': options.timeout},
               'tools': versions, 'skipped': skipped, 'images': []}
    jobs = []
    for plan in plans:
        path = directory / plan['version'] / plan['image_tag'] / 'cve-report.json'
        report = {'schema_version': 1, 'operation': 'push_and_scan', 'product': 'openriak-kv',
                  'started_at': tool.isoformat(), 'finished_at': None, 'status': 'pending',
                  'source': plan, 'tools': versions, 'settings': summary['settings'],
                  'pushes': [], 'scans': {}, 'scan_status': 'pending', 'error': None}
        jobs.append((plan, report, path))
        summary['images'].append({'image': plan['image'], 'expected_digest': plan['archive']['digest'],
                                  'report': str(path.relative_to(directory))})
        write_report(path, report)
    tool.write_json(directory / 'report.json', summary)
    print(f'{tool.log_timestamp()} Push PID: {os.getpid()}; reports: {directory}', flush=True)
    try:
        with docker_auth(options, tool) as auth_args:
            options.auth_args = auth_args
            for plan, report, path in jobs:
                save = lambda p=path, r=report: write_report(p, r)
                report['status'] = 'pushing'
                try:
                    push_tags(plan, report, options, tool, save)
                except (OSError, ValueError, tool.DockerToolError) as error:
                    report['error'] = str(error)
                report['status'] = 'awaiting_scan'
                save()
        if any(p.get('verified') for _, r, _ in jobs for p in r['pushes']):
            summary['uploads_finished_at'] = tool.isoformat()
            tool.write_json(directory / 'report.json', summary)
            print(f'{tool.log_timestamp()} All uploads finished; waiting {options.wait_seconds:g}s before Scout scans', flush=True)
            time.sleep(options.wait_seconds)
        for plan, report, path in jobs:
            save = lambda p=path, r=report: write_report(p, r)
            report['status'] = 'scanning'
            save()
            try:
                scan_image(plan, report, options, tool, save)
            except (OSError, ValueError, tool.DockerToolError) as error:
                report['error'] = str(error)
                report['scan_status'] = 'failed'
            successful = (not report['error'] and report['scan_status'] == 'complete'
                          and len(report['pushes']) == len(plan['tags'])
                          and all(p['status'] in ('pushed', 'already_present') for p in report['pushes']))
            report.update(status='complete' if successful else 'failed', finished_at=tool.isoformat())
            save()
        summary['status'] = 'complete' if all(r['status'] == 'complete' for _, r, _ in jobs) else 'failed'
    except KeyboardInterrupt:
        summary['status'] = 'interrupted'
        for _, report, path in jobs:
            if report['status'] not in ('complete', 'failed'):
                report.update(status='interrupted', finished_at=tool.isoformat())
                write_report(path, report)
        print(f'{tool.log_timestamp()} Push/scan interrupted; reports retained at {directory}', flush=True)
        return 130
    except (OSError, ValueError, tool.DockerToolError) as error:
        summary.update(status='failed', error=str(error))
        for _, report, path in jobs:
            if report['status'] not in ('complete', 'failed'):
                report.update(status='failed', error=str(error), finished_at=tool.isoformat())
                write_report(path, report)
    finally:
        summary['finished_at'] = tool.isoformat()
        for item, (_, report, _) in zip(summary['images'], jobs):
            item.update(status=report['status'], scan_status=report['scan_status'])
        tool.write_json(directory / 'report.json', summary)
    print(f"{tool.log_timestamp()} {summary['status'].upper()}; CVE reports: {directory}", flush=True)
    # Findings are data, not command errors. Missing scans/uploads are failures.
    return 0 if summary['status'] == 'complete' else 1
