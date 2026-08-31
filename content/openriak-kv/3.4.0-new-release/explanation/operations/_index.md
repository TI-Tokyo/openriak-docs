---
title: 'Operational concepts'
description: 'Introduce the system behaviors operators need to understand before changing or recovering a cluster.'
weight: 1
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
  - 'architects'
source_material:
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
quickdocs_sources:
  - 'https://openriak.github.io/riak/RiakTheoryGuide.html#background-processes'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce the system behaviors operators need to understand before changing or recovering a cluster.

## Overview

### Background processes

Riak has three main categories of background processes:

- The primary background process in Riak, when configured, is [Tictacaae active anti-entropy]({{< product-version-root >}}explanation/replication/active-anti-entropy/), the continuous reconciliation process used to ensure all vnodes are eventually consistent.
  - This exists for both intra-cluster reconciliation and inter-cluster reconciliation if required.
- [Queue based]({{< product-version-root >}}explanation/replication/queues/) background processes, through which non-urgent activity can be deferred, to manage the impact of this activity on the performance of externally prompted requests.
- Maintenance of the distributed knowledge of the cluster state is managed by [background processes within the riak_core application]({{< product-version-root >}}explanation/operations/ring-changes-and-handoffs/).

## In this section

- [Backups and restores]({{< product-version-root >}}explanation/operations/backups-and-restores/) — Explain backups and restores, including relevant state transitions, risks, and recovery assumptions.
- [Garbage collection and compaction]({{< product-version-root >}}explanation/operations/garbage-collection/) — Explain how reaping, erasure, backend compaction, and backup-file cleanup reclaim storage.
- [Node failure and recovery]({{< product-version-root >}}explanation/operations/node-failure-and-recovery/) — Explain node failure and recovery, including relevant state transitions, risks, and recovery assumptions.
- [Object deletion and tombstones]({{< product-version-root >}}explanation/operations/object-deletion-and-tombstones/) — Explain object deletion and tombstones, including relevant state transitions, risks, and recovery assumptions.
- [Store, vnode, range, and object repair]({{< product-version-root >}}explanation/operations/repair-granularity/) — Explain the available repair scopes and how to choose the least disruptive effective option.
- [Ring changes and handoffs]({{< product-version-root >}}explanation/operations/ring-changes-and-handoffs/) — Explain ring changes and handoffs, including relevant state transitions, risks, and recovery assumptions.
- [Rolling maintenance]({{< product-version-root >}}explanation/operations/rolling-maintenance/) — Explain rolling maintenance, including relevant state transitions, risks, and recovery assumptions.
- [Upgrade and downgrade behavior]({{< product-version-root >}}explanation/operations/upgrade-and-downgrade/) — Explain upgrade and downgrade behavior, including relevant state transitions, risks, and recovery assumptions.
