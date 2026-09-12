"""Shared EL9 PCRE2-patched runtime construction and validation."""
from builders import pcre2

BUILD_DEPENDENCIES = ('../../../images/minimal.py',)


def configure(target, context):
    context.update(description='Minimal runtime base with a tested native PCRE2 security backport',
                   patch_labels={'org.openriak.pcre2.minimum-version': pcre2.RPM_VERSION})


def render_stage(target, pinned, tool, context):
    arch = target.platform.split('/')[1]
    return tool.minimal.package_stage(target, pinned, arch, '', '', base_only=True)


def runtime_check(target, context):
    import images.minimal as minimal
    return f'''set -eu
. /etc/os-release
test "$ID" = {target.family}
case "$VERSION_ID" in
    9|9.*) ;;
    *) exit 1 ;;
esac
test ! -d /usr/lib/riak
test ! -d /usr/lib64/riak
test ! -d /sources
test ! -d /root/rpmbuild
test ! -e /usr/bin/gcc
test -s /usr/share/openriak-build/pcre2-packages.txt
test -s /usr/share/openriak-build/pcre2-build.log
grep -q 'width=8 invalid_frees=0 leaks=0' /usr/share/openriak-build/pcre2-regression.log
# grep exercises the installed PCRE2 shared library in the exported filesystem.
printf 'OpenRiak\\n' | grep -P '^OpenRiak$'
''' + minimal.runtime_check(target)
