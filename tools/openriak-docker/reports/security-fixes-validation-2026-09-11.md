# Security fixes validation — 2026-09-11

All six metadata-backed amd64 variants for Ubuntu Noble and Rocky 8/9 passed the production single-node and five-node OpenRiak KV test suites. Every node ran `riak admin test`. All final Dockerfiles reproduce the tested files byte for byte. Full Scout SARIF and SBOM output is retained beside each validation report.

## Generator changes

- Every explicit refresh build uses `--no-cache`, so package upgrades execute even if the pulled OS release digest is unchanged. Normal compatible passed-cache skipping is preserved. Tested layers remain available for the final OCI export.
- Ubuntu Noble requires `libc6 >= 2.39-0ubuntu8.9`, covering the six findings in [USN-8737-2](https://ubuntu.com/security/notices/USN-8737-2).
- Rocky 8 requires `gzip >= 1.9-15.el8_10`.
- Rocky 9 requires `glib2 >= 2.68.4-19.el9_8.10`, `expat >= 2.5.0-6.el9_8.3`, and `pam >= 1.5.1-28.el9_8.1`. Its updated filesystem is exported from scratch so superseded base-layer bytes are omitted.
- Minimum versions are shared release configuration, covering both OpenRiak KV versions, every OTP and every generated architecture. Debian uses dpkg comparisons; RPM uses its native Lua comparator for epoch, version and release. RPM floors run before installer removal for minimal roots. Newer vendor versions are accepted, while missing or outdated packages fail the build.

## Validation results

Counts below are raw Scout findings before our Markdown exemptions. C/H/M/L means Critical/High/Medium/Low.

| Image | Before C/H/M/L | After C/H/M/L | Targeted findings removed |
| --- | ---: | ---: | ---: |
| 3.4.0-rocky-9-otp26 | 0/0/0/3 | 0/0/0/0 | 3 |
| 3.4.0-ubuntu-noble-otp24 | 0/0/9/2 | 0/0/3/2 | 6 |
| 3.4.0-ubuntu-noble-otp26 | 0/0/9/2 | 0/0/3/2 | 6 |
| 3.4.1-rocky-8-otp26 | 0/0/0/1 | 0/0/0/0 | 1 |
| 3.4.1-rocky-9-otp26 | 0/0/0/3 | 0/0/0/0 | 3 |
| 3.4.1-ubuntu-noble-otp26 | 0/0/9/2 | 0/0/3/2 | 6 |

Noble retains two active Medium findings: CVE-2026-18374 (`fopen`) and CVE-2026-19617 (lvm2). Its third raw Medium is the existing, scoped CVE-2026-2219 dpkg false positive.

## Other OS releases

Fresh repository queries used the configured OS releases, with output saved in the evidence directory linked from the JSON report.

| OS | Result |
| --- | --- |
| Alpine 3.21 | BusyBox 1.37.0-r14 and coreutils 9.5-r2 remain the newest available packages; retain their unresolved findings. |
| RHEL 8/9 | The checked glibc, OpenSSL, systemd and libgcrypt packages already match the configured UBI repositories. Their remaining findings need vendor fixes, verified runtime assessments or maintained backports. |
| CentOS Stream 9 | The checked glibc and systemd packages already match the repositories. |
| CentOS Stream 8 | The configured vault has no newer fixes for the checked libraries. Scout references newer RHEL-compatible builds, which are not CentOS Stream 8 updates. [CentOS ended Stream 8 builds in May 2024](https://www.centos.org/centos-linux/); fixing these findings requires maintained backports or migration. |
| Amazon Linux, Debian, Fedora, Oracle Linux, SUSE | The latest review has no active Medium-or-higher findings in these images. Existing upgrades, removals and backports are retained; fresh refreshes now rerun package installation. |

No cross-distribution RPM replacement or OS-release migration was performed. Coreutils remains installed. No unresolved finding was marked fixed or excluded merely because an update exists upstream.

## Evidence and publication

Docker CVE metadata and watcher tests passed. The Downloads metadata was refreshed
for all 17 + 18 approved targets; current Scout ratings and exclusions remain unchanged.

- [Exact images, package versions, checks and local report paths](security-fixes-validation-2026-09-11.json).
- All 209 unit tests passed, including cache bypass and package-floor coverage across metadata-derived versions and architectures. Native RPM checks on Rocky 8 and 9 verify equality, older versions and epoch handling.
- The first Rocky attempts exposed an unsupported RPM query for version ranges. Their failed reports remain intact; successful retries use the corrected native comparator.
- The validation ran only on amd64. ARM must be tested during the manual production refresh.
- Production approvals, published Dockerfiles and Docker Hub tags were not replaced by these isolated validations. A normal `refresh` regeneration and test, followed by `push`, publishes the fixes and fresh Scout reports. `--do-not-test` builds approved old Dockerfiles and cannot adopt these generator changes.
- Affected Markdown assessments say **Rebuild available**, retaining their exact old package scopes and Scout ratings until the production images are replaced.
