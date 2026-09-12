"""Runtime filesystem strategies, enabled per OS release only after validation."""
from __future__ import annotations
from builders.debian.bookworm import backports
from builders.debian.bookworm.backports import OPENSSL_VERSION, OPENSSL_DEB_VERSION, OPENSSL_SOURCE_SHA256, OPENSSL_PACKAGING_SHA256, LIBBLKID_DEB_VERSION, LIBBLKID_SOURCE_SHA256, LIBBLKID_PACKAGING_SHA256, LIBBLKID_PATCH_SHA256, LIBBLKID_REGRESSION, OPENSSL_TEST_PATCH
import sys
import json
import re
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config/runtime-images.json"
RUNTIME_PACKAGES = (
    'bash coreutils findutils gawk grep sed ca-certificates '
    'glibc glibc-minimal-langpack hostname libgcc libstdc++ ncurses-libs '
    'openssl-libs pam procps-ng shadow-utils sudo util-linux zlib tzdata'
)





def libblkid_build_stage(target, pinned, stage):
    return backports.libblkid_build_stage(target, pinned, stage)


def remove_tar_script():
    return '''# dpkg requires tar for installation. It is deliberately absent at runtime.
# Child builds supply a pinned build-only tar and reinstall it before using apt.
dpkg --purge --force-remove-essential --force-depends tar
test ! -e /bin/tar
test ! -e /usr/bin/tar
'''


# Test-only platform detection; no OpenSSL library code or IPv6 feature is disabled.

def openssl_build_stage(target, pinned, stage):
    return backports.openssl_build_stage(target, pinned, stage)


class ConfigurationError(RuntimeError):
    """An invalid runtime strategy should stop generation, never silently fall back."""


def configuration(target):
    config = json.loads(CONFIG_PATH.read_text())
    if not isinstance(config, dict) or config.get('schema_version') != 1:
        raise ConfigurationError('Unsupported runtime-images.json schema')
    releases = config.get('releases', {})
    if not isinstance(releases, dict) or not isinstance(releases.get(target.family, {}), dict):
        raise ConfigurationError('runtime-images.json releases must map OS families to release objects')
    mode = releases.get(target.family, {}).get(target.release)
    if mode is not None and (not isinstance(mode, dict) or mode.get('strategy') not in ('rpm-root', 'clean-root')):
        raise ConfigurationError(f'Invalid runtime strategy for {target.family} {target.release}')
    if mode and mode['strategy'] == 'rpm-root':
        package = mode.get('release_package', '')
        if not isinstance(package, str) or not re.fullmatch(r'[a-z0-9][a-z0-9+._-]*', package):
            raise ConfigurationError(f'Invalid release package for {target.family} {target.release}')
        if target.operating_system['package_family'] != 'rpm':
            raise ConfigurationError(f'rpm-root requires RPM packages: {target.family} {target.release}')
    if mode and 'openssl_backport' in mode:
        if (target.family, target.release, mode['strategy'], mode['openssl_backport']) != (
                'debian', '12', 'clean-root', OPENSSL_VERSION):
            raise ConfigurationError('OpenSSL backport is validated only for Debian 12 / OpenSSL 3.0.22')
    if mode and 'base_image' in mode:
        valid_debian = (target.family, target.release, mode.get('openssl_backport'), mode['base_image']) == (
                'debian', '12', OPENSSL_VERSION, 'debian:bookworm-slim-for-openriak')
        valid_el9 = (target.family in ('rhel', 'centos') and target.release == '9'
                     and mode['strategy'] == 'rpm-root'
                     and mode.get('pcre2_backport') == '10.40-6.el9.openriak1'
                     and mode['base_image'] == {'rhel': 'rhel:9-for-openriak',
                                               'centos': 'centos:stream9-for-openriak'}[target.family])
        if not (valid_debian or valid_el9):
            raise ConfigurationError('Unsupported patched base image configuration')
    if mode and 'remove_packages' in mode:
        packages = mode['remove_packages']
        if (target.operating_system['package_family'] != 'rpm' or not isinstance(packages, list)
                or not packages or any(not isinstance(p, str) or not re.fullmatch(r'[a-z0-9][a-z0-9+._-]*', p) for p in packages)):
            raise ConfigurationError('remove_packages requires a list of exact RPM package names')
    if mode and 'minimum_packages' in mode:
        packages = mode['minimum_packages']
        if (target.operating_system['package_family'] not in ('deb', 'rpm') or not isinstance(packages, dict)
                or not packages or any(not isinstance(p, str) or not re.fullmatch(r'[a-z0-9][a-z0-9+._-]*', p)
                    or not isinstance(v, str) or not re.fullmatch(r'[A-Za-z0-9._+:~\-]+', v)
                    for p, v in packages.items())):
            raise ConfigurationError('minimum_packages requires Debian or RPM package names and versions')
    if mode and 'remove_tar' in mode and (not isinstance(mode['remove_tar'], bool)
            or target.operating_system['package_family'] != 'deb'):
        raise ConfigurationError('remove_tar requires a boolean for a Debian-family image')
    if mode and 'perl_removal' in mode and (mode['perl_removal'] not in ('apt', 'dpkg')
            or target.operating_system['package_family'] != 'deb'):
        raise ConfigurationError('perl_removal requires apt or dpkg for a Debian-family image')
    return mode


def minimum_package_check(mode, package_family='deb', root=''):
    if package_family == 'rpm':
        command = f'rpm --root {root}' if root else 'rpm'
        checks = ''
        for package, version in mode.get('minimum_packages', {}).items():
            epoch, evr = version.split(':', 1) if ':' in version else ('0', version)
            upstream, release = evr.rsplit('-', 1) if '-' in evr else (evr, '')
            # Native RPM comparison, including epochs, tilde and release numbers.
            # The installed value enters Lua through the environment, never as code.
            checks += f'''# Require {package} >= {version}; keep newer vendor updates.
installed_rpm=$({command} -q --qf '%{{EPOCHNUM}} %{{VERSION}} %{{RELEASE}}' {package})
OPENRIAK_RPM_VERSION="$installed_rpm" rpm --eval '%{{lua:
local e, v, r = os.getenv("OPENRIAK_RPM_VERSION"):match("^(%d+) ([^ ]+) ([^ ]+)$")
assert(e, "Cannot identify installed {package} version")
local comparison = rpm.vercmp(e, "{epoch}")
if comparison == 0 then comparison = rpm.vercmp(v, "{upstream}") end
if comparison == 0 then comparison = rpm.vercmp(r, "{release}") end
assert(comparison >= 0, "Installed {package} is older than {version}")
}}' >/dev/null
'''
        return checks
    return ''.join(f"dpkg --compare-versions \"$(dpkg-query -W -f='${{Version}}' {package})\" ge '{version}'\n"
                   for package, version in mode.get('minimum_packages', {}).items())


def remove_rpm_packages(mode, root=''):
    packages = ' '.join(mode.get('remove_packages', []))
    if not packages:
        return ''
    command = f'rpm --root {root}' if root else 'rpm'
    return f'''# Remove optional runtime tools only after all installation operations.
# Keep dependency checks: an unexpected remaining dependency fails the build.
remove_packages=
for package in {packages}
do
    if {command} -q "$package" >/dev/null 2>&1
    then
        remove_packages="$remove_packages $package"
    fi
done
if [ -n "$remove_packages" ]
then
    {command} -e $remove_packages
fi
for package in {packages}
do
    if {command} -q "$package" >/dev/null 2>&1
    then
        echo "Unexpected runtime package: $package" >&2
        exit 1
    fi
done
'''


def removed_runtime_check(mode):
    packages = mode.get('remove_packages', [])
    check = ''
    if 'sudo' in packages:
        check += 'test ! -e /usr/bin/sudo\ntest ! -e /usr/bin/sudoreplay\n'
        check += "! grep -Eq '^[[:space:]]*sudo ' /usr/sbin/riak\n"
    if 'vim-minimal' in packages:
        check += 'test ! -e /usr/bin/vi\ntest ! -e /usr/bin/vim\ntest ! -d /usr/share/vim\n'
    if 'libssh' in packages:
        check += '''if find /usr /lib /lib64 -name 'libssh.so*' | grep .
then
    echo 'Unexpected libssh runtime library' >&2
    exit 1
fi
'''
    return check


def launcher_without_sudo(mode, root=''):
    if 'sudo' not in mode.get('remove_packages', []):
        return ''
    return f'''# The official RPM launcher uses sudo only to run commands as riak.
# runuser is supplied by util-linux, preserves argument boundaries, and sets HOME.
# Keep the rest of the package launcher (including PID cleanup) unchanged.
test -x {root}/usr/sbin/runuser
sed -i 's/sudo -H -E -u riak --/runuser -u riak --/' {root}/usr/sbin/riak
if grep -Eq '^[[:space:]]*sudo ' {root}/usr/sbin/riak
then
    echo 'Unsupported sudo invocation in OpenRiak KV launcher' >&2
    exit 1
fi
'''


def runtime_check(target):
    mode = configuration(target)
    if not mode:
        return None
    if mode['strategy'] == 'rpm-root':
        return removed_runtime_check(mode) + r'''for name in python python3 perl pip pip3 dnf yum microdnf rpm
do
    if command -v "$name" >/dev/null 2>&1
    then
        echo "Unexpected runtime command: $name" >&2
        exit 1
    fi
done
if find /usr /opt -type f \( -iname '*python*' -o -iname '*setuptools*' -o -name perl \) | grep .
then
    echo 'Unexpected interpreter files' >&2
    exit 1
fi
test -s /usr/share/openriak-build/runtime-packages.txt
test -s /etc/os-release
'''
    if target.operating_system['package_family'] == 'deb':
        check = 'test ! -e /usr/bin/perl\ntest ! -e /usr/bin/python3\ntest -s /var/lib/dpkg/status\n'
        check += minimum_package_check(mode)
        if mode.get('remove_tar'):
            check += 'test ! -e /bin/tar\ntest ! -e /usr/bin/tar\n'
        if mode.get('libblkid_backport'):
            check += f'''test ! -e /bin/tar
test ! -e /usr/bin/tar
test ! -e /usr/local/bin/tar
test -s /usr/share/openriak-build/libblkid-packages.txt
dpkg --compare-versions "$(dpkg-query -W -f='${{Version}}' libblkid1)" eq '{LIBBLKID_DEB_VERSION}'
'''
        if mode.get('openssl_backport'):
            check += f'''test ! -e /usr/bin/gcc
test ! -d /build
test -s /usr/share/openriak-build/openssl-packages.txt
dpkg --compare-versions "$(dpkg-query -W -f='${{Version}}' libssl3)" ge '{OPENSSL_DEB_VERSION}'
openssl version
'''
        return check
    return (removed_runtime_check(mode) + minimum_package_check(
        mode, target.operating_system['package_family'])) or None


def package_stage(target, pinned, stage, download, install_script, *, base_only=False):
    mode = configuration(target)
    if mode is None:
        return None
    filename = target.package['filename']
    if mode['strategy'] == 'clean-root':
        from builders.registry import minimal_setup
        build_stage, package_mount, bootstrap, extra = minimal_setup(sys.modules[__name__], target, pinned, stage, mode)
        if target.operating_system['package_family'] == 'deb':
            extra += '# Require the reviewed security updates; reject stale mirrors.\n' + minimum_package_check(mode)
            if mode.get('perl_removal') == 'dpkg':
                extra += '''# Essential installation helpers depend on Perl on this release.
# Keep PAM/login and remove only Perl after every installation script has run.
# As with runtime tar removal, package maintenance belongs in the build stage.
dpkg --purge --force-remove-essential --force-depends perl-base
test ! -e /usr/bin/perl
'''
            else:
                extra += """# The runtime does not execute Perl; remove it and dependent tools explicitly.
# This is a final runtime filesystem, not a general-purpose administration image.
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get purge -y --allow-remove-essential perl-base
"""
            extra += """
apt-get clean
rm -rf /var/lib/apt/lists/*
"""
        elif mode.get('minimum_packages'):
            extra += '# Require the reviewed security updates; reject stale mirrors.\n'
            extra += minimum_package_check(mode, target.operating_system['package_family'])
        if mode.get('libblkid_backport'):
            extra += f'''dpkg --compare-versions "$(dpkg-query -W -f='${{Version}}' libblkid1)" eq '{LIBBLKID_DEB_VERSION}'
'''
            extra += remove_tar_script()
        elif mode.get('remove_tar'):
            extra += remove_tar_script()
        extra += remove_rpm_packages(mode)
        extra += launcher_without_sudo(mode)
        return f'''{build_stage}FROM --platform={target.platform} {pinned} AS install-{stage}
RUN --mount=type=bind,from={download},target=/opt/openriak-package,ro{package_mount} <<'OPENRIAK_PACKAGE_INSTALL'
set -eu
{bootstrap}
cp /opt/openriak-package/{filename} /tmp/{filename}
{install_script}
{extra}OPENRIAK_PACKAGE_INSTALL

# Export the cleaned filesystem; removed base-image files cannot remain in layers.
FROM scratch AS package-{stage}
COPY --from=install-{stage} / /
# Shell command search path for OpenRiak KV lifecycle scripts.
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
'''
    if mode['strategy'] != 'rpm-root':
        raise ConfigurationError(f"Unknown runtime strategy: {mode['strategy']}")
    packages = mode['release_package'] + ' ' + ' '.join(p for p in RUNTIME_PACKAGES.split()
                                                       if p not in mode.get('remove_packages', []))
    from builders.registry import minimal_repositories
    repository_setup = minimal_repositories(target, install_script)
    stage_prefix = ''
    root_copy = ''
    mount = f' --mount=type=bind,from={download},target=/opt/openriak-package,ro'
    package_install = f'''# Install the verified official package; its OTP runtime is bundled in the RPM.
rpm --root /openriak-rootfs -Uvh --replacepkgs --nodeps /opt/openriak-package/{filename}
'''
    if base_only:
        if not mode.get('pcre2_backport'):
            raise ConfigurationError('RPM base generation requires a configured backport')
        from builders.pcre2 import rpm_repositories
        repository_setup = rpm_repositories(target, install_script)
        mount = ''
        package_install = ''
    elif mode.get('base_image'):
        tools_image = mode.get('package_tools_image', '')
        expected_tools = {'rhel': 'registry.access.redhat.com/ubi9/ubi:9.8',
                          'centos': 'quay.io/centos/centos:stream9'}[target.family]
        if not re.fullmatch(re.escape(expected_tools) + r'@sha256:[0-9a-f]{64}', tools_image):
            raise ConfigurationError('Patched RPM bases require a pinned tools image for the same OS release')
        stage_prefix = f'FROM --platform={target.platform} {pinned} AS runtime-base-{stage}\n'
        pinned = tools_image
        root_copy = f'COPY --from=runtime-base-{stage} / /openriak-rootfs/\n'
    return f'''{stage_prefix}# The full OS image is an installer only; none of its layers reach runtime.
FROM --platform={target.platform} {pinned} AS install-{stage}
{root_copy}RUN{mount} <<'OPENRIAK_PACKAGE_INSTALL'
set -eu
# Resolve runtime packages from this OS release, without weak dependencies.
{repository_setup}# Slim installers may provide only microdnf. Full dnf is build-only.
if ! command -v dnf >/dev/null 2>&1
then
    microdnf install -y dnf
fi
mkdir -p /openriak-rootfs
dnf install -y --refresh --installroot=/openriak-rootfs --releasever={target.release} --setopt=install_weak_deps=False --setopt=tsflags=nodocs {packages}
{package_install}{remove_rpm_packages(mode, '/openriak-rootfs')}\
{launcher_without_sudo(mode, '/openriak-rootfs')}\
# Reject stale repository mirrors before exporting the runtime filesystem.
{minimum_package_check(mode, 'rpm', '/openriak-rootfs')}\
# Preserve the RPM database and an explicit inventory for vulnerability scanners.
mkdir -p /openriak-rootfs/usr/share/openriak-build
rpm --root /openriak-rootfs -qa --qf '%{{NAME}} %{{VERSION}}-%{{RELEASE}}\\n' > /openriak-rootfs/usr/share/openriak-build/runtime-packages.txt
# Install escript's compatibility link without retaining the installer tools.
for bundled_escript in /openriak-rootfs/usr/lib64/riak/erts-*/bin/escript /openriak-rootfs/usr/lib/riak/erts-*/bin/escript
do
    if [ -x "$bundled_escript" ]
    then
        ln -sf "${{bundled_escript#/openriak-rootfs}}" /openriak-rootfs/usr/bin/escript
        break
    fi
done
# These are cache files from installation, not runtime packages or inventory.
rm -rf /openriak-rootfs/var/cache/dnf /openriak-rootfs/var/cache/yum
rm -rf /openriak-rootfs/var/log/dnf* /openriak-rootfs/var/log/yum*
# libstdc++ includes Python helpers for GDB, which is not in this runtime.
# Keep libstdc++ itself; remove only these unused debugger scripts/bytecode.
rm -rf /openriak-rootfs/usr/share/gcc-*/python /openriak-rootfs/usr/share/gdb/auto-load
# Fail if package dependencies reintroduce interpreters or package managers.
if grep -Ei '^(python[^ ]*|platform-python[^ ]*|perl[^ ]*|dnf[^ ]*|yum[^ ]*|microdnf|rpm) ' /openriak-rootfs/usr/share/openriak-build/runtime-packages.txt
then
    echo 'Unexpected runtime interpreter or package manager' >&2
    exit 1
fi
OPENRIAK_PACKAGE_INSTALL

FROM scratch AS package-{stage}
COPY --from=install-{stage} /openriak-rootfs/ /
# Standard command search path for the shell-based OpenRiak KV lifecycle.
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
'''
