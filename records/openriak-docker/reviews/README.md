# OpenRiak KV Docker reports

Start with the [current CVE review](cve-review-latest.md) for verified scan status
and severity counts for the latest scanned registry images, including any local
replacements awaiting a push and scan. Its [JSON summary](cve-review-latest.json)
identifies the exact image digests and push reports used.

The [12 September cleanup audit](cve-cleanup-2026-09-12.json) records assessment
changes and integrity checks for all 229 stored Scout reports and 1,158 compressed
payload references. The original scan reports, including failed and interrupted
attempts, remain available as evidence.

The [PCRE2 remediation](pcre2-security-validation-2026-09-12.md) records the EL9
backport and the binary evidence correcting the Debian 12 and EL8 assessments.

Files with dates in their names describe the evidence available at that time.
Their counts and proposed actions may have been superseded by later rebuilds.
Build-validation reports also distinguish local checks from subsequent registry
pushes; use the current review to determine which image is now published.

Maintain assessments in
[`content/openriak-kv/docker`](../../../content/openriak-kv/docker/README.md).
Generated version JSON and the Downloads page consume those Markdown files.

- [Reusable patched OS bases](reusable-os-bases-2026-09-12.md): moves custom PCRE2 builds into independent RHEL 9 and CentOS 9 bases, alongside the existing Debian base.
