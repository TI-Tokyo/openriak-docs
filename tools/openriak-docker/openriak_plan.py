"""Single read-only decision engine used by preview, execution and workers."""
import json
from openriak_dependencies import matches as input_matches

INPUT_NAMES = {
    'runtime_sha256': 'Startup/healthcheck code',
    'renderer_sha256': 'Dockerfile/Compose/environment generator code',
    'schema_version': 'Cache schema',
    'cluster_nodes': 'Cluster size',
    'identity': 'Image identity',
    'labels': 'Image labels',
    'runtime_options': 'Runtime defaults/comments',
    'compose_options': 'Compose defaults/comments',
    'packages': 'Package/base-image selection',
    'tags': 'Image tags',
    'build_dependencies': 'Build dependency',
    'repository_setup': 'Repository setup',
}


def display(value):
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return text if len(text) <= 180 else text[:177] + '...'


def input_changes(previous, expected):
    changes = []
    for key in sorted(set(previous) | set(expected)):
        old, new = previous.get(key), expected.get(key)
        if old == new and (key in previous) == (key in expected):
            continue
        label = INPUT_NAMES.get(key, key)
        if key.endswith('_sha256'):
            changes.append(f'{label} changed: {str(old)[:12]} -> {str(new)[:12]}')
        elif isinstance(old, dict) and isinstance(new, dict):
            for name in sorted(set(old) | set(new)):
                if old.get(name) != new.get(name):
                    changes.append(f'{label} [{name}] changed: {display(old.get(name))} -> {display(new.get(name))}')
        else:
            changes.append(f'{label} changed: {display(old)} -> {display(new)}')
    return changes


def evaluate(tool, targets, options, all_targets):
    target = targets[0]
    root = target.group_directory
    path = root / 'report.json'
    report = tool.read_json(path) if path.is_file() else {}
    if getattr(options, "do_not_test", False):
        if report.get('status') != 'passed':
            return {'action': 'SKIP', 'reasons': ['No passed group approval for --do-not-test'], 'platforms': []}
        approval = tool.approved_group_report(targets)
        tags = tool.namespaced_tags(approval['tags'], options.extra_namespace)
        return {'action': 'REBUILD', 'reasons': [
            '--do-not-test: rebuild the approved saved files; no regeneration or tests',
            'Apply tags: ' + ', '.join(tags)],
            'platforms': [(t.platform, 'REBUILD', 'approved Dockerfile; tests disabled') for t in targets]}

    tags = tool.image_aliases(target, all_targets)
    inputs = tool.group_input(targets, options.cluster_nodes, tags)
    # Use the real skip predicate, including its full input fingerprint comparison.
    passed = tool.group_is_passed(targets, report, inputs)
    if passed and not options.force:
        return {'action': 'SKIP', 'reasons': ['Complete passed cache; inputs and all artifact checksums match'],
                'platforms': [(t.platform, 'SKIP', 'passed group approval') for t in targets], 'reuse_artifacts': True}

    reasons = []
    if options.force:
        reasons.append('--force requested: pull fresh release digests, regenerate, rebuild and retest every platform')
    if not report:
        reasons.append('No cached group report')
    else:
        if report.get('status') != 'passed':
            reasons.append(f'Cached group status: {report.get("status", "missing")}')
            if report.get('error'):
                reasons.append('Previous error: ' + display(report['error']))
        reasons.extend(input_changes(report.get('inputs', {}), inputs))
        results = report.get('platform_results', {})
        for platform in sorted({t.platform for t in targets} | set(results)):
            if platform not in {t.platform for t in targets}:
                reasons.append(f'{platform}: no longer in the selected package group')
            elif results.get(platform, {}).get('status') != 'passed':
                reasons.append(f'{platform}: cached result is {results.get(platform, {}).get("status", "missing")}')
        artifacts = report.get('artifacts', {})
        if len(artifacts) != len(tool.ARTIFACT_FILENAMES):
            reasons.append('Group artifact approval is incomplete')
        for artifact in artifacts.values():
            filename = artifact['filename']
            if not (root / filename).is_file():
                reasons.append(f'Missing cached file: {filename}')
            elif tool.sha256_file(root / filename) != artifact['sha256']:
                reasons.append(f'Cached file content changed: {filename} (SHA-256 differs from approval)')

    if report and not (options.force or options.retry_failed):
        return {'action': 'BLOCKED', 'reasons': reasons + ['Requires --retry-failed or --force'], 'platforms': []}

    # Mirror refresh_group's partial retry rule: only identical shared files can
    # reuse passed platforms. Regeneration creates a fresh cookie and new bytes.
    reusable = (
        input_matches(tool, targets, report, inputs) and not options.force
        and set(report.get('base_images', {})) == {t.platform for t in targets}
        and bool(report.get('distributed_cookie'))
        and all((root / name).is_file() and tool.sha256_file(root / name) == report.get('generated_artifacts', {}).get(name)
                for name in tool.ARTIFACT_FILENAMES)
    )
    if not reusable:
        reasons.append('Pull release tags and regenerate shared files; rebuild and test all platforms')
    else:
        reasons.append('Reuse saved base digests and shared files; retain matching passed platforms')
    platforms = []
    for platform_target in targets:
        state, detail = tool.cache_state(platform_target, options.cluster_nodes)
        matches = state == 'valid' and all(
            (root / name).is_file() and tool.sha256_file(platform_target.cache_directory / name) == tool.sha256_file(root / name)
            for name in tool.ARTIFACT_FILENAMES)
        if reusable and matches:
            platforms.append((platform_target.platform, 'SKIP', 'same shared files already passed'))
        else:
            why = 'shared files will be regenerated' if not reusable else (detail or 'no matching platform approval')
            platforms.append((platform_target.platform, 'REBUILD + TEST', why))
    reasons.append('Export OCI image and apply tags after all platform tests pass')
    return {'action': 'REBUILD', 'reasons': reasons, 'platforms': platforms, 'reuse_artifacts': reusable}

