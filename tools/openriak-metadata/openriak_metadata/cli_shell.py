"""Inspect shell dispatchers without executing their command branches."""
from __future__ import annotations

from dataclasses import dataclass, field
import itertools
import re

TOKEN = re.compile(r'''\#[^\n]*|"(?:\\.|[^"\\])*"|'[^']*'|`(?:\\.|[^`\\])*`|;;|[(){};|]|[^\s(){};|"'`#]+''', re.S)


def mask_heredocs(text: str) -> str:
    # Help prose is data: quotes and shell keywords inside it must not affect
    # shell parsing. Retain offsets so provenance still points at the script.
    return re.sub(r"<<-?\s*['\"]?(\w+)['\"]?\s*\n(.*?)\n\1\b",
                  lambda m: m[0][:m.start(2)-m.start()] + re.sub(r'[^\n]', ' ', m[2]) + m[0][m.end(2)-m.start():], text, flags=re.S)


@dataclass
class Arm:
    patterns: list[str]
    start: int
    end: int = 0
    children: list = field(default_factory=list)


@dataclass
class Case:
    subject: str
    start: int
    end: int = 0
    arms: list[Arm] = field(default_factory=list)


def cases(text: str) -> list[Case]:
    tokens = [(m.group(), m.start(), m.end()) for m in TOKEN.finditer(mask_heredocs(text)) if not m.group().startswith('#')]
    found = []

    def parse(index):
        start = index
        index += 1
        subject = tokens[index][0].strip('"\'')
        index += 1
        if index >= len(tokens) or tokens[index][0] != 'in':
            return None, start + 1
        result = Case(subject, tokens[start][1])
        index += 1
        while index < len(tokens):
            if tokens[index][0] == 'esac':
                result.end = tokens[index][2]
                return result, index + 1
            patterns = []
            while index < len(tokens) and tokens[index][0] != ')':
                if tokens[index][0] not in ('(', '|'):
                    patterns.append(tokens[index][0].strip('"\''))
                index += 1
            if index == len(tokens):
                break
            arm = Arm(patterns, tokens[index][2])
            result.arms.append(arm)
            index += 1
            while index < len(tokens):
                word = tokens[index][0]
                if word == 'case':
                    child, index = parse(index)
                    if child:
                        arm.children.append(child)
                    continue
                if word in (';;', 'esac'):
                    arm.end = tokens[index][1]
                    if word == ';;':
                        index += 1
                    break
                index += 1
        return None, max(start + 1, index)

    index = 0
    while index < len(tokens):
        if tokens[index][0] == 'case':
            case, index = parse(index)
            if case:
                found.append(case)
        else:
            index += 1
    return found


def functions(text: str) -> dict[str, tuple[int, int]]:
    result = {}
    tokens = list(TOKEN.finditer(mask_heredocs(text)))
    for match in re.finditer(r'^\s*([a-zA-Z_]\w*)\s*\(\)\s*\{', text, re.M):
        depth = 1
        for token in tokens:
            if token.start() < match.end():
                continue
            if token.group() == '{':
                depth += 1
            elif token.group() == '}':
                depth -= 1
                if not depth:
                    result[match[1]] = (match.end(), token.start())
                    break
    return result


def expand_pattern(pattern: str) -> list[str]:
    # Common Riak aliases use e.g. force[_-]remove. Preserve both spellings.
    parts = re.split(r'(\[[^\]]+\])', pattern)
    options = [list(p[1:-1]) if p.startswith('[') else [p] for p in parts]
    return [''.join(items) for items in itertools.product(*options)
            if re.fullmatch(r'[a-zA-Z0-9_-]+', ''.join(items))]


def shell_strings(text: str, replacements: dict[str, str]) -> str:
    values = []
    for match in re.finditer(r"<<\s*['\"]?(\w+)['\"]?\s*\n(.*?)\n\1\b", text, re.S):
        values.append(match[2])
    # Capture echo/printf strings, including multiline help; never evaluate shell.
    for match in re.finditer(r'\b(?:echo|printf)\s+(?:-[a-z]+\s+)?("(?:\\.|[^"\\])*"|\'[^\']*\')', text, re.S):
        value = match[1][1:-1]
        value = re.sub(r'\\\n', '', value)
        value = re.sub(r'\\(["`\'$\\])', r'\1', value)
        value = value.replace('\\n', '\n').replace('\\t', '\t')
        for key, replacement in replacements.items():
            value = value.replace('${' + key + '}', replacement)
            value = re.sub(r'\$' + re.escape(key) + r'(?![A-Za-z0-9_])', lambda _: replacement, value)
        if value.strip() and value not in values:
            values.append(value)
    return '\n'.join(values).strip()


def option_tokens(text: str) -> list[dict]:
    found = {}
    for match in re.finditer(r'(?<![\w/-])(--?[a-zA-Z][a-zA-Z0-9_-]*)(?:[ =](<[\w.-]+>|[A-Z][A-Z_]*)(?![a-zA-Z]))?', text):
        name = match[1]
        found.setdefault(name, {"name": name, "value_name": match[2], "description": None,
                                "source": "usage"})
    for line in text.splitlines():
        # An option declaration line, rather than an incidental mention in prose.
        match = re.match(r'^\s*((?:--?[\w-]+(?:,?\s+)?)+)\s{2,}(.+)', line)
        if match:
            for name in re.findall(r'--?[\w-]+', match[1]):
                if name in found:
                    found[name]['description'] = match[2].strip()
    return list(found.values())


def inspect_script(name: str, text: str, prefix: list[str]) -> tuple[list[dict], list[str]]:
    all_cases = cases(text)
    funcs = functions(text)
    entries, gaps = {}, []
    roots = [c for c in all_cases if c.subject in ('$1', '${1}')
             and not any(start <= c.start < end for start, end in funcs.values())]
    helpers = {fn: [c for c in all_cases if start <= c.start < end] for fn, (start, end) in funcs.items()}
    help_text = shell_strings(text, {'SCRIPT': ' '.join(prefix), 'REL_NAME': 'riak'})

    def visit(case, path, depth=0, action=None):
        if depth > 8:
            gaps.append(f'{name}: dispatcher recursion at {" ".join(path)}')
            return
        for arm in case.arms:
            names = [n for p in arm.patterns for n in expand_pattern(p)]
            if not names:
                if arm.patterns != ['*'] and not all(p.startswith('-') for p in arm.patterns):
                    gaps.append(f'{name}: unparsed dispatch pattern {arm.patterns}')
                continue
            body = text[arm.start:arm.end]
            for sub in names:
                if sub.startswith('-') or sub.isdigit():
                    continue
                command = path + [sub]
                current_action = sub if re.search(r'ACTION=["\']?\$1', body) else (action or sub)
                replacements = {'SCRIPT': ' '.join(prefix), 'REL_NAME': 'riak', 'ACTION': current_action,
                                '1': sub, 'SUB_CMD': sub, 'command': sub}
                # Conditional branches on ACTION redispatch the same token.
                own_body = body
                for child in reversed(arm.children):
                    if child.subject in ('$SUB_CMD', '$1', '${1}'):
                        before = text[arm.start:child.start]
                        consumes_argument = child.subject == '$SUB_CMD' or bool(re.search(r'\bshift\b', before))
                        replacement = ''
                        if not consumes_argument:
                            matches = [a for a in child.arms if sub in [n for p in a.patterns for n in expand_pattern(p)]]
                            if matches:
                                replacement = text[matches[0].start:matches[0].end]
                        own_body = own_body[:child.start-arm.start] + replacement + own_body[child.end-arm.start:]
                required_action = re.search(r'if\s+\[\s*"\$ACTION"\s*!=\s*"([\w-]+)"', own_body)
                if required_action and path[-1] != required_action[1]:
                    continue
                # Runtime diagnostics are not help. Keep them in dispatch_source.
                help_value = shell_strings(own_body, replacements) if re.search(r'usage:?', own_body, re.I) else ''
                for fn, (start, end) in funcs.items():
                    if re.search(r'(?m)^\s*' + re.escape(fn) + r'(?:\s|$)', own_body) and ('help' in fn or 'usage' in fn):
                        help_value += '\n' + shell_strings(text[start:end], replacements)
                    if fn.endswith('_admin') and re.search(r'(?m)^\s*' + re.escape(fn) + r'\s', own_body):
                        for helper in helpers[fn]:
                            for h in helper.arms:
                                if h.patterns == ['*']:
                                    help_value += '\n' + shell_strings(text[h.start:h.end], replacements)
                # relx_usage has per-command help in its own case statement.
                for helper in helpers.get('relx_usage', []):
                    for h in helper.arms:
                        if sub in [n for p in h.patterns for n in expand_pattern(p)]:
                            help_value += '\n' + shell_strings(text[h.start:h.end], replacements)
                if not help_value.strip():
                    summary = re.search(r'(?m)^\s*' + re.escape(sub) + r'(?=\s)([^\n]+)', help_text)
                    if summary:
                        help_value = sub + summary[1]
                handlers = [{'module': m[1], 'function': m[2]} for m in
                            re.finditer(r'\brpc(?:_raw)?\s+([a-z]\w*)\s+([a-z]\w*)', own_body)]
                for match in re.finditer(r'\brpc(?:_raw)?\s+([a-z]\w*)\s+\$(ACTION|SUB_CMD|CMD)\b', own_body):
                    function = sub if match[2] == 'SUB_CMD' else current_action
                    handlers.append({'module': match[1], 'function': function.replace('-', '_')})
                deprecated = bool(re.search(r'deprecat|V2REPLDEP', own_body, re.I))
                status = re.search(r'CMD_STATUS="(\w+)"', own_body)
                if status:
                    deprecated = status[1] == 'deprecated'
                aliases = [a for p in arm.patterns if sub in expand_pattern(p) for a in expand_pattern(p) if a != sub]
                entry = {'path': command, 'help': help_value.strip(), 'options': option_tokens(help_value),
                         'deprecated': deprecated,
                         'removed': bool(re.search(r'no longer exists|not currently supported', own_body)),
                         'aliases': [path + [alias] for alias in aliases],
                         'line': text[:arm.start].count('\n') + 1, 'handlers': handlers,
                         'dispatch_source': own_body.strip()}
                entries[tuple(command)] = entry
                for child in arm.children:
                    if child.subject == '$SUB_CMD' or (child.subject in ('$1', '${1}')
                            and re.search(r'\bshift\b', text[arm.start:child.start])):
                        visit(child, command, depth + 1, current_action)
                for fn, helper_cases in helpers.items():
                    if fn.endswith('_admin') and re.search(r'(?m)^\s*' + re.escape(fn) + r'\s', own_body):
                        for child in helper_cases:
                            if child.subject in ('$1', '${1}'):
                                visit(child, command, depth + 1, current_action)
                for helper in re.findall(r'(?m)^\s*([a-z]\w*_admin)\s', own_body):
                    if helper not in funcs:
                        entry['unavailable_reason'] = 'Dispatcher calls missing shell function ' + helper

    for case in roots:
        visit(case, prefix)
    # Scripts with flag dispatch (riak-debug) or no subcommands (chkconfig).
    if tuple(prefix) not in entries:
        if 'usage' in funcs:
            start, end = funcs['usage']
            help_text = shell_strings(text[start:end], {'SCRIPT': ' '.join(prefix), 'REL_NAME': 'riak'})
        elif 'relx_usage' in funcs:
            start, end = funcs['relx_usage']
            help_text = shell_strings(text[start:end], {'SCRIPT': ' '.join(prefix), 'REL_NAME': 'riak'})
        root_options = option_tokens(help_text)
        dispatched_flags = []
        for case in roots:
            for arm in case.arms:
                for pattern in arm.patterns:
                    if re.fullmatch(r'--?[a-zA-Z][\w-]*', pattern) and not any(o['name'] == pattern for o in root_options):
                        root_options.append({'name': pattern, 'value_name': None, 'description': None,
                                             'source': 'dispatcher', 'hidden': True})
                    if pattern.startswith('-'):
                        dispatched_flags.append(pattern)
        if dispatched_flags:
            root_options = [o for o in root_options if o['name'] in dispatched_flags]
        for helper in helpers.get('process_internal_args', []):
            for arm in helper.arms:
                for pattern in arm.patterns:
                    if re.fullmatch(r'--?[\w-]+', pattern):
                        root_options.append({'name': pattern, 'source': 'dispatcher', 'hidden': True})
        entries[tuple(prefix)] = {'path': prefix, 'help': help_text, 'options': option_tokens(help_text),
            'deprecated': False, 'removed': False, 'aliases': [], 'line': 1,
            'handlers': [], 'dispatch_source': ''}
        entries[tuple(prefix)]['options'] = root_options
    return list(entries.values()), gaps
