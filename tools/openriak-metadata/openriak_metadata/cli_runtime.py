"""Read a release image in a disposable, network-isolated container."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import uuid

DEFAULT_IMAGE = "tiotjp/openriak-kv:{version}-alpine-3.24"
PROBE = Path(__file__).parent / "probes" / "cli.escript"


def run(*args: str, timeout: int = 120, input: str | None = None) -> str:
    try:
        result = subprocess.run(args, input=input, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        raise ValueError(f"CLI discovery timed out: {' '.join(args[:3])}") from error
    if result.returncode:
        raise ValueError(f"CLI discovery command failed ({' '.join(args[:3])}): {result.stderr.strip()}\n{result.stdout[-3000:]}")
    return result.stdout


def inspect_runtime(version: str, image: str | None, *, refresh: bool = False,
                    extra_modules: list[str] | None = None) -> dict:
    tag = (image or DEFAULT_IMAGE).replace("{version}", version)
    if not tag or tag.startswith("-") or any(c.isspace() for c in tag):
        raise ValueError("--runtime-image must be an image tag or digest")
    try:
        inspected = json.loads(run("docker", "image", "inspect", tag))[0]
    except ValueError as error:
        if not any(message in str(error).lower() for message in ('no such image', 'no such object')):
            raise
        run("docker", "pull", tag, timeout=600)
        inspected = json.loads(run("docker", "image", "inspect", tag))[0]
    else:
        if refresh:
            run("docker", "pull", tag, timeout=600)
            inspected = json.loads(run("docker", "image", "inspect", tag))[0]
    identity = inspected["Id"]
    label_version = (inspected.get("Config", {}).get("Labels") or {}).get("org.opencontainers.image.version")
    if label_version and label_version != version:
        raise ValueError(f"Runtime image identifies release {label_version}, requested {version}")
    name = "openriak-metadata-cli-" + uuid.uuid4().hex
    script = r'''
set -eu
for root in /usr/lib/riak /opt/riak /usr/local/lib/riak; do
    if [ -d "$root/bin" ] && [ -d "$root/lib" ]; then break; fi
done
test -d "$root/lib"
printf '%s\n' "$root" > /tmp/cli-root
cat > /tmp/cli.escript
boot=$(find "$root/releases" -name start_clean.boot | sort | tail -1)
test -n "$boot"
export ERL_FLAGS="+S 2:2 +A 2 -boot ${boot%.boot}"
for escript in "$root"/erts-*/bin/escript; do test -x "$escript" && break; done
"$escript" /tmp/cli.escript "$root" "$@"
'''
    created = False
    try:
        run("docker", "create", "--name", name, "--network", "none", "--no-healthcheck",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges", "--read-only",
            "--tmpfs", "/tmp:rw,nosuid,size=128m", "--entrypoint", "/bin/sh", "-i",
            identity, "-c", script, "cli-probe", *(extra_modules or []))
        created = True
        # stdin supplies code only; no host source tree or Docker socket is mounted.
        output = run("docker", "start", "-a", "-i", name, input=PROBE.read_text(), timeout=180)
        if "OPENRIAK_CLI_JSON_BEGIN\n" not in output:
            raise ValueError("Runtime probe produced no CLI inventory: " + output[-2000:])
        inventory = json.loads(output.split("OPENRIAK_CLI_JSON_BEGIN\n", 1)[1].split("\nOPENRIAK_CLI_JSON_END", 1)[0])
        # Read scripts from the stopped container; docker cp does not run them.
        import tempfile
        with tempfile.TemporaryDirectory(prefix="openriak-cli-image-") as temporary:
            folder = Path(temporary)
            # Root is encoded in the probe's inventory; /tmp tmpfs vanishes on exit.
            root = inventory["root"]
            run("docker", "cp", f"{name}:{root}/bin", str(folder / "bin"))
            inventory["scripts"] = {}
            for path in sorted((folder / "bin").iterdir()):
                if path.is_file() and not path.is_symlink():
                    data = path.read_bytes()
                    if data.startswith(b"#!"):
                        inventory["scripts"][path.name] = {
                            "path": root + "/bin/" + path.name,
                            "sha256": hashlib.sha256(data).hexdigest(),
                            "text": data.decode("utf-8", "replace"),
                        }
        inventory["image"] = {"tag": tag, "id": identity, "digests": inspected.get("RepoDigests", []),
                              "version_label": label_version}
        return inventory
    finally:
        if created:
            run("docker", "rm", "-f", "-v", name, timeout=30)
