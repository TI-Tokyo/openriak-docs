# Minimal runtime experiments

The metadata-driven matrix validates candidates for every image with Critical
or High findings in a saved CVE review:

```sh
python3 tools/openriak-docker/experiments/minimal_matrix.py --jobs 2 --timeout 1800
```

It uses the production renderer with the isolated strategies in
`runtime-candidates.json`. It never enables those strategies in production;
update `../runtime-images.json` only after the relevant tests pass.

| Option | Meaning |
| --- | --- |
| `--review FILE` | Saved review defining affected images; defaults to `../reports/cve-review-2026-09-08.json`. |
| `--family FAMILY` | Limit candidates to an OS family; repeatable. |
| `--image-tag TAG` | Limit to an exact image tag without repository; repeatable. |
| `--severity LEVEL` | Select saved findings of this severity; repeatable. Defaults to `CRITICAL` and `HIGH`; use `MEDIUM` for Medium findings. |
| `--jobs 1\|2` | Concurrent image tests; default `2`. |
| `--timeout SECONDS` | Timeout per expensive phase; default `1800`. |
| `--openssl-backport` | Test the Debian 12 OpenSSL 3.0.22 candidate, including packaged-OTP crypto/TLS compatibility. |
| `--base-cache PATH` | Validate against an approved patched-base directory using its local OCI archive; implies the Debian 12 crypto/TLS checks. No registry push is needed. |

Each selected image runs on **linux/amd64 only**, with single-node and five-node
integration tests, `riak admin test` on every node, runtime inventory checks,
and Docker Scout scans. Reports, generated files and compressed SARIF/SBOM data
are retained in a new timestamped directory under
`tools/cache/openriak-docker-minimal-validation/`. A final `matrix.json` records
all results, including failures. Failed attempts are preserved for diagnosis.
The builder has one shared lifecycle across concurrent jobs and returns to its
original running/stopped state after all jobs finish.

Explicit `--image-tag` selections do not require a finding in the review file.
They still require a metadata-backed amd64 package. This lets a fix be validated
across sibling OpenRiak KV versions even when only one version has a finding.

For example, test the runtime cleanup candidate on one Ubuntu image:

```sh
python3 tools/openriak-docker/experiments/minimal_matrix.py \
  --image-tag 3.4.0-ubuntu-jammy-otp24 --jobs 1 --timeout 1800
```

Candidate configuration supports exact RPM `remove_packages` lists (dependency
checks stay enabled), Debian `minimum_packages` version checks, `remove_tar`,
and a `perl_removal` method. `perl_removal: "dpkg"` is reserved for a final
runtime whose Essential installation helpers prevent apt's dependency solver
from removing Perl. Installation must finish first; PAM/login are retained,
and package maintenance must happen in a build stage. These options affect the
generated files and therefore invalidate previous cache inputs when enabled.

## Original RHEL proof of concept

Build and test an isolated **OpenRiak KV** image using RHEL runtime packages
installed into an empty filesystem. The full pinned UBI image supplies the
installer tools; only the runtime filesystem reaches the final `scratch` stage.
The official metadata-selected OpenRiak KV RPM is downloaded and checksum
verified, with its bundled OTP runtime. OpenRiak KV is not compiled from source.

```sh
python3 tools/openriak-docker/experiments/rhel_minimal.py \
  --version 3.4.1 --release 9 --timeout 1800
```

Requires the same Docker/Buildx setup as `openriak-docker refresh`, plus Docker
Scout and its authentication. Runs single-node and five-node integration tests
on **linux/amd64 only**, then saves full compressed Scout SARIF and SBOM data.
The highest metadata-backed OTP version is selected. The runtime checks fail if
Python, Perl or package managers reappear; the scanner checks that the OS and
OpenRiak KV RPM inventory remain identifiable. A unique experimental image tag
is retained locally for inspection. Containers and networks are cleaned up, and
the builder returns to its original running/stopped state.

Options:

| Option | Meaning |
| --- | --- |
| `--version VERSION` | OpenRiak KV version; default `3.4.1`, minimum `3.4.0`. |
| `--release 8\|9` | RHEL major release; default `9`. Both releases have passed amd64 validation. |
| `--timeout SECONDS` | Timeout per expensive phase/command; default `1800`. |
| `--output DIRECTORY` | New, isolated output directory; defaults to a timestamped directory under `tools/cache/openriak-docker-minimal-validation/`. An existing directory is rejected to preserve evidence. |

The experiment does not publish downloads, update documentation metadata, push
images, or modify approved production caches. Validated strategies are now
integrated into the production generator through `../runtime-images.json`.
Runtime package updates require rebuilding the
image; there is no package manager in the final image.

See [the RHEL 9 results](../reports/rhel-minimal-validation-2026-09-08.md).

### Debian 12 OpenSSL backport

Prototype all affected metadata-backed Debian 12 amd64 images, using isolated
reports and tags:

```sh
python3 tools/openriak-docker/experiments/minimal_matrix.py \
  --openssl-backport --jobs 1 --timeout 1800
```

Add `--image-tag 3.4.0-debian-12-otp24` to select a canary. The backport builds
OpenSSL only, with Debian packaging and the static/shared upstream test suites.
The harness runs the normal single-node and five-node integration tests and a
separate bundled-OTP crypto/TLS compatibility probe, then saves full compressed
Scout output. It does not publish or replace production approvals.

The crypto probe verifies runtime linkage, SHA-256/HMAC/PBKDF2 known-answer
vectors, random generation, AES-GCM/ChaCha20-Poly1305 authenticated encryption
(including empty payloads and rejected forged tags), ECDH, RSA signatures, and
certificate-verified TLS 1.2 and 1.3 request/response exchanges over IPv4 and
IPv6. It can be replayed against a retained local image:

```sh
python3 tools/openriak-docker/experiments/openssl_compatibility.py IMAGE \
  --output /tmp/openriak-openssl-check --timeout 1800
```

The default required runtime library is 3.0.22; `--version 3.0.20` can validate
the test harness against the previous image. Test containers use only loopback
networking and are removed after completion or failure.
