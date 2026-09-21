---
title: Release notes
linkTitle: Release Notes
description: Changes and compatibility notes for OpenRiak KV 3.4.1.
weight: -20
diataxis: reference
product: OpenRiak KV
product_version: 3.4.1
status: editorially-rewritten
draft: true
audience:
- all-readers
source_material:
- source-code-release-notes-3.4
- openriak-discussions
- live-3.2.5
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\about\release-notes.md
migration_review:
- Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.
- Earlier release notes are retained as historical source material and must not be read as the OpenRiak KV 3.4 release
  contract.
- Legacy version text or MDX syntax remains and requires editorial review.
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-08-28'
review_scope: editorial-and-site-integration
related:
- how-to/cluster-lifecycle/upgrade-a-cluster
- reference/orientation-and-compatibility/feature-status-and-deprecations
---

OpenRiak KV 3.4.1 adds queued Query API result delivery, vnode/backend status inspection, and improvements to reconciliation and operational visibility.

## Additions and changes

- [Continuations and result delivery]({{< product-version-root >}}reference/query-api/continuations-and-result-delivery/) adds disk-backed result queues using `queue_raw_keys` and `queue_raw_terms`.
- [Inspect vnode and backend status]({{< product-version-root >}}how-to/monitoring-and-diagnostics/inspect-vnode-and-backend-status/) exposes vnode and backend observations through the new command.
- [Remove obsolete Leveled backup files]({{< product-version-root >}}how-to/storage-maintenance/remove-obsolete-leveled-backup-files/) includes startup detection of unused Leveled journal files as well as ledger files.
- [Node and cluster metrics]({{< product-version-root >}}reference/operations-and-observability/node-and-cluster-metrics/) includes additional VM usage and limit statistics.
- [Reconcile selected buckets]({{< product-version-root >}}how-to/replication-and-reconciliation/reconcile-selected-buckets/) includes the bucket resynchronisation helper and improved handling of large reconciliation differences.

The release supports OTP 24 and OTP 26. Choose packages from the versioned download catalogue and rehearse the upgrade procedure before changing an existing cluster.

Source: [OpenRiak release notes](https://github.com/OpenRiak/riak/blob/77bbdbe5cd86428d98f9953c1fecb579a4d96b14/RELEASE-NOTES.md).
