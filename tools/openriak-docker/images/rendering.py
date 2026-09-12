"""Render operations; dependencies are supplied by the public tool facade."""
from __future__ import annotations
import json
import pathlib
import re
import images.minimal as minimal
DEFAULT_CLUSTER_NODES = 5


def create_riak_user_script(tool, target: Target) -> str:
    if target.operating_system["package_family"] == "apk":
        return """if ! getent group riak >/dev/null 2>&1
then
    addgroup -S riak
fi
if ! id riak >/dev/null 2>&1
then
    adduser -S -D -H -h /var/lib/riak -s /sbin/nologin -G riak riak
fi"""
    return """if ! getent group riak >/dev/null 2>&1
then
    groupadd --system riak
fi
if ! id riak >/dev/null 2>&1
then
    useradd --system --gid riak --home-dir /var/lib/riak --shell /sbin/nologin riak
fi"""


def compose_runtime_options(tool, ) -> str:
    return "".join(f'      {name}: "${{{name}:-{default}}}"\n' for name, (default, _) in tool.RUNTIME_OPTIONS.items())


def compose_resource_options(tool, ) -> str:
    return '''    # Optional per-node resource limits; zero leaves the resource unrestricted.
    cpus: "${OPENRIAK_CPUS:-0}"
    mem_limit: "${OPENRIAK_MEMORY_LIMIT:-0}"
    # Rotate Docker stdout/stderr logs separately from OpenRiak KV file logs.
    logging:
      driver: json-file
      options:
        max-size: "${OPENRIAK_DOCKER_LOG_MAX_SIZE:-10m}"
        max-file: "${OPENRIAK_DOCKER_LOG_MAX_FILES:-3}"
'''


def image_labels(tool, target: Target) -> dict[str, str]:
    return {
        "org.opencontainers.image.title": "OpenRiak KV",
        "org.opencontainers.image.description": "Package-backed OpenRiak KV with single-node and cluster startup support",
        "org.opencontainers.image.version": target.version,
        "org.opencontainers.image.vendor": target.identity.vendor,
        "org.opencontainers.image.url": target.identity.url,
        "org.opencontainers.image.source": target.identity.source,
        "org.openriak.otp.version": target.otp,
        "org.openriak.os.name": target.family,
        "org.openriak.os.release": target.release,
        "org.openriak.os.version": str(target.operating_system.get("release_version") or target.release),
        "org.openriak.image.tag": target.image,
    }


def render_image_labels(tool, target: Target) -> str:
    lines = []
    for key, value in tool.image_labels(target).items():
        quoted = json.dumps(value).replace("$", r"\$")
        lines.append(f"LABEL {key}={quoted}")
    return "\n".join(lines)


def setting_comment(tool, name: str) -> str:
    canonical = re.sub(r"^OPENRIAK_NODE_\d+_", "OPENRIAK_", name)
    if canonical == "OPENRIAK_HOST":
        canonical = "RIAK_NODE_HOST"
    if canonical == "OPENRIAK_CONTAINER_NAME" and "_NODE_" in name:
        return "Docker container name for this cluster node."
    if canonical not in tool.SETTING_COMMENTS and canonical.startswith("OPENRIAK_"):
        canonical = canonical.replace("OPENRIAK_", "RIAK_", 1)
    return tool.SETTING_COMMENTS[canonical]


def annotate_artifact(tool, contents: str, kind: str, image: str) -> str:
    """Add documentation only, preserving every executable/configuration line."""
    notice = [
        "# Created by TI Tokyo, www.tiot.jp, for the OpenRiak project at https://openriak.org",
        "# WARNING: Edit only if you understand the effect of your changes.",
        f"# Original image tag: {image}",
    ]
    lines = contents.splitlines()
    lines = [line for line in lines if not line.startswith("# Generated and tested by tools/openriak-docker/")]
    insertion = 1 if lines and lines[0].startswith("# syntax=") else 0
    lines[insertion:insertion] = notice
    output = []
    for line in lines:
        match = None
        if kind == "Dockerfile":
            match = re.match(r"ENV ([A-Za-z_][A-Za-z_0-9]*)=", line)
        elif kind == "example.env":
            match = re.match(r"([A-Za-z_][A-Za-z_0-9]*)=", line)
        else:
            match = re.match(r"      ((?:RIAK_|OPENRIAK_)[A-Z_0-9]+|role|TZ):", line)
        if match:
            indent = line[:len(line) - len(line.lstrip())]
            output.append(f"{indent}# {tool.setting_comment(match[1])}")
        output.append(line)
    return "\n".join(output) + "\n"


def render_dockerfile(tool,
    target: Target,
    pinned_base_image: str,
    distributed_cookie: str | None = None,
    *,
    _minimal: bool = True,
) -> str:
    distributed_cookie = distributed_cookie or tool.generate_distributed_cookie()
    checksum = target.package["checksum"]["value"]
    filename = target.package["filename"]
    package_url = target.package["url"]
    runtime_defaults = "\n".join(f"ENV {name}={json.dumps(default)}" for name, (default, _) in tool.RUNTIME_OPTIONS.items())
    source = tool.annotate_artifact(f"""# syntax=docker/dockerfile:1.7
# Generated and tested by tools/openriak-docker/openriak-docker. Do not edit by hand.
# Download and verify in a separate stage; its layers are not in the final image.
FROM scratch AS download
ADD --checksum=sha256:{checksum} {package_url} /{filename}

FROM --platform={target.platform} {pinned_base_image}

{tool.render_image_labels(target)}

# -----------------------------------------------------------------------------
# OpenRiak KV default settings
# Environment settings initialize new configurations; existing riak.conf is preserved.
# -----------------------------------------------------------------------------
{runtime_defaults}
ENV RIAK_NODE_HOST=""
ENV RIAK_NODE_NAME=""
ENV RIAK_DISTRIBUTED_COOKIE="{distributed_cookie}"
ENV RIAK_RING_SIZE="8"
ENV RIAK_STORAGE_BACKEND="leveled"
ENV RIAK_ANTI_ENTROPY="passive"
ENV RIAK_TICTACAAE_ACTIVE="active"
ENV RIAK_TICTACAAE_STOREHEADS="enabled"
ENV RIAK_HTTP_LISTENER="0.0.0.0:8098"
ENV RIAK_PB_LISTENER="0.0.0.0:8087"
ENV RIAK_NOFILE_LIMIT="100000"
ENV RIAK_INIT_ONLY="0"
ENV RIAK_STARTUP_POLL_SECONDS="1"
ENV RIAK_SHUTDOWN_POLL_SECONDS="1"
ENV RIAK_MONITOR_INTERVAL_SECONDS="10"
ENV OPENRIAK_CLUSTER_MODE="single"
ENV OPENRIAK_CLUSTER_CONTROL_DIR="/var/lib/openriak-cluster-control"
ENV OPENRIAK_CLUSTER_POLL_SECONDS="1"
ENV OPENRIAK_CLUSTER_WAIT_SECONDS="300"
ENV role=""

RUN --mount=type=bind,from=download,target=/opt/openriak-package,ro <<'OPENRIAK_PACKAGE_INSTALL'
set -eu
# Copy, install, and remove in this one layer; only the installed files persist.
cp /opt/openriak-package/{filename} /tmp/{filename}
{tool.package_install_script(target)}
OPENRIAK_PACKAGE_INSTALL

RUN <<'OPENRIAK_IMAGE_SETUP'
set -eu
{tool.create_riak_user_script(target)}
test -x /usr/sbin/riak
id riak
mkdir -p /opt/openriak-defaults/etc-riak /var/lib/riak /var/log/riak /run/riak /usr/lib/riak/log
cp -a /etc/riak/. /opt/openriak-defaults/etc-riak/
chown -R riak:riak /var/lib/riak /var/log/riak /run/riak /usr/lib/riak/log
OPENRIAK_IMAGE_SETUP

COPY <<'OPENRIAK_ENTRYPOINT' /usr/local/bin/openriak-entrypoint
{tool.ENTRYPOINT_SCRIPT.rstrip()}
OPENRIAK_ENTRYPOINT

COPY <<'OPENRIAK_HEALTHCHECK' /usr/local/bin/openriak-healthcheck
{tool.HEALTHCHECK_SCRIPT.rstrip()}
OPENRIAK_HEALTHCHECK

RUN <<'OPENRIAK_SCRIPT_SETUP'
set -eu
chmod 0755 /usr/local/bin/openriak-entrypoint
chmod 0755 /usr/local/bin/openriak-healthcheck
OPENRIAK_SCRIPT_SETUP

VOLUME ["/etc/riak"]
VOLUME ["/var/lib/riak"]
VOLUME ["/var/log/riak"]
EXPOSE 8087
EXPOSE 8098
# Health probe interval, maximum duration, startup allowance, and failure threshold.
HEALTHCHECK --interval={target.lifecycle_options.healthcheck_interval}s --timeout={target.lifecycle_options.healthcheck_timeout}s --start-period={target.lifecycle_options.healthcheck_start_period}s --retries={target.lifecycle_options.healthcheck_retries} CMD ["/usr/local/bin/openriak-healthcheck"]
STOPSIGNAL SIGTERM
ENTRYPOINT ["/usr/local/bin/openriak-entrypoint"]
""", "Dockerfile", target.image)


    if _minimal:
        stage = minimal.package_stage(target, pinned_base_image, "runtime", "download", tool.package_install_script(target))
        if stage:
            start = source.index("FROM --platform=")
            end = source.index("LABEL ", start)
            source = source[:start] + stage + "\nFROM package-runtime AS final\n\n" + source[end:]
            # Installation already happened in the isolated installer stage.
            start = source.index("RUN --mount=", source.index("FROM package-runtime AS final"))
            end = source.index("RUN <<'OPENRIAK_IMAGE_SETUP'", start)
            source = source[:start] + source[end:]
    return source


def render_single_compose(tool,
    target: Target,
    distributed_cookie: str | None = None,
    publish_ports: bool = True,
) -> str:
    distributed_cookie = distributed_cookie or tool.generate_distributed_cookie()
    node = target.node_name
    host = tool.default_node_host(1)
    ports = f'''    ports:
      - "${{OPENRIAK_PB_PORT:-8087}}:8087"
      - "${{OPENRIAK_HTTP_PORT:-8098}}:8098"
''' if publish_ports else ""
    return tool.annotate_artifact(f"""# Generated and tested by tools/openriak-docker/openriak-docker. Do not edit by hand.
name: {node}

services:
  node:
    build:
      context: .
      dockerfile: ./Dockerfile
    image: {target.image}
    container_name: "${{OPENRIAK_CONTAINER_NAME:-{node}}}"
    hostname: "${{OPENRIAK_NODE_1_HOST:-{host}}}"
    environment:
{tool.compose_runtime_options()}      RIAK_NODE_HOST: "${{OPENRIAK_NODE_1_HOST:-{host}}}"
      RIAK_DISTRIBUTED_COOKIE: "${{OPENRIAK_DISTRIBUTED_COOKIE:-{distributed_cookie}}}"
      RIAK_MONITOR_INTERVAL_SECONDS: "${{OPENRIAK_MONITOR_INTERVAL_SECONDS:-10}}"
{ports}    volumes:
      - "${{OPENRIAK_CONFIG_PATH:-./{node}/config}}:/etc/riak"
      - "${{OPENRIAK_DATA_PATH:-./{node}/data}}:/var/lib/riak"
      - "${{OPENRIAK_LOGS_PATH:-./{node}/logs}}:/var/log/riak"
    networks:
      openriak:
        aliases:
          - "${{OPENRIAK_NODE_1_HOST:-{host}}}"
    ulimits:
      nofile:
        soft: 100000
        hard: 100000
{tool.compose_resource_options()}    # Time allowed for graceful OpenRiak KV shutdown before Docker sends SIGKILL.
    stop_grace_period: {target.lifecycle_options.stop_grace_period}s

networks:
  openriak:
    driver: bridge
""", "compose.single.yaml", target.image)


def cluster_node_name(tool, target: Target, index: int) -> str:
    return f"{target.node_name}-{index}"


def render_cluster_service(tool,
    target: Target,
    index: int,
    distributed_cookie: str,
    publish_ports: bool,
) -> str:
    node = tool.cluster_node_name(target, index)
    host = tool.default_node_host(index)
    port_prefix = 18000 + (index - 1) * 100
    role_line = "      role: coordinator\n" if index == 1 else ""
    ports = f'''    ports:
      - "${{OPENRIAK_NODE_{index}_PB_PORT:-{port_prefix + 87}}}:8087"
      - "${{OPENRIAK_NODE_{index}_HTTP_PORT:-{port_prefix + 98}}}:8098"
''' if publish_ports else ""
    return f"""  node{index}:
    build:
      context: .
      dockerfile: ./Dockerfile
    image: {target.image}
    container_name: "${{OPENRIAK_NODE_{index}_CONTAINER_NAME:-{node}}}"
    hostname: "${{OPENRIAK_NODE_{index}_HOST:-{host}}}"
    environment:
{tool.compose_runtime_options()}      OPENRIAK_CLUSTER_MODE: cluster
{role_line}      RIAK_NODE_HOST: "${{OPENRIAK_NODE_{index}_HOST:-{host}}}"
      RIAK_DISTRIBUTED_COOKIE: "${{OPENRIAK_DISTRIBUTED_COOKIE:-{distributed_cookie}}}"
      RIAK_MONITOR_INTERVAL_SECONDS: "${{OPENRIAK_MONITOR_INTERVAL_SECONDS:-10}}"
      OPENRIAK_CLUSTER_POLL_SECONDS: "${{OPENRIAK_CLUSTER_POLL_SECONDS:-1}}"
      OPENRIAK_CLUSTER_WAIT_SECONDS: "${{OPENRIAK_CLUSTER_WAIT_SECONDS:-300}}"
{ports}    volumes:
      - "${{OPENRIAK_NODE_{index}_CONFIG_PATH:-./{node}/config}}:/etc/riak"
      - "${{OPENRIAK_NODE_{index}_DATA_PATH:-./{node}/data}}:/var/lib/riak"
      - "${{OPENRIAK_NODE_{index}_LOGS_PATH:-./{node}/logs}}:/var/log/riak"
      - "${{OPENRIAK_CLUSTER_CONTROL_PATH:-./{target.node_name}-cluster-control}}:{tool.CONTROL_DIRECTORY}"
    networks:
      openriak:
        aliases:
          - "${{OPENRIAK_NODE_{index}_HOST:-{host}}}"
    ulimits:
      nofile:
        soft: 100000
        hard: 100000
{tool.compose_resource_options()}    # Time allowed for graceful OpenRiak KV shutdown before Docker sends SIGKILL.
    stop_grace_period: {target.lifecycle_options.stop_grace_period}s
"""


def render_cluster_compose(tool,
    target: Target,
    node_count: int = DEFAULT_CLUSTER_NODES,
    distributed_cookie: str | None = None,
    publish_ports: bool = True,
) -> str:
    if node_count < 2 or node_count > 253:
        raise tool.DockerToolError("Cluster Compose generation supports between 2 and 253 nodes")
    distributed_cookie = distributed_cookie or tool.generate_distributed_cookie()
    services = "\n".join(
        tool.render_cluster_service(target, index, distributed_cookie, publish_ports).rstrip()
        for index in range(1, node_count + 1)
    )
    return tool.annotate_artifact(f"""# Generated and tested by tools/openriak-docker/openriak-docker. Do not edit by hand.
# Set role=coordinator on exactly one service. An omitted or empty role is a follower.
name: {target.node_name}-cluster

services:
{services}

networks:
  openriak:
    driver: bridge
""", "compose.cluster.yaml", target.image)


def render_environment_example(tool,
    target: Target,
    distributed_cookie: str,
    node_count: int = DEFAULT_CLUSTER_NODES,
) -> str:
    lines = [
        "# Copy this file to .env before running either Compose file.",
        "# All values below match the generated defaults and may be edited.",
        "# Every member of one cluster must use the same distributed cookie.",
        *(f"{name}={default}" for name, (default, _) in {**tool.RUNTIME_OPTIONS, **tool.COMPOSE_OPTIONS}.items()),
        f"OPENRIAK_DISTRIBUTED_COOKIE={distributed_cookie}",
        "OPENRIAK_MONITOR_INTERVAL_SECONDS=10",
        "OPENRIAK_CLUSTER_POLL_SECONDS=1",
        "OPENRIAK_CLUSTER_WAIT_SECONDS=300",
        "",
        "# Single-node container, ports, and bind-mount source paths.",
        f"OPENRIAK_CONTAINER_NAME={target.node_name}",
        "OPENRIAK_PB_PORT=8087",
        "OPENRIAK_HTTP_PORT=8098",
        f"OPENRIAK_CONFIG_PATH=./{target.node_name}/config",
        f"OPENRIAK_DATA_PATH=./{target.node_name}/data",
        f"OPENRIAK_LOGS_PATH=./{target.node_name}/logs",
        "",
        "# Cluster-wide shared control-directory source path.",
        f"OPENRIAK_CLUSTER_CONTROL_PATH=./{target.node_name}-cluster-control",
        "",
        "# Cluster node identities, ports, and bind-mount source paths.",
    ]
    for index in range(1, node_count + 1):
        node = tool.cluster_node_name(target, index)
        port_prefix = 18000 + (index - 1) * 100
        lines.extend(
            [
                f"OPENRIAK_NODE_{index}_HOST={tool.default_node_host(index)}",
                f"OPENRIAK_NODE_{index}_CONTAINER_NAME={node}",
                f"OPENRIAK_NODE_{index}_PB_PORT={port_prefix + 87}",
                f"OPENRIAK_NODE_{index}_HTTP_PORT={port_prefix + 98}",
                f"OPENRIAK_NODE_{index}_CONFIG_PATH=./{node}/config",
                f"OPENRIAK_NODE_{index}_DATA_PATH=./{node}/data",
                f"OPENRIAK_NODE_{index}_LOGS_PATH=./{node}/logs",
                "",
            ]
        )
    return tool.annotate_artifact("\n".join(lines), "example.env", target.image)


def render_multiarch_dockerfile(tool,
    targets: list[Target], base_images: dict[str, dict[str, str]], cookie: str, tags: list[str],
) -> str:
    if not targets or len({(t.version, t.family, t.release, t.otp) for t in targets}) != 1:
        raise tool.DockerToolError("A shared Dockerfile requires one version, OS release, and OTP")
    if len({t.platform.split("/")[1] for t in targets}) != len(targets):
        raise tool.DockerToolError("Multiple variants of the same TARGETARCH require separate image groups")
    stages = []
    for target in sorted(targets, key=lambda t: t.platform):
        stage = target.platform.split("/")[1]
        pinned = base_images[target.platform]["pinned"]
        if not re.search(r"@sha256:[0-9a-f]{64}$", pinned):
            raise tool.DockerToolError(f"Unpinned base image for {target.platform}")
        checksum = target.package["checksum"]["value"]
        isolated_stage = minimal.package_stage(target, pinned, stage, f"download-{stage}", tool.package_install_script(target))
        if isolated_stage:
            stages.append(f"FROM scratch AS download-{stage}\nADD --checksum=sha256:{checksum} {target.package['url']} /{target.package['filename']}\n\n" + isolated_stage)
            continue
        stages.append(f'''# {target.platform}: official package and immutable OS release base.
# Download layers stay outside the final image; the install only mounts them.
FROM scratch AS download-{stage}
ADD --checksum=sha256:{checksum} {target.package['url']} /{target.package['filename']}

FROM --platform={target.platform} {pinned} AS package-{stage}
RUN --mount=type=bind,from=download-{stage},target=/opt/openriak-package,ro <<'OPENRIAK_PACKAGE_INSTALL'
set -eu
# Copy, install, and remove in this one layer; only the installed files persist.
cp /opt/openriak-package/{target.package['filename']} /tmp/{target.package['filename']}
{tool.package_install_script(target)}
OPENRIAK_PACKAGE_INSTALL
''')
    reference = tool.render_dockerfile(targets[0], base_images[targets[0].platform]["pinned"], cookie, _minimal=False)
    defaults = reference[reference.index("# -----------------------------------------------------------------------------"):reference.index("RUN --mount=")]
    runtime = reference[reference.index("RUN <<'OPENRIAK_IMAGE_SETUP'"):]
    header = tool.annotate_artifact("# syntax=docker/dockerfile:1.7\n", "Dockerfile", targets[0].image)
    header += "# Supported platforms: " + ", ".join(t.platform for t in targets) + "\n"
    header += "# Image tags: " + ", ".join(tags) + "\n"
    header += "# BuildKit supplies TARGETARCH from --platform in the global scope.\n# Do not redeclare ARG TARGETARCH here: that clears its automatic value.\n\n"
    return header + "\n".join(stages) + '\nFROM package-${TARGETARCH} AS final\n\n' + tool.render_image_labels(targets[0]) + '\n\n' + defaults + runtime


def render_group_assets(tool, targets: list[Target], bases: dict[str, dict[str, str]], cookie: str,
                        tags: list[str], cluster_nodes: int, destination: pathlib.Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    target = targets[0]
    (destination / "Dockerfile").write_text(tool.render_multiarch_dockerfile(targets, bases, cookie, tags))
    (destination / "compose.single.yaml").write_text(tool.render_single_compose(target, cookie))
    (destination / "compose.cluster.yaml").write_text(tool.render_cluster_compose(target, cluster_nodes, cookie))
    (destination / "example.env").write_text(tool.render_environment_example(target, cookie, cluster_nodes))
