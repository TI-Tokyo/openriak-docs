# Docker CVE assessments

Maintain one Markdown file per image tag and CVE:

```text
content/openriak-kv/docker/{version}/{docker-tag}/cve-{year}-{number}.md
```

For example: `3.4.1/3.4.1-rhel-9-otp26/cve-2026-40356.md`.
These files are assessment data, outside Hugo's documentation content mounts.
They do not appear in navigation, search, or as standalone pages.

```markdown
---
cve-id: CVE-2026-40356
image: openriak-kv:3.4.1-rhel-9-otp26
flags:
  falsePositive: true
appliesTo:
  packageVersions:
    krb5:
      - "1.21.1-10.el9_8"
---

Fixed in vendor package `krb5-libs 1.21.1-10.el9_8`.
See [RHSA-2026:19357](https://access.redhat.com/errata/RHSA-2026:19357).
```

The `image` field must match the directory tag and omit the registry and namespace.
This example covers `openriak/openriak-kv:3.4.1-rhel-9-otp26`,
`tiotjp/openriak-kv:3.4.1-rhel-9-otp26`, and the same image tag in other registries.
It does not cover a different version, OS release, or OTP tag. Scope checks still
apply even when the tag matches.

## Flags and status

`flags` is a mapping. Omit flags that are false, or omit the entire mapping if
none apply. Use YAML booleans (`true` and `false`), not quoted strings.

| Flag | Meaning | Included in the overall severity? |
| --- | --- | --- |
| `mitigated` | Exposure reduced, but the vulnerability may still apply. | Yes |
| `fixedByBackporting` | The installed package contains a verified backport. | No, when scope matches |
| `notRelevant` | The affected component or functionality is absent. | No, when scope matches |
| `falsePositive` | The scanner finding does not apply to the reviewed contents. | No, when scope matches |
| `unfixable` | No feasible fix is available for this image. | Yes, even with other flags |

When no flags are true, optional `status: Update available` supplies a short
label. Otherwise the status defaults to `Under investigation`. Missing files
also default to `Under investigation` and never hide Scout findings.

The Markdown body is required. Explain what was checked, why the conclusion
applies, and include links to advisories or evidence. Use inline code for package
versions and command options, Markdown links for sources, and paragraphs or
lists for longer explanations. A claim in prose alone never excludes a finding.

## Evidence scope

`appliesTo.packageVersions` maps Scout package names (often source package names)
to lists of **exact quoted versions**. Every reported package and architecture
for that CVE must match. Later versions are not automatically accepted.

For conclusions based on inspecting a particular image's files, use:

```yaml
appliesTo:
  imageDigests:
    - "sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
```

Replace the example with a reviewed OCI image/index digest, not a local image
configuration ID. A list can contain multiple reviewed digests, irrespective of
namespace. If both `imageDigests` and `packageVersions` are specified, both must
match. Unmatched evidence shows `Needs review` and keeps the Scout rating.
Omitting `appliesTo` makes the assessment apply to every report for this tag;
use a scope whenever the conclusion depends on particular image contents.

## Updating the Downloads page

Use the [current CVE review](../../../tools/openriak-docker/reports/cve-review-latest.md)
for the latest verified per-image counts. Dated review reports are historical
snapshots and can describe images that have since been replaced.

When a finding disappears, put the latest scan result before a clearly labelled
historical assessment. Preserve the earlier rationale and evidence, but do not
present old rebuild instructions as outstanding work. Claim a vendor fix only
after checking the installed package versions on every scanned architecture;
scan absence alone is insufficient. `status: Fixed by vendor update` is descriptive
and does not automatically exclude a finding. Keep such assessments scoped to
their reviewed image digests and package versions.

The development metadata watcher detects file additions, edits and deletions.
For a manual metadata-only refresh, run from the repository root:

```sh
node tools/scripts/sync-product-metadata.js --docker-only \
  --include-version openriak-kv=3.4.0 \
  --include-version openriak-kv=3.4.1
```

Normal builds read the files automatically. Generated version JSON remains a
cacheable helper consumed by the Downloads templates, not the editing source.
Scout reports and payloads remain unchanged. No Docker build, push or scan is
needed to edit an assessment.

Validation: `node tools/scripts/docker-cve-metadata.test.js`.

## Migration from JSON

The former 701 namespace-specific entries were migrated into 562 image/CVE
files. There were 129 identical namespace duplicates and 10 later reviews that
extended the earlier explanation and reviewed digest list. Those ten retain
the longer explanation and every previously reviewed digest. Flags, package
scopes and status labels were preserved; omitted false flags mean the same thing.
