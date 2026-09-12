"""rhel 9: consume the reusable PCRE2-patched runtime base."""
from builders.el9_base import child_repositories


def minimal_repositories(target, install_script):
    return child_repositories(target, install_script)
