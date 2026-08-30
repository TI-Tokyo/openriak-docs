from __future__ import annotations

import re
from dataclasses import dataclass, field

from .erlang import ErlangParseError, TermParser, raw_erlang, tuple_values


@dataclass
class SchemaResult:
    mappings: list[dict] = field(default_factory=list)
    translations: list[dict] = field(default_factory=list)
    validators: dict[str, dict] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


def parse_schema(text: str, repository: str, path: str) -> SchemaResult:
    result = SchemaResult()
    docs = _documentation_by_line(text)
    try:
        terms = TermParser(text).parse_all()
    except ErlangParseError as exc:
        result.warnings.append(f"{repository}/{path}: {exc}")
        return result
    for term, line in terms:
        values = tuple_values(term)
        if not values or not values:
            continue
        source = {"repository": repository, "path": path, "line": line}
        kind = values[0]
        if kind == "mapping" and len(values) >= 4:
            props = _properties(values[3])
            doc, see = docs.get(line, (None, []))
            known = {"default", "new_conf_value", "commented", "datatype", "validators", "hidden",
                     "merge", "level", "include_default"}
            mapping = {"key": values[1], "erlang_target": values[2],
                       "default": props.get("default"), "new_conf_value": props.get("new_conf_value"),
                       "commented": props.get("commented"), "datatype": _datatype(props.get("datatype")),
                       "validators": _as_list(props.get("validators")), "hidden": bool(props.get("hidden", False)),
                       "merge": bool(props.get("merge", False)), "level": props.get("level"),
                       "include_default": props.get("include_default"), "documentation": doc, "see": see,
                       "source": source, "extra_attributes": {k: v for k, v in props.items() if k not in known}}
            mapping["has_default"] = "default" in props
            if "default" in props:
                mapping["raw_default"] = raw_erlang(props["default"])
            result.mappings.append(mapping)
        elif kind == "translation" and len(values) >= 3:
            result.translations.append({"target": values[1], "raw_erlang": raw_erlang(values[2]), "source": source})
        elif kind == "validator" and len(values) >= 4:
            result.validators[str(values[1])] = {"name": values[1], "message": values[2],
                                                  "raw_erlang": raw_erlang(values[3]), "source": source}
    return result


def _properties(value) -> dict:
    result = {}
    if not isinstance(value, list):
        return result
    for item in value:
        values = tuple_values(item)
        if not values:
            continue
        result[str(values[0])] = values[1] if len(values) == 2 else values[1:]
    return result


def _datatype(value):
    values = tuple_values(value)
    if values and values[0] == "enum":
        return {"type": "enum", "values": values[1] if len(values) > 1 else []}
    if values:
        return {"type": str(values[0]), "arguments": values[1:]}
    if value is None:
        return None
    return {"type": str(value)}


def _as_list(value) -> list:
    if value is None: return []
    return value if isinstance(value, list) else [value]


def _documentation_by_line(text: str) -> dict[int, tuple[str | None, list[str]]]:
    result = {}
    pending: list[str] = []
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("%%"):
            pending.append(re.sub(r"^%%\s?", "", stripped))
        elif stripped:
            if stripped.startswith("{mapping") and pending:
                doc: list[str] = []
                see: list[str] = []
                for comment in pending:
                    if comment.startswith("@doc"):
                        doc.append(comment[4:].strip())
                    elif comment.startswith("@see"):
                        see.append(comment[4:].strip())
                    elif doc:
                        doc.append(comment.strip())
                result[number] = (" ".join(filter(None, doc)) or None, see)
            pending = []
    return result


def merge_mappings(mappings: list[dict]) -> tuple[dict, list[str]]:
    effective: dict[str, dict] = {}
    warnings: list[str] = []
    for mapping in mappings:
        key = str(mapping["key"])
        definition = mapping["source"]
        if key in effective and mapping.get("merge"):
            prior = effective[key]
            definitions = prior.get("definitions", []) + [definition]
            merged = dict(prior)
            for field, value in mapping.items():
                if field not in ("source", "definitions") and value is not None and field != "merge":
                    merged[field] = value
            merged["definitions"] = definitions
            effective[key] = merged
        else:
            clean = dict(mapping)
            clean["definitions"] = ([*effective[key].get("definitions", []), definition]
                                     if key in effective else [definition])
            clean.pop("source", None)
            effective[key] = clean
    return effective, warnings
