# PCRE2 CVE-2026-89161 remediation

This review corrects the initial version-only assessment. The reported seven
image/CVE pairs do not all need a new library.

| Images | Verified finding | Action |
| --- | --- | --- |
| Debian 12: KV 3.4.0 OTP24/26 and 3.4.1 OTP26 | The vendor package `10.42-1+deb12u1` already contains the upstream fix. Extracted registry libraries pass the public-API regression. | Record a vendor backport, scoped to the reviewed package and image digest. |
| CentOS 8 and RHEL 8: KV 3.4.1 OTP26 | PCRE2 10.32 predates `PCRE2_COPY_MATCHED_SUBJECT`. Both registry libraries reject the option with `PCRE2_ERROR_BADOPTION`. | Record a false positive, scoped to the reviewed package and image digest. |
| CentOS 9 and RHEL 9: KV 3.4.0/3.4.1 OTP26 | Registry libraries reproduce an invalid free and a leaked allocation when match data is reused for JIT matching. | Backport the upstream fix into native `10.40-6.el9.openriak1` RPMs. |

The archived OCI manifests, configurations and layers were verified against their
recorded hashes before extracting the libraries. This avoids relying on local
Docker tags, which can differ from distributed builds. The captured library
hashes, results and archive references are in the
[machine-readable evidence](pcre2-security-validation-2026-09-12.json).

## Implementation

`builders/pcre2.py` contains the upstream ten-line library change adapted to the
older source filename. It retains the source RPM's vendor patches, configuration,
SONAMEs and package metadata. The source RPM is downloaded from Rocky's official
EL9 source repository with an exact SHA-256 check and compiled inside each target
OS's installer. It does not replace the target OS with Rocky.

The OS release layers select the helper for RHEL 9 and CentOS 9 only. Both OpenRiak
KV versions receive the change; unrelated Dockerfiles remain byte-identical.
A newer vendor package is retained instead of being downgraded. Only runtime
packages, inventory and build/test logs reach the final filesystem.

## Validation

The distribution's full PCRE2 test suite remains enabled. An additional test uses
custom allocation callbacks to detect the invalid free and leaked copied subject
through public PCRE2 APIs, for all three character widths (8, 16 and 32 bits).
It must pass on the patched libraries, fail with exit 42 when the patch is removed,
and pass again after restoring it. It also runs against the installed runtime
library. Removing/restoring the patch touches the containing JIT compilation unit
because RPM builds disable automatic include-dependency tracking.

All four `linux/amd64` images passed the full OpenRiak KV integration suite:

| Image tag (under `tiotjp/openriak-kv`) | Single node | Five-node cluster | Completed (UTC) |
| --- | --- | --- | --- |
| `3.4.0-centos-9-otp26` | Passed | Passed | 2026-09-12 12:42:17 |
| `3.4.0-rhel-9-otp26` | Passed | Passed | 2026-09-12 12:53:57 |
| `3.4.1-centos-9-otp26` | Passed | Passed | 2026-09-12 13:03:13 |
| `3.4.1-rhel-9-otp26` | Passed | Passed | 2026-09-12 12:31:53 |

Each suite includes `riak admin test` on the single node and all five cluster
nodes, CLI and HTTP pings, healthy containers, consistent membership, populated
volumes, configuration/cookie preservation, coordinator cookie adoption and
graceful shutdown. No ARM64 tests were run.

The final runtime libraries pass the CVE regression and retain exactly the
original libraries' exported ABI symbols. All 293 Python unit tests and the
Docker CVE metadata/live-watcher tests passed. Rendering checks confirm that
unrelated target files remain unchanged.

All four OCI archives and approval reports were validated, and their four
downloadable files match the published static copies. The generated version
metadata contains all 17 passed targets for 3.4.0 and 18 for 3.4.1. Push preflight
accepts all four replacement images and their secondary tags. Test containers
were removed and the build worker stopped; the documentation preview remains up.

The replacement images have **not been pushed**. Existing registry Scout reports
remain evidence for the previous image digests. The four new backport assessments
require the replacement digest and patched package version, so they do not exempt
the old vulnerable images. Push and scan the replacement images to update those
registry results.

## Sources

- [Upstream fix](https://github.com/PCRE2Project/pcre2/commit/82443294822e9d7a650b2f38dfc6144270a78420)
- [Debian security source](https://security.debian.org/debian-security/pool/updates/main/p/pcre2/pcre2_10.42-1+deb12u1.diff.gz)
- [PCRE2 10.32 API](https://github.com/PCRE2Project/pcre2/blob/pcre2-10.32/src/pcre2.h.generic)
- [EL9 source RPM](https://dl.rockylinux.org/pub/rocky/9/BaseOS/source/tree/Packages/p/pcre2-10.40-6.el9.src.rpm)
