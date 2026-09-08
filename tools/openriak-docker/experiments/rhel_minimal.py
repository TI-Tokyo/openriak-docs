#!/usr/bin/env python3
"""Isolated amd64 RHEL minimal-runtime experiment; never publishes docs or pushes."""
from __future__ import annotations
import argparse
import dataclasses
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import openriak_docker as tool
from openriak_cve_storage import store_output
from openriak_push import execute

RUNTIME_PACKAGES = (
    'redhat-release bash coreutils findutils gawk grep sed ca-certificates '
    'glibc glibc-minimal-langpack hostname libgcc libstdc++ ncurses-libs '
    'openssl-libs pam procps-ng shadow-utils sudo util-linux zlib tzdata'
)


def scan_image(image, platform, timeout, summary_path, expected_packages=None, reject_interpreters=True):
    """Keep full scanner evidence and verify the minimal OS remains identifiable."""
    result = {}
    for mode, format in (('cves', 'sarif'), ('sbom', 'json')):
        scan = execute([tool.docker_command(), 'scout', mode, '--format', format,
                        '--platform', platform, 'local://' + image], timeout)
        result[mode + '_command'] = {k: v for k, v in scan.items() if k != 'stdout'}
        if scan['exit_code'] != 0:
            raise tool.DockerToolError(f"Scout {mode} failed: {scan['stderr']}")
        payload = json.loads(scan['stdout'])
        result[mode + '_data'] = store_output(summary_path, scan['stdout'], 'json')
        if mode == 'cves':
            cves = {}
            ranks = ['UNSPECIFIED', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
            for run in payload['runs']:
                rules = run['tool']['driver'].get('rules', [])
                for finding in run.get('results', []):
                    rule = rules[finding['ruleIndex']]
                    properties = rule.get('properties', {})
                    severity = properties.get('cvssV3_severity', 'UNSPECIFIED').upper()
                    if severity not in ranks or severity == 'UNSPECIFIED':
                        score = float(properties.get('security-severity', 0))
                        severity = ('CRITICAL' if score >= 9 else 'HIGH' if score >= 7
                                    else 'MEDIUM' if score >= 4 else 'LOW' if score > 0
                                    else 'UNSPECIFIED')
                    previous = cves.get(rule['id'], 'UNSPECIFIED')
                    cves[rule['id']] = max(previous, severity, key=ranks.index)
            result['cves'] = cves
            result['counts'] = {s: list(cves.values()).count(s) for s in reversed(ranks)}
        else:
            artifacts = payload['artifacts']
            names = {a['name'] for a in artifacts}
            if not (expected_packages or {'redhat-release', 'glibc', 'openssl-libs', 'riak'}) <= names:
                raise tool.DockerToolError('Scout did not identify the expected runtime RPM packages')
            unwanted = sorted(n for n in names if n.startswith(('python', 'platform-python', 'perl'))
                              or n in {'pip', 'setuptools', 'dnf', 'microdnf', 'yum', 'rpm'})
            if unwanted and reject_interpreters:
                raise tool.DockerToolError(f'Unwanted packages in Scout inventory: {unwanted}')
            result['package_names'] = sorted(names)
            result['artifact_count'] = len(artifacts)
    return result


def render(target, bases, cookie):
    """Reuse the production lifecycle, replacing only installation/base layers."""
    original = tool.render_multiarch_dockerfile([target], bases, cookie, [target.image])
    start = original.index('FROM --platform=')
    end = original.index('\nFROM package-${TARGETARCH} AS final')
    pinned = bases[target.platform]['pinned']
    filename = target.package['filename']
    replacement = f'''# The full UBI image is an installer only; none of its layers reach runtime.
FROM --platform=linux/amd64 {pinned} AS install-amd64
RUN --mount=type=bind,from=download-amd64,target=/opt/openriak-package,ro <<'OPENRIAK_MINIMAL_INSTALL'
set -eu
# Resolve current runtime packages from this RHEL release, without weak dependencies.
mkdir -p /openriak-rootfs
dnf install -y --refresh --installroot=/openriak-rootfs --releasever={target.release} --setopt=install_weak_deps=False --setopt=tsflags=nodocs {RUNTIME_PACKAGES}
# Install the verified official package; its OTP runtime is bundled in the RPM.
rpm --root /openriak-rootfs -Uvh --replacepkgs --nodeps /opt/openriak-package/{filename}
# Preserve the RPM database and an explicit inventory for vulnerability scanners.
mkdir -p /openriak-rootfs/usr/share/openriak-build
rpm --root /openriak-rootfs -qa --qf '%{{NAME}} %{{VERSION}}-%{{RELEASE}}\\n' > /openriak-rootfs/usr/share/openriak-build/runtime-packages.txt
# Install escript's compatibility link without retaining the installer tools.
for bundled_escript in /openriak-rootfs/usr/lib64/riak/erts-*/bin/escript /openriak-rootfs/usr/lib/riak/erts-*/bin/escript
do
    if [ -x "$bundled_escript" ]
    then
        ln -sf "${{bundled_escript#/openriak-rootfs}}" /openriak-rootfs/usr/bin/escript
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
OPENRIAK_MINIMAL_INSTALL

FROM scratch AS package-amd64
COPY --from=install-amd64 /openriak-rootfs/ /
# Standard command search path for the shell-based OpenRiak KV lifecycle.
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
'''
    return original[:start] + replacement + original[end:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', default='3.4.1')
    parser.add_argument('--release', choices=['8', '9'], default='9')
    parser.add_argument('--timeout', type=int, default=tool.DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument('--output', type=pathlib.Path)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    targets = [t for t in tool.discover_targets([args.version]) if t.family == 'rhel' and t.release == args.release and t.platform == 'linux/amd64']
    if not targets:
        parser.error('No matching RHEL amd64 package in the documentation metadata')
    output = (args.output or tool.REPOSITORY_ROOT / 'tools/cache/openriak-docker-minimal-validation' / tool.run_id()).resolve()
    output.mkdir(parents=True, exist_ok=False)
    target = max(targets, key=lambda t: int(t.otp))
    target = dataclasses.replace(target, grouped=True, output_root=output,
                                identity=tool.ImageIdentity(namespace='openriak-minimal-validation'))
    retained_image = target.image + '-' + tool.run_id().lower()
    summary = {'experiment': 'minimal-rhel-runtime', 'output': str(output), 'image': retained_image,
               'platform': target.platform, 'version': target.version, 'release': target.release,
               'started_at': tool.isoformat(), 'status': 'running'}
    summary_path = output / 'validation.json'
    summary_path.write_text(json.dumps(summary, indent=2) + '\n')
    print('Evidence:', output, flush=True)
    original_verify = tool.verify_runtime_options

    def verify(container, t, timeout, log):
        result = original_verify(container, t, timeout, log)
        tool.run_logged([tool.docker_command(), 'exec', container, '/bin/sh', '-ec', '''
for unwanted in python python3 perl pip pip3 dnf microdnf yum rpm
 do
    if command -v "$unwanted" >/dev/null 2>&1
    then
        echo "Unexpected runtime command: $unwanted" >&2
        exit 1
    fi
 done
# Also check files, so absence from PATH alone cannot satisfy the experiment.
if find /usr /opt -type f \\( -iname '*python*' -o -iname '*setuptools*' -o -name 'perl' \\) | grep .
then
    echo 'Unexpected interpreter or Python package files' >&2
    exit 1
fi
cat /usr/share/openriak-build/runtime-packages.txt
'''], log.parent / f'minimal-runtime-{container}.log', timeout_seconds=timeout)
        if 'image_inspection' not in summary:
            inspection = json.loads(tool.run_logged([tool.docker_command(), 'container', 'inspect', container],
                log.parent / 'minimal-container-inspect.log', timeout_seconds=timeout).stdout)[0]
            tool.run_logged([tool.docker_command(), 'image', 'tag', inspection['Image'], retained_image],
                log.parent / 'retain-minimal-image.log', timeout_seconds=timeout)
            image = json.loads(tool.run_logged([tool.docker_command(), 'image', 'inspect', retained_image],
                log.parent / 'minimal-image-inspect.log', timeout_seconds=timeout).stdout)[0]
            summary['image_inspection'] = {'id': image['Id'], 'size_bytes': image['Size'], 'layers': image['RootFS']['Layers']}
            summary_path.write_text(json.dumps(summary, indent=2) + '\n')
        result['minimal_runtime'] = 'No Python, Perl, pip, setuptools or package-manager commands/files'
        return result

    tool.verify_runtime_options = verify
    try:
        with tool.MultiarchBuilderLifecycle() as lifecycle:
            tool.ensure_multiarch_builder(output / 'logs', args.timeout, lifecycle)
            base, pinned = tool.resolve_base_image(target, output / 'logs', args.timeout)
            bases = {target.platform: {'requested': base, 'pinned': pinned, 'resolved_at': tool.isoformat()}}
            cookie = tool.generate_distributed_cookie()
            tool.render_group_assets([target], bases, cookie, [target.image], 5, target.group_directory)
            (target.group_directory / 'Dockerfile').write_text(render(target, bases, cookie))
            summary['base_image'] = bases[target.platform]
            passed = tool.refresh_target(target, args.timeout, cluster_nodes=5,
                prepared={'base_images': bases, 'distributed_cookie': cookie},
                progress=lambda m: print(tool.log_timestamp(), m, flush=True))
            summary['status'] = 'passed' if passed else 'failed'
            summary['integration_report'] = str(target.cache_directory / 'report.json')
        if passed:
            print(tool.log_timestamp(), 'Scanning the retained image and validating its package inventory', flush=True)
            summary['scout'] = scan_image(retained_image, target.platform, args.timeout, summary_path)
    except BaseException as error:
        summary['status'] = 'error'
        summary['error'] = str(error)
        raise
    finally:
        tool.verify_runtime_options = original_verify
        summary['finished_at'] = tool.isoformat()
        summary_path.write_text(json.dumps(summary, indent=2) + '\n')
        print(json.dumps(summary, indent=2), flush=True)
    return 0 if summary['status'] == 'passed' else 1

if __name__ == '__main__':
    raise SystemExit(main())
