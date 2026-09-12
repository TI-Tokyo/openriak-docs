# Medium CVE fixes — 2026-09-10

All 11 metadata-backed amd64 image groups for the five affected OS releases
passed the production single-node and five-node OpenRiak KV integration suites.
Every node ran `riak admin test`; CLI/HTTP pings, Docker health, configuration,
bind mounts, cookie handling, cluster membership and graceful shutdown passed.
ARM was not tested. Production cache approvals, published Dockerfiles and Docker
Hub tags were not replaced by these isolated validations.

## Changes

- Ubuntu Jammy requires `libc6 >= 2.35-0ubuntu3.15`, covering the five reviewed
  glibc findings in [USN-8737-1](https://ubuntu.com/security/notices/USN-8737-1).
  The build and runtime assertions reject an older library. Later vendor updates
  remain acceptable.
- Ubuntu Jammy and Noble remove Perl and tar after installation, then export the
  cleaned filesystem into `FROM scratch`. Removed bytes are not retained in
  inherited layers. Jammy removes only Perl with dpkg's explicit dependency and
  essential-package overrides, retaining PAM/login; Noble uses apt to remove
  Perl and dependent administration tools. Package maintenance requires a
  rebuild or restoring the removed installation helpers first.
- CentOS 8 and RHEL 8 omit sudo and Vim. The official package launcher delegates
  to `runuser -u riak --` instead of sudo; its argument handling and remaining
  launcher logic are preserved. Root-run CLI commands, healthchecks, all admin
  tests and graceful stops passed. RPM cleanup retains dependency checks.
- Oracle Linux 9 uses a clean runtime installation root without libssh or
  package-manager tooling. Its slim base supplies microdnf; full dnf is installed
  in the discarded installer stage only. The RPM database and package inventory
  remain available to Scout.
- Noble's existing `dpkg 1.22.6ubuntu6.6` is already fixed for CVE-2026-2219,
  according to [Ubuntu's advisory](https://ubuntu.com/security/CVE-2026-2219).
  The three version-specific Markdown assessments now mark that exact package
  version as a false positive. Other package versions are not exempted.
- The CLI readiness wait now fails immediately when its container exits,
  instead of continuing to retry for the full timeout.

The validated release settings are in [runtime-images.json](../runtime-images.json).
They apply to every generated KV version, OTP and architecture for those OS
releases. The final production renderer reproduced every tested Dockerfile
byte for byte. All 200 Python unit tests and the CVE metadata/watcher tests passed.

## Scout results

Counts are distinct raw Scout CVE IDs per amd64 image, before applying our Markdown
assessments. The baseline is the verified 2026-09-09 push review; new scans are from
2026-09-10. Counts therefore retain vendor/backport false positives, including
Noble's dpkg finding. The package inventories independently confirm the selected
packages are absent and record the installed security-library versions.
Sizes are Docker `image inspect` bytes expressed in decimal MB.

| Image tag | Before C / H / M | After C / H / M | New size MB |
| --- | ---: | ---: | ---: |
| 3.4.0-oracle-linux-9-otp24 | 0 / 0 / 7 | 0 / 0 / 0 | 176.4 |
| 3.4.0-oracle-linux-9-otp26 | 0 / 0 / 7 | 0 / 0 / 0 | 178.1 |
| 3.4.0-ubuntu-jammy-otp24 | 0 / 0 / 10 | 0 / 0 / 1 | 128.2 |
| 3.4.0-ubuntu-jammy-otp26 | 0 / 0 / 10 | 0 / 0 / 1 | 129.9 |
| 3.4.0-ubuntu-noble-otp24 | 0 / 0 / 7 | 0 / 0 / 3 | 144.3 |
| 3.4.0-ubuntu-noble-otp26 | 0 / 0 / 7 | 0 / 0 / 3 | 146.0 |
| 3.4.1-centos-8-otp26 | 0 / 18 / 44 | 0 / 12 / 33 | 137.7 |
| 3.4.1-oracle-linux-9-otp26 | 0 / 0 / 0 | 0 / 0 / 0 | 178.2 |
| 3.4.1-rhel-8-otp26 | 0 / 10 / 16 | 0 / 5 / 15 | 137.8 |
| 3.4.1-ubuntu-jammy-otp26 | 0 / 0 / 10 | 0 / 0 / 1 | 130.0 |
| 3.4.1-ubuntu-noble-otp26 | 0 / 0 / 7 | 0 / 0 / 3 | 146.0 |

The remaining Jammy Medium is CVE-2026-18374. Noble also retains CVE-2026-19617,
plus the already-fixed dpkg finding described above. CentOS 8 and RHEL 8 retain
library findings requiring their existing vendor/version assessments or further
work; removing optional tools does not fix every library vulnerability.

## Evidence and publication

[The comparison JSON](medium-fixes-validation-2026-09-10.json) records exact
baseline digests, prototype image IDs, Dockerfile hashes, package versions,
removed/new/remaining findings, all per-image evidence paths and the reproduction
command. Each validation retains complete compressed Scout SARIF and SBOM payloads
with integrity hashes, together with integration reports and local command logs.
Earlier failed/interrupted canaries remain available for diagnosis.

Markdown CVE explanations for affected published images say **Rebuild available**
where appropriate. They continue to count those old vulnerable package versions;
passing a prototype does not change an already-pushed image. Existing verified
exemptions remain scoped to their original package/image evidence.

Use the normal `refresh` workflow with the intended namespace and vendor options
to regenerate and test changed inputs, then `push` to publish and obtain fresh
registry scans. `--retry-failed` accepts stale cache inputs; `--force` explicitly
regenerates even a passed cache. `--do-not-test` uses old approved Dockerfiles and
does not adopt these generator changes. Ordinary documentation builds perform no
Docker work.
