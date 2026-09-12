"""Base-layer compatibility, architecture dispatch and dependency isolation."""
import dataclasses
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest import mock

from test_openriak_docker import docker_tool as tool
import bases.workflow as base
from builders_base import registry


def selected(name, profile='default'):
    args = ['base', 'refresh', '--base', name]
    if profile == 'custom':
        args += ['--namespace', 'tiotjp', '--vendor', 'TI Tokyo', '--source',
                 'https://github.com/TI-Tokyo/openriak-docs', '--url', 'https://www.tiot.jp/']
    return base.selected_targets(tool.parser().parse_args(args), tool)


def pins(targets):
    return {t.platform: {'pinned': tool.base_image_for(t, upstream=True) + '@sha256:' +
                        hashlib.sha256(t.platform.encode()).hexdigest()} for t in targets}


class BaseHierarchyTests(unittest.TestCase):
    def test_all_base_files_and_runtime_checks_match_before_refactor(self):
        expected = json.loads(Path(__file__).with_name('base-rendering-baseline.json').read_text())
        actual = {}
        with mock.patch.object(tool, 'docker_command', side_effect=AssertionError('No Docker during rendering')):
            for name in registry.catalogue()['releases']:
                for profile in ('default', 'custom'):
                    targets = selected(name, profile)
                    for group in [[t] for t in targets] + [targets]:
                        key = name + '/' + profile + '/' + ','.join(t.platform for t in group)
                        actual[key] = {
                            'dockerfile': hashlib.sha256(base.render(group, pins(group), tool).encode()).hexdigest(),
                            'runtime_checks': {t.platform: hashlib.sha256(base.runtime_check(t).encode()).hexdigest() for t in group}}
        self.assertEqual(actual, expected)

    def test_recipe_and_patch_changes_affect_only_their_release_chains(self):
        groups = {name: selected(name) for name in registry.catalogue()['releases']}
        original = tool.sha256_file
        before = {name: registry.dependencies(targets, tool) for name, targets in groups.items()}
        for suffix, families in [
                ('builders_base/debian/bookworm/common.py', {'debian'}),
                ('builders/debian/bookworm/backports.py', {'debian'}),
                ('builders_base/rhel/v9/common.py', {'rhel'}),
                ('builders_base/rpm.py', {'rhel', 'centos'}),
                ('builders_base/enterprise_linux/v9/common.py', {'rhel', 'centos'}),
                ('builders/pcre2.py', {'rhel', 'centos'})]:
            with mock.patch.object(tool, 'sha256_file', side_effect=lambda p: 'changed' if str(p).endswith(suffix) else original(p)):
                for name, targets in groups.items():
                    with self.subTest(source=suffix, base=name):
                        self.assertEqual(before[name] != registry.dependencies(targets, tool), targets[0].family in families)

    def test_architecture_hooks_are_resolved_for_each_platform(self):
        target = selected('debian-12')[0]
        arm = dataclasses.replace(target, package={**target.package, 'architecture': 'arm64'})
        original = registry.layers
        hook = registry.resolve(target)[0]['render_stage']
        override = SimpleNamespace(render_stage=lambda t, p, tool, ctx: hook(t, p, tool, ctx) + '# arm64 override\n',
                                   runtime_check=lambda t, ctx: 'arm64-only-check\n')
        with mock.patch.object(registry, 'layers', side_effect=lambda t: original(t) + ([override] if t.platform == 'linux/arm64' else [])):
            rendered = base.render([target, arm], pins([target, arm]), tool)
            self.assertEqual(rendered.count('# arm64 override'), 1)
            self.assertEqual(base.runtime_check(arm), 'arm64-only-check\n')
            self.assertIn('openssl verify', base.runtime_check(target))
        deps = registry.dependencies([arm], tool)
        self.assertIsNone(deps['builders_base/debian/bookworm/arm64.py'])

    def test_mixed_os_and_mutable_pins_are_rejected(self):
        targets = [selected('debian-12')[0], selected('rhel-9')[0]]
        with self.assertRaisesRegex(tool.DockerToolError, 'one OS release'):
            base.render(targets, pins(targets), tool)
        with self.assertRaisesRegex(tool.DockerToolError, 'immutable'):
            base.render(targets[:1], {targets[0].platform: {'pinned': 'example:mutable'}}, tool)
