#!/usr/bin/env python3
"""Validate candidate runtime filesystems against metadata-backed amd64 images."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import dataclasses
import json
from pathlib import Path
import sys
import shutil
import tarfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import openriak_docker as tool
import openriak_minimal as minimal
from rhel_minimal import scan_image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review', type=Path, default=Path(__file__).resolve().parents[1] / 'reports/cve-review-2026-09-08.json')
    parser.add_argument('--family', action='append')
    parser.add_argument('--image-tag', action='append')
    parser.add_argument('--severity', action='append', choices=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'UNSPECIFIED'],
                        help='Saved finding severities to select; repeatable (default: CRITICAL and HIGH)')
    parser.add_argument('--jobs', type=int, default=2)
    parser.add_argument('--timeout', type=int, default=tool.DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument('--openssl-backport', action='store_true',
                        help='Prototype the Debian 12 OpenSSL security backport (amd64 only)')
    parser.add_argument('--base-cache', type=Path,
                        help='Validate against an approved patched-base directory without publishing it')
    args = parser.parse_args()
    if args.base_cache:
        args.openssl_backport = True
    if args.timeout < 1 or args.jobs not in (1, 2):
        parser.error('Positive timeout and one or two jobs required')
    severities = args.severity or ['CRITICAL', 'HIGH']
    if args.image_tag:
        # Explicit tags also validate siblings with no findings in an older review.
        # Discovery still requires a real metadata-backed package and amd64 target.
        affected = set(args.image_tag)
    else:
        review = json.loads(args.review.read_text())
        affected = {row['image'].split(':')[1] for row in review['images']
                    if any(row['counts'].get(severity, 0) for severity in severities)}
    versions = sorted({tag.split('-')[0] for tag in affected})
    groups = tool.grouped_targets(tool.discover_targets(versions))
    selected = [next(t for t in group if t.platform == 'linux/amd64') for group in groups
                if group[0].image_tag in affected
                and (not args.family or group[0].family in args.family)
                and (not args.image_tag or group[0].image_tag in args.image_tag)]
    if args.openssl_backport:
        selected = [t for t in selected if (t.family, t.release) == ('debian', '12')]
    if not selected:
        parser.error('No affected metadata-backed amd64 targets match')
    candidates = json.loads(Path(__file__).with_name('runtime-candidates.json').read_text())
    original_configuration = minimal.configuration
    if args.openssl_backport:
        candidates['debian']['12']['openssl_backport'] = minimal.OPENSSL_VERSION
    if args.base_cache:
        import openriak_base
        base_approval, base_archive, base_metadata = openriak_base.approval(args.base_cache.resolve(), tool)
        candidates['debian']['12']['base_image'] = openriak_base.BASE_TAG
    def candidate_configuration(target):
        current = original_configuration(target)
        candidate = candidates.get(target.family, {}).get(target.release)
        return {**(current or {}), **candidate} if candidate else current

    minimal.configuration = candidate_configuration
    output = tool.REPOSITORY_ROOT / 'tools/cache/openriak-docker-minimal-validation' / tool.run_id()
    output.mkdir(parents=True)
    original_resolve = tool.resolve_base_image
    original_run_logged = tool.run_logged
    if args.base_cache:
        layout = output / 'base-layout'
        layout.mkdir()
        # The approval validates every OCI member/hash; extraction also confines paths.
        with tarfile.open(base_archive) as archive:
            for member in archive:
                destination = (layout / member.name).resolve()
                if not destination.is_relative_to(layout.resolve()):
                    raise ValueError('OCI member escapes the layout')
                if member.isdir():
                    destination.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with archive.extractfile(member) as source, destination.open('wb') as dest:
                        shutil.copyfileobj(source, dest)
                else:
                    raise ValueError('Unexpected OCI member type')
        def resolve_patched(target, logs, timeout):
            image = f'{target.identity.namespace}/{openriak_base.BASE_TAG}'
            return image, image + '@' + base_metadata['digest']
        tool.resolve_base_image = resolve_patched
        def local_base_context(command, *arguments, **keywords):
            if list(command[1:3]) == ['buildx', 'build']:
                reference = 'openriak-minimal-validation/' + openriak_base.BASE_TAG + '@' + base_metadata['digest']
                command = [*command[:-1], '--build-context',
                           f'{reference}=oci-layout://{layout}@{base_metadata["digest"]}', command[-1]]
            return original_run_logged(command, *arguments, **keywords)
        tool.run_logged = local_base_context
    targets = [dataclasses.replace(t, grouped=True, output_root=output,
               identity=tool.ImageIdentity(namespace='openriak-minimal-validation')) for t in selected]
    states = {}
    for t in targets:
        t.group_directory.mkdir(parents=True)
        states[t.image_tag] = {'status': 'pending', 'image_tag': t.image_tag,
            'image': t.image + '-' + output.name.lower(), 'platform': t.platform,
            'strategy': minimal.configuration(t), 'output': str(t.group_directory)}
        if args.base_cache:
            states[t.image_tag]['patched_base'] = {'image': base_approval['image'], 'digest': base_metadata['digest'],
                'approval': str(args.base_cache.resolve() / 'report.json'),
                'approval_sha256': tool.sha256_file(args.base_cache.resolve() / 'report.json')}
    original_verify = tool.verify_runtime_options

    def verify(container, target, timeout, log):
        result = original_verify(container, target, timeout, log)
        state = states[target.image_tag]
        if state['strategy']['strategy'] == 'rpm-root':
            tool.run_logged([tool.docker_command(), 'exec', container, 'sh', '-ec', '''
for name in python python3 perl pip pip3 dnf yum microdnf rpm
do
    if command -v "$name" >/dev/null 2>&1
    then
        echo "Unexpected runtime command: $name" >&2
        exit 1
    fi
done
if find /usr /opt -type f \( -iname '*python*' -o -iname '*setuptools*' -o -name perl \) | grep .
then
    exit 1
fi
cat /usr/share/openriak-build/runtime-packages.txt
'''], log.parent / f'minimal-runtime-{container}.log', timeout_seconds=timeout)
            result['minimal_runtime'] = 'No Python, Perl, pip, setuptools or package managers'
        if target.family == 'debian':
            tool.run_logged([tool.docker_command(), 'exec', container, 'sh', '-ec',
                'test ! -e /usr/bin/perl\ntest ! -e /usr/bin/python3'],
                log.parent / f'minimal-runtime-{container}.log', timeout_seconds=timeout)
        if 'image_inspection' not in state:
            inspection = json.loads(tool.run_logged([tool.docker_command(), 'container', 'inspect', container],
                log.parent / 'minimal-container-inspect.log', timeout_seconds=timeout).stdout)[0]
            tool.run_logged([tool.docker_command(), 'image', 'tag', inspection['Image'], state['image']],
                log.parent / 'retain-minimal-image.log', timeout_seconds=timeout)
            image = json.loads(tool.run_logged([tool.docker_command(), 'image', 'inspect', state['image']],
                log.parent / 'minimal-image-inspect.log', timeout_seconds=timeout).stdout)[0]
            state['image_inspection'] = {'id': image['Id'], 'size_bytes': image['Size'], 'layers': image['RootFS']['Layers']}
        return result

    def run(target):
        state = states[target.image_tag]
        summary = target.group_directory / 'validation.json'
        state.update(status='running', started_at=tool.isoformat())
        summary.write_text(json.dumps(state, indent=2) + '\n')
        progress = lambda message: print(f'{tool.log_timestamp()} {target.image_tag}: {message}', flush=True)
        try:
            progress('Using approved patched-base OCI archive' if args.base_cache else 'Pulling release base')
            base, pinned = tool.resolve_base_image(target, target.group_directory / 'logs', args.timeout)
            bases = {target.platform: {'requested': base, 'pinned': pinned, 'resolved_at': tool.isoformat()}}
            cookie = tool.generate_distributed_cookie()
            tool.render_group_assets([target], bases, cookie, [target.image], 5, target.group_directory)
            state['dockerfile_sha256'] = tool.sha256_file(target.group_directory / 'Dockerfile')
            state['base_images'] = bases
            passed = tool.refresh_target(target, args.timeout, cluster_nodes=5,
                prepared={'base_images': bases, 'distributed_cookie': cookie}, progress=progress)
            state['integration_report'] = str(target.cache_directory / 'report.json')
            state['status'] = 'passed' if passed else 'failed'
            if passed:
                if args.openssl_backport:
                    from openssl_compatibility import verify as verify_openssl
                    progress('Checking packaged OTP crypto and certificate-verified TLS')
                    state['openssl_compatibility'] = verify_openssl(
                        state['image'], target.group_directory, timeout=args.timeout)
                progress('PASSED amd64 integration; scanning runtime and package inventory')
                expected = {'riak', 'libc6' if target.operating_system['package_family'] == 'deb' else 'glibc'}
                state['scout'] = scan_image(state['image'], target.platform, args.timeout, summary,
                    expected_packages=expected, reject_interpreters=state['strategy']['strategy'] == 'rpm-root')
                progress('Scout: ' + json.dumps(state['scout']['counts']))
        except Exception as error:
            state.update(status='error', error=str(error))
            progress('ERROR: ' + str(error))
        finally:
            state['finished_at'] = tool.isoformat()
            summary.write_text(json.dumps(state, indent=2) + '\n')
        return state

    print('Evidence:', output, flush=True)
    tool.verify_runtime_options = verify
    try:
        with tool.MultiarchBuilderLifecycle() as lifecycle:
            tool.ensure_multiarch_builder(output / 'logs', args.timeout, lifecycle)
            with ThreadPoolExecutor(max_workers=args.jobs) as pool:
                for future in as_completed([pool.submit(run, t) for t in targets]):
                    result = future.result()
                    print(tool.log_timestamp(), result['image_tag'], result['status'].upper(), flush=True)
    finally:
        tool.verify_runtime_options = original_verify
        minimal.configuration = original_configuration
        tool.resolve_base_image = original_resolve
        tool.run_logged = original_run_logged
        (output / 'matrix.json').write_text(json.dumps(states, indent=2) + '\n')
    return 0 if all(s['status'] == 'passed' for s in states.values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())
