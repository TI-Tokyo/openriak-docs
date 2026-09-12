"""CentOS Stream 8 final release archive."""
def configure(tool, target, context):
    context["repository_setup"] = r"""# CentOS Stream 8 repositories were moved to the release archive.
sed -i 's|^mirrorlist=|#mirrorlist=|' /etc/yum.repos.d/CentOS-Stream-*.repo
sed -i 's|^#baseurl=http://mirror.centos.org/\$contentdir/\$stream/|baseurl=https://vault.centos.org/8-stream/|' /etc/yum.repos.d/CentOS-Stream-*.repo
"""


def minimal_repositories(target, install_script):
    return install_script.split('# Update installed OS packages', 1)[0]
