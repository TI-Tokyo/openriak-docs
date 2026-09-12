"""CVE-2026-89161 backport, preserving distribution patches, packaging and ABI.

Only EL9 layers import this helper. EL8's PCRE2 10.32
predates PCRE2_COPY_MATCHED_SUBJECT; do not upgrade it just to silence Scout.
Upstream: https://github.com/PCRE2Project/pcre2/commit/82443294822e9d7a650b2f38dfc6144270a78420
"""

RPM_VERSION = '10.40-6.el9.openriak1'
RPM_SOURCE_SHA256 = '06d57c69f091a37c16c7f9401246c2897fb39b21d51ccd36be72e66999ddc036'

# The upstream ten-line library fix, with context adapted to the older filename.
# Test harness changes from upstream 10.48 are replaced by the public-API test below.
PATCH = '''--- a/src/pcre2_jit_match.c
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
'''

# Custom allocators make both the invalid free and leaked copied subject observable
# without invoking undefined behaviour. Used for all three code-unit widths.
REGRESSION = r'''#include <pcre2.h>
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
'''


def sources():
    return f'''cat > /sources/openriak-pcre2.patch <<'OPENRIAK_PCRE2_PATCH'
{PATCH}OPENRIAK_PCRE2_PATCH
cat > /sources/pcre2-regression.c <<'OPENRIAK_PCRE2_REGRESSION'
{REGRESSION}OPENRIAK_PCRE2_REGRESSION
'''


def regression_checks(build):
    """Check packaged libraries and prove the test rejects the unpatched library."""
    return f'''cd {build}
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
'''


def rpm_repositories(target, install_script):
    """Prepare native patched RPMs before the existing minimal installroot step."""
    return f'''# PCRE2 CVE-2026-89161: preserve the EL9 source package's vendor patches.
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
echo '{RPM_SOURCE_SHA256}  /sources/pcre2.src.rpm' | sha256sum -c -
rpm -i /sources/pcre2.src.rpm
{sources()}
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
{regression_checks('/root/rpmbuild/BUILD/pcre2-10.40')}OPENRIAK_PCRE2_CHECKS
if ! sh /sources/check-pcre2.sh > /sources/pcre2-regression.log 2>&1
then
    cat /sources/pcre2-regression.log
    tail -n 80 /sources/negative-build.log /sources/restored-build.log
    exit 1
fi
cat /sources/pcre2-regression.log
# Resolve vendor packages first, retaining newer vendor fixes when available.
dnf install -y --installroot=/openriak-rootfs --releasever=9 --setopt=install_weak_deps=False --setopt=tsflags=nodocs pcre2
installed=$(rpm --root /openriak-rootfs -q --qf '%{{EPOCHNUM}}:%{{VERSION}}-%{{RELEASE}}' pcre2)
comparison=$(OPENRIAK_PCRE2_VERSION="$installed" rpm --eval '%{{lua:print(rpm.vercmp(os.getenv("OPENRIAK_PCRE2_VERSION"), "0:{RPM_VERSION}"))}}')
if [ "$comparison" -lt 0 ]
then
    dnf install -y --installroot=/openriak-rootfs --releasever=9 --setopt=install_weak_deps=False --setopt=tsflags=nodocs /root/rpmbuild/RPMS/*/pcre2-{RPM_VERSION}.*.rpm /root/rpmbuild/RPMS/noarch/pcre2-syntax-{RPM_VERSION}.noarch.rpm
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
'''
