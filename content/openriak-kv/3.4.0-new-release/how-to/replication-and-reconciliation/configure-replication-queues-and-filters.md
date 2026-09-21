---
title: Configure replication queues and filters
description: Define source queues and filters so each destination receives the intended objects. Each independent
  destination needs its own queue on every source node.
weight: 620
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\replication\queue.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\next-gen-replication\queuing.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/configure/replication/configure-replication-queues.md
related:
- how-to/replication-and-reconciliation/enable-real-time-replication
- how-to/replication-and-reconciliation/configure-sink-nodes-and-consumers
- how-to/replication-and-reconciliation/re-replicate-a-key-range-or-time-window
- reference/configuration/next-generation-replication-settings
- reference/replication-interfaces/replication-references-and-queue-payloads
- foundations/replication-and-repair/read-repair-and-tictac-anti-entropy
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
previous_page: how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication
next_page: how-to/replication-and-reconciliation/configure-sink-nodes-and-consumers
---

Define source queues and filters so each destination receives the intended objects. Each independent destination needs its own queue on every source node.

## Choose names and scope

Use stable queue names describing their consumers. Select `any` for all eligible real-time changes, or the release's bucket-type, bucket-name, or bucket-prefix filter for a subset. Name and prefix filters do not distinguish types by themselves; use a type filter when that distinction matters.

{{< configuration-reference-item config-name="replrtq_srcqueue" >}}

For example:

{{< settings-example >}}
replrtq_srcqueue = cluster_b:any|audit:buckettype.audit
{{< /settings-example >}}

Use the schema's blocking filter only for queues that should carry explicit seeding or reconciliation work without ordinary real-time events. Check the exact spelling in the metadata rather than borrowing one from an older guide.

## Apply and check capacity

Apply the queue definitions consistently to every source node. Review memory and overflow limits in [Next-generation replication settings]({{< product-version-root >}}reference/configuration/next-generation-replication-settings/), and monitor discard counters; persisted overflow is still a temporary queue, not a durable change log.

## Verify inclusion and exclusion

Write samples inside and outside each filter. Confirm intended consumers receive only their selected objects. Queue changes do not retroactively seed old objects, and dropping a queue discards pending work; plan reconciliation after changes.
