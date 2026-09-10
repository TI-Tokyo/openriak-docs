"""Runtime filesystem strategies, enabled per OS release only after validation."""
from __future__ import annotations
import json
import re
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("runtime-images.json")
RUNTIME_PACKAGES = (
    'bash coreutils findutils gawk grep sed ca-certificates '
    'glibc glibc-minimal-langpack hostname libgcc libstdc++ ncurses-libs '
    'openssl-libs pam procps-ng shadow-utils sudo util-linux zlib tzdata'
)

# Upstream release and Debian Bookworm packaging, both pinned to reviewed bytes.
OPENSSL_VERSION = '3.0.22'
OPENSSL_DEB_VERSION = '3.0.22-0openriak1~deb12u1'
OPENSSL_SOURCE_SHA256 = '67ebca7e50d17383028045486653492195b83db95f8558709701bb47b5c1ef81'
OPENSSL_PACKAGING_SHA256 = '7279efe85c359500c95aa88347e3395dd303d7566e2bb818d80d96e0c3bb9629'

LIBBLKID_DEB_VERSION = '2.38.1-5+deb12u3+openriak1'
LIBBLKID_SOURCE_SHA256 = '60492a19b44e6cf9a3ddff68325b333b8b52b6c59ce3ebd6a0ecaa4c5117e84f'
LIBBLKID_PACKAGING_SHA256 = 'd46b85313f536fc4831a69ba3fa2c8160450b5b26c7c5dfafce4f078fe4f205c'
LIBBLKID_PATCH_SHA256 = '935ae9372061b9988c58297d1d5b12aa04cbc01e538e8606d0103b401f68de1c'

# Exercise the pointer lifetime directly, including nested tables and reuse.
# Included into partitions.c so the test can reach internal allocation routines.
LIBBLKID_REGRESSION = r'''
#include "libblkid/src/partitions/partitions.c"
#include <assert.h>
int main(void)
{
    blkid_partlist ls = calloc(1, sizeof(*ls));
    assert(ls);
    INIT_LIST_HEAD(&ls->l_tabs);
    for (int round = 0; round < 3; round++) {
        blkid_parttable table = blkid_partlist_new_parttable(ls, "dos", 0);
        assert(table);
        blkid_partition parent = blkid_partlist_add_partition(ls, table, 2048, 65536);
        assert(parent);
        ls->next_parent = parent;
        blkid_parttable child = blkid_partlist_new_parttable(ls, "bsd", 2048);
        assert(child);
        for (int i = 0; i < 4096; i++) {
            assert(blkid_partlist_add_partition(ls, child, 2048 + i, 1));
            assert(blkid_partlist_get_partition(ls, 0) == parent);
            assert(child->parent == parent);
            assert(blkid_partition_get_start(parent) == 2048);
        }
        reset_partlist(ls);
        assert(ls->nparts == 0);
    }
    partitions_free_data(NULL, ls);
    puts("CVE-2026-13595: nested partition pointers and reset passed");
    return 0;
}
'''


def libblkid_build_stage(target, pinned, stage):
    """Backport only the partition lifetime fix, keeping Bookworm ABI/packaging."""
    return f'''# CVE-2026-13595: stable partition pointers in Bookworm libblkid.
# Sources, compiler, regression binaries and test dependencies remain build-only.
FROM --platform={target.platform} {pinned} AS libblkid-build-{stage}
ADD --checksum=sha256:{LIBBLKID_SOURCE_SHA256} https://deb.debian.org/debian/pool/main/u/util-linux/util-linux_2.38.1.orig.tar.xz /sources/util-linux.tar.xz
ADD --checksum=sha256:{LIBBLKID_PACKAGING_SHA256} https://deb.debian.org/debian/pool/main/u/util-linux/util-linux_2.38.1-5+deb12u3.debian.tar.xz /sources/debian.tar.xz
ADD --checksum=sha256:{LIBBLKID_PATCH_SHA256} https://github.com/util-linux/util-linux/commit/132d9c8aa15a8efd0a23d8ca7ed8b98f365e84fa.patch /sources/upstream.patch
RUN <<'OPENRIAK_LIBBLKID_SOURCE'
set -eu
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends build-essential debhelper dh-exec gettext bison libtool pkg-config po-debconf asciidoctor bc socat netbase libaudit-dev libcap-ng-dev libcrypt-dev libcryptsetup-dev libncurses-dev libpam0g-dev libreadline-dev libselinux1-dev libsystemd-dev libudev-dev systemd zlib1g-dev valgrind
mkdir /build
tar -xJf /sources/util-linux.tar.xz -C /build
cd /build/util-linux-2.38.1
tar -xJf /sources/debian.tar.xz
# Adapt only the context: Bookworm uses realloc instead of reallocarray here.
sed -e 's/reallocarray(ls->parts, ls->nparts_max + 32,/realloc(ls->parts, (ls->nparts_max + 32) */' -e 's/	 sizeof/	sizeof/' /sources/upstream.patch > debian/patches/openriak-CVE-2026-13595.patch
printf '\\nopenriak-CVE-2026-13595.patch\\n' >> debian/patches/series
mv debian/changelog debian/changelog.distribution
cat > debian/changelog <<'OPENRIAK_LIBBLKID_CHANGELOG'
util-linux ({LIBBLKID_DEB_VERSION}) bookworm; urgency=high

  * Backport upstream CVE-2026-13595 partition pointer lifetime fix.
  * Preserve Debian 12 configuration, symbols and package metadata.

 -- OpenRiak <packages@openriak.org>  Tue, 08 Sep 2026 00:00:00 +0000

OPENRIAK_LIBBLKID_CHANGELOG
cat debian/changelog.distribution >> debian/changelog
OPENRIAK_LIBBLKID_SOURCE

RUN --network=none <<'OPENRIAK_LIBBLKID_PACKAGES'
set -eu
cd /build/util-linux-2.38.1
# Defer tests to the mandatory following step, preserving Debian symbol checks.
if DEB_BUILD_OPTIONS='parallel=4 terse nocheck' dpkg-buildpackage -b -us -uc -Pnoudeb -j4 > /build/libblkid-build.log 2>&1
then
    grep -E 'dpkg-gensymbols|dpkg-deb: building package' /build/libblkid-build.log
else
    tail -150 /build/libblkid-build.log
    exit 1
fi
OPENRIAK_LIBBLKID_PACKAGES

RUN --network=none <<'OPENRIAK_LIBBLKID_TESTS'
set -eu
cd /build/util-linux-2.38.1
dpkg-source --before-build .
build=.
if ! make -C "$build" -j4 check-programs > /build/libblkid-check-programs.log 2>&1
then
    tail -100 /build/libblkid-check-programs.log
    exit 1
fi
if ! tests/run.sh --srcdir="$PWD" --builddir="$PWD/$build" --parallel=4 blkid > /build/libblkid-tests.log 2>&1
then
    cat /build/libblkid-tests.log
    exit 1
fi
cat /build/libblkid-tests.log
cat > openriak-partition-test.c <<'OPENRIAK_PARTITION_TEST'
{LIBBLKID_REGRESSION}OPENRIAK_PARTITION_TEST
cc -g -O1 -include config.h -I"$build" -I"$build/libblkid/src" -I. -Iinclude -Ilibblkid/src openriak-partition-test.c "$build/.libs/libblkid.a" "$build/.libs/libcommon.a" -o /build/partition-test
valgrind --error-exitcode=99 --leak-check=full --errors-for-leak-kinds=all /build/partition-test > /build/libblkid-regression.log 2>&1
cat /build/libblkid-regression.log
# Verify the regression rejects the unpatched implementation as well.
cp libblkid/src/partitions/partitions.c /build/partitions.patched.c
patch --reverse --fuzz=0 -p1 < debian/patches/openriak-CVE-2026-13595.patch
cc -g -O1 -include config.h -I"$build" -I"$build/libblkid/src" -I. -Iinclude -Ilibblkid/src openriak-partition-test.c "$build/.libs/libblkid.a" "$build/.libs/libcommon.a" -o /build/partition-unpatched
if valgrind --error-exitcode=99 /build/partition-unpatched > /build/libblkid-negative-control.log 2>&1
then
    echo 'ERROR: regression did not reject vulnerable source' >&2
    exit 1
fi
cp /build/partitions.patched.c libblkid/src/partitions/partitions.c
mkdir /packages
cp /build/libblkid1_{LIBBLKID_DEB_VERSION}_*.deb /packages/
cp /build/libblkid-*.log /packages/
sha256sum /packages/*.deb > /packages/SHA256SUMS
OPENRIAK_LIBBLKID_TESTS

'''


def remove_tar_script():
    return '''# dpkg requires tar for installation. It is deliberately absent at runtime.
# Child builds supply a pinned build-only tar and reinstall it before using apt.
dpkg --purge --force-remove-essential --force-depends tar
test ! -e /bin/tar
test ! -e /usr/bin/tar
'''


# Test-only platform detection; no OpenSSL library code or IPv6 feature is disabled.
OPENSSL_TEST_PATCH = r'''
--- a/util/perl/OpenSSL/Test/Utils.pm
+++ b/util/perl/OpenSSL/Test/Utils.pm
@@ -180,6 +180,11 @@
             Listen=>1,
             );
         $s or die "\n";
+        # Binding alone is insufficient in containers with filtered IPv6.
+        my $peer = $s->new(PeerAddr => $listenaddress,
+                          PeerPort => $s->sockport(), Timeout => 1);
+        $peer or die "\n";
+        $peer->close();
         $s->close();
     };
     if ($@ eq "") {
@@ -194,6 +199,11 @@
             Listen=>1,
             );
         $s or die "\n";
+        # Binding alone is insufficient in containers with filtered IPv6.
+        my $peer = $s->new(PeerAddr => $listenaddress,
+                          PeerPort => $s->sockport(), Timeout => 1);
+        $peer or die "\n";
+        $peer->close();
         $s->close();
     };
     if ($@ eq "") {
@@ -208,6 +218,11 @@
             Listen=>1,
             );
         $s or die "\n";
+        # Binding alone is insufficient in containers with filtered IPv6.
+        my $peer = $s->new(PeerAddr => $listenaddress,
+                          PeerPort => $s->sockport(), Timeout => 1);
+        $peer or die "\n";
+        $peer->close();
         $s->close();
     };
     if ($@ eq "") {
--- a/test/recipes/80-test_cmp_http.t
+++ b/test/recipes/80-test_cmp_http.t
@@ -216,6 +216,12 @@
   LOOP:
     while (my $line = <$data>) {
         chomp $line;
+        # These two CSV cases explicitly depend on host IP configuration.
+        # Preserve the library's IPv6 support; skip only unusable host paths.
+        if (!have_IPv6() && $line =~ /disabled as not supported by some host IP configurations: server (?:IPv6 address|domain name)/) {
+            note "Skipping CMP hostname/IPv6 case: IPv6 loopback connection unavailable";
+            next LOOP;
+        }
         $line =~ s{\r\n}{\n}g; # adjust line endings
         $line =~ s{_CA_DN}{$ca_dn}g;
         $line =~ s{_SERVER_DN}{$server_dn}g;
--- a/util/perl/TLSProxy/Proxy.pm
+++ b/util/perl/TLSProxy/Proxy.pm
@@ -43,6 +43,10 @@
             Listen=>1,
             );
         $s or die "\n";
+        my $peer = $s->new(PeerAddr => "::1",
+                          PeerPort => $s->sockport(), Timeout => 1);
+        $peer or die "\n";
+        $peer->close();
         $s->close();
     };
     if ($@ eq "") {
@@ -57,6 +61,10 @@
                 Listen=>1,
                 );
             $s or die "\n";
+            my $peer = $s->new(PeerAddr => "::1",
+                              PeerPort => $s->sockport(), Timeout => 1);
+            $peer or die "\n";
+            $peer->close();
             $s->close();
         };
         if ($@ eq "") {
'''

def openssl_build_stage(target, pinned, stage):
    """Build real Bookworm packages; never replace libraries behind dpkg's back."""
    return f'''# OpenSSL security backport: official 3.0.22 source with Bookworm packaging.
# This compiles OpenSSL only; OpenRiak KV and its bundled OTP remain official binaries.
# Compiler, Perl, source, headers, and static libraries stay in this build stage.
FROM --platform={target.platform} {pinned} AS openssl-build-{stage}
ADD --checksum=sha256:{OPENSSL_SOURCE_SHA256} https://github.com/openssl/openssl/releases/download/openssl-{OPENSSL_VERSION}/openssl-{OPENSSL_VERSION}.tar.gz /sources/openssl.tar.gz
ADD --checksum=sha256:{OPENSSL_PACKAGING_SHA256} https://deb.debian.org/debian/pool/main/o/openssl/openssl_3.0.20-1~deb12u2.debian.tar.xz /sources/debian.tar.xz
RUN <<'OPENRIAK_OPENSSL_BUILD'
set -eu
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y --no-install-recommends
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends build-essential debhelper m4 bc dpkg-dev ca-certificates netbase libio-socket-inet6-perl
mkdir /build
tar -xzf /sources/openssl.tar.gz -C /build
cd /build/openssl-{OPENSSL_VERSION}
tar -xJf /sources/debian.tar.xz
# Retain Debian configuration/ABI/build patches. The subsequent security patches
# in the 3.0.20 packaging are already included in upstream 3.0.22.
cat > debian/patches/series <<'OPENRIAK_DEBIAN_PATCHES'
debian-targets.patch
man-section.patch
no-symbolic.patch
pic.patch
c_rehash-compat.patch
Configure-allow-to-enable-ktls-if-target-does-not-start-w.patch
Remove-the-provider-section.patch
conf-Serialize-allocation-free-of-ssl_names.patch
Fix-tests-for-new-default-security-level.patch
OPENRIAK_DEBIAN_PATCHES
mv debian/changelog debian/changelog.distribution
cat > debian/changelog <<'OPENRIAK_OPENSSL_CHANGELOG'
openssl ({OPENSSL_DEB_VERSION}) bookworm; urgency=high

  * OpenRiak-maintained backport of upstream OpenSSL 3.0.22 security fixes.
  * Preserve Bookworm library names, symbol checks, configuration and packaging.
  * Retain Debian distribution patches; omit security patches merged upstream.

 -- OpenRiak <packages@openriak.org>  Tue, 08 Sep 2026 00:00:00 +0000

OPENRIAK_OPENSSL_CHANGELOG
cat debian/changelog.distribution >> debian/changelog
OPENRIAK_OPENSSL_BUILD

# Cache compilation separately from tests, retaining Debian's ABI symbol checks.
# nocheck defers the upstream suites to the mandatory next step, not a skip.
RUN --network=none <<'OPENRIAK_OPENSSL_PACKAGES'
set -eu
cd /build/openssl-{OPENSSL_VERSION}
# Limit build parallelism to avoid exhausting memory on multi-image workers.
if DEB_BUILD_OPTIONS='parallel=4 terse nocheck' dpkg-buildpackage -b -us -uc -Pnoudeb -j4 > /build/openssl-package-build.log 2>&1
then
    grep -E 'Files=|Result:|dpkg-gensymbols|dpkg-deb: building package' /build/openssl-package-build.log
else
    tail -200 /build/openssl-package-build.log
    exit 1
fi
OPENRIAK_OPENSSL_PACKAGES

# These test-only changes detect hosts that can bind IPv6 but cannot connect.
# OpenSSL's library retains IPv6 support. Both suites must pass before export.
RUN --network=none <<'OPENRIAK_OPENSSL_TESTED_PACKAGES'
set -eu
cd /build/openssl-{OPENSSL_VERSION}
# dpkg-source removes its patches after packaging; restore the tested source view.
dpkg-source --before-build .
cat > /build/openriak-test-loopback.patch <<'OPENRIAK_OPENSSL_TEST_PATCH'
{OPENSSL_TEST_PATCH}OPENRIAK_OPENSSL_TEST_PATCH
patch -p1 < /build/openriak-test-loopback.patch
for build in build_static build_shared
do
    # Run against the exact packaged binaries without reconfiguring/recompiling.
    if HARNESS_JOBS=4 make -C "$build" -o Makefile -o configdata.pm link-utils run_tests > "/build/openssl-$build-tests.log" 2>&1
    then
        grep -E 'Files=|Result:' "/build/openssl-$build-tests.log"
    else
        tail -200 "/build/openssl-$build-tests.log"
        exit 1
    fi
done
mkdir /packages
cp /build/libssl3_{OPENSSL_DEB_VERSION}_*.deb /packages/
cp /build/openssl_{OPENSSL_DEB_VERSION}_*.deb /packages/
sha256sum /packages/*.deb > /packages/SHA256SUMS
cp /build/openssl-package-build.log /build/openssl-build_*-tests.log /packages/
OPENRIAK_OPENSSL_TESTED_PACKAGES

'''


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
        if (target.family, target.release, mode.get('openssl_backport'), mode['base_image']) != (
                'debian', '12', OPENSSL_VERSION, 'debian:bookworm-slim-for-openriak'):
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
        # RPM's own provider matching compares epoch/version/release correctly.
        # Run before removing installer tools in rpm-root images.
        return ''.join(f"{command} -q --whatprovides '{package} >= {version}' >/dev/null\n"
                       for package, version in mode.get('minimum_packages', {}).items())
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


def package_stage(target, pinned, stage, download, install_script):
    mode = configuration(target)
    if mode is None:
        return None
    filename = target.package['filename']
    if mode['strategy'] == 'clean-root':
        extra = ''
        build_stage = ''
        package_mount = ''
        bootstrap = ''
        if mode.get('libblkid_backport'):
            tools_image = mode.get('package_tools_image', '')
            if not re.fullmatch(r'debian:bookworm-slim@sha256:[0-9a-f]{64}', tools_image):
                raise ConfigurationError('Debian tar bootstrap requires a pinned Bookworm tools image')
            build_stage += f'FROM --platform={target.platform} {tools_image} AS package-tools-{stage}\n'
            package_mount += f' --mount=type=bind,from=package-tools-{stage},source=/usr/bin/tar,target=/usr/local/bin/tar,ro'
            bootstrap = '''# The reusable runtime base omits tar. Borrow it only for package installation.
# dpkg checks /bin/tar even when the mount is available in /usr/local/bin.
cp /usr/local/bin/tar /bin/tar
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tar
'''
        if mode.get('openssl_backport') and not mode.get('base_image'):
            build_stage = openssl_build_stage(target, pinned, stage)
            package_mount = f' --mount=type=bind,from=openssl-build-{stage},source=/packages,target=/opt/openssl-packages,ro'
            extra = f'''# Upgrade both libraries and CLI with dpkg-tracked packages; retain newer vendor fixes.
installed_openssl=$(dpkg-query -W -f='${{Version}}' libssl3)
if dpkg --compare-versions "$installed_openssl" lt '{OPENSSL_DEB_VERSION}'
then
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends /opt/openssl-packages/*.deb
fi
ldconfig
mkdir -p /usr/share/openriak-build
dpkg-query -W libssl3 openssl > /usr/share/openriak-build/openssl-packages.txt
'''
        elif mode.get('base_image'):
            extra = f'''# Require the tested patched base; fail rather than build with older libraries.
dpkg --compare-versions "$(dpkg-query -W -f='${{Version}}' libssl3)" ge '{OPENSSL_DEB_VERSION}'
test -s /usr/share/openriak-build/openssl-packages.txt
'''
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
    repository_setup = ''
    if target.family == 'centos' and target.release == '8':
        repository_setup = install_script.split('# Update installed OS packages', 1)[0]
    return f'''# The full OS image is an installer only; none of its layers reach runtime.
FROM --platform={target.platform} {pinned} AS install-{stage}
RUN --mount=type=bind,from={download},target=/opt/openriak-package,ro <<'OPENRIAK_PACKAGE_INSTALL'
set -eu
# Resolve runtime packages from this OS release, without weak dependencies.
{repository_setup}# Slim installers may provide only microdnf. Full dnf is build-only.
if ! command -v dnf >/dev/null 2>&1
then
    microdnf install -y dnf
fi
mkdir -p /openriak-rootfs
dnf install -y --refresh --installroot=/openriak-rootfs --releasever={target.release} --setopt=install_weak_deps=False --setopt=tsflags=nodocs {packages}
# Install the verified official package; its OTP runtime is bundled in the RPM.
rpm --root /openriak-rootfs -Uvh --replacepkgs --nodeps /opt/openriak-package/{filename}
{remove_rpm_packages(mode, '/openriak-rootfs')}\
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
