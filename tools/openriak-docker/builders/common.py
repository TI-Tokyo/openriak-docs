"""Defaults shared by OS layers; package and release layers amend this context."""
def configure(tool, target, context):
    context.update(repository_setup='', release_option='', runtime_cleanup='',
        dependencies='bash ca-certificates glibc hostname libgcc libstdc++ ncurses-libs openssl-libs pam procps-ng shadow-utils sudo util-linux zlib tzdata',
        suse_openssl='libopenssl1_1', official_rpm=False)
    # Keep generated RPM fallback branches consistent with the package ABI.
    context['suse_openssl'] = 'libopenssl3' if target.operating_system.get('alias_of', '').startswith('rhel-9-') else 'libopenssl1_1'
