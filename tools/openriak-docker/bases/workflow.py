"""Reusable, independently approved OS base images for OpenRiak KV."""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import os
from pathlib import Path
import sys

import images.minimal as minimal
import publishing.workflow as push
from builders_base import registry


def selected_release(options):
    catalogue = registry.catalogue()
    name = getattr(options, 'base', catalogue['default'])
    entry = catalogue['releases'][name]
    return entry['family'], entry['release']


def base_tag(options, tool):
    family, release = selected_release(options)
    config = tool.read_json(minimal.CONFIG_PATH)
    return config['releases'][family][release]['base_image']


def configure_parser(parser, tool):
    parser.add_argument('action', choices=('generate', 'refresh', 'push'))
    push.configure_parser(parser, selection=False)
    catalogue = registry.catalogue()
    parser.add_argument('--base', choices=tuple(catalogue['releases']), default=catalogue['default'],
                        help=f"Reusable patched OS release (default: {catalogue['default']})")
    parser.add_argument('--platform', action='append', dest='platforms',
                        help='Metadata-backed platform to include (repeatable; default: all metadata platforms for the selected base)')
    parser.add_argument('--force', action='store_true', help='Pull the upstream release again and rebuild/retest from scratch')
    parser.add_argument('--nohup', action='store_true', help='Run detached and print the PID and timestamped log path')
    parser.add_argument('--vendor', type=tool.label_text)
    parser.add_argument('--source', type=tool.label_url)
    parser.add_argument('--url', type=tool.label_url)
    parser.set_defaults(product='openriak-base')


def selected_targets(options, tool):
    identity = tool.identity_from_options(options)
    tool.extra_namespace(identity.namespace)
    available = {}
    for target in tool.discover_targets(None):
        if (target.family, target.release) == selected_release(options):
            available.setdefault(target.platform, dataclasses.replace(target, identity=identity))
    wanted = set(options.platforms or available)
    if not wanted or not wanted <= set(available):
        raise tool.DockerToolError(f'Base platforms must come from {options.base} OpenRiak KV metadata')
    return [available[p] for p in sorted(wanted)]


def cache_directory(options, tool):
    parent = (options.cache_root or tool.REPOSITORY_ROOT / '.work/openriak-docker/bases').expanduser().resolve()
    namespace = options.namespace or tool.ImageIdentity().namespace
    tool.extra_namespace(namespace)
    repository, tag = base_tag(options, tool).split(':', 1)
    return parent / namespace / repository / tag


def image_tags(identity, extras, tool, tag):
    namespaces = [identity.namespace, *extras]
    for namespace in namespaces:
        tool.extra_namespace(namespace)
    return list(dict.fromkeys(f'{namespace}/{tag}' for namespace in namespaces))


def render(targets, bases, tool):
    return registry.render(targets, bases, tool)


def runtime_check(target):
    return registry.runtime_check(target)


def approval(root, tool, *, require_archive=True):
    report = tool.read_json(root / 'report.json')
    if report.get('schema_version') != 1 or report.get('status') != 'passed' or report.get('product') != 'openriak-base':
        raise tool.DockerToolError('No passed patched-base approval; run base refresh first')
    if not report.get('tags') or report.get('image') not in report['tags']:
        raise tool.DockerToolError('Base approval is missing its primary tag')
    allowed = {entry.get('base_image') for releases in tool.read_json(minimal.CONFIG_PATH)['releases'].values()
               for entry in releases.values()} - {None}
    approved_tag = report['image'].partition('/')[2]
    if approved_tag not in allowed:
        raise tool.DockerToolError('Unknown patched base image in approval')
    for tag in report['tags']:
        namespace, separator, suffix = tag.partition('/')
        tool.extra_namespace(namespace)
        if not separator or suffix != approved_tag:
            raise tool.DockerToolError('Base approvals can publish only <namespace>/' + approved_tag)
    history = (root / 'runs' / report['run_id']).resolve()
    if not history.is_relative_to(root.resolve()) or tool.read_json(history / 'report.json') != report:
        raise tool.DockerToolError('Base approval differs from its saved run')
    for path in (root / 'Dockerfile', history / 'Dockerfile'):
        if tool.sha256_file(path) != report['dockerfile_sha256']:
            raise tool.DockerToolError('Approved base Dockerfile changed; regenerate and retest')
    archive_path = history / 'image.oci.tar'
    if not archive_path.resolve().is_relative_to(history):
        raise tool.DockerToolError('Base archive escapes its approved run')
    if not require_archive:
        if any(report.get('tests', {}).get(platform, {}).get('status') != 'passed' for platform in report['platforms']):
            raise tool.DockerToolError('Base platform test evidence is incomplete')
        return report, archive_path, None
    if tool.sha256_file(archive_path) != report['archive_sha256']:
        raise tool.DockerToolError('Approved base OCI archive changed; rebuild and retest')
    metadata = push.archive_metadata(archive_path, report['platforms'])
    if report.get('digest') != metadata['digest']:
        raise tool.DockerToolError('Base digest differs from its approval')
    tag_name = report['image'].split(':', 1)[1]
    if not any(entry.get('annotations', {}).get('org.opencontainers.image.ref.name') == tag_name
               for entry in metadata['layout_index']['manifests']):
        raise tool.DockerToolError('Base archive is missing its approved primary tag')
    for platform, descriptor in metadata['platforms'].items():
        proof = report['tests'].get(platform, {})
        config = metadata['manifests'][descriptor['digest']]['manifest']['config']['digest']
        if proof.get('status') != 'passed' or proof.get('image_id') != config:
            raise tool.DockerToolError('Base archive does not contain the tested platform image')
    return report, archive_path, metadata


def push_plan(options, tool):
    root = cache_directory(options, tool)
    try:
        report, archive_path, metadata = approval(root, tool)
        identity = tool.ImageIdentity(**report['identity'])
        if report['image'] != f'{options.namespace or "openriak"}/{base_tag(options, tool)}':
            raise tool.DockerToolError('Base approval namespace does not match')
        tags = list(dict.fromkeys([*report['tags'], *image_tags(identity, options.extra_namespace, tool, base_tag(options, tool))]))
        plan = {'image': report['image'], 'version': base_tag(options, tool).split(':')[0], 'image_tag': base_tag(options, tool).split(':')[1],
                'approval': report, 'approval_path': str(root / 'report.json'),
                'approval_sha256': tool.sha256_file(root / 'report.json'),
                'platform_approvals': report['tests'], 'tags': tags, 'archive': metadata,
                'archive_path': str(archive_path), 'archive_sha256': report['archive_sha256'],
                'archive_size': archive_path.stat().st_size}
        return root, [plan], [], []
    except (OSError, ValueError, KeyError, tool.DockerToolError) as error:
        return root, [], [], [{'image': base_tag(options, tool), 'reason': str(error)}]


def main(options, tool, arguments=None):
    if options.timeout <= 0:
        raise tool.DockerToolError('--timeout must be positive')
    if options.os_id or options.otp:
        raise tool.DockerToolError('Use --base for the patched OS release and --platform for architecture selection')
    try:
        for namespace in [options.namespace or tool.ImageIdentity().namespace, *options.extra_namespace]:
            tool.extra_namespace(namespace)
    except argparse.ArgumentTypeError as error:
        raise tool.DockerToolError(str(error)) from error
    if options.nohup and not options.whatif:
        import core.background as openriak_background
        background = argparse.Namespace(**vars(options))
        background.output = str(cache_directory(options, tool))
        background.command = 'base-' + options.action
        return openriak_background.launch(tool, background, sys.argv[1:] if arguments is None else arguments)
    if options.action == 'push':
        if options.force or options.platforms or any((options.vendor, options.source, options.url)):
            raise tool.DockerToolError('base push publishes approved bytes; build/label/platform options require base refresh')
        return push.main(options, tool, plan_loader=push_plan)
    targets = selected_targets(options, tool)
    identity = targets[0].identity
    tags = image_tags(identity, options.extra_namespace, tool, base_tag(options, tool))
    root = cache_directory(options, tool)
    inputs = {'identity': dataclasses.asdict(identity), 'platforms': [t.platform for t in targets], 'tags': tags,
              'upstreams': {t.platform: tool.base_image_for(t, upstream=True) for t in targets},
              'renderer_sha256': tool.sha256_file(Path(__file__)),
              'common_renderer_sha256': tool.sha256_file(Path(tool.__file__)),
              'build_dependencies': registry.dependencies(targets, tool),
              'runtime_checks': {t.platform: runtime_check(t) for t in targets}}
    previous = tool.read_json(root / 'report.json') if (root / 'report.json').exists() else {}
    if previous and not options.force:
        try:
            saved, _, _ = approval(root, tool, require_archive=False)
            keys = ('identity', 'platforms', 'tags', 'upstreams')
            # Older approvals predate layered fingerprints. Preserve them only
            # when their substantive inputs and every Dockerfile byte still match.
            if 'build_dependencies' in saved['inputs']:
                keys += ('build_dependencies', 'runtime_checks')
            if (any(saved['inputs'].get(key) != inputs[key] for key in keys)
                    or render(targets, saved['base_images'], tool) != (root / 'Dockerfile').read_text()):
                raise tool.DockerToolError('Base generation inputs changed')
        except (OSError, ValueError, KeyError, tool.DockerToolError) as error:
            raise tool.DockerToolError(f'{error}; use base {options.action} --force') from error
        print(f'{tool.log_timestamp()} SKIPPED {tags[0]} (complete base cache exists)', flush=True)
        return 0
    if options.whatif:
        print(f'{tool.log_timestamp()} WOULD {options.action.upper()} {tags[0]} ({", ".join(inputs["platforms"])})', flush=True)
        return 0
    history = root / 'runs' / tool.run_id()
    history.mkdir(parents=True, exist_ok=False)
    report = {'schema_version': 1, 'product': 'openriak-base', 'status': 'running', 'image': tags[0],
              'pid': os.getpid(),
              'identity': inputs['identity'], 'tags': tags, 'platforms': inputs['platforms'], 'inputs': inputs,
              'run_id': history.name, 'started_at': tool.isoformat(), 'finished_at': None,
              'base_images': {}, 'tests': {}, 'error': None}
    def save():
        tool.write_json(history / 'report.json', report)
        tool.write_json(root / 'report.json', report)
    save()
    print(f'{tool.log_timestamp()} Base {options.action} PID: {os.getpid()}; image: {tags[0]}; reports: {root}', flush=True)
    if os.environ.get('OPENRIAK_DOCKER_LOG_FILE'):
        print(f'{tool.log_timestamp()} Log file: {os.environ["OPENRIAK_DOCKER_LOG_FILE"]}', flush=True)
    temporary_tags = []
    try:
        for target in targets:
            print(f'{tool.log_timestamp()} Pulling upstream {targets[0].family} {targets[0].release} for {target.platform}', flush=True)
            requested, pinned = tool.resolve_base_image(target, history / 'logs' / target.platform.replace('/', '-'), options.timeout, upstream=True)
            report['base_images'][target.platform] = {'requested': requested, 'pinned': pinned}
        source = render(targets, report['base_images'], tool)
        (root / 'Dockerfile').write_text(source)
        (history / 'Dockerfile').write_text(source)
        (history / '.dockerignore').write_text('*\n')
        report['dockerfile_sha256'] = hashlib.sha256(source.encode()).hexdigest()
        if options.action == 'generate':
            report['status'] = 'generated'
            print(f'Generated {root / "Dockerfile"}; base not built, tested or pushed', flush=True)
            return 0
        with tool.MultiarchBuilderLifecycle() as lifecycle:
            tool.ensure_multiarch_builder(history / 'logs', options.timeout, lifecycle)
            common = [tool.docker_command(), 'buildx', 'build', '--builder', tool.MULTIARCH_BUILDER, '--pull=false']
            for target in targets:
                platform = target.platform
                temporary = f'{identity.namespace}/{base_tag(options, tool).split(":")[0]}:test-{history.name.lower()}-{platform.split("/")[1]}'
                temporary_tags.append(temporary)
                print(f'{tool.log_timestamp()} Building/testing {tags[0]} for {platform}', flush=True)
                tool.run_logged([*common, '--platform', platform, '--load', '--tag', temporary,
                    *(['--no-cache'] if options.force else []), str(history)],
                    history / 'logs' / f'build-{platform.split("/")[1]}.log', timeout_seconds=options.timeout)
                # Pin test execution to the image ID, not a mutable tag.
                image_id = tool.run_logged([tool.docker_command(), 'image', 'inspect', '--format', '{{.Id}}', temporary],
                    history / 'logs' / f'inspect-{platform.split("/")[1]}.log', timeout_seconds=options.timeout).stdout.strip()
                name = 'openriak-base-test-' + history.name.lower().replace('.', '-') + '-' + platform.split('/')[-1]
                try:
                    tool.run_logged([tool.docker_command(), 'run', '--rm', '--name', name, '--platform', platform,
                        '--network', 'none', '--entrypoint', 'sh', image_id, '-ec', runtime_check(target)],
                        history / 'logs' / f'test-{platform.split("/")[1]}.log', timeout_seconds=options.timeout)
                finally:
                    tool.run_logged([tool.docker_command(), 'rm', '-f', name], history / 'logs' / 'cleanup.log',
                                    check=False, timeout_seconds=options.timeout)
                report['tests'][platform] = {'status': 'passed', 'image_id': image_id, 'finished_at': tool.isoformat()}
                save()
            tag_args = [item for tag in tags for item in ('--tag', tag)]
            archive_path = history / 'image.oci.tar'
            tool.run_logged([*common, '--platform', ','.join(report['platforms']), *tag_args,
                             '--output', f'type=oci,dest={archive_path}', str(history)],
                            history / 'logs' / 'export.log', timeout_seconds=options.timeout)
            metadata = push.archive_metadata(archive_path, report['platforms'])
            for platform, descriptor in metadata['platforms'].items():
                config = metadata['manifests'][descriptor['digest']]['manifest']['config']['digest']
                if config != report['tests'][platform]['image_id']:
                    raise tool.DockerToolError('Exported base differs from its tested image')
            report.update(archive_sha256=tool.sha256_file(archive_path), digest=metadata['digest'])
            host = tool.run_logged([tool.docker_command(), 'info', '--format', '{{.Architecture}}'],
                                  history / 'logs' / 'host.log', timeout_seconds=options.timeout).stdout.strip()
            host_platform = tool.ARCHITECTURE_PLATFORMS.get(host)
            if host_platform in report['tests']:
                for tag in tags:
                    tool.run_logged([tool.docker_command(), 'image', 'tag', report['tests'][host_platform]['image_id'], tag],
                                    history / 'logs' / 'tags.log', timeout_seconds=options.timeout)
            report['status'] = 'passed'
    except KeyboardInterrupt:
        report.update(status='interrupted', error='Stopped by operator')
        raise
    except Exception as error:
        report.update(status='failed', error=str(error))
        raise
    finally:
        for tag in temporary_tags:
            try:
                tool.run_logged([tool.docker_command(), 'image', 'rm', tag], history / 'logs' / 'cleanup.log',
                                check=False, timeout_seconds=options.timeout)
            except (OSError, tool.DockerToolError) as error:
                report.setdefault('cleanup_errors', []).append(str(error))
        report['finished_at'] = tool.isoformat()
        save()
    print(f'{tool.log_timestamp()} PASSED {tags[0]}; digest {report["digest"]}; report {root / "report.json"}', flush=True)
    return 0
