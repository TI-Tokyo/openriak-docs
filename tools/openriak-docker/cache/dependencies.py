"""Per-target build inputs and byte-verified compatibility with legacy approvals."""
import dataclasses
import hashlib
import inspect
import json
from pathlib import Path
import tempfile
from builders import registry

ROOT = Path(__file__).resolve().parents[1]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def sources(tool, targets):
    paths = {ROOT / 'images/rendering.py', ROOT / 'builders/registry.py'}
    for target in targets:
        paths.update(registry.dependencies(target))
        paths.update(ROOT / 'runtime' / name for name in ('entrypoint.sh', 'healthcheck.sh'))
        mode = tool.minimal.configuration(target)
        if mode:
            paths.add(ROOT / 'images/minimal.py')
            if mode.get('openssl_backport') or mode.get('libblkid_backport'):
                paths.add(ROOT / 'builders/debian/bookworm/backports.py')
    result = {str(p.relative_to(ROOT)): tool.sha256_file(p) if p.is_file() else None for p in sorted(paths)}
    result['shared:target-model-and-hostname'] = digest([inspect.getsource(x) for x in (tool.Target, tool.default_node_host)])
    return result


def inputs(tool, targets, cluster_nodes, tags):
    dependencies = sources(tool, targets)
    return {
        'schema_version': tool.MULTIARCH_SCHEMA_VERSION,
        'identity': dataclasses.asdict(targets[0].identity),
        'lifecycle_options': dataclasses.asdict(targets[0].lifecycle_options),
        'labels': tool.image_labels(targets[0]),
        'runtime_options': {k: list(v) for k, v in tool.RUNTIME_OPTIONS.items()},
        'compose_options': {k: list(v) for k, v in tool.COMPOSE_OPTIONS.items()},
        'cluster_nodes': cluster_nodes, 'tags': tags,
        'packages': {t.platform: {'url': t.package['url'], 'checksum': t.package['checksum'], 'base': tool.base_image_for(t)} for t in targets},
        'runtime_sha256': hashlib.sha256((tool.ENTRYPOINT_SCRIPT + tool.HEALTHCHECK_SCRIPT).encode()).hexdigest(),
        'runtime_filesystem': tool.minimal.configuration(targets[0]),
        'runtime_renderer_sha256': digest({k: v for k, v in dependencies.items() if 'minimal' in k or 'backports' in k}),
        'renderer_sha256': digest(dependencies),
        'build_dependencies': dependencies,
        'repository_setup': {t.platform: tool.debian_repository_setup(t) for t in targets},
        'setting_comments': tool.SETTING_COMMENTS,
    }


def matches(tool, targets, report, expected):
    previous = report.get('inputs', {})
    if previous == expected:
        return True
    if 'build_dependencies' in previous and not relocation_matches(previous, expected):
        return False
    # Old fingerprints covered unrelated OS code and omitted some helpers.
    # Accept them only when substantive inputs AND every rendered byte agree.
    ignored = {'renderer_sha256', 'runtime_renderer_sha256', 'build_dependencies', 'repository_setup', 'setting_comments'}
    if {k: v for k, v in previous.items() if k not in ignored} != {k: v for k, v in expected.items() if k not in ignored}:
        return False
    if not report.get('base_images') or not report.get('distributed_cookie'):
        return False
    try:
        with tempfile.TemporaryDirectory(prefix='openriak-approval-compare-') as directory:
            root = Path(directory)
            tool.render_group_assets(targets, report['base_images'], report['distributed_cookie'],
                                     expected['tags'], expected['cluster_nodes'], root)
            return all((targets[0].group_directory / name).is_file()
                       and (root / name).read_bytes() == (targets[0].group_directory / name).read_bytes()
                       for name in tool.ARTIFACT_FILENAMES)
    except (KeyError, ValueError, OSError):
        return False


def relocation_matches(previous, expected):
    """Recognise only explicitly recorded, byte-verified source relocations."""
    path = ROOT / 'config/refactor-compatibility.json'
    if not path.is_file():
        return False
    mappings = json.loads(path.read_text())
    translated = dict(previous)
    for key, mapping in (('renderer_sha256', 'renderers'), ('runtime_renderer_sha256', 'runtime_renderers')):
        translated[key] = mappings[mapping].get(previous.get(key), previous.get(key))
    old = digest(previous.get('build_dependencies'))
    new = digest(expected.get('build_dependencies'))
    if mappings['dependency_sets'].get(old) != new:
        return False
    translated['build_dependencies'] = expected['build_dependencies']
    return translated == expected
