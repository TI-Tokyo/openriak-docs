from __future__ import annotations

import re
from pathlib import Path

from .erlang import TermParser, raw_erlang, tuple_values
from .schema import merge_mappings, parse_schema
from .source import Repository, is_erlang_repository


_RPM_BUILTIN_MACROS = {
    "_prefix": "/usr",
    "_exec_prefix": "%{_prefix}",
    "_bindir": "%{_exec_prefix}/bin",
    "_sbindir": "%{_exec_prefix}/sbin",
    "_libdir": "%{_exec_prefix}/lib64",
    "_sysconfdir": "/etc",
    "_sharedstatedir": "/var/lib",
    "_localstatedir": "/var",
}


def extract_defaults(product: dict, version: str, targets: list[dict], root: Repository,
                     repositories: list[Repository], initial_warnings: list[str]) -> dict:
    warnings = list(initial_warnings)
    ordered_schemas = discover_schemas(root, repositories)
    mappings: list[dict] = []
    translations: list[dict] = []
    validators: dict[str, dict] = {}
    for repository, path in ordered_schemas:
        relative = path.relative_to(repository.path).as_posix()
        parsed = parse_schema(path.read_text("utf-8", errors="replace"), repository.name, relative)
        mappings.extend(parsed.mappings)
        translations.extend(parsed.translations)
        validators.update(parsed.validators)
        warnings.extend(parsed.warnings)
    settings, merge_warnings = merge_mappings(mappings)
    warnings.extend(merge_warnings)
    release_vars, release_sources = discover_release_vars(root.path)
    package_vars, package_sources = discover_package_vars(root.path, warnings)
    effective_defaults: dict[str, dict] = {}
    for target in targets:
        package_family = _package_family(target)
        context = dict(release_vars)
        context.update(package_vars.get(package_family, {}))
        target_defaults = {}
        for key, setting in settings.items():
            target_defaults[key] = calculate_default(key, setting, context, release_vars,
                                                     package_vars.get(package_family, {}),
                                                     release_sources, package_sources.get(package_family, []), settings)
        effective_defaults[target["id"]] = target_defaults
    status = "partial" if warnings or not ordered_schemas else "complete"
    if not ordered_schemas:
        warnings.append("No Cuttlefish schemas were found in the resolved Erlang repositories.")
    for setting in settings.values():
        setting.pop("default", None)
        setting.pop("raw_default", None)
        setting.pop("has_default", None)
    return {
        "schema_version": 1, "product": "kv", "product_name": product["display_name"], "version": version,
        "status": status,
        "source": {"repository": product["source_repository"], "ref": product["tag_template"].format(version=version),
                   "commit": root.commit},
        "repositories": [{"name": r.name, "repository": r.repository, "commit": r.commit,
                          "dependency_depth": r.dependency_depth} for r in sorted(repositories, key=lambda r: (r.dependency_depth, r.name, r.commit))],
        "settings": dict(sorted(settings.items())), "effective_defaults": effective_defaults,
        "translations": sorted(translations, key=lambda item: (str(item["target"]), item["source"]["path"], item["source"]["line"])),
        "validators": dict(sorted(validators.items())), "warnings": sorted(set(warnings)),
    }


def discover_schemas(root: Repository, repositories: list[Repository]) -> list[tuple[Repository, Path]]:
    candidates: list[tuple[Repository, Path]] = []
    for repository in repositories:
        if not is_erlang_repository(repository.path):
            continue
        actual = list(repository.path.glob("priv/**/*.schema"))
        actual_stems = {str(path) for path in actual}
        generated = [p for pattern in ("priv/**/*.schema.src", "priv/**/*.schema.in") for p in repository.path.glob(pattern)]
        for path in actual + generated:
            base = re.sub(r"\.(?:src|in)$", "", str(path))
            if path.suffix in (".src", ".in") and base in actual_stems:
                continue
            candidates.append((repository, path))
    order = schema_order(root.path / "rebar.config")
    rank = {name: position for position, name in enumerate(order)}
    return sorted(candidates, key=lambda pair: (rank.get(pair[1].name.split(".")[0], len(rank)),
                                                pair[0].dependency_depth, pair[0].name,
                                                pair[1].relative_to(pair[0].path).as_posix()))


def schema_order(path: Path) -> list[str]:
    if not path.exists():
        return []
    text = re.sub(r"<<(\"(?:\\.|[^\"])*\")>>", r"\1", path.read_text("utf-8", errors="replace"))
    try:
        terms = TermParser(text).parse_all()
    except Exception:
        return []
    for term, _ in terms:
        found = _find_named_tuple(term, "schema_order")
        if found and isinstance(found, list):
            return [str(item) for item in found]
    return []


def _find_named_tuple(value, name: str):
    values = tuple_values(value)
    if values:
        if len(values) == 2 and values[0] == name:
            return values[1]
        for child in values:
            found = _find_named_tuple(child, name)
            if found is not None: return found
    elif isinstance(value, list):
        for child in value:
            found = _find_named_tuple(child, name)
            if found is not None: return found
    return None


def parse_vars(text: str) -> dict:
    try:
        terms = TermParser(text).parse_all()
    except Exception:
        return {}
    result: dict = {}
    for term, _ in terms:
        _collect_pairs(term, result)
    return result


def _collect_pairs(value, result: dict) -> None:
    values = tuple_values(value)
    if values:
        if len(values) == 2 and isinstance(values[0], str):
            result[values[0]] = values[1]
        else:
            for child in values: _collect_pairs(child, result)
    elif isinstance(value, list):
        for child in value: _collect_pairs(child, result)


def discover_release_vars(root: Path) -> tuple[dict, list[dict]]:
    paths = []
    direct = root / "rel" / "vars.config"
    if direct.exists(): paths.append(direct)
    for directory in (root / "rel" / "var", root / "rel" / "vars"):
        if directory.exists(): paths.extend(sorted(p for p in directory.rglob("*") if p.is_file()))
    values, sources = {}, []
    for path in paths:
        parsed = parse_vars(path.read_text("utf-8", errors="replace")); values.update(parsed)
        sources.append({"repository": root.name, "path": path.relative_to(root).as_posix(), "line": 1})
    return values, sources


def discover_package_vars(root: Path, warnings: list[str]) -> tuple[dict[str, dict], dict[str, list[dict]]]:
    base = root / "rel" / "pkg"
    values: dict[str, dict] = {}
    sources: dict[str, list[dict]] = {}
    if not base.exists(): return values, sources
    for directory in sorted(path for path in base.iterdir() if path.is_dir()):
        family = directory.name
        vars_file = directory / "vars.config"
        if vars_file.exists():
            values[family] = parse_vars(vars_file.read_text("utf-8", errors="replace"))
            sources[family] = [{"repository": root.name, "path": vars_file.relative_to(root).as_posix(), "line": 1}]
        elif family == "rpm":
            rpm_values, rpm_sources = parse_rpm_vars(directory, root)
            if rpm_values:
                values[family], sources[family] = rpm_values, rpm_sources
            elif (directory / "specfile").exists():
                warnings.append("RPM packaging variables could not be fully reconstructed from the specfile.")
    return values, sources


def parse_rpm_vars(directory: Path, root: Path) -> tuple[dict, list[dict]]:
    values: dict = {}
    sources: list[dict] = []
    part = directory / "vars.config.part"
    if part.exists():
        values.update(parse_vars(part.read_text("utf-8", errors="replace")))
        sources.append({"repository": root.name, "path": part.relative_to(root).as_posix(), "line": 1,
                        "source_type": "rpm-generated-vars"})
    spec = directory / "specfile"
    if not spec.exists(): return values, sources
    text = spec.read_text("utf-8", errors="replace")
    macros = dict(_RPM_BUILTIN_MACROS)
    macros.update({name: value.strip() for name, value in re.findall(r"(?m)^%(?:define|global)\s+(\w+)\s+(.+)$", text)})
    def expand(value: str) -> str:
        previous = None
        while value != previous:
            previous = value
            value = re.sub(r"%\{(\w+)\}", lambda m: macros.get(m.group(1), m.group(0)), value)
        return value.strip(' "')
    for match in re.finditer(r"\{\s*([a-zA-Z_][\w]*)\s*,\s*(?:\\?\"([^\"]+)\\?\"|([^},\n]+))\s*\}", text):
        key, quoted, bare = match.groups()
        raw = quoted if quoted is not None else bare
        if "%{" in raw:
            values[key] = expand(raw)
    sources.append({"repository": root.name, "path": spec.relative_to(root).as_posix(), "line": 1,
                    "source_type": "rpm-generated-vars"})
    return values, sources


def calculate_default(key: str, setting: dict, context: dict, release_vars: dict, package_vars: dict,
                      release_sources: list[dict], package_sources: list[dict], all_settings: dict) -> dict:
    has_schema = setting.get("has_default", False)
    expression = setting.get("default")
    resolved_schema, template_variables, complete = resolve_templates(expression, context)
    release_default = setting.get("new_conf_value")
    package_default = None
    source_layer = "schema"
    value = resolved_schema if complete else expression
    provenance = list(setting.get("definitions", [])) if has_schema else []
    # new_conf_value describes the generated active configuration, unlike commented.
    if release_default is not None:
        value, source_layer = release_default, "release"
        provenance.extend(release_sources)
    # A package variable changing a schema template is a package-layer override.
    changed_variables = [name for name in template_variables if name in package_vars]
    if changed_variables:
        package_default, source_layer = resolved_schema, "package"
        value = resolved_schema
        provenance.extend(package_sources)
    resolved_reference = resolve_config_references(value, all_settings, context)
    if not has_schema and release_default is None:
        return {"value": None, "resolved_value": None, "has_default": False,
                "reason": "No explicit Cuttlefish or package default found.",
                "schema_default": None, "release_default": None, "package_default": None,
                "os_default": None, "source_layer": None, "provenance": []}
    result = {"value": value, "resolved_value": resolved_reference, "has_default": True,
              "source_layer": source_layer, "schema_default": expression,
              "release_default": release_default, "package_default": package_default,
              "os_default": None, "provenance": provenance}
    if template_variables:
        result.update({"schema_expression": raw_erlang(expression),
                       "resolved_schema_default": resolved_schema if complete else None,
                       "template_variables": template_variables})
    return result


def resolve_templates(value, context: dict) -> tuple[object, list[str], bool]:
    def render(current, stack: tuple[str, ...] = ()) -> tuple[object, list[str], bool]:
        if isinstance(current, dict):
            if "$template" in current:
                return render(current["$template"], stack)
            rendered, names, complete = {}, [], True
            for key, child in current.items():
                rendered_child, child_names, child_complete = render(child, stack)
                rendered[key] = rendered_child
                names.extend(child_names)
                complete = complete and child_complete
            return rendered, names, complete
        if isinstance(current, list):
            rendered, names, complete = [], [], True
            for child in current:
                rendered_child, child_names, child_complete = render(child, stack)
                rendered.append(rendered_child)
                names.extend(child_names)
                complete = complete and child_complete
            return rendered, names, complete
        if not isinstance(current, str):
            return current, [], True
        current_names = re.findall(r"\{\{\s*([A-Za-z_]\w*)\s*\}\}", current)
        stripped = current.strip()
        if len(current_names) == 1 and re.fullmatch(r"\{\{\s*" + re.escape(current_names[0]) + r"\s*\}\}", stripped):
            name = current_names[0]
            if name not in context or name in stack:
                return current, current_names, False
            replacement, nested_names, complete = render(context[name], stack + (name,))
            return replacement, current_names + nested_names, complete
        rendered = current
        complete = True
        names = list(current_names)
        for name in current_names:
            if name not in context or name in stack:
                complete = False
                continue
            replacement, nested_names, resolved = render(context[name], stack + (name,))
            names.extend(nested_names)
            complete = complete and resolved
            rendered = re.sub(r"\{\{\s*" + re.escape(name) + r"\s*\}\}", str(replacement), rendered)
        return rendered, names, complete

    rendered, names, complete = render(value)
    return rendered, list(dict.fromkeys(names)), complete


def resolve_config_references(value, settings: dict, context: dict, stack: tuple[str, ...] = ()):
    if isinstance(value, dict):
        return {key: resolve_config_references(child, settings, context, stack) for key, child in value.items()}
    if isinstance(value, list):
        return [resolve_config_references(child, settings, context, stack) for child in value]
    if not isinstance(value, str): return value
    complete = True
    def replace(match):
        nonlocal complete
        name = match.group(1)
        if name in stack:
            complete = False; return match.group(0)
        if name in context:
            return str(context[name])
        setting = settings.get(name)
        if setting and setting.get("has_default"):
            nested, _, ok = resolve_templates(setting.get("default"), context)
            if ok:
                resolved = resolve_config_references(nested, settings, context, stack + (name,))
                if resolved is not None: return str(resolved)
        complete = False
        return match.group(0)
    rendered = re.sub(r"\$\(([^)]+)\)", replace, value)
    return rendered if complete else None


def _package_family(target: dict) -> str:
    if target["family"] == "alpine": return "alpine"
    if target["package_family"] == "deb": return "deb"
    if target["package_family"] == "rpm": return "rpm"
    return target["package_family"]
