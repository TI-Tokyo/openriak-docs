"""Final signed Debian 11 repositories after public LTS ended."""
import re
def repositories(tool, target):
    """Use signed final snapshots for explicitly configured EOL Debian releases."""
    if target.family != "debian":
        return ""
    config = tool.read_json(tool.BASE_IMAGES_PATH)
    entry = config["families"]["debian"]
    snapshot = entry.get("apt_snapshots", {}).get(target.release)
    if snapshot is None:
        return ""
    codename = config["release_maps"][entry["release_map"]][target.release]
    if not re.fullmatch(r"[0-9]{8}T[0-9]{6}Z", snapshot) or not re.fullmatch(r"[a-z]+", codename):
        raise tool.DockerToolError(f"Invalid Debian APT snapshot configuration for {target.release}")
    return f"""# Debian {target.release} public security support has ended; retain its final signed updates.
# Only these dated snapshots may have expired Release metadata. Signatures and
# package hashes are still verified using the Debian archive keyring.
# HTTP bootstraps the slim image before ca-certificates is installed.
rm -f /etc/apt/sources.list.d/debian.sources
cat > /etc/apt/sources.list <<'OPENRIAK_DEBIAN_SOURCES'
deb [check-valid-until=no signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] http://snapshot.debian.org/archive/debian/{snapshot}/ {codename} main
deb [check-valid-until=no signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] http://snapshot.debian.org/archive/debian/{snapshot}/ {codename}-updates main
deb [check-valid-until=no signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] http://snapshot.debian.org/archive/debian-security/{snapshot}/ {codename}-security main
OPENRIAK_DEBIAN_SOURCES
"""
