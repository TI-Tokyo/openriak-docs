# Debian 12 libblkid backport and tar removal — 2026-09-08

The locally built and approved base is `tiotjp/debian:bookworm-slim-for-openriak`.
Its OCI digest is `sha256:857fff6b7d9698aeb6d04777dc4d7b33ab4254c0a33b0887a78cb88c8ef0376b`
and its image size is 81,861,339 bytes (about 78.1 MiB).

It retains OpenSSL `3.0.22-0openriak1~deb12u1`, installs the new
`libblkid1 2.38.1-5+deb12u3+openriak1` backport, and removes GNU tar.
The upstream Debian image, source archives, Debian packaging and upstream fix
are pinned by digest or checksum in the generated Dockerfile.

The libblkid fix is upstream commit
[`132d9c8`](https://github.com/util-linux/util-linux/commit/132d9c8aa15a8efd0a23d8ca7ed8b98f365e84fa),
adapted only for Bookworm's `realloc` context and whitespace. Debian's existing
patches, configuration, library ABI and symbol checks are retained. Only the
libblkid1 runtime package is installed from this build; other util-linux binaries
retain Debian's packages and are not claimed to contain additional fixes.

Validation passed:

- Debian library symbol/ABI checks and all six upstream blkid test groups.
- Partition-pointer stability through repeated growth, nested tables and reset;
  Valgrind reported zero errors and zero leaked bytes.
- The same regression rejected the original vulnerable partition implementation.
- Base runtime assertions, OpenSSL digest and certificate checks, and verification
  that the OCI archive contains the exact tested image configuration.
- All 195 generator unit tests.

| OpenRiak KV variant | Architecture | Single node | Five-node cluster | OTP crypto/TLS |
| --- | --- | --- | --- | --- |
| 3.4.0 Debian 12 OTP24 | amd64 | Passed | Passed | Passed |
| 3.4.0 Debian 12 OTP26 | amd64 | Passed | Passed | Passed |
| 3.4.1 Debian 12 OTP26 | amd64 | Passed | Passed | Passed |

KV checks include `riak admin test` on the single node and every cluster node,
HTTP/CLI pings, healthchecks, configuration and bind mounts, consistent membership,
ring readiness, transfers, cookie adoption and graceful shutdown. Runtime assertions
require the exact reviewed libblkid package version and absence of tar, Perl and
Python. Crypto checks exercise the packaged OTP, including verified TLS over IPv4
and IPv6. Tests used the approved local base OCI archive without registry publication.

GNU tar is also needed by dpkg. The runtime base intentionally lacks that dependency;
ordinary apt/dpkg installation requires bootstrapping tar first. The KV generator
mounts tar from a pinned Debian tools stage, copies it to `/bin/tar` for dpkg,
installs the package temporarily and purges it after KV installation. Flattening
removes the old bytes from runtime layers. The mounted bootstrap binary is absent
from the final image. Custom child images need the same installation pattern.

Fresh local Scout scans of all three variants report 1 Critical, 8 High, 2 Medium
and 33 Low findings before our assessments. The tar CVE is absent. Scout still
reports CVE-2026-13595 using both the patched libblkid source version and the
unchanged util-linux source version. This is not a failed backport: the regression
and installed package prove the fix, but mixed source-version matches need an
assessment tied to the actual rebuilt image. Existing published images are not
excluded merely because this base has been built.

The approved base is in the normal `tools/cache/openriak-docker-bases/tiotjp/`
cache. Previous current files were saved under `snapshots/`; historical runs,
failed prototype evidence and previous KV approvals were preserved. Test containers
were cleaned up and the builder was stopped after validation.

Publish the approved base, then refresh and publish the dependent KV images:

```sh
tools/openriak-docker/openriak-docker base push --namespace tiotjp
```

Use the normal KV refresh command with `--force` to guarantee adoption of the new
base digest, followed by KV `push` for registry publication and fresh Scout reports.
No registry push or replacement of normal KV cache/download approvals was performed
by this validation.

Exact image IDs, report paths and scan evidence are in the
[machine-readable report](debian12-libblkid-tar-validation-2026-09-08.json).
