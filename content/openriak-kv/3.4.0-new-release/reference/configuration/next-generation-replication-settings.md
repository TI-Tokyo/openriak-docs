---
title: Next-generation replication settings
description: Next-generation replication settings define source queues, sink consumers, and TicTac fullsync. Configure
  both ends of a path and verify the queue and dataset scope agree.
weight: 170
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\next-gen-replication\reference.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ReplicationGuide.html#additional-configuration
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/configuration/replication.md
related:
- how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication
- how-to/replication-and-reconciliation/configure-and-schedule-fullsync
- foundations/data-and-consistency/bucket-types-and-data-policies
---

Next-generation replication settings define source queues, sink consumers, and TicTac fullsync. Configure both ends of a path and verify the queue and dataset scope agree.

## Settings

Select an operating system, then search by setting name or description. Values shown are the defaults from that release’s settings metadata; explicit configuration overrides take precedence.

{{< configuration-reference-table >}}
^(replrtq_|ttaaefs_|repl_(cacert|cert|key|username|reap))
{{< /configuration-reference-table >}}
