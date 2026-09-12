# Generator refactor validation — 2026-09-11

The refactor preserves generated OpenRiak KV image behavior and adds distributed
planning, worker execution and verified result collection. No image builds,
container starts, integration reruns or registry pushes were performed for this
refactor. Existing cache approvals, historical evidence and published files were
preserved.

## Generated output

A baseline was captured from the dirty working tree before moving code, including
the preceding Debian 11 repository fix. This deliberately compares against the
user's working source, rather than the older Git HEAD.

- 45 metadata-derived platform targets, comprising 35 shared image groups.
- Both default settings and custom TI Tokyo identity/lifecycle settings.
- Fixed cookies and base digests for deterministic comparison.
- Dockerfile, single-node Compose, cluster Compose and example.env for every case.
- **640 of 640 artifacts are byte-for-byte identical.**

The durable hash fixture is `../tests/rendering-baseline.json`. Its regression test
discovers targets from metadata and checks both target coverage and every file.

## Unit and local workflow checks

**238 tests passed.** Run the suite with direct Docker/Skopeo calls prohibited:

```sh
python3 tools/openriak-docker/tests/run_without_docker.py
```

Coverage includes selected dependency invalidation; byte-verified migration of
legacy approvals; live subprocess logs; atomic report writes; interruption
checkpoints; locks across processes; diagnostics; saved CVE comparisons; complete
matrix assignment; standalone source bundles; simulated workers; OCI archive
validation; receipt/hash failures; destination symlinks; conflicting historical
evidence; and publication failure recovery.

Distributed tests use synthetic OCI archives and mocked builds. Real execution
across multiple machines remains unverified and should be validated during the
first manually started distributed run.

## Current cache compatibility

This read-only command returned **35 SKIP, zero rebuilds, zero blocked groups**:

```sh
tools/openriak-docker/openriak-docker refresh \
  --version 3.4.0 --version 3.4.1 --retry-failed --whatif \
  --vendor 'TI Tokyo' --source 'https://github.com/TI-Tokyo/openriak-docs' \
  --url 'https://www.tiot.jp/' --namespace tiotjp
```

No cache migration was written by the preview. Compatible legacy approvals migrate
only during a subsequent explicit refresh. The Git status outside this tool's
directory was unchanged from the initial status capture.
