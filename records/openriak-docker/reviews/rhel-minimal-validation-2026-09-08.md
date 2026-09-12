# Minimal RHEL 9 runtime validation — 2026-09-08

**Passed:** OpenRiak KV 3.4.1, OTP26, RHEL 9.8, linux/amd64. The isolated
prototype preserves the existing entrypoint, runtime options and Compose
behavior while excluding the full UBI installer filesystem from the final image.

| Measurement | Existing image | Minimal prototype |
| --- | ---: | ---: |
| Uncompressed exported layer bytes | 296,834,560 | 151,008,768 |
| Uncompressed exported layers, decimal MB | 296.8 | 151.0 |
| Scout Critical CVEs | 1 | 0 |
| Scout High CVEs | 38 | 7 |
| Scout Medium CVEs | 48 | 18 |
| Scout Low CVEs | 21 | 12 |
| Scout unspecified CVEs | 1 | 0 |
| Scout indexed artifacts | 254 | 102 |

The exported layers are **49.1% smaller**. Both size measurements include tar
headers/padding and exclude compression. Docker reports a separate image `Size`
of 146,440,226 bytes for the prototype; that is not the exported-tar measurement.
Scout artifact counts include source-package records and are not installed RPM
counts. Severity counts deduplicate CVE IDs and retain Scout's assigned severity;
its numeric CVSS score can differ from that classification.

## What changed

The pinned full UBI 9.8 base acts as an installer stage. DNF installs explicitly
selected runtime packages and their required dependencies into a new root,
with weak dependencies and documentation disabled. The verified official
OpenRiak KV RPM is installed into that root. A final `scratch` stage receives
only this filesystem, followed by the normal generated lifecycle configuration.

Python, Perl, pip, setuptools, DNF, Yum, microdnf and the RPM executable are absent.
Their files are not hidden in inherited runtime image layers. Unused libstdc++
Python GDB helpers are also removed. Shell tools, coreutils, certificates,
timezone data, user switching and the OpenRiak KV/OTP runtime remain available.
The RPM database, OS identity and an explicit runtime package inventory remain
present so vulnerability scanners can identify packages. The inventory contains
83 installed package records plus two GPG-key records.

## Validation

- Existing single-node integration suite passed: initialization/configuration,
  bind mounts, CLI/HTTP ping, `riak admin test`, healthcheck, daemon monitoring,
  runtime options and graceful shutdown.
- Existing cookie survived startup; fresh cluster followers adopted the
  coordinator cookie before starting OpenRiak KV.
- Five-node cluster suite passed: identical membership, ready ring, completed
  transfers, CLI/HTTP ping, healthcheck and `riak admin test` on every node.
- Absence of unwanted runtime commands/files checked on the single node and
  all five cluster nodes. Scout SBOM independently confirmed package absence
  and recognized the expected RHEL/OpenRiak KV packages.
- All **174 unit tests** passed. The experiment script compiles successfully.
- No test containers remain; the dedicated builder returned to its stopped state.

The initial attempt built and booted, but its strict file check rejected unused
Python debugger helpers from libstdc++. That failed run is preserved beside the
successful run. Removing those helpers was followed by a complete integration
rerun. Scanner/inventory reporting was subsequently expanded against the same
tested image without rebuilding it.

## Remaining High findings

The following are still reported as High by Scout. Its saved report lists
`not fixed` for each; this records scanner output, not an independent conclusion
about vendor advisories, exploitability or backported patches.

| CVE | Scout source package |
| --- | --- |
| CVE-2026-40356 | krb5 |
| CVE-2026-54369 | acl |
| CVE-2026-54371 | attr |
| CVE-2026-4046 | glibc |
| CVE-2026-45447 | openssl |
| CVE-2026-22184 | zlib |
| CVE-2026-0861 | glibc |

There are no newly introduced CVE IDs relative to the saved baseline scan.

### Vendor review of the seven High findings

Reviewed on 2026-09-08 against Red Hat advisories and the retained prototype.
The raw Scout findings above remain unchanged. **Six installed RPM versions
match or supersede Red Hat's fixed releases; the seventh concerns a utility
that is absent.** These conclusions apply to the tested image and package
versions, not automatically to other tags, operating systems or future builds.

| CVE | Installed runtime RPM | Assessment and primary evidence |
| --- | --- | --- |
| CVE-2026-40356 | krb5-libs 1.21.1-10.el9_8 | Fixed release matches [RHSA-2026:19357](https://access.redhat.com/errata/RHSA-2026:19357). |
| CVE-2026-54369 | libacl 2.4.0-1.el9_8 | Fixed release matches [RHSA-2026:42736](https://access.redhat.com/errata/RHSA-2026:42736). |
| CVE-2026-54371 | libattr 2.6.0-1.el9_8 | Fixed release matches [RHSA-2026:60226](https://access.redhat.com/errata/RHSA-2026:60226); affected getfattr/setfattr utilities are also absent. |
| CVE-2026-4046 | glibc 2.34-275.el9_8 | Newer than fixed 2.34-270.el9_8 in [RHSA-2026:20597](https://access.redhat.com/errata/RHSA-2026:20597). IBM1390/IBM1399 converters are also absent. |
| CVE-2026-45447 | openssl-libs 3.5.5-6.el9_8 | Newer than fixed 3.5.5-4.el9_8 in [RHSA-2026:25239](https://access.redhat.com/errata/RHSA-2026:25239). The RPM release includes the vendor backport despite the upstream 3.5.5 version. |
| CVE-2026-0861 | glibc 2.34-275.el9_8 | Supersedes fixed 2.34-231.el9_7.10 in [RHSA-2026:2786](https://access.redhat.com/errata/RHSA-2026:2786). |
| CVE-2026-22184 | zlib 1.2.11-40.el9 | Affected component absent. [Red Hat's description](https://access.redhat.com/security/cve/cve-2026-22184) confines the flaw to the untgz utility, which is not installed. Keep the runtime zlib library. |

Read-only inspection used ephemeral containers with `--network none` and a
shell entrypoint. `command -v` and file searches under `/usr` and `/opt` found
no `untgz`, `getfattr` or `setfattr`. Listing `/usr/lib64/gconv` found no
IBM1390/IBM1399 modules; `iconv` rejected both encodings as unsupported while
UTF-8 conversion succeeded. No image changes or additional builds were made.

Recommended follow-up: record these as image-specific, evidence-backed
assessments (six "Fixed by vendor package" and one "Not affected: component
not present"), retaining the original Scout output. Report the exact package
versions/advisories to Scout for matching-data correction. An assessment or
VEX statement does not patch an image; here it documents existing fixes and
component absence. Do not erase raw findings or apply global CVE suppressions.

## Evidence and reproduction

- [Experiment command and options](../experiments/README.md)
- [Successful validation, inventory, comparison and compressed Scout references](../../cache/openriak-docker-minimal-validation/20260908T003238.444366Z/validation.json)
- [Integration report](../../cache/openriak-docker-minimal-validation/20260908T003238.444366Z/3.4.1/3.4.1-rhel-9-otp26/platforms/linux-amd64/report.json)
- [Tested Dockerfile](../../cache/openriak-docker-minimal-validation/20260908T003238.444366Z/3.4.1/3.4.1-rhel-9-otp26/Dockerfile)
- [Baseline pushed-image scan](../../cache/openriak-docker-multiarch/pushes/20260907T232344.134367Z/3.4.1/3.4.1-rhel-9-otp26/cve-report.json)

The retained local image is
`openriak-minimal-validation/openriak-kv:3.4.1-rhel-9-otp26-20260908t003238.444366z`,
image ID `sha256:9f1f7d319004dcdf5b19ce9e3c52382efa63f38eecd8d7cea169a3bee8f70da5`.

At the end of this initial RHEL 9 amd64 proof of concept, RHEL 8, other OpenRiak KV
versions, other operating systems and ARM had not been validated with this method.
The production generator, approved caches and published downloads were unchanged;
no image was pushed. Adopting this method would make rebuilds the supported way
to update OS packages because the final image has no package manager. This
report does not establish Red Hat support or certification for the custom image.

The subsequent [14-image amd64 validation](minimal-runtime-validation-2026-09-08.md)
passed and the validated layouts were integrated into the production generator.
The seven assessments above are now recorded per image in
[Markdown CVE assessments](../../../content/openriak-kv/docker/README.md). Existing approved downloads and registry
images still require an explicit refresh and push to adopt the new layouts.
