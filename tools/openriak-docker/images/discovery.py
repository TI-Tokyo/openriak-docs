"""Discovery operations; dependencies are supplied by the public tool facade."""
from __future__ import annotations
import dataclasses
import fnmatch
import json
import re
import urllib.parse
from typing import Any, Callable, Iterable
import images.minimal as minimal
DEFAULT_CLUSTER_NODES = 5


def metadata_versions(tool, ) -> list[str]:
    return sorted(
        [
            entry.name
            for entry in tool.METADATA_ROOT.iterdir()
            if entry.is_dir()
            and re.fullmatch(r"\d+\.\d+\.\d+", entry.name)
            and tool.semver_key(entry.name) >= tool.MINIMUM_OPENRIAK_VERSION
        ],
        key=tool.semver_key,
    )


def targets_for_version(tool, version: str) -> list[Target]:
    if tool.semver_key(version) < tool.MINIMUM_OPENRIAK_VERSION:
        raise tool.DockerToolError(
            f"OpenRiak KV Docker targets start at 3.4.0; unsupported version: {version}"
        )
    root = tool.METADATA_ROOT / version
    supported_path = root / "supported-os.json"
    downloads_path = root / "downloads.json"
    if not supported_path.is_file() or not downloads_path.is_file():
        return []
    supported = tool.read_json(supported_path)
    downloads = tool.read_json(downloads_path)
    if supported.get("product") != "kv" or downloads.get("product") != "kv":
        raise tool.DockerToolError(f"Mismatched product metadata for OpenRiak KV {version}")
    if supported.get("version") != version or downloads.get("version") != version:
        raise tool.DockerToolError(f"Mismatched version metadata for OpenRiak KV {version}")
    if supported.get("status") != "complete" or downloads.get("status") != "complete":
        return []

    operating_systems = list(supported.get("operating_systems", []))
    alias_rules = tool.read_json(tool.OS_ALIASES_PATH)
    native_families = {item["family"] for item in operating_systems}
    native_ids = {item["id"] for item in operating_systems}
    for source in supported.get("operating_systems", []):
        if source["family"] != alias_rules["source_family"]:
            continue
        for alias in alias_rules["aliases"]:
            if alias.get("docker") is False:
                continue
            if alias.get("nativeFamily", alias["family"]) in native_families:
                continue
            release = alias.get("modernReleases", alias.get("releases", {})).get(str(source["release"]))
            alias_release = release["id"] if release else source["release"]
            alias_id = f"{alias['family']}-{alias_release}-{source['architecture']}"
            if alias_id in native_ids:
                continue
            operating_systems.append({
                **source,
                "id": alias_id,
                "family": alias["family"],
                "release": alias_release,
                "display_name": f"{alias.get('name', alias['family'])} {release['version'] if release else alias_release}",
                "alias_of": source["id"],
            })

    targets: list[tool.Target] = []
    for operating_system in operating_systems:
        os_id = operating_system["id"]
        package_os_id = operating_system.get("alias_of", os_id)
        for download_id, package in downloads.get("downloads", {}).get(package_os_id, {}).items():
            checksum = package.get("checksum", {})
            if checksum.get("algorithm") != "sha256" or not re.fullmatch(
                r"[0-9a-f]{64}", str(checksum.get("value", ""))
            ):
                raise tool.DockerToolError(f"Invalid package checksum for {version}/{os_id}/{download_id}")
            targets.append(tool.Target(version, operating_system, download_id, package))
    grouped: dict[str, list[tool.Target]] = {}
    for target in targets:
        grouped.setdefault(target.image, []).append(target)

    unique: list[tool.Target] = []
    for candidates in grouped.values():
        source_path = str(candidates[0].operating_system.get("source", {}).get("path", ""))

        def preference(candidate: tool.Target) -> tuple[Any, ...]:
            package_path = urllib.parse.unquote(urllib.parse.urlparse(candidate.package["url"]).path)
            return (
                int(bool(source_path) and package_path.startswith(source_path)),
                tool.natural_key(candidate.package.get("package_revision")),
                tool.natural_key(candidate.download_id),
            )

        unique.append(max(candidates, key=preference))
    return sorted(unique, key=lambda item: (item.os_id, tool.natural_key(item.otp), item.download_id))


def discover_targets(tool,
    versions: Iterable[str] | None = None,
    os_id: str | Iterable[str] | None = None,
    otp: str | None = None,
    download_id: str | None = None,
) -> list[Target]:
    selected_versions = list(versions) if versions is not None else tool.metadata_versions()
    targets = [target for version in selected_versions for target in tool.targets_for_version(version)]
    if os_id:
        patterns = [os_id] if isinstance(os_id, str) else list(os_id)
        targets = [target for target in targets
                   if any(fnmatch.fnmatchcase(target.os_id, pattern) for pattern in patterns)]
    if otp:
        targets = [target for target in targets if target.otp == str(otp)]
    if download_id:
        targets = [target for target in targets if target.download_id == download_id]
    return targets


def base_image_for(tool, target: Target, *, upstream: bool = False) -> str:
    mode = minimal.configuration(target)
    if not upstream and mode and mode.get("base_image"):
        return f"{target.identity.namespace}/{mode['base_image']}"
    try:
        config = tool.read_json(tool.BASE_IMAGES_PATH)
        if config.get("schema_version") != 1:
            raise ValueError("unsupported schema_version")
        families = config["families"]
        family = target.family
        visited = set()
        while True:
            if family in visited:
                raise ValueError(f"cyclic family alias: {family}")
            visited.add(family)
            entry = families[family]
            if "alias" not in entry:
                break
            family = entry["alias"]
        release = target.release
        for old, new in entry.get("release_replacements", {}).items():
            release = release.lower().replace(old, new)
        if "release_map" in entry:
            mapping = config["release_maps"][entry["release_map"]]
            if entry.get("require_release_mapping") and release not in mapping:
                raise ValueError(f"No release-specific image mapping for {target.family} {target.release}")
            release = mapping.get(release, release)
        major = release.split(".")[0]
        for rule in entry["rules"]:
            if "architectures" in rule and target.architecture not in rule["architectures"]:
                continue
            if "minimum_major" in rule and int(major) < rule["minimum_major"]:
                continue
            image = rule["image"].format(release=release, os_release=target.release,
                                         major=major, architecture=target.architecture)
            # A release tag is mandatory; refresh resolves its immutable digest.
            if not re.fullmatch(r"[a-z0-9][a-z0-9./:_-]*:[A-Za-z0-9_][A-Za-z0-9_.-]*", image) or image.rsplit(":", 1)[1].lower() == "latest":
                raise ValueError(f"Expected a release-specific base image tag, got {image!r}")
            return image
        raise ValueError(f"No base-image rule matches architecture {target.architecture}")
    except (KeyError, TypeError, ValueError, AttributeError, OSError) as error:
        raise tool.DockerToolError(f"Invalid base-image configuration {tool.BASE_IMAGES_PATH} for {target.family} {target.release}: {error}") from error


def grouped_targets(tool, targets: list[Target]) -> list[list[Target]]:
    groups: dict[str, dict[str, tool.Target]] = {}
    for original in targets:
        target = dataclasses.replace(original, grouped=True)
        platforms = groups.setdefault(target.image, {})
        if target.platform in platforms and platforms[target.platform].package != target.package:
            raise tool.DockerToolError(f"Ambiguous packages for {target.image} {target.platform}")
        platforms[target.platform] = target
    return [list(sorted(platforms.values(), key=lambda t: t.platform)) for _, platforms in sorted(groups.items())]


def release_key(tool, target: Target) -> tuple[int, ...]:
    release = str(target.operating_system.get("release_version", target.release))
    numbers = tuple(int(part) for part in re.findall(r"\d+", release))
    if not numbers:
        raise tool.DockerToolError(f"Metadata needs release_version to order {target.family} {release}")
    return numbers


def image_aliases(tool, target: Target, all_targets: list[Target]) -> list[str]:
    """Aliases are selected from metadata, never from whichever build finishes last."""
    target = dataclasses.replace(target, grouped=True)
    tags = [target.image]
    peers = [t for t in all_targets if t.version == target.version and t.family == target.family]
    same_release = [t for t in peers if t.release == target.release]
    otp_key = lambda t: tuple(int(n) for n in t.otp.split("."))
    if otp_key(target) != max(map(otp_key, same_release)):
        return tags
    prefix = f"{target.identity.namespace}/openriak-kv:{target.version}"
    tags.append(f"{prefix}-{target.family}-{target.release}")
    if tool.release_key(target) != max(map(tool.release_key, peers)):
        return tags
    tags.append(f"{prefix}-{target.family}")
    if target.family == "alpine":
        tags.append(prefix)
        if tool.semver_key(target.version) == max(tool.semver_key(t.version) for t in all_targets):
            tags.append(f"{target.identity.namespace}/openriak-kv:latest")
    return tags


def print_matrix(tool, targets: list[Target], as_json: bool) -> None:
    all_targets = tool.discover_targets()
    selected = {(t.version, t.family, t.release, t.otp) for t in targets}
    groups = tool.grouped_targets([t for t in all_targets if (t.version, t.family, t.release, t.otp) in selected])
    records = []
    for group in groups:
        target = group[0]
        tags = tool.image_aliases(target, all_targets)
        path = target.group_directory / "report.json"
        report = tool.read_json(path) if path.is_file() else {}
        records.append({
            "version": target.version, "os_family": target.family, "os_release": target.release,
            "otp": target.otp, "image": target.image, "tags": tags,
            "platforms": [t.platform for t in group],
            "packages": [{"os_id": t.os_id, "download_id": t.download_id, "platform": t.platform,
                          "url": t.package["url"]} for t in group],
            "cached": tool.group_is_passed(group, report, tool.group_input(group, tool.DEFAULT_CLUSTER_NODES, tags)),
        })
    if as_json:
        print(json.dumps(records, indent=2))
        return
    for record in records:
        marker = "cached" if record["cached"] else "not cached"
        print(f"{record['image']} ({', '.join(record['platforms'])}; {marker})")


def validate_output_targets(tool, targets: list[Target]) -> None:
    for target in targets:
        if target.output_root is None:
            continue
        paths = [target.group_directory, target.cache_directory,
                 target.group_directory / "runs", target.group_directory / "rebuilds",
                 target.cache_directory / "runs"]
        for directory in (target.group_directory, target.cache_directory):
            paths.extend(directory / name for name in (*tool.ARTIFACT_FILENAMES, "report.json", ".dockerignore"))
        for path in paths:
            if not path.resolve().is_relative_to(target.output_root.resolve()):
                raise tool.DockerToolError(f"Standalone output contains a path or symlink outside its root: {path}")
