"""Suse family installation policy."""
def configure(tool, target, context):
    context["official_rpm"] = True
    context["suse_openssl"] = "libopenssl3" if target.operating_system.get("alias_of", "").startswith("rhel-9-") else "libopenssl1_1"
    context["runtime_cleanup"] = """# Repository registration is only needed during installation, not by OpenRiak KV.
# Remove the helper and its embedded Go runtime after all repository operations.
# Keep RPM dependency checks: fail rather than remove any dependent package.
if rpm -q container-suseconnect >/dev/null 2>&1
then
    rpm -e container-suseconnect
fi
test ! -e /usr/bin/container-suseconnect
"""
