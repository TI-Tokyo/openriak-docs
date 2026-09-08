# Debian 12 OpenSSL compatibility backport — 2026-09-08

Validated and enabled in the generator for every metadata-backed Debian 12
OpenRiak KV image. All three current amd64 variants passed. Production images
and downloads have not been replaced by this isolated validation.

## Scope and source

The generator upgrades Debian 12 OpenSSL from `3.0.20-1~deb12u2` to
`3.0.22-0openriak1~deb12u1`. OpenRiak KV and its bundled Erlang/OTP remain the
official, checksum-verified package binaries. The change applies by OS release,
covering all metadata-backed Debian 12 KV/OTP variants.

- Upstream source: [OpenSSL 3.0.22](https://github.com/openssl/openssl/releases/download/openssl-3.0.22/openssl-3.0.22.tar.gz),
  SHA-256 `67ebca7e50d17383028045486653492195b83db95f8558709701bb47b5c1ef81`.
- Packaging: [Debian Bookworm 3.0.20-1~deb12u2](https://deb.debian.org/debian/pool/main/o/openssl/openssl_3.0.20-1~deb12u2.debian.tar.xz),
  SHA-256 `7279efe85c359500c95aa88347e3395dd303d7566e2bb818d80d96e0c3bb9629`.
- The [upstream security advisory](https://openssl-library.org/news/secadv/20260825.txt)
  and source changelog record fixes for CVE-2026-75803, CVE-2026-54874,
  CVE-2026-63072, and CVE-2026-63076.

This is an OpenRiak-maintained backport, not an official Debian security update.
It retains Debian configuration, `libcrypto.so.3`/`libssl.so.3` names, package
ownership and ABI symbol checks. A newer installed Debian package is retained.
Only `libssl3` and `openssl` binary packages enter the runtime. Build tools,
source, headers, static libraries and build logs remain in the build stage.

Nine Debian configuration/build patches are retained; security patches already
present in upstream 3.0.22 are omitted. Their exact names, the source pins, and
the test-only patch are embedded in every generated Dockerfile by
[`openriak_minimal.py`](../openriak_minimal.py).

## Upstream testing and builder networking

The initial attempts found a builder networking problem: IPv6 loopback sockets
could bind, but IPv6 connections failed. The same compiled OpenSSL binaries
completed IPv4, hostname and IPv6 CMP exchanges in a fresh Docker container.

OpenSSL has independent bind-only IP detection in both `OpenSSL::Test::Utils`
and `TLSProxy::Proxy`. The build's test-only patch checks an actual local
connection before declaring that family usable, and skips two explicitly
host-dependent CMP cases when IPv6 connectivity is absent. No library source
or IPv6 feature is disabled. Tests run in a network-isolated build step.

Both **upstream test suites without the container-network patch**, using the
Debian-patched source from the second attempt and working IPv6 networking,
passed independently:

| Suite | Recipes | Tests | Result |
| --- | ---: | ---: | --- |
| Static | 259 | 2,980 | PASS |
| Shared | 259 | 3,415 | PASS |

The independent run completed at `2026-09-08T07:40:06Z`. Its log, runner and
summary are preserved under
`tools/cache/openriak-docker-minimal-validation/20260908T072303.367342Z/openssl-upstream/`.
The uncompressed log SHA-256 is
`a5a817fe417b536070b92404acd6d7aea0cceab96bbc8ca721521c8aef5d38c3`.
Failed image attempts are retained separately and are not counted as passes.

In the final Dockerfile, compilation/package creation and upstream testing are
separate cached steps. `dpkg-buildpackage` defers tests with `nocheck`, but both
static and shared suites must subsequently pass before any package can be
exported to the runtime stage. Unit tests verify that failure of either suite
prevents export. Debian's symbol checks are not bypassed.

The final package build passed `dh_makeshlibs ... -- -c4`. Its complete log is
under `20260908T074710.902344Z/openssl-packaging/` in the validation cache.
The deferred suites also passed against the packaged build: static 2,980 tests
in 155 seconds; shared 3,415 tests in 180 seconds. Their complete compressed
logs and checksums are under `20260908T080013.454733Z/openssl-upstream/`.
Debian source patches are restored after package creation, and the upstream
`run_tests` target tests the existing binaries without recompiling them.

## OpenRiak KV validation

Only amd64 is integration-tested, as requested.

| Image tag suffix | Single node | Five nodes | Crypto/TLS | Runtime size |
| --- | --- | --- | --- | ---: |
| `3.4.0-debian-12-otp24` | PASS | PASS | PASS | 123.15 MiB |
| `3.4.0-debian-12-otp26` | PASS | PASS | PASS | 124.76 MiB |
| `3.4.1-debian-12-otp26` | PASS | PASS | PASS | 124.84 MiB |

Each image passed the existing single-node and five-node harness, including
`riak admin test` on every node, CLI/HTTP pings, health checks, ring/membership,
configuration, bind mounts, startup and graceful shutdown. A separate probe
uses the packaged OTP to check dynamic library linkage; SHA-256, HMAC and
PBKDF2 known-answer vectors; random generation; AES-GCM/ChaCha20-Poly1305 with
empty payloads and rejected forged tags; ECDH; RSA; and certificate-verified
TLS 1.2/1.3 over both IPv4 and IPv6.

The final production renderer reproduces each tested Dockerfile byte-for-byte.
All **183 unit tests pass** with the production configuration enabled. The
[compact JSON report](openssl-backport-validation-2026-09-08.json) records image
IDs, source/artifact hashes, package versions and paths to complete validation,
integration and scanner evidence. The test containers were removed and the
builder was returned to its stopped state.

The same crypto/TLS probe passed against the existing OTP24 image with OpenSSL
3.0.20 before testing the upgrade.

For OTP24, the probe confirms runtime linkage to `OpenSSL 3.0.22 25 Aug 2026`.
The official-package binaries are unchanged from the existing image:

| Binary | SHA-256 before and after |
| --- | --- |
| `crypto-5.0.6.5/priv/lib/crypto.so` | `4ae2bf802fcafaed245294a1d8ab0867453a391218c1cf560769011c9007d231` |
| `erts-12.3.2.17/bin/beam.smp` | `fca05e8b4975b53bef9b51d0e8a8c7b64bd2d50d10882b72930458441d9c7f30` |

## Scanner interpretation and deployment

Scout correctly identifies both installed packages as
`3.0.22-0openriak1~deb12u1`, but continues reporting all four OpenSSL CVEs. Its
Bookworm advisory has `affected_version: >0` and `fixed_version: not fixed`.
All three raw scans therefore still report **one Critical and eight High**
CVEs. These four OpenSSL findings are fixed in the backport according to the
upstream advisory and installed source version; the raw scanner evidence is
retained unchanged. Findings in util-linux and zlib are outside this update.

The backport is enabled in [`runtime-images.json`](../runtime-images.json).
[`cve-statuses.json`](../cve-statuses.json) records the fixed package version
for the existing OpenRiak/TI Tokyo Debian 12 image entries, with an explicit
condition: older 3.0.20 images still require rebuild and repush. These statuses
do not claim that the currently published images already contain the fix.

The existing pushed OTP24 image digest
`sha256:90e65639e34b8200baa7e510a229325017bb5b6df0d3e0d8f08a96e9b027467b`
contains OpenSSL 3.0.20. Its saved Scout result has one Critical and eight High
CVEs, four of which are the OpenSSL issues above. Changing the generator does
not fix that existing image. A tested refresh and a subsequent push are
required to distribute an updated image; `--do-not-test` reuses previously
approved Dockerfiles and is not the way to adopt this source change.

The [OpenSSL source page](https://openssl-library.org/source/) lists the end of
public support for the 3.0 branch as 7 September 2026. This backport addresses
the identified fixes; it does not extend upstream support. Revisit the override
when Debian provides an equivalent security update, and keep monitoring both
Debian and upstream advisories.
