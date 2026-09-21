"""Versioned CLI inventory from runtime registrations, launchers and locked sources."""
from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
import re

from .cli_runtime import inspect_runtime
from .cli_shell import inspect_script, option_tokens
from .source import SourceResolver


def identifier(path: list[str], context: str = "shell") -> str:
    return context + ":" + " ".join(path)


def entry(path: list[str], kind: str, provenance: dict) -> dict:
    return {"id": identifier(path), "path": path, "invocation": " ".join(path),
            "context": "shell", "kind": kind, "aliases": [], "deprecated": False,
            "removed": False, "hidden": False, "arguments": [], "options": [],
            "help": "", "help_sources": [], "provenance": [provenance],
            "variants": [], "subcommands": []}


def canonical(path: list[str]) -> list[str]:
    if path and path[0] == '_' and len(path) == 2 and path[1] in ('set', 'show', 'describe'):
        return ['riak', 'admin', path[1]]
    return ["riak", "admin", *path[1:]] if path and path[0] == "riak-admin" else path


def erlang_strings(source: str) -> str:
    strings = []
    for match in re.finditer(r'"(?:\\.|[^"\\])*"', source):
        try:
            value = json.loads(match[0])
        except ValueError:
            value = match[0][1:-1]
        strings.append(value.replace("~n", "\n"))
    return "".join(strings)


def source_modules(repositories: list) -> dict[str, dict]:
    modules = {}
    for repository in sorted(repositories, key=lambda r: getattr(r, 'dependency_depth', 0)):
        for path in sorted(repository.path.rglob("*.erl")):
            if not any(part in ("src", "escript") for part in path.relative_to(repository.path).parts):
                continue
            source = path.read_text(encoding="utf-8", errors="replace")
            match = re.search(r'-module\(\s*([a-zA-Z0-9_]+)\s*\)', source)
            if match:
                modules.setdefault(match[1], {"text": source, "repository": repository.repository,
                    "commit": repository.commit, "path": path.relative_to(repository.path).as_posix()})
    return modules


def callback_help(module: dict, function: str) -> str:
    candidates = related_functions(module, function)
    texts = []
    for candidate in candidates:
        for match in re.finditer(r'io:(?:format|put_chars)\(\s*((?:"(?:\\.|[^"\\])*"\s*)+)', candidate['source']):
            value = erlang_strings(match[1])
            if re.search(r'usage|options|arguments', value, re.I) or re.search(r'usage|help', candidate['name']):
                texts.append(value)
    return "\n".join(dict.fromkeys(texts))


def related_functions(module: dict, function: str) -> list[dict]:
    functions = module.get('functions', [])
    pending, seen, result = [function], set(), []
    while pending:
        name = pending.pop()
        if name in seen:
            continue
        seen.add(name)
        for defined in functions:
            if defined['name'] != name:
                continue
            result.append(defined)
            pending.extend(re.findall(r'(?<![:\w])([a-z]\w*)\(', defined['source']))
    return result


def documentation_index(docs: Path) -> tuple[dict, list]:
    shell, attach = {}, []
    for path in sorted(docs.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(docs).as_posix()
        for match in re.finditer(r'^```([^\n]*)\n(.*?)^```', text, re.M | re.S):
            language, code = match[1].strip(), match[2].strip()
            if language == 'riakattach' or (language in ('erlang', '') and 'riak attach' in text):
                attach.append({"path": relative, "line": text[:match.start()].count('\n') + 1,
                               "expression": code, "documentation": text})
            if language in ('bash', 'sh', 'shell', ''):
                for line in code.splitlines():
                    m = re.match(r'\s*(?:\$\s*)?(riak(?:-admin|-repl|-debug|-chkconfig)?)(\s+[a-z][\w-]*(?:\s+[a-z][\w-]*)*)?', line)
                    if m:
                        tokens = canonical(m[0].strip().removeprefix('$').split())
                        shell.setdefault(' '.join(tokens), []).append({"path": relative,
                            "line": text[:match.start()].count('\n') + 1, "example": line.strip()})
    return shell, attach


def source_help(source: str, function: str) -> str:
    lines = source.splitlines()
    for i, line in enumerate(lines):
        if re.match(r'(?:-spec\s+)?' + re.escape(function) + r'\s*\(', line):
            comments = []
            for previous in reversed(lines[:i]):
                if previous.lstrip().startswith('%'):
                    comments.append(re.sub(r'^\s*%+\s?', '', previous))
                elif previous.strip():
                    break
            if comments:
                return '\n'.join(reversed(comments)).strip()
    return ''


def erlang_calls(expression: str) -> list[tuple[str, str, int]]:
    """Count call arguments while respecting nested terms, binaries and strings."""
    calls = []
    for match in re.finditer(r'\b([a-z]\w*):([a-z]\w*)\s*\(', expression):
        depth, commas, tokens = 1, 0, []
        for token in re.finditer(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|<<|>>|[(){}\[\],]|[^\s]', expression[match.end():]):
            value = token[0]
            if value in ('(', '[', '{', '<<'):
                depth += 1
            elif value in (')', ']', '}', '>>'):
                depth -= 1
                if depth == 0:
                    calls.append((match[1], match[2], commas + 1 if tokens else 0))
                    break
            elif value == ',' and depth == 1:
                commas += 1
            tokens.append(value)
    return calls


def inspect_attach(examples: list, modules: dict, sources: dict) -> tuple[list[dict], list[dict]]:
    entries, checks = {}, []
    requested = {}
    for example in examples:
        for module, function, arity in erlang_calls(example['expression']):
            if module.startswith('riak'):
                requested.setdefault((module, function, arity), []).append(example)
    # The client is the supported interactive entry point. Include its exported
    # API, so newly introduced administrative operations need not already have
    # a page in the historical documentation to be discovered.
    for name in ('riak', 'riak_client'):
        for exported in modules.get(name, {}).get('exports', []):
            if exported['name'] != 'module_info':
                requested.setdefault((name, exported['name'], exported['arity']), [])
    for (module_name, function, arity), examples_for_call in sorted(requested.items()):
        runtime_module = modules.get(module_name, {})
        defined = next((f for f in runtime_module.get('functions', []) if f['name'] == function and f['arity'] == arity), None)
        exported = {'name': function, 'arity': arity} in runtime_module.get('exports', [])
        if runtime_module.get('missing') or not runtime_module:
            status = 'not_in_runtime'
        elif not exported:
            status = 'not_exported'
        elif not defined:
            status = 'missing_abstract_code'
        else:
            status = 'resolved'
        checks.append({'module': module_name, 'function': function, 'arity': arity, 'status': status,
                       'documentation': sorted(set(e['path'] for e in examples_for_call))})
        if status != 'resolved':
            continue
        key = f"{module_name}:{function}/{arity}"
        item = entry(['riak', 'attach', key], 'erlang_function',
                     {'kind': 'beam', 'module': module_name, 'sha256': runtime_module['sha256'], 'line': defined['line']})
        comment = source_help(sources.get(module_name, {}).get('text', ''), function)
        item.update(id='erlang:' + key, context='erlang', invocation=key,
                    module=module_name, function=function, arity=arity,
                    signatures=defined['heads'], specifications=defined['specs'],
                    examples=[], prerequisites=['Open an Erlang shell with riak attach or riak remote_console.'],
                    help=comment or callback_help(runtime_module, function),
                    implementation=defined['source'],
                    arguments=[{'position': i + 1} for i in range(arity)])
        item['deprecated'] = bool(re.search(r'@deprecated\b', comment, re.I))
        item['visibility'] = 'internal' if re.search(r'@private\b', comment) else 'public'
        item['hidden'] = item['visibility'] == 'internal'
        if comment:
            item['help_sources'].append({'kind': 'source_comment', 'text': comment})
        if module_name in sources:
            item['provenance'].append({k: v for k, v in sources[module_name].items() if k != 'text'})
        for example in examples_for_call:
            row = {k: example[k] for k in ('path', 'line', 'expression')}
            if row not in item['examples']:
                item['examples'].append(row)
        entries[key] = item
    aae = modules.get('riak_kv_clusteraae_fsm', {})
    for item in list(entries.values()):
        if item['module'] == 'riak_client' and item['function'] == 'aae_fold':
            item['argument_types'] = aae.get('types', [])
            selectors = sorted(set(q['selector'] for q in aae.get('query_forms', [])))
            for selector in selectors:
                child = dict(item)
                child.update(id=item['id'] + ':' + selector, kind='erlang_subcommand',
                             path=item['path'] + [selector], selector=selector,
                             specifications=[q['signature'] for q in aae['query_forms'] if q['selector'] == selector],
                             invocation=f"riak_client:aae_fold({{{selector}, ...}}" + (", Client)." if item['arity'] == 2 else ")."),
                             invocation_is_template=True,
                             examples=[ex for ex in item['examples'] if re.search(r'\{\s*' + re.escape(selector) + r'\s*[,}]', ex['expression'])],
                             subcommands=[])
                entries[child['id']] = child
                item['subcommands'].append(child['id'])
    return list(entries.values()), checks


def auxiliary_commands(runtime: dict) -> tuple[list[dict], list[dict], list[str]]:
    commands, scripts, warnings = [], [], []
    for name, script in runtime['scripts'].items():
        proof = {'kind': 'runtime_script', 'path': script['path'], 'sha256': script['sha256']}
        if name == 'cf_config':
            scripts.append({'name': name, 'role': 'configuration_hook', 'provenance': proof})
            continue
        if re.fullmatch(r'riak-\d.*', name):
            scripts.append({'name': name, 'role': 'versioned_launcher', 'provenance': proof})
            if script['sha256'] != runtime['scripts'].get('riak', {}).get('sha256'):
                warnings.append('Versioned launcher differs from riak: ' + name)
            continue
        if name == 'riak' or name.startswith('riak-'):
            continue
        text = script['text']
        item = entry([name], 'auxiliary', proof)
        item['invocation'] = script['path']
        item['hidden'] = True
        item['prerequisites'] = ['Bundled release helper; normally invoked by the Riak launcher.']
        if name == 'cuttlefish':
            module = next((m for m in runtime['modules'] if m['module'] == 'cuttlefish_escript'), {})
            main = next((f['source'] for f in module.get('functions', []) if f['name'] == 'main'), '')
            selectors = re.findall(r'^        ([a-z]\w*) ->', main, re.M)
            item['options'] = [{**o, 'name': '--' + o['name'], 'short': '-' + o['short'] if o.get('short') else None}
                               for o in runtime.get('cuttlefish_options', [])]
            item['help'] = '\n'.join(o['name'] + ': ' + o['description'] for o in item['options'])
            if module.get('sha256'):
                item['provenance'].append({'kind': 'beam', 'module': 'cuttlefish_escript', 'sha256': module['sha256']})
            item['implementation'] = main
            if not item['options'] or not selectors:
                warnings.append('Cannot inspect cuttlefish command/option declaration')
        elif name == 'nodetool':
            dispatch = re.search(r'case RestArgs of(.*?)\n    end,', text, re.S)
            selectors = re.findall(r'\["([a-z]\w*)"', dispatch[1] if dispatch else '')
            item['options'] = [{'name': m[1], 'value_name': m[2], 'source': 'dispatcher'} for m in
                               re.finditer(r'process_args\(\["(-[\w-]+)", (\w+)', text)]
            item['help'] = '\n'.join(re.findall(r'io:format\("(Usage:[^"\n]+)', text)).replace('~n', '\n')
            item['implementation'] = text
            item['deprecated'] = 'will be removed' in text
            item['prerequisites'].append('Not used by relx on OTP 23 and later; erl_call is used instead.')
        elif name == 'install_upgrade.escript':
            dispatch = re.search(r'case Command0 of(.*?)\n    end,', text, re.S)
            selectors = re.findall(r'"([a-z]\w*)" ->', dispatch[1] if dispatch else '')
            item['options'] = [{'name': o, 'source': 'dispatcher'} for o in
                               re.findall(r'parse_arguments\(\["(--[\w-]+)"', text)]
            item['arguments'] = [{'name': 'Command'}, {'name': 'DistInfoStr', 'format': 'Erlang distribution tuple'},
                                 {'name': 'Version', 'optional': True}]
            item['implementation'] = text
        else:
            warnings.append('Uninspected release executable: ' + name)
            scripts.append({'name': name, 'role': 'uninspected', 'provenance': proof})
            continue
        commands.append(item)
        for selector in sorted(set(selectors)):
            child = dict(item)
            child.update(id=identifier([name, selector]), path=[name, selector],
                         invocation=script['path'] + ' ' + selector, subcommands=[])
            commands.append(child)
        if not selectors:
            warnings.append('No dispatch found for auxiliary executable: ' + name)
        scripts.append({'name': name, 'role': 'auxiliary', 'provenance': proof})
    return commands, scripts, warnings


def lifecycle_variants(root, commands: dict) -> list[dict]:
    variants = []
    definitions = [
        ('openrc', ['alpine'], 'rel/pkg/alpine/abuild/riak.initd'),
        ('systemd', ['debian', 'ubuntu', 'raspbian'], 'rel/pkg/deb/debian/riak.riak.service'),
        ('systemd', ['rhel', 'centos', 'rocky', 'oracle-linux', 'amazon-linux', 'fedora', 'sles'], 'rel/pkg/rpm/riak.service'),
        ('rc.d', ['freebsd'], 'rel/pkg/fbsdng/rc.d'),
    ]
    for manager, families, relative in definitions:
        path = root.path / relative
        if not path.is_file():
            continue
        content = path.read_text(encoding='utf-8')
        for action in ('start', 'stop', 'restart', 'status'):
            invocation = (f'rc-service riak {action}' if manager == 'openrc' else
                          f'systemctl {action} riak' if manager == 'systemd' else f'service riak {action}')
            variants.append({"action": action, "os_families": families, "service_manager": manager,
                "invocation": invocation, "requires": [f"Riak {manager} service installed", "service manager running", "service management privileges"],
                "provenance": {"repository": root.repository, "commit": root.commit, "path": relative,
                               "sha256": hashlib.sha256(content.encode()).hexdigest()},
                "service_definition": content})
    # Direct invocation is a deployment-context choice, not a universal OS rule.
    for action, direct in (('start', 'daemon'), ('stop', 'stop'), ('restart', 'restart'), ('status', 'ping')):
        if identifier(['riak', direct]) in commands:
            variants.append({"action": action, "os_families": ['*'], "service_manager": 'direct',
                "invocation": f'riak {direct}', "requires": ['Riak executable on PATH', 'run as the Riak service user'],
                "provenance": commands[identifier(['riak', direct])]['provenance'][0]})
    return variants


def build_inventory(version: str, runtime: dict, root, repositories: list, docs: Path,
                    source_warnings: list[str] | None = None) -> dict:
    warnings = list(source_warnings or [])
    commands = {}
    modules = {m['module']: m for m in runtime['modules']}
    sources = source_modules(repositories)
    for result in runtime['registrations']:
        if result['status'] != 'ok':
            warnings.append(f"Clique registration failed: {result['module']}: {result.get('error')}")
    if not runtime['commands']:
        warnings.append('Runtime exposed no Clique commands')
    for name, module in modules.items():
        if not module.get('missing') and not module.get('source'):
            warnings.append('Missing runtime abstract code: ' + name)
    for spec in runtime['commands']:
        path = canonical(spec['path'])
        item = entry(path, 'clique', {"kind": 'clique_registry', "image_id": runtime['image']['id'],
                                    "registered_path": spec['path'], "callback": spec['callback']})
        help_text = spec['help'].replace('Usage: _ ', 'Usage: riak-admin ')
        item.update(arguments=spec['arguments'], options=spec['options'], help=help_text)
        item['argument_format'] = 'key=value'
        item['wildcard_path'] = '*' in path
        item['options'] = [{**o, 'name': '--' + o['name'],
                            'short': '-' + o['short'] if o.get('short') else None}
                           if 'name' in o else o for o in item['options']]
        item['help_sources'].append({"kind": 'clique_usage', "text": help_text})
        if path[:2] == ['riak', 'admin']:
            item['aliases'].append({"invocation": ' '.join(['riak-admin', *path[2:]]), "deprecated": False})
        item['global_options'] = [{"name": '--help', "short": '-h'}, {"name": '--format', "value_name": 'FORMAT'}]
        if any('unsupported_spec' in option for option in spec['options']):
            warnings.append('Unsupported Clique option specification: ' + item['invocation'])
        commands[item['id']] = item
    for usage in runtime['usage']:
        path = canonical(usage['path'])
        key = identifier(path)
        if key not in commands:
            item = entry(path, 'command_group', {"kind": 'clique_usage', "image_id": runtime['image']['id']})
            item['help'] = usage['help']
            commands[key] = item
    inspected_scripts = []
    for required in ('riak', 'riak-admin'):
        if required not in runtime['scripts']:
            warnings.append('Missing release launcher: ' + required)
    for name, script in runtime['scripts'].items():
        if name == 'riak' or (name.startswith('riak-') and not re.fullmatch(r'riak-\d.*', name)):
            prefix = ['riak'] if name == 'riak' else ['riak', name.removeprefix('riak-')]
            discovered, gaps = inspect_script(name, script['text'], prefix)
            warnings.extend(gaps)
            inspected_scripts.append(name)
            for found in discovered:
                path, key = found['path'], identifier(found['path'])
                proof = {"kind": 'runtime_script', "path": script['path'], "sha256": script['sha256'], "line": found['line']}
                item = commands.setdefault(key, entry(path, 'shell', proof))
                if proof not in item['provenance']:
                    item['provenance'].append(proof)
                item['deprecated'] |= found['deprecated']
                item['removed'] |= found['removed']
                if found.get('unavailable_reason'):
                    item['availability'] = 'unavailable'
                    item['unavailable_reason'] = found['unavailable_reason']
                item['aliases'].extend({"invocation": ' '.join(alias), "deprecated": found['deprecated']} for alias in found['aliases'])
                if name != 'riak':
                    item['aliases'].append({"invocation": ' '.join([name, *path[2:]]), "deprecated": found['deprecated']})
                text = found['help']
                for handler in found['handlers']:
                    module = modules.get(handler['module'], {})
                    exported = [e for e in module.get('exports', []) if e['name'] == handler['function']]
                    if not exported and handler['module'].startswith('riak'):
                        item['availability'] = 'unavailable'
                        item['unavailable_reason'] = 'Missing runtime handler ' + handler['module'] + ':' + handler['function']
                    related = related_functions(module, handler['function'])
                    item.setdefault('handlers', []).append({**handler, 'functions': related})
                    text += '\n' + callback_help(module, handler['function'])
                    # Literal flag comparisons also reveal unadvertised options.
                    for defined in related:
                        item['options'].extend({'name': flag, 'source': 'dispatcher'} for flag in
                            re.findall(r'"(--?[a-zA-Z][\w-]*)"', defined['source']))
                    # Legacy console functions dispatch additional string arguments.
                    for defined in module.get('functions', []):
                        if defined['name'] != handler['function']:
                            continue
                        item.setdefault('handler_signatures', []).extend(defined['heads'])
                        for head in defined['heads']:
                            m = re.match(re.escape(handler['function']) + r'\(\["([a-z][\w-]*)"', head)
                            if m and handler['function'] != 'command':
                                child_path = path + [m[1]]
                                child = commands.setdefault(identifier(child_path), entry(child_path, 'console_dispatch',
                                    {"kind": 'beam', "module": handler['module'], "sha256": module['sha256'], "line": defined['line']}))
                                child['help'] = callback_help(module, handler['function'])
                                child['signatures'] = defined['heads']
                                child['options'] = option_tokens(child['help'])
                                child['deprecated'] = found['deprecated']
                text = text.strip()
                if text:
                    item['help_sources'].append({"kind": 'shell_and_console_usage', "text": text})
                    if not item['help']:
                        item['help'] = text
                    item['options'].extend(option_tokens(text))
                item['options'].extend(found['options'])
                item['dispatch_source'] = found['dispatch_source']
    auxiliary, auxiliary_scripts, gaps = auxiliary_commands(runtime)
    warnings.extend(gaps)
    for item in auxiliary:
        commands[item['id']] = item
    # The release scripts themselves identify installed extension entry points.
    launcher = runtime['scripts'].get('riak', {}).get('text', '')
    extensions = re.search(r'^EXTENSIONS="([^"]+)"', launcher, re.M)
    if extensions:
        for extension in extensions[1].split('|'):
            if extension != 'undefined' and 'riak-' + extension not in runtime['scripts']:
                warnings.append('Missing installed launcher extension: ' + extension)
    shell_docs, attach_docs = documentation_index(docs)
    attached, attach_checks = inspect_attach(attach_docs, modules, sources)
    for check in attach_checks:
        if check['status'] == 'missing_abstract_code' or (check['status'] == 'not_in_runtime'
                and check['module'] in runtime.get('available_modules', [])):
            warnings.append('Uninspected attach function: ' + check['module'] + ':' + check['function'])
    if any(i.get('function') == 'aae_fold' for i in attached) and not modules.get('riak_kv_clusteraae_fsm', {}).get('query_forms'):
        warnings.append('Could not resolve AAE query type union')
    for item in attached:
        commands[item['id']] = item
    for item in commands.values():
        if item['context'] == 'shell':
            item['documentation_examples'] = shell_docs.get(item['invocation'], [])
        item['help_status'] = 'available' if item['help'] else 'not_provided'
        item['usage'] = [line.strip() for line in item['help'].splitlines() if re.match(r'\s*usage\b', line, re.I)]
        if item['context'] == 'shell' and not item['arguments']:
            item['arguments'] = [{'name': name, 'source': 'usage_placeholder'} for name in
                dict.fromkeys(re.findall(r'<([\w .-]+)>', '\n'.join(item['usage'])))]
        item['options'] = list({json.dumps(v, sort_keys=True): v for v in item['options']}.values())
        item['aliases'] = list({json.dumps(v, sort_keys=True): v for v in item['aliases']}.values())
    # Record the type and implementation text needed to render attach argument
    # references and to audit options not expressed by the old help printers.
    argument_types = {name: module.get('types', []) for name, module in modules.items() if module.get('types')}
    for item in commands.values():
        if item['context'] == 'shell':
            item['subcommands'] = sorted(other['id'] for other in commands.values()
                if other['context'] == 'shell' and len(other['path']) == len(item['path']) + 1
                and other['path'][:-1] == item['path'])
        item.setdefault('availability', 'removed' if item['removed'] else
                        'help_only' if item['kind'] == 'command_group' and not item['subcommands'] else 'available')
    service_variants = lifecycle_variants(root, commands)
    for item in commands.values():
        if item['path'] in (['riak', 'start'], ['riak', 'daemon'], ['riak', 'stop'], ['riak', 'restart'], ['riak', 'ping']):
            action = {'daemon': 'start', 'ping': 'status'}.get(item['path'][-1], item['path'][-1])
            item['variants'] = [v for v in service_variants if v['action'] == action]
    package_version = None
    for package in (runtime.get('apk_database') or '').split('\n\n'):
        if re.search(r'^P:riak$', package, re.M):
            match = re.search(r'^V:(.+)$', package, re.M)
            if match:
                package_version = match[1]
    for package in (runtime.get('dpkg_database') or '').split('\n\n'):
        if re.search(r'^Package: (?:openriak|riak)$', package, re.M):
            match = re.search(r'^Version: (.+)$', package, re.M)
            if match:
                package_version = match[1].split(':')[-1]
    if package_version and not re.match(re.escape(version) + r'(?:[.\-]|$)', package_version):
        raise ValueError(f'Runtime package {package_version} does not match requested {version}')
    if not package_version and not runtime['image'].get('version_label'):
        warnings.append('Runtime version could not be verified from package metadata or image labels')
    if not attached:
        warnings.append('No documented attach commands could be resolved against the runtime')
    return {"schema_version": 1, "product": 'kv', "version": version,
        "status": 'partial' if warnings else 'complete', "warnings": sorted(set(warnings)),
        "source": {"repository": root.repository, "ref": 'riak-' + version, "commit": root.commit},
        "runtime": {**runtime['image'], "otp_release": runtime['otp_release'], "package_version": package_version,
                    "os_release": runtime.get('os_release'), "probe": 'isolated-registration-vm'},
        "commands": sorted(commands.values(), key=lambda c: c['id']),
        "service_variants": service_variants, "argument_types": argument_types,
        "coverage": {"registrations": runtime['registrations'], "scripts": inspected_scripts,
                     "auxiliary_scripts": auxiliary_scripts,
                     "clique_commands": len(runtime['commands']), "attach_checks": attach_checks,
                     "documentation_root": 'content/riak-kv/3.2.5-new-release',
                     "documentation_commands": sorted(shell_docs),
                     "documentation_checks": [{"invocation": invocation,
                         "status": 'resolved_prefix' if any(invocation == c['invocation'] or
                            (not c['subcommands'] and invocation.startswith(c['invocation'] + ' '))
                            for c in commands.values() if c['context'] == 'shell' and len(c['path']) > 1) else 'not_in_runtime'}
                            for invocation in sorted(shell_docs)],
                     "scope": 'installed Riak launchers, bundled helpers, Clique registry, console dispatch, exported riak/riak_client functions and documented attach operations'},
        "repositories": [{"name": r.name, "repository": r.repository, "commit": r.commit} for r in repositories]}


def generate_cli_commands(args, docs_root: Path) -> dict:
    logging.info('Inspecting CLI runtime for KV %s', args.version)
    docs = docs_root / 'content/riak-kv/3.2.5-new-release'
    if not docs.is_dir():
        raise ValueError(f'CLI discovery documentation not found: {docs}; use --docs-root PATH')
    _, attach = documentation_index(docs)
    extra_modules = sorted(set(m for ex in attach for m in re.findall(r'\b(riak\w*):\w+\(', ex['expression'])))
    runtime = inspect_runtime(args.version, args.runtime_image, refresh=args.refresh, extra_modules=extra_modules)
    resolver = SourceResolver(args.cache_dir, args.refresh, args.keep_workdir)
    try:
        logging.info('Resolving exact source tag riak-%s and its pinned dependencies', args.version)
        root, repositories, warnings = resolver.resolve('github.com/OpenRiak/riak', 'riak-' + args.version, recursive=False)
        document = build_inventory(args.version, runtime, root, repositories,
                                   docs, warnings)
        if args.keep_workdir:
            document['working_directory'] = str(resolver.workdir)
        return document
    except Exception as error:
        raise ValueError(f'CLI source discovery failed for KV {args.version}: {error}') from error
    finally:
        resolver.close()
