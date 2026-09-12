# Reusable patched OS bases — 2026-09-12

Custom library patches now belong to independently approved OS base images, shared
by every OpenRiak KV/OTP version that uses that OS release.

| Base selector | Namespace-relative tag | Patches |
| --- | --- | --- |
| `debian-12` (existing default) | `debian:bookworm-slim-for-openriak` | OpenSSL and libblkid; runtime tar removal |
| `rhel-9` | `rhel:9-for-openriak` | PCRE2 CVE-2026-89161 |
| `centos-9` | `centos:stream9-for-openriak` | PCRE2 CVE-2026-89161 |

The implementation inventory found no other custom source-library backports in
production OS layers. Other fixes use vendor package updates, package removals,
repository selection or OpenRiak launcher compatibility changes. The launcher
changes remain in the KV installation step because the base contains no KV package.

## EL9 build design

The source RPM, SHA-256, patch, upstream suite and positive/negative regression
checks are unchanged from the [PCRE2 validation](pcre2-security-validation-2026-09-12.md).
They now run when building the reusable OS base. Native patched RPMs are installed
into the minimal runtime filesystem; compiler/source/package-installation files
remain in a discarded installer stage. The final base keeps the RPM database,
package inventory and PCRE2 test logs, with no KV package or cookie.

A child Dockerfile takes the base by immutable digest and copies its filesystem
into an installer from the same OS release. The build-only installer image is
also digest-pinned, in `runtime-images.json`. It verifies the inherited PCRE2
package meets the required version, installs the official KV RPM, and exports
only the runtime filesystem. It does not compile PCRE2.

## Validation and publication

All 297 Python tests passed. Rendering checks covered every metadata-derived
single-platform/grouped target with default and custom settings. Only the 16
RHEL 9/CentOS 9 Dockerfile hashes changed; all other Dockerfiles and all Compose
and environment files remain byte-identical to the reviewed baseline.

The existing Debian base was not regenerated. Previous KV approvals, downloads,
archives, historical logs and registry CVE reports remain intact. New base builds
have their own approvals under `tools/cache/openriak-docker-bases/tiotjp/`.

Both new amd64 bases passed build, upstream/regression tests, exported-runtime
checks, archive validation and push preflight:

| Image | Completed (UTC) | Result |
| --- | --- | --- |
| `tiotjp/rhel:9-for-openriak` | 2026-09-12 13:33:39 | Passed |
| `tiotjp/centos:stream9-for-openriak` | 2026-09-12 13:38:53 | Passed |

Their installed PCRE2 libraries are byte-identical to the corresponding libraries
that passed the earlier KV single-node and five-node tests. Source compilers,
Python, Perl and package managers are absent from both exported bases. The
[companion JSON](reusable-os-bases-2026-09-12.json) records immutable digests,
archive/Dockerfile hashes, platform image IDs and captured regression evidence.

These base checks do not replace KV single-node/five-node tests after the child
Dockerfile changes. Publish both bases, then refresh/retest and publish their
dependent KV images. No registry publication was performed. Test containers were
removed and the dedicated builder stopped after completion.


## Hierarchical generator refactor

Base recipes and runtime checks now live under `builders_base/`, with shared,
package-family, OS-family, OS-release and optional architecture layers. The
shared `openriak_base.py` contains no OS-specific recipes or tests. The selector
catalogue and default are in `builders-base.json`.

All 301 Python tests passed after the refactor. A captured pre-refactor baseline
confirms identical base Dockerfiles and runtime-check scripts for every configured
metadata-backed base/platform selection, with default and TI Tokyo identities.
The complete KV rendering baseline also passes. Architecture dispatch and
release-specific dependency isolation have dedicated coverage.

Read-only validation accepted the existing TI Tokyo Debian, RHEL and CentOS base
approvals with byte-identical Dockerfiles and unchanged reports. No images were
rebuilt, containers started, archives replaced or registry pushes performed for
this refactor.
