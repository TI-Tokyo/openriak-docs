# Rocky 9 security validation — 2026-09-12

> Historical snapshot. See the [current CVE review](cve-review-latest.md) for the latest verified image results and resolved actions.

Rebuilt the Rocky 9 / OTP26 images for OpenRiak KV 3.4.0 and 3.4.1 on amd64.
Both passed all single-node and five-node cluster tests, including `riak admin test`
on the single node and each of the five cluster nodes. Local Docker Scout scans
of both exact exported image configurations reported **zero CVEs of any severity**.

Removed optional Vim packages with dependency checks and required
`coreutils-single >= 8.32-41.el9_8.1`. Newer vendor updates remain allowed;
a stale mirror now fails the build. The rules apply to every Rocky 9 target.
Other OS rendering hashes and rebuild fingerprints are unchanged.

The 292 unit tests passed. Current Dockerfiles, Compose files, environment files
and Downloads metadata were updated for both images. Existing TI Tokyo labels
and all three `tiotjp` aliases per version were preserved. Historical reports
and OCI archives remain on disk; OCI archives are ignored by Git.

## Local image results

| Image | Single node | Five-node cluster | Local Scout CVEs |
| --- | --- | --- | ---: |
| tiotjp/openriak-kv:3.4.0-rocky-9-otp26 | Passed | Passed | 0 |
| tiotjp/openriak-kv:3.4.1-rocky-9-otp26 | Passed | Passed | 0 |

## Docker Hub

No registry push was performed. Both images pass push preflight. To publish all
aliases and download fresh registry Scout reports:

```sh
tools/openriak-docker/openriak-docker push \
  --version 3.4.0 --version 3.4.1 \
  --os-id 'rocky-9*' --namespace tiotjp
```

Until that push, the registry still contains the older images. The Downloads
metadata intentionally does not reuse those older scans for the new approvals.

[Validation evidence](rocky9-security-validation-2026-09-12.json) includes image
and configuration digests, package checks, test results, and references to the
complete compressed Scout SARIF/SBOM payloads.
