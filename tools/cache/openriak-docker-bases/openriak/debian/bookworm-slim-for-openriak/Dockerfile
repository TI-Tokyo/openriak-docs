# syntax=docker/dockerfile:1.7
# Created by TI Tokyo, www.tiot.jp, for the OpenRiak project at https://openriak.org
# WARNING: Edit only if you understand the effect of your changes.
# Original image tag: openriak/debian:bookworm-slim-for-openriak
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

FROM --platform=linux/amd64 debian:bookworm-slim@sha256:88200866dfff7ea7f5cbcb6ec7c8a701889efe6fe859fe64d6990e4b07ea4171 AS patched-install-amd64
RUN --mount=type=bind,from=openssl-build-amd64,source=/packages,target=/opt/openssl-packages,ro <<'OPENRIAK_PATCHED_BASE'
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
ldconfig
mkdir -p /usr/share/openriak-build
dpkg-query -W libssl3 openssl > /usr/share/openriak-build/openssl-packages.txt
apt-get clean
rm -rf /var/lib/apt/lists/*
OPENRIAK_PATCHED_BASE

# Flatten the patched Debian filesystem so replaced vulnerable bytes do not remain in lower layers.
FROM scratch AS patched-amd64
COPY --from=patched-install-amd64 / /

FROM patched-${TARGETARCH} AS final
LABEL org.opencontainers.image.title="Debian Bookworm slim for OpenRiak"
LABEL org.opencontainers.image.description="Reusable Debian 12 base with the tested OpenSSL security backport"
LABEL org.opencontainers.image.vendor="OpenRiak"
LABEL org.opencontainers.image.source="https://github.com/OpenRiak/openriak-docs"
LABEL org.opencontainers.image.url="https://openriak.org"
LABEL org.opencontainers.image.version="bookworm-slim-for-openriak"
LABEL org.openriak.os.name="debian"
LABEL org.openriak.os.release="bookworm"
LABEL org.openriak.os.version="12"
LABEL org.openriak.openssl.minimum-version="3.0.22-0openriak1~deb12u1"
# Standard Debian executable search path.
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
CMD ["bash"]
