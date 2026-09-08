# Reusable patched Debian base validation — 2026-09-08

The generator now supports the independent image `{namespace}/debian:bookworm-slim-for-openriak`, based on pinned `debian:bookworm-slim`. Debian 12 OpenRiak KV Dockerfiles consume this image by immutable digest for every metadata-backed KV/OTP variant and selected namespace.

## Base image

The locally built and approved image is `openriak/debian:bookworm-slim-for-openriak` (82,454,219 bytes, about 78.6 MiB). Its OCI index digest is `sha256:d48fefcffa3e3a49aac8317b5ad203a523d7e7e845694619fb56a1083653154e`.

It contains Debian package updates and the tested OpenSSL `3.0.22-0openriak1~deb12u1` backport. Source hashes, Debian patches, ABI checks, mandatory upstream tests, and maintenance limits are unchanged from the [OpenSSL backport validation](openssl-backport-validation-2026-09-08.md). Previously validated compiler/test layers were reused for this base build.

The final base has no OpenRiak KV package, Erlang cookie, compiler, build sources, or downloaded package files. It retains Debian package-management tools for reuse. KV installation subsequently removes unnecessary runtime packages, including Perl, and flattens the cleaned filesystem so removed bytes do not survive in lower KV layers.

Base smoke checks passed: Debian 12 identity, minimum OpenSSL package version, absence of build artifacts, known-answer SHA-256, and certificate generation/verification. The exported OCI platform config digest exactly matches the image ID used for those tests. Cache reuse and push preflight (including a secondary namespace) passed without registry writes.

## Dependent KV validation

| OpenRiak KV image | Architecture | Single node | Five-node cluster | OTP crypto/TLS |
| --- | --- | --- | --- | --- |
| 3.4.0-debian-12-otp24 | amd64 | Passed | Passed | Passed |
| 3.4.0-debian-12-otp26 | amd64 | Passed | Passed | Passed |
| 3.4.1-debian-12-otp26 | amd64 | Passed | Passed | Passed |

Tests include `riak admin test` on the single node and every cluster node, healthchecks, CLI/HTTP pings, populated mounts, consistent membership, ring readiness, transfers, cookie adoption, and graceful shutdown. Compatibility probes exercise packaged OTP cryptography and certificate-verified TLS over IPv4 and IPv6.

The local approved base archive was supplied using BuildKit's `oci-layout` context override, avoiding publication during validation. After enabling the production mapping, all three generated Dockerfiles matched the tested files byte for byte, and the production runtime assertions passed against their exact tested image IDs. All 193 unit tests passed. The harness removed its test containers and stopped the builder it had started.

Raw Scout counts remain 1 Critical, 8 High, 3 Medium, and 34 Low per KV image. This restructuring does not introduce new OpenSSL fixes beyond the existing backport. The previously documented broad Debian vulnerability matches and conditional CVE statuses still apply; old published images have not acquired these changes.

## Publication and reuse

```sh
tools/openriak-docker/openriak-docker base refresh --namespace tiotjp
tools/openriak-docker/openriak-docker base push --namespace tiotjp --whatif
tools/openriak-docker/openriak-docker base push --namespace tiotjp
```

Publish the base first, then use normal KV `refresh --force` and `push` with the same namespace. `base refresh --force` updates the upstream digest, rebuilds without cached layers, and retests. Existing pinned KV images require an explicit refresh to adopt a newer base. No registry push, normal KV cache replacement, or documentation publication was performed by this validation.

See the [machine-readable evidence](patched-base-validation-2026-09-08.json) for image IDs, hashes, and retained report paths, and the [command documentation](../README.md#reusable-patched-debian-base) for options.
