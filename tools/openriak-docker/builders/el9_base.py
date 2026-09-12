"""KV installation checks for inherited EL9 bases; recipes live in builders_base."""
# Keep the backport in the inherited KV build dependency chain.
from builders import pcre2


def child_repositories(target, install_script):
    import images.minimal as minimal
    mode = minimal.configuration(target)
    return '''# Inherit the approved runtime and its package database from the patched base.
# Package installation tools belong to a separate, pinned stage of the same OS.
test -s /openriak-rootfs/usr/share/openriak-build/pcre2-regression.log
''' + minimal.minimum_package_check({'minimum_packages': {'pcre2': mode['pcre2_backport']}},
                                    'rpm', '/openriak-rootfs')
