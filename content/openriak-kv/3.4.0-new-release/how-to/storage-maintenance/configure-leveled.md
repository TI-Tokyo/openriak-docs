---
title: Configure Leveled
description: Configure Leveled on empty nodes, or tune an existing Leveled deployment using a measured workload.
  Use [[H33]] to move data from another backend.
weight: 310
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\backends\configure-leveled.md
source_material:
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/InitialDesignDecisions.html#leveled
- https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---leveled-backend
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/backends/leveled.md
related:
- reference/configuration/leveled-settings
- how-to/planning-a-deployment/choose-a-storage-backend
- how-to/storage-maintenance/schedule-leveled-compaction
- how-to/performance/benchmark-a-representative-workload
- foundations/storage-and-performance/how-leveled-stores-data
---

Configure Leveled on empty nodes, or tune an existing Leveled deployment using a measured workload. Use [Migrate to another storage backend]({{< product-version-root >}}how-to/storage-maintenance/migrate-to-another-storage-backend/) to move data from another backend.

## Prepare storage

Choose persistent data paths with enough free space for maintenance and recovery. Verify service-account ownership and filesystem behaviour. Back up the current configuration before tuning an existing node.

## Set the backend and options

Use `storage_backend` to select leveled on a new node. Review the release-specific settings here:

{{< configuration-reference-table >}}
^leveled\.
{{< /configuration-reference-table >}}

Measure compression with representative values. Already compressed values may not benefit from a second compression pass; ledger keys and metadata can still benefit separately. Observe both journal compaction and ledger backlog.

Change one related group of options at a time and document the intended effect. Avoid copying tuning values from a workload with different object sizes or mutation rates.

## Validate and measure

{{< cli-example key="shell:riak chkconfig" >}}

Restart in a controlled sequence when required. Verify sample reads and writes, then compare latency, memory, disk growth, and maintenance logs over a full maintenance cycle. Revert a tuning change if the measured result is worse.
