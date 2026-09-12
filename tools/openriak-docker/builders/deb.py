"""Debian package installation shared by Debian and Ubuntu."""
def install(tool, target, context):
    package_path = context["package_path"]
    return f"""{tool.debian_repository_setup(target)}# Update installed OS packages from this release's configured repositories.
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y --no-install-recommends
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates passwd procps tzdata {package_path}
apt-get clean
rm -rf /var/lib/apt/lists/*
rm -f {package_path}"""
