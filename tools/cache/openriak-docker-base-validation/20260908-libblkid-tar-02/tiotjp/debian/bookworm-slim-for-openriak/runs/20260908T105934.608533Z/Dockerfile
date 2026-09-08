# syntax=docker/dockerfile:1.7
# Created by TI Tokyo, www.tiot.jp, for the OpenRiak project at https://openriak.org
# WARNING: Edit only if you understand the effect of your changes.
# Original image tag: tiotjp/debian:bookworm-slim-for-openriak
# Reusable Debian base; no OpenRiak KV package or Erlang cookie is installed here.
# BuildKit supplies TARGETARCH from --platform.

# OpenSSL security backport: official 3.0.22 source with Bookworm packaging.
# This compiles OpenSSL only; OpenRiak KV and its bundled OTP remain official binaries.
# Compiler, Perl, source, headers, and static libraries stay in this build stage.
FROM --platform=linux/amd64 debian:bookworm-slim@sha256:88200866dfff7ea7f5cbcb6ec7c8a701889efe6fe859fe64d6990e4b07ea4171 AS openssl-build-amd64
ADD --checksum=sha256:67ebca7e50d17383028045486653492195b83db95f8558709701bb47b5c1ef81 https://github.com/openssl/openssl/releases/download/openssl-3.0.22/openssl-3.0.22.tar.gz /sources/openssl.tar.gz
ADD --checksum=sha256:7279efe85c359500c95aa88347e3395dd303d7566e2bb818d80d96e0c3bb9629 https://deb.debian.org/debian/pool/main/o/openssl/openssl_3.0.20-1~deb12u2.debian.tar.xz /sources/debian.tar.xz
RUN <<'OPENRIAK_OPENSSL_BUILD'
set -eu
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y --no-install-recommends
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends build-essential debhelper m4 bc dpkg-dev ca-certificates netbase libio-socket-inet6-perl
mkdir /build
tar -xzf /sources/openssl.tar.gz -C /build
cd /build/openssl-3.0.22
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
openssl (3.0.22-0openriak1~deb12u1) bookworm; urgency=high

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
cd /build/openssl-3.0.22
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
cd /build/openssl-3.0.22
# dpkg-source removes its patches after packaging; restore the tested source view.
dpkg-source --before-build .
cat > /build/openriak-test-loopback.patch <<'OPENRIAK_OPENSSL_TEST_PATCH'

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
OPENRIAK_OPENSSL_TEST_PATCH
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
cp /build/libssl3_3.0.22-0openriak1~deb12u1_*.deb /packages/
cp /build/openssl_3.0.22-0openriak1~deb12u1_*.deb /packages/
sha256sum /packages/*.deb > /packages/SHA256SUMS
cp /build/openssl-package-build.log /build/openssl-build_*-tests.log /packages/
OPENRIAK_OPENSSL_TESTED_PACKAGES

# CVE-2026-13595: stable partition pointers in Bookworm libblkid.
# Sources, compiler, regression binaries and test dependencies remain build-only.
FROM --platform=linux/amd64 debian:bookworm-slim@sha256:88200866dfff7ea7f5cbcb6ec7c8a701889efe6fe859fe64d6990e4b07ea4171 AS libblkid-build-amd64
ADD --checksum=sha256:60492a19b44e6cf9a3ddff68325b333b8b52b6c59ce3ebd6a0ecaa4c5117e84f https://deb.debian.org/debian/pool/main/u/util-linux/util-linux_2.38.1.orig.tar.xz /sources/util-linux.tar.xz
ADD --checksum=sha256:d46b85313f536fc4831a69ba3fa2c8160450b5b26c7c5dfafce4f078fe4f205c https://deb.debian.org/debian/pool/main/u/util-linux/util-linux_2.38.1-5+deb12u3.debian.tar.xz /sources/debian.tar.xz
ADD --checksum=sha256:935ae9372061b9988c58297d1d5b12aa04cbc01e538e8606d0103b401f68de1c https://github.com/util-linux/util-linux/commit/132d9c8aa15a8efd0a23d8ca7ed8b98f365e84fa.patch /sources/upstream.patch
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
printf '\nopenriak-CVE-2026-13595.patch\n' >> debian/patches/series
mv debian/changelog debian/changelog.distribution
cat > debian/changelog <<'OPENRIAK_LIBBLKID_CHANGELOG'
util-linux (2.38.1-5+deb12u3+openriak1) bookworm; urgency=high

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
OPENRIAK_PARTITION_TEST
cc -g -O1 -DHAVE_CONFIG_H -I"$build" -I"$build/libblkid/src" -I. -Iinclude -Ilibblkid/src openriak-partition-test.c "$build/.libs/libblkid.a" "$build/.libs/libcommon.a" -o /build/partition-test
valgrind --error-exitcode=99 --leak-check=full --errors-for-leak-kinds=all /build/partition-test > /build/libblkid-regression.log 2>&1
cat /build/libblkid-regression.log
# Verify the regression rejects the unpatched implementation as well.
cp libblkid/src/partitions/partitions.c /build/partitions.patched.c
patch --reverse --fuzz=0 -p1 < debian/patches/openriak-CVE-2026-13595.patch
cc -g -O1 -DHAVE_CONFIG_H -I"$build" -I"$build/libblkid/src" -I. -Iinclude -Ilibblkid/src openriak-partition-test.c "$build/.libs/libblkid.a" "$build/.libs/libcommon.a" -o /build/partition-unpatched
if valgrind --error-exitcode=99 /build/partition-unpatched > /build/libblkid-negative-control.log 2>&1
then
    echo 'ERROR: regression did not reject vulnerable source' >&2
    exit 1
fi
cp /build/partitions.patched.c libblkid/src/partitions/partitions.c
mkdir /packages
cp /build/libblkid1_2.38.1-5+deb12u3+openriak1_*.deb /packages/
cp /build/libblkid-*.log /packages/
sha256sum /packages/*.deb > /packages/SHA256SUMS
OPENRIAK_LIBBLKID_TESTS

FROM --platform=linux/amd64 debian:bookworm-slim@sha256:88200866dfff7ea7f5cbcb6ec7c8a701889efe6fe859fe64d6990e4b07ea4171 AS patched-install-amd64
RUN --mount=type=bind,from=openssl-build-amd64,source=/packages,target=/opt/openssl-packages,ro --mount=type=bind,from=libblkid-build-amd64,source=/packages,target=/opt/libblkid-packages,ro <<'OPENRIAK_PATCHED_BASE'
set -eu
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y --no-install-recommends
if installed_openssl=$(dpkg-query -W -f='${Version}' libssl3 2>/dev/null)
then
    :
else
    installed_openssl=0
fi
# Retain newer Debian fixes; never downgrade an installed vendor package.
if dpkg --compare-versions "$installed_openssl" lt '3.0.22-0openriak1~deb12u1'
then
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends /opt/openssl-packages/*.deb
else
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends openssl
fi
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates
if dpkg --compare-versions "$(dpkg-query -W -f='${Version}' libblkid1)" lt '2.38.1-5+deb12u3+openriak1'
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
# dpkg requires tar for installation. It is deliberately absent at runtime.
# Child builds supply a pinned build-only tar and reinstall it before using apt.
dpkg --purge --force-remove-essential --force-depends tar
test ! -e /bin/tar
test ! -e /usr/bin/tar

OPENRIAK_PATCHED_BASE

# Flatten the patched Debian filesystem so replaced vulnerable bytes do not remain in lower layers.
FROM scratch AS patched-amd64
COPY --from=patched-install-amd64 / /

FROM patched-${TARGETARCH} AS final
LABEL org.opencontainers.image.title="Debian Bookworm slim for OpenRiak"
LABEL org.opencontainers.image.description="Tar-free Debian 12 runtime base with tested OpenSSL and libblkid security backports"
LABEL org.opencontainers.image.vendor="TI Tokyo"
LABEL org.opencontainers.image.source="https://github.com/TI-Tokyo/openriak-docs"
LABEL org.opencontainers.image.url="https://www.tiot.jp/"
LABEL org.opencontainers.image.version="bookworm-slim-for-openriak"
LABEL org.openriak.os.name="debian"
LABEL org.openriak.os.release="bookworm"
LABEL org.openriak.os.version="12"
LABEL org.openriak.openssl.minimum-version="3.0.22-0openriak1~deb12u1"
LABEL org.openriak.libblkid.minimum-version="2.38.1-5+deb12u3+openriak1"
# Standard Debian executable search path.
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
CMD ["bash"]
