"""Resolve optional build layers from generic through architecture-specific.

Each layer may expose configure(tool, target, context), repositories(tool, target),
or a package-stage hook. No layer builds images or invokes Docker itself.
"""
from importlib import import_module
from pathlib import Path
import re

ROOT = Path(__file__).parent


def layer_names(target):
    family = target.family.replace('-', '_')
    release = ({'11': 'bullseye', '12': 'bookworm'}.get(target.release)
               if family == 'debian' else None)
    release = release or 'v' + target.release.replace('-', '_').replace('.', '_')
    arch = target.platform.removeprefix('linux/').replace('/', '_')
    package = target.operating_system['package_family']
    if any(not re.fullmatch(r'[a-zA-Z_][a-zA-Z_0-9]*', value)
           for value in (family, release, arch, package)):
        raise ValueError('Invalid build layer identifier in target metadata')
    return ['common', package, f'{family}.common', f'{family}.{release}.common',
            f'{family}.{release}.{arch}']


def paths(target):
    # Include absent optional layers, so adding an override invalidates its targets.
    return [ROOT / (name.replace('.', '/') + '.py') for name in layer_names(target)]


def layers(target):
    return [import_module('builders.' + name) for name, path in zip(layer_names(target), paths(target))
            if path.is_file()]


def repositories(tool, target):
    result = ''
    for layer in layers(target):
        if hasattr(layer, 'repositories'):
            result = layer.repositories(tool, target)
    return result


def install(tool, target):
    filename = target.package['filename']
    if not re.fullmatch(r'[A-Za-z0-9_.+-]+', filename):
        raise tool.DockerToolError(f'Unsafe package filename in metadata: {filename}')
    context = {'package_path': '/tmp/' + filename}
    renderer = None
    for layer in layers(target):
        if hasattr(layer, 'configure'):
            layer.configure(tool, target, context)
        renderer = getattr(layer, 'install', renderer)
    if renderer is None:
        raise tool.DockerToolError(f'Unsupported package family: {target.operating_system["package_family"]}')
    return renderer(tool, target, context)


def minimal_setup(minimal, target, pinned, stage, mode):
    result = ('', '', '', '')
    for layer in layers(target):
        if hasattr(layer, 'prepare_minimal'):
            result = layer.prepare_minimal(minimal, target, pinned, stage, mode)
    return result


def minimal_repositories(target, install_script):
    result = ''
    for layer in layers(target):
        if hasattr(layer, 'minimal_repositories'):
            result = layer.minimal_repositories(target, install_script)
    return result


def dependencies(target):
    """Track layer files, package initializers and statically imported build helpers.

    Dynamically selected helpers can additionally declare BUILD_DEPENDENCIES as
    paths relative to the declaring module. Dependencies stay inside this tool.
    """
    import ast
    pending = list(paths(target))
    tool_root = ROOT.parent.resolve()
    for layer in layers(target):
        for name in getattr(layer, 'BUILD_DEPENDENCIES', ()):
            dependency = (Path(layer.__file__).parent / name).resolve()
            if not dependency.is_relative_to(tool_root):
                raise ValueError('Build dependency escapes the tool directory')
            pending.append(dependency)
    found = set()
    while pending:
        path = pending.pop()
        if path in found:
            continue
        found.add(path)
        if not path.is_file():
            continue
        for parent in path.parents:
            if parent == ROOT.parent:
                break
            initializer = parent / '__init__.py'
            if initializer.is_file() and initializer != path:
                pending.append(initializer)
        module = '.'.join(path.relative_to(ROOT.parent).with_suffix('').parts)
        for node in ast.walk(ast.parse(path.read_text())):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                prefix = node.module or ''
                if node.level:
                    prefix = '.'.join(module.split('.')[:-node.level]) + ('.' + prefix if prefix else '')
                names = [prefix] + [prefix + '.' + alias.name for alias in node.names]
            for name in names:
                if name.startswith('builders.'):
                    candidate = ROOT.parent / (name.replace('.', '/') + '.py')
                    if candidate.is_file():
                        pending.append(candidate)
    return found
