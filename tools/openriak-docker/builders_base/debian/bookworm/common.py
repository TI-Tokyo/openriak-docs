"""Bookworm reusable base: OpenSSL/libblkid backports, tar removal and checks."""
import json
import images.minimal as minimal

BUILD_DEPENDENCIES = ('../../../builders/debian/bookworm/backports.py', '../../../images/minimal.py')


def render_header(target, tool, context):
    identity = target.identity
    image = f"{identity.namespace}/{minimal.configuration(target)['base_image']}"
    source = tool.annotate_artifact('# syntax=docker/dockerfile:1.7\n', 'Dockerfile', image)
    source += '# Reusable Debian base; no OpenRiak KV package or Erlang cookie is installed here.\n'
    source += '# BuildKit supplies TARGETARCH from --platform.\n\n'
    return source


def render_stage(target, pinned, tool, context):
    arch = target.platform.split('/')[1]
    source = ''
    source += minimal.openssl_build_stage(target, pinned, arch)
    source += minimal.libblkid_build_stage(target, pinned, arch)
    source += f'''FROM --platform={target.platform} {pinned} AS patched-install-{arch}
RUN --mount=type=bind,from=openssl-build-{arch},source=/packages,target=/opt/openssl-packages,ro --mount=type=bind,from=libblkid-build-{arch},source=/packages,target=/opt/libblkid-packages,ro <<'OPENRIAK_PATCHED_BASE'
set -eu
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y --no-install-recommends
if installed_openssl=$(dpkg-query -W -f='${{Version}}' libssl3 2>/dev/null)
then
    :
else
    installed_openssl=0
fi
# Retain newer Debian fixes; never downgrade an installed vendor package.
if dpkg --compare-versions "$installed_openssl" lt '{minimal.OPENSSL_DEB_VERSION}'
then
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends /opt/openssl-packages/*.deb
else
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends openssl
fi
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates
if dpkg --compare-versions "$(dpkg-query -W -f='${{Version}}' libblkid1)" lt '{minimal.LIBBLKID_DEB_VERSION}'
then
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends /opt/libblkid-packages/*.deb
fi
ldconfig
mkdir -p /usr/share/openriak-build
dpkg-query -W libssl3 openssl > /usr/share/openriak-build/openssl-packages.txt
dpkg-query -W libblkid1 > /usr/share/openriak-build/libblkid-packages.txt
# Retain compact upstream-test evidence, not compilers or downloaded packages.
cp /opt/libblkid-packages/libblkid-tests.log /opt/libblkid-packages/libblkid-regression.log /usr/share/openriak-build/
apt-get clean
rm -rf /var/lib/apt/lists/*
{minimal.remove_tar_script()}
OPENRIAK_PATCHED_BASE

# Flatten the patched Debian filesystem so replaced vulnerable bytes do not remain in lower layers.
FROM scratch AS patched-{arch}
COPY --from=patched-install-{arch} / /

'''
    return source


def render_footer(target, tool, context):
    identity = target.identity
    source = ''
    labels = {
        'org.opencontainers.image.title': 'Debian Bookworm slim for OpenRiak',
        'org.opencontainers.image.description': 'Tar-free Debian 12 runtime base with tested OpenSSL and libblkid security backports',
        'org.opencontainers.image.vendor': identity.vendor,
        'org.opencontainers.image.source': identity.source,
        'org.opencontainers.image.url': identity.url,
        'org.opencontainers.image.version': 'bookworm-slim-for-openriak',
        'org.openriak.os.name': 'debian', 'org.openriak.os.release': 'bookworm',
        'org.openriak.os.version': '12', 'org.openriak.openssl.minimum-version': minimal.OPENSSL_DEB_VERSION,
        'org.openriak.libblkid.minimum-version': minimal.LIBBLKID_DEB_VERSION,
    }
    source += 'FROM patched-${TARGETARCH} AS final\n'
    source += '\n'.join(f'LABEL {key}={json.dumps(value)}' for key, value in labels.items())
    return source + '''
# Standard Debian executable search path.
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
CMD ["bash"]
'''


def runtime_check(target, context):
    return f'''set -eu
. /etc/os-release
test "$ID" = debian
test "$VERSION_ID" = 12
test ! -d /usr/lib/riak
test ! -d /build
test ! -d /sources
test ! -e /usr/bin/gcc
test ! -e /opt/openssl-packages
test ! -e /opt/libblkid-packages
test ! -e /bin/tar
test ! -e /usr/bin/tar
test -s /usr/share/openriak-build/libblkid-regression.log
dpkg --compare-versions "$(dpkg-query -W -f='${{Version}}' libblkid1)" eq '{minimal.LIBBLKID_DEB_VERSION}'
test -s /usr/share/openriak-build/openssl-packages.txt
dpkg --compare-versions "$(dpkg-query -W -f='${{Version}}' libssl3)" ge '{minimal.OPENSSL_DEB_VERSION}'
openssl version -a
printf abc > /tmp/digest-input
openssl dgst -sha256 /tmp/digest-input > /tmp/digest-result
grep -q ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad /tmp/digest-result
openssl req -x509 -newkey rsa:2048 -nodes -days 1 -subj /CN=base-test -keyout /tmp/key.pem -out /tmp/cert.pem
openssl verify -CAfile /tmp/cert.pem /tmp/cert.pem
'''
