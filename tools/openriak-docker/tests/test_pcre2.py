"""PCRE2 backport selection and native RPM upgrade safeguards."""
import os
import shutil
import subprocess
import unittest

from test_openriak_docker import docker_tool as tool
from builders import pcre2


class Pcre2BackportTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('rpm'), 'native RPM comparison is required')
    def test_newer_vendor_packages_are_not_downgraded(self):
        body = pcre2.rpm_repositories(None, '').split(
            '# Resolve vendor packages first,', 1)[1].split(
            '# Exercise the installed runtime library', 1)[0]
        body = body[body.index('\ndnf install'):]
        rpm = shutil.which('rpm')
        stubs = '''
dnf() { printf 'DNF %s\n' "$*"; }
rpm() {
    if [ "$1" = --root ]; then
        printf '%s\n' "$INSTALLED_VERSION"
    else
        "$NATIVE_RPM" "$@"
    fi
}
'''
        for version, upgrade in [('0:10.40-6.el9', True),
                                 ('0:10.40-6.el9.openriak1', False),
                                 ('0:10.40-7.el9', False),
                                 ('0:10.48-1.el9', False),
                                 ('1:10.40-1.el9', False)]:
            with self.subTest(version=version):
                result = subprocess.run(['sh', '-c', 'set -eu\n' + stubs + body],
                    env={**os.environ, 'INSTALLED_VERSION': version, 'NATIVE_RPM': rpm},
                    capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual('/root/rpmbuild/RPMS/' in result.stdout, upgrade)


if __name__ == '__main__':
    unittest.main()
