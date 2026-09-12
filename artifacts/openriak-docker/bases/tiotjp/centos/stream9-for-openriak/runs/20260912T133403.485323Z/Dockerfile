# syntax=docker/dockerfile:1.7
# Created by TI Tokyo, www.tiot.jp, for the OpenRiak project at https://openriak.org
# WARNING: Edit only if you understand the effect of your changes.
# Original image tag: tiotjp/centos:stream9-for-openriak
# Reusable minimal OS base; no OpenRiak KV package or Erlang cookie is installed.
# BuildKit supplies TARGETARCH from --platform.

# The full OS image is an installer only; none of its layers reach runtime.
FROM --platform=linux/amd64 quay.io/centos/centos:stream9@sha256:7d3c87ab567add60d0153a6a17bc10d0f19cd982a2d533724298ebd1ee751eab AS install-amd64
RUN <<'OPENRIAK_PACKAGE_INSTALL'
set -eu
# Resolve runtime packages from this OS release, without weak dependencies.
# PCRE2 CVE-2026-89161: preserve the EL9 source package's vendor patches.
# Compiler, source and package tooling remain in the discarded installer stage.
if ! command -v dnf >/dev/null 2>&1
then
    microdnf install -y dnf
fi
dnf install -y --setopt=install_weak_deps=False rpm-build redhat-rpm-config gcc make autoconf automake libtool gnupg2 patch tar bzip2 diffutils
if ! command -v curl >/dev/null 2>&1
then
    dnf install -y curl-minimal
fi
mkdir -p /sources /root/rpmbuild/SOURCES /root/rpmbuild/SPECS
curl --fail --location --retry 3 https://dl.rockylinux.org/pub/rocky/9/BaseOS/source/tree/Packages/p/pcre2-10.40-6.el9.src.rpm -o /sources/pcre2.src.rpm
echo '06d57c69f091a37c16c7f9401246c2897fb39b21d51ccd36be72e66999ddc036  /sources/pcre2.src.rpm' | sha256sum -c -
rpm -i /sources/pcre2.src.rpm
cat > /sources/openriak-pcre2.patch <<'OPENRIAK_PCRE2_PATCH'
--- a/src/pcre2_jit_match.c
+++ b/src/pcre2_jit_match.c
@@ -123,2 +123,12 @@
+/* If the match data block was previously used with PCRE2_COPY_MATCHED_SUBJECT,
+free the memory that was obtained. */
+
+if ((match_data->flags & PCRE2_MD_COPIED_SUBJECT) != 0)
+  {
+  match_data->memctl.free((void *)match_data->subject,
+    match_data->memctl.memory_data);
+  match_data->flags &= ~PCRE2_MD_COPIED_SUBJECT;
+  }
+
 /* Sanity checks should be handled by pcre2_match. */
 arguments.str = subject + start_offset;
OPENRIAK_PCRE2_PATCH
cat > /sources/pcre2-regression.c <<'OPENRIAK_PCRE2_REGRESSION'
#include <pcre2.h>
#include <stdio.h>
#include <stdlib.h>
static void *allocations[1024];
static int invalid_frees;
static void *tracked_malloc(PCRE2_SIZE n, void *data) {
    (void)data;
    for (int i = 0; i < 1024; i++) if (!allocations[i]) {
        allocations[i] = malloc(n);
        if (!allocations[i]) abort();
        return allocations[i];
    }
    abort();
}
static void tracked_free(void *p, void *data) {
    (void)data;
    if (!p) return;
    for (int i = 0; i < 1024; i++) if (allocations[i] == p) {
        free(p); allocations[i] = NULL; return;
    }
    invalid_frees++;
}
int main(void) {
    int error, rc, leaks = 0;
    PCRE2_SIZE offset;
    PCRE2_UCHAR pattern[] = {'a', 0}, first[] = {'a', 0}, second[] = {'a', 0};
    pcre2_general_context *general = pcre2_general_context_create(tracked_malloc, tracked_free, NULL);
    pcre2_compile_context *context = pcre2_compile_context_create(general);
    pcre2_code *code = pcre2_compile(pattern, 1, 0, &error, &offset, context);
    if (!code || pcre2_jit_compile(code, PCRE2_JIT_COMPLETE)) return 2;
    pcre2_match_data *match = pcre2_match_data_create_from_pattern(code, general);
    /* Numeric value also permits checking libraries predating this option. */
    rc = pcre2_match(code, first, 1, 0, 0x00004000u | PCRE2_NO_JIT, match, NULL);
    if (rc == PCRE2_ERROR_BADOPTION) {
        puts("NOT AFFECTED: copied-subject option is unsupported");
        return 77;
    }
    if (rc != 1) return 3;
    if (pcre2_jit_match(code, second, 1, 0, 0, match, NULL) != 1) return 4;
    pcre2_match_data_free(match);
    pcre2_code_free(code);
    pcre2_compile_context_free(context);
    pcre2_general_context_free(general);
    for (int i = 0; i < 1024; i++) if (allocations[i]) {
        leaks++; free(allocations[i]);
    }
    printf("CVE-2026-89161 width=%d invalid_frees=%d leaks=%d\n",
           PCRE2_CODE_UNIT_WIDTH, invalid_frees, leaks);
    return invalid_frees || leaks ? 42 : 0;
}
OPENRIAK_PCRE2_REGRESSION

cp /sources/openriak-pcre2.patch /root/rpmbuild/SOURCES/
sed -i 's/^Release:.*/Release: 6.el9.openriak1/' /root/rpmbuild/SPECS/pcre2.spec
sed -i '/^Patch0:/i Patch99: openriak-pcre2.patch' /root/rpmbuild/SPECS/pcre2.spec
if ! rpmbuild -ba --without pcre2_enables_readline --define '_smp_mflags -j4' /root/rpmbuild/SPECS/pcre2.spec > /sources/pcre2-build.log 2>&1
then
    tail -100 /sources/pcre2-build.log
    exit 1
fi
mkdir -p /openriak-rootfs/usr/share/openriak-build
cat > /sources/check-pcre2.sh <<'OPENRIAK_PCRE2_CHECKS'
set -eu
cd /root/rpmbuild/BUILD/pcre2-10.40
for width in 8 16 32
do
    cc -DPCRE2_CODE_UNIT_WIDTH=$width -I. -Isrc /sources/pcre2-regression.c -L.libs -Wl,-rpath,"$PWD/.libs" -lpcre2-$width -o /sources/regression-$width
    /sources/regression-$width
done
# Rebuild just the libraries without our patch: the negative control must fail.
patch --reverse --fuzz=0 -p1 < /sources/openriak-pcre2.patch
# RPM builds disable automatic dependencies; jit_match.c is included by this unit.
touch src/pcre2_jit_compile.c
make -j4 libpcre2-8.la libpcre2-16.la libpcre2-32.la > /sources/negative-build.log 2>&1
for width in 8 16 32
do
    result=0
    /sources/regression-$width || result=$?
    test "$result" = 42
done
patch --fuzz=0 -p1 < /sources/openriak-pcre2.patch
touch src/pcre2_jit_compile.c
make -j4 libpcre2-8.la libpcre2-16.la libpcre2-32.la > /sources/restored-build.log 2>&1
for width in 8 16 32
do
    /sources/regression-$width
done
OPENRIAK_PCRE2_CHECKS
if ! sh /sources/check-pcre2.sh > /sources/pcre2-regression.log 2>&1
then
    cat /sources/pcre2-regression.log
    tail -n 80 /sources/negative-build.log /sources/restored-build.log
    exit 1
fi
cat /sources/pcre2-regression.log
# Resolve vendor packages first, retaining newer vendor fixes when available.
dnf install -y --installroot=/openriak-rootfs --releasever=9 --setopt=install_weak_deps=False --setopt=tsflags=nodocs pcre2
installed=$(rpm --root /openriak-rootfs -q --qf '%{EPOCHNUM}:%{VERSION}-%{RELEASE}' pcre2)
comparison=$(OPENRIAK_PCRE2_VERSION="$installed" rpm --eval '%{lua:print(rpm.vercmp(os.getenv("OPENRIAK_PCRE2_VERSION"), "0:10.40-6.el9.openriak1"))}')
if [ "$comparison" -lt 0 ]
then
    dnf install -y --installroot=/openriak-rootfs --releasever=9 --setopt=install_weak_deps=False --setopt=tsflags=nodocs /root/rpmbuild/RPMS/*/pcre2-10.40-6.el9.openriak1.*.rpm /root/rpmbuild/RPMS/noarch/pcre2-syntax-10.40-6.el9.openriak1.noarch.rpm
fi
# Exercise the installed runtime library too, then remove the test executable.
mkdir -p /openriak-rootfs/tmp
cp /sources/regression-8 /openriak-rootfs/tmp/pcre2-regression
chroot /openriak-rootfs /tmp/pcre2-regression >> /sources/pcre2-regression.log
rm /openriak-rootfs/tmp/pcre2-regression
# A second installroot transaction uses that root's repository configuration.
# UBI's redhat-release package does not include ubi.repo: retain the installer
# image's release-specific repositories for the remaining runtime installation.
mkdir -p /openriak-rootfs/etc/yum.repos.d
cp -a /etc/yum.repos.d/. /openriak-rootfs/etc/yum.repos.d/
rpm --root /openriak-rootfs -q pcre2 > /openriak-rootfs/usr/share/openriak-build/pcre2-packages.txt
cp /sources/pcre2-build.log /sources/pcre2-regression.log /openriak-rootfs/usr/share/openriak-build/
# Slim installers may provide only microdnf. Full dnf is build-only.
if ! command -v dnf >/dev/null 2>&1
then
    microdnf install -y dnf
fi
mkdir -p /openriak-rootfs
dnf install -y --refresh --installroot=/openriak-rootfs --releasever=9 --setopt=install_weak_deps=False --setopt=tsflags=nodocs centos-stream-release bash coreutils findutils gawk grep sed ca-certificates glibc glibc-minimal-langpack hostname libgcc libstdc++ ncurses-libs openssl-libs pam procps-ng shadow-utils sudo util-linux zlib tzdata
# Reject stale repository mirrors before exporting the runtime filesystem.
# Preserve the RPM database and an explicit inventory for vulnerability scanners.
mkdir -p /openriak-rootfs/usr/share/openriak-build
rpm --root /openriak-rootfs -qa --qf '%{NAME} %{VERSION}-%{RELEASE}\n' > /openriak-rootfs/usr/share/openriak-build/runtime-packages.txt
# Install escript's compatibility link without retaining the installer tools.
for bundled_escript in /openriak-rootfs/usr/lib64/riak/erts-*/bin/escript /openriak-rootfs/usr/lib/riak/erts-*/bin/escript
do
    if [ -x "$bundled_escript" ]
    then
        ln -sf "${bundled_escript#/openriak-rootfs}" /openriak-rootfs/usr/bin/escript
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

FROM scratch AS package-amd64
COPY --from=install-amd64 /openriak-rootfs/ /
# Standard command search path for the shell-based OpenRiak KV lifecycle.
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

FROM package-${TARGETARCH} AS final
LABEL org.opencontainers.image.title="centos 9 for OpenRiak"
LABEL org.opencontainers.image.description="Minimal runtime base with a tested native PCRE2 security backport"
LABEL org.opencontainers.image.vendor="TI Tokyo"
LABEL org.opencontainers.image.source="https://github.com/TI-Tokyo/openriak-docs"
LABEL org.opencontainers.image.url="https://www.tiot.jp/"
LABEL org.opencontainers.image.version="stream9-for-openriak"
LABEL org.openriak.os.name="centos"
LABEL org.openriak.os.release="stream9"
LABEL org.openriak.os.version="9"
LABEL org.openriak.pcre2.minimum-version="10.40-6.el9.openriak1"
# Standard executable search path for the minimal runtime.
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
CMD ["bash"]
