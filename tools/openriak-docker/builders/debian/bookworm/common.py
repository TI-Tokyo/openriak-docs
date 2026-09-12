"""Debian 12 patched-base installation hooks."""
import re

BUILD_DEPENDENCIES = ("backports.py",)


def prepare_minimal(minimal, target, pinned, stage, mode):
    extra = ''
    build_stage = ''
    package_mount = ''
    bootstrap = ''
    if mode.get('libblkid_backport'):
        tools_image = mode.get('package_tools_image', '')
        if not re.fullmatch(r'debian:bookworm-slim@sha256:[0-9a-f]{64}', tools_image):
            raise minimal.ConfigurationError('Debian tar bootstrap requires a pinned Bookworm tools image')
        build_stage += f'FROM --platform={target.platform} {tools_image} AS package-tools-{stage}\n'
        package_mount += f' --mount=type=bind,from=package-tools-{stage},source=/usr/bin/tar,target=/usr/local/bin/tar,ro'
        bootstrap = '''# The reusable runtime base omits tar. Borrow it only for package installation.
# dpkg checks /bin/tar even when the mount is available in /usr/local/bin.
cp /usr/local/bin/tar /bin/tar
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tar
'''
    if mode.get('openssl_backport') and not mode.get('base_image'):
        build_stage = minimal.openssl_build_stage(target, pinned, stage)
        package_mount = f' --mount=type=bind,from=openssl-build-{stage},source=/packages,target=/opt/openssl-packages,ro'
        extra = f'''# Upgrade both libraries and CLI with dpkg-tracked packages; retain newer vendor fixes.
installed_openssl=$(dpkg-query -W -f='${{Version}}' libssl3)
if dpkg --compare-versions "$installed_openssl" lt '{minimal.OPENSSL_DEB_VERSION}'
then
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends /opt/openssl-packages/*.deb
fi
ldconfig
mkdir -p /usr/share/openriak-build
dpkg-query -W libssl3 openssl > /usr/share/openriak-build/openssl-packages.txt
'''
    elif mode.get('base_image'):
        extra = f'''# Require the tested patched base; fail rather than build with older libraries.
dpkg --compare-versions "$(dpkg-query -W -f='${{Version}}' libssl3)" ge '{minimal.OPENSSL_DEB_VERSION}'
test -s /usr/share/openriak-build/openssl-packages.txt
'''
    return build_stage, package_mount, bootstrap, extra
