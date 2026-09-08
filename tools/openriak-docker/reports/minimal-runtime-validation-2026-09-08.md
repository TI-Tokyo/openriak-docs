# Minimal runtime validation — 2026-09-08

All **14 affected image groups passed on linux/amd64**, using the production single-node and five-node integration suites. Each node ran `riak admin test`. ARM was not tested, as requested. Full compressed Scout SARIF and SBOM evidence is retained alongside each validation report.

The generator now adopts the validated layouts through [runtime-images.json](../runtime-images.json). Existing production cache approvals, published Dockerfiles and Docker Hub images have not been replaced. A normal documentation build performs no image work.

## Results

Counts are distinct CVE IDs per image, retaining Scout severity. Manual assessments do not reduce the raw numbers below. Sizes use the same Docker `image inspect` measurement for both images, with baseline configuration digests verified against approved OCI archives; decimal MB, not compressed transfer sizes.

| Image tag | Before C / H | After C / H | Before → after MB |
| --- | ---: | ---: | ---: |
| 3.4.0-centos-9-otp26 | 1 / 31 | 0 / 8 | 311.2 → 179.7 |
| 3.4.0-debian-12-otp24 | 3 / 10 | 1 / 8 | 138.9 → 129.1 |
| 3.4.0-debian-12-otp26 | 3 / 10 | 1 / 8 | 140.6 → 130.8 |
| 3.4.0-rhel-9-otp26 | 1 / 38 | 0 / 7 | 287.6 → 146.3 |
| 3.4.0-suse-16.0-otp26 | 1 / 4 | 0 / 0 | 183.4 → 166.2 |
| 3.4.1-centos-8-otp26 | 1 / 53 | 0 / 18 | 286.0 → 142.0 |
| 3.4.1-centos-9-otp26 | 1 / 31 | 0 / 8 | 311.4 → 179.8 |
| 3.4.1-debian-12-otp26 | 3 / 10 | 1 / 8 | 140.6 → 130.9 |
| 3.4.1-fedora-29-otp26 | 0 / 5 | 0 / 0 | 528.1 → 133.9 |
| 3.4.1-rhel-8-otp26 | 1 / 35 | 0 / 10 | 293.6 → 142.1 |
| 3.4.1-rhel-9-otp26 | 1 / 38 | 0 / 7 | 287.7 → 146.4 |
| 3.4.1-rocky-8-otp26 | 0 / 5 | 0 / 0 | 465.0 → 142.1 |
| 3.4.1-suse-15-sp4-otp26 | 4 / 26 | 0 / 0 | 190.4 → 175.5 |
| 3.4.1-suse-16.0-otp26 | 1 / 4 | 0 / 0 | 183.5 → 166.3 |

## Implemented layouts

- RHEL 8/9, CentOS 8/9, Fedora 29 and Rocky 8 install explicit runtime dependencies into an empty root, then copy that filesystem into `FROM scratch`. Python, Perl, pip, setuptools and package-manager executables are absent. The RPM database, OS identity and explicit package inventory remain available to scanners. Coreutils, certificates, timezone data and the bundled OpenRiak KV/OTP runtime remain present.
- Debian 12 removes Perl through apt, including dependent administration tools, and exports the cleaned filesystem. Runtime package databases remain present; this is not a general-purpose Debian administration image.
- SUSE 15 SP4/16.0 exports the cleaned filesystem after removing `container-suseconnect`. Its embedded Go code is absent from both the runtime and inherited layers.
- The OS release, official OpenRiak KV package, digest pinning, cookie preservation/adoption, daemon lifecycle, configuration options, labels and Compose behavior retain their existing semantics. No OpenRiak KV source build was introduced.

## Remaining reports and assessments

Image-specific assessments are in [cve-statuses.json](../cve-statuses.json). [The evidence JSON](minimal-runtime-cve-assessments-2026-09-08.json) records exact package versions, vendor advisories, source references, binary checksums and runtime inspections. Existing baseline versions were checked before applying assessments to published image tags. Entries are dated and version-specific; they are not global CVE suppressions.

- **RHEL 9:** all seven remaining High reports have verified vendor fixes or an absent affected utility. See the [original RHEL 9 review](rhel-minimal-validation-2026-09-08.md).
- **RHEL 8:** all ten remaining High reports have verified vendor fixes, an unaffected Vim version, or an absent affected component. Vendor RPM changelogs establish the Vim backport that Scout missed.
- **CentOS 9:** all eight remaining High reports have verified fixes or an absent affected utility. CentOS source patches and RPM changelogs were checked; comparing only RHEL update suffixes produces incorrect matches for several CentOS builds.
- **CentOS 8:** eight of eighteen High reports have verified fixes or absent-component explanations. Ten remain unresolved in the archived runtime packages; these require further backports or moving to a maintained image. Removing Python and package managers does not provide newer vendor updates for the remaining libraries.
- **Debian 12:** two of eight High reports concern util-linux features newer than installed 2.38.1. Upstream advisories explicitly identify the relevant affected versions: [nsenter](https://github.com/util-linux/util-linux/security/advisories/GHSA-55fx-f4gg-cfhj) and [detached mount subdirectories](https://github.com/util-linux/util-linux/security/advisories/GHSA-8f2p-47x3-43mv). The remaining Critical OpenSSL report, CVE-2026-75803, still needs a vendor fix or a separate applicability assessment; [Debian marks the installed version vulnerable](https://security-tracker.debian.org/tracker/CVE-2026-75803). Three OpenSSL High reports and two mount-related High reports also remain unresolved. CVE-2026-85091 remains under investigation: the report describes newer zlib code absent from the installed source, but the Debian tracker still flags Bookworm. No unsupported claim of a fix was added.
- **SUSE:** the old findings identify the removed registration helper in an inherited layer. Existing runtime-absence checks were verified against the exact baseline image digests; the new clean-filesystem images remove those bytes from the image layers too.

Zero findings from a scan is not a guarantee of complete vulnerability coverage or renewed vendor support for an archived release. The full findings and component inventories remain in the saved evidence.

## Evidence and reproduction

- [Machine-readable comparison, per-image reports and remaining Critical/High IDs](minimal-runtime-validation-2026-09-08.json)
- [Image-specific CVE assessment evidence](minimal-runtime-cve-assessments-2026-09-08.json)
- [Prototype commands and options](../experiments/README.md)

```sh
python3 tools/openriak-docker/experiments/minimal_matrix.py --jobs 2 --timeout 1800
```

Use the normal `refresh --force` workflow with the desired namespace/vendor options to regenerate approved production assets, rebuild and retest them, then use `push` to publish and obtain new registry scans. `--do-not-test` uses the previously approved files and therefore cannot adopt these generator changes.

## Final checks

- Production rendering reproduced all 14 tested Dockerfiles byte for byte.
- Current production runtime assertions passed against all 11 applicable retained images; SUSE helper-absence checks passed in the integration suite.
- All 179 Python unit tests and the CVE metadata Node test passed.
- Docker-only metadata refresh retained 17 entries for 3.4.0 and 18 for 3.4.1. Only CVE data changed; other metadata and published artifacts were preserved.
- Prototype containers were removed and the dedicated builder was stopped.
