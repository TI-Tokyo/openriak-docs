#!/usr/bin/env python3
"""Convert a Hugo 0.18 content tree to modern Hugo branch bundles.

Hugo 0.18 sites commonly represented a section with both ``section.md`` and
``section/...``. Modern Hugo represents that landing page as
``section/_index.md``. This importer performs that conversion and promotes the
old menu label and weight to top-level front matter used by the current site.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


class ImportError018(RuntimeError):
    """Raised when legacy content cannot be converted without data loss."""


@dataclass(frozen=True)
class MenuEntry:
    name: str | None = None
    identifier: str | None = None
    parent: str | None = None
    weight: int | None = None


@dataclass(frozen=True)
class Conversion:
    source: Path
    target: Path
    discard: bool = False


FIELD_RE = re.compile(r"^(?P<indent>\s*)(?P<key>[A-Za-z0-9_.-]+):\s*(?P<value>.*?)\s*$")
DOCUMENT_START_RE = re.compile(r"(?m)^---\r?\ntitle:\s*(?P<title>.*?)\s*$")


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        if value[0] == '"':
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        return value[1:-1].replace("''", "'")
    return value


def split_front_matter(text: str, path: Path) -> tuple[list[str], str, str]:
    newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ImportError018(f"{path}: expected YAML front matter")
    try:
        closing = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as error:
        raise ImportError018(f"{path}: unterminated YAML front matter") from error
    body = newline.join(lines[closing + 1 :])
    if text.endswith(("\n", "\r")):
        body += newline
    return lines[1:closing], body, newline


def legacy_menu(front: list[str], path: Path) -> MenuEntry | None:
    menu_start = next((i for i, line in enumerate(front) if line == "menu:"), None)
    if menu_start is None:
        return None
    menu_end = next(
        (i for i in range(menu_start + 1, len(front)) if front[i] and not front[i][0].isspace()),
        len(front),
    )
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in front[menu_start + 1 : menu_end]:
        match = FIELD_RE.match(line)
        if not match:
            continue
        indent = len(match.group("indent"))
        if indent == 2:
            current = {}
            entries.append(current)
        elif indent == 4 and current is not None:
            current[match.group("key")] = _unquote(match.group("value"))
    if not entries:
        return None
    if len(entries) != 1:
        raise ImportError018(f"{path}: expected one legacy menu entry, found {len(entries)}")
    values = entries[0]
    weight = values.get("weight")
    try:
        parsed_weight = int(weight) if weight is not None else None
    except ValueError as error:
        raise ImportError018(f"{path}: menu weight is not an integer: {weight!r}") from error
    return MenuEntry(values.get("name"), values.get("identifier"), values.get("parent"), parsed_weight)


def deduplicate_top_level_fields(front: list[str]) -> list[str]:
    """Preserve the final value when legacy YAML repeats a top-level key.

    Hugo 0.18's YAML parser accepted duplicate mapping keys and effectively
    kept the final value. Modern Hugo rejects the page, so reproduce the old
    behavior explicitly before writing the imported front matter.
    """
    fields = [
        (index, match.group("key"))
        for index, line in enumerate(front)
        if (match := FIELD_RE.match(line)) and not match.group("indent")
    ]
    seen: set[str] = set()
    discard: set[int] = set()
    for field_index in range(len(fields) - 1, -1, -1):
        start, key = fields[field_index]
        end = fields[field_index + 1][0] if field_index + 1 < len(fields) else len(front)
        if key in seen:
            discard.update(range(start, end))
        else:
            seen.add(key)
    return [line for index, line in enumerate(front) if index not in discard]


def discard_appended_duplicate_document(text: str, path: Path) -> str:
    """Discard an accidentally concatenated second copy of the same page.

    Some Hugo 0.18 exports contain a complete second document after the first
    document's body. A repeated YAML delimiter followed immediately by the
    same title is sufficiently specific to distinguish this corruption from
    ordinary Markdown horizontal rules and fenced examples.
    """
    starts = list(DOCUMENT_START_RE.finditer(text))
    if len(starts) <= 1:
        return text
    original_title = _unquote(starts[0].group("title"))
    for duplicate in starts[1:]:
        duplicate_title = _unquote(duplicate.group("title"))
        if duplicate_title != original_title:
            raise ImportError018(
                f"{path}: appended document has a different title: {duplicate_title!r}"
            )
        newline = "\r\n" if "\r\n" in text else "\n"
        return text[: duplicate.start()].rstrip() + newline
    return text


def modernize_front_matter(text: str, path: Path) -> tuple[str, MenuEntry | None]:
    text = text.lstrip("\ufeff")
    text = re.sub(r"\A(?:[ \t]*\r?\n)+(?=---(?:\r?\n))", "", text)
    fragment = path.name.startswith("_") and path.name != "_index.md"
    if not text.startswith("---") and fragment:
        return (
            "---\n"
            "build:\n"
            "  list: never\n"
            "  render: never\n"
            "---\n\n"
            + text,
            None,
        )
    if not text.startswith("---"):
        return text, None
    text = discard_appended_duplicate_document(text, path)
    front, body, newline = split_front_matter(text, path)
    front = deduplicate_top_level_fields(front)
    menu = legacy_menu(front, path)
    top_level = {
        match.group("key")
        for line in front
        if (match := FIELD_RE.match(line)) and not match.group("indent")
    }
    additions: list[str] = []
    if menu and menu.name and "linkTitle" not in top_level and "linktitle" not in top_level:
        additions.append(f"linkTitle: {json.dumps(menu.name, ensure_ascii=False)}")
    if menu and menu.weight is not None and "weight" not in top_level:
        additions.append(f"weight: {menu.weight}")
    if fragment and "build" not in top_level:
        additions.extend(["build:", "  list: never", "  render: never"])
    if additions:
        front.extend(additions)
    rendered = newline.join(["---", *front, "---"])
    if body:
        rendered += newline + body
    else:
        rendered += newline
    return rendered, menu


def conversion_plan(root: Path) -> list[Conversion]:
    markdown = sorted(root.rglob("*.md"))
    has_legacy_home = (root / "index.md").is_file()
    plan: list[Conversion] = []
    for source in markdown:
        relative = source.relative_to(root)
        if relative == Path("_index.md") and has_legacy_home:
            plan.append(Conversion(source, root / "_index.md", discard=True))
        elif relative == Path("index.md"):
            plan.append(Conversion(source, root / "_index.md"))
        else:
            sibling_directory = source.with_suffix("")
            target = sibling_directory / "_index.md" if sibling_directory.is_dir() else source
            plan.append(Conversion(source, target))
    targets: dict[Path, Path] = {}
    for item in plan:
        if item.discard:
            continue
        previous = targets.get(item.target)
        if previous and previous != item.source:
            raise ImportError018(f"both {previous} and {item.source} map to {item.target}")
        if item.target.exists() and item.target != item.source:
            occupants = {entry.source for entry in plan if entry.target == item.target and entry.discard}
            if item.target not in occupants:
                raise ImportError018(f"{item.target} already exists")
        targets[item.target] = item.source
    return plan


def convert_in_place(root: Path, *, check: bool = False) -> dict[str, int]:
    root = root.resolve()
    if not root.is_dir():
        raise ImportError018(f"source directory does not exist: {root}")
    plan = conversion_plan(root)
    rendered: dict[Path, tuple[str, MenuEntry | None]] = {}
    identifiers: dict[str, Path] = {}
    parent_references: list[tuple[Path, str]] = []
    for item in plan:
        if item.discard:
            continue
        text = item.source.read_text(encoding="utf-8-sig")
        updated, menu = modernize_front_matter(text, item.source)
        rendered[item.target] = (updated, menu)
        if menu and menu.identifier:
            if menu.identifier in identifiers:
                raise ImportError018(
                    f"duplicate menu identifier {menu.identifier!r}: "
                    f"{identifiers[menu.identifier]} and {item.source}"
                )
            identifiers[menu.identifier] = item.target
        if menu and menu.parent:
            parent_references.append((item.source, menu.parent))
    missing = [(path, parent) for path, parent in parent_references if parent not in identifiers]
    if missing:
        details = ", ".join(f"{path}: {parent}" for path, parent in missing[:5])
        raise ImportError018(f"menu parent identifier not found ({details})")
    if not check:
        for item in plan:
            if item.discard and item.source.exists():
                item.source.unlink()
        for target, (text, _) in rendered.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8", newline="")
        for item in plan:
            if not item.discard and item.source != item.target and item.source.exists():
                item.source.unlink()
    return {
        "markdown": len(rendered),
        "branch_bundles": sum(item.source != item.target for item in plan if not item.discard),
        "discarded_search_indexes": sum(item.discard for item in plan),
        "fragments": sum(
            item.source.name.startswith("_") and item.source.name != "_index.md"
            for item in plan
            if not item.discard
        ),
        "menu_entries": len(identifiers),
    }


def import_tree(source: Path, destination: Path, *, check: bool = False) -> dict[str, int]:
    source = source.resolve()
    destination = destination.resolve()
    if source == destination:
        return convert_in_place(source, check=check)
    if destination.exists():
        raise ImportError018(f"destination already exists: {destination}")
    if check:
        with tempfile.TemporaryDirectory(prefix="hugo-018-check-") as temporary:
            copied = Path(temporary) / "content"
            shutil.copytree(source, copied)
            return convert_in_place(copied, check=False)
    shutil.copytree(source, destination)
    try:
        return convert_in_place(destination, check=False)
    except Exception:
        shutil.rmtree(destination)
        raise


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Hugo 0.18 content directory")
    parser.add_argument("destination", nargs="?", type=Path, help="new converted directory")
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="convert SOURCE directly (cannot be combined with DESTINATION)",
    )
    parser.add_argument("--check", action="store_true", help="validate and report without writing")
    args = parser.parse_args(argv)
    if args.in_place and args.destination:
        parser.error("--in-place cannot be combined with DESTINATION")
    if not args.in_place and not args.destination:
        parser.error("provide DESTINATION or use --in-place")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    destination = args.source if args.in_place else args.destination
    try:
        counts = import_tree(args.source, destination, check=args.check)
    except ImportError018 as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    action = "Validated" if args.check else "Imported"
    print(
        f"{action} {counts['markdown']} Markdown files; "
        f"created {counts['branch_bundles']} branch bundles, "
        f"preserved {counts['menu_entries']} menu entries, and "
        f"excluded {counts['fragments']} Markdown fragments from navigation; "
        f"discarded {counts['discarded_search_indexes']} obsolete search indexes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
