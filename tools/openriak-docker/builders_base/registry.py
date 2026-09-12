"""Select base recipes through the same generic-to-architecture hierarchy as KV."""
import ast
from importlib import import_module
import json
from pathlib import Path
import re

from builders.registry import layer_names

ROOT = Path(__file__).parent
CONFIG_PATH = ROOT.parent / 'config/builders-base.json'


def catalogue():
    config = json.loads(CONFIG_PATH.read_text())
    if config.get('schema_version') != 1 or not isinstance(config.get('releases'), dict):
        raise ValueError('Invalid builders-base.json catalogue')
    if config.get('default') not in config['releases']:
        raise ValueError('Base default must name a configured release')
    for name, entry in config['releases'].items():
        if (not re.fullmatch(r'[a-z0-9][a-z0-9.-]*', name) or not isinstance(entry, dict)
                or any(not isinstance(entry.get(key), str) or not entry[key] for key in ('family', 'release'))):
            raise ValueError('Base releases require a selector, family and release')
    return config


def paths(target):
    return [ROOT / (name.replace('.', '/') + '.py') for name in layer_names(target)]


def layers(target):
    return [import_module('builders_base.' + name) for name, path in zip(layer_names(target), paths(target))
            if path.is_file()]


def resolve(target):
    context, hooks = {}, {}
    for layer in layers(target):
        if hasattr(layer, 'configure'):
            layer.configure(target, context)
        for name in ('render_header', 'render_stage', 'render_footer', 'runtime_check'):
            if hasattr(layer, name):
                hooks[name] = getattr(layer, name)
    missing = {'render_header', 'render_stage', 'render_footer', 'runtime_check'} - hooks.keys()
    if missing:
        raise ValueError(f'Incomplete base recipe for {target.family} {target.release}: {", ".join(sorted(missing))}')
    return hooks, context


def render(targets, bases, tool):
    if not targets:
        raise tool.DockerToolError('Base rendering requires at least one metadata target')
    reference = targets[0]
    if any((t.family, t.release, t.identity) != (reference.family, reference.release, reference.identity)
           for t in targets) or len({t.platform for t in targets}) != len(targets):
        raise tool.DockerToolError('A reusable base must contain one OS release/identity and distinct platforms')
    stages, header, footer = [], None, None
    for target in targets:
        pinned = bases[target.platform]['pinned']
        if not re.search(r'@sha256:[0-9a-f]{64}$', pinned):
            raise tool.DockerToolError('Patched bases require immutable upstream image digests')
        hooks, context = resolve(target)
        prefix = hooks['render_header'](target, tool, context)
        suffix = hooks['render_footer'](target, tool, context)
        if header is not None and (prefix, suffix) != (header, footer):
            raise tool.DockerToolError('Base architecture layers must share the same header and final labels')
        header, footer = prefix, suffix
        stages.append(hooks['render_stage'](target, pinned, tool, context))
    return header + ''.join(stages) + footer


def runtime_check(target):
    hooks, context = resolve(target)
    return hooks['runtime_check'](target, context)


def dependencies(targets, tool):
    """Hash selected/absent layers and imported recipe helpers, isolated by release."""
    tool_root = ROOT.parent.resolve()
    pending = [Path(__file__)]
    for target in targets:
        pending.extend(paths(target))
    found = set()
    while pending:
        path = pending.pop().resolve()
        if not path.is_relative_to(tool_root):
            raise ValueError('Base build dependency escapes the tool directory')
        if path in found:
            continue
        found.add(path)
        if not path.is_file():
            continue
        for parent in path.parents:
            if parent == tool_root:
                break
            initializer = parent / '__init__.py'
            if initializer.is_file():
                pending.append(initializer)
        # Shared infrastructure is hashed as a whole. Its unrelated OS imports
        # are not recipe dependencies (e.g. minimal's legacy Debian aliases).
        if not path.is_relative_to(ROOT.resolve()) and not path.is_relative_to(tool_root / 'builders'):
            continue
        module = '.'.join(path.relative_to(tool_root).with_suffix('').parts)
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'BUILD_DEPENDENCIES' for t in node.targets):
                for name in ast.literal_eval(node.value):
                    pending.append(path.parent / name)
            names = []
            if isinstance(node, ast.Import):
                names = [item.name for item in node.names]
            elif isinstance(node, ast.ImportFrom):
                prefix = node.module or ''
                if node.level:
                    prefix = '.'.join(module.split('.')[:-node.level]) + ('.' + prefix if prefix else '')
                names = [prefix] + [prefix + '.' + item.name for item in node.names]
            for name in names:
                if name.startswith(('builders_base.', 'builders.')):
                    candidate = tool_root / (name.replace('.', '/') + '.py')
                    if candidate.is_file():
                        pending.append(candidate)
    return {str(p.relative_to(tool_root)): tool.sha256_file(p) if p.is_file() else None for p in sorted(found)}
