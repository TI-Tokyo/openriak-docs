---
title: Legacy riak_repl runtime controls
weight: 1000
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Legacy v2/v3 replication uses the `riak_repl` command family. Its listeners, site connections, real-time
  streams, and fullsync controls are distinct from next-generation replication queues and consumers.
related:
- reference/orientation-and-compatibility/replication-generation-compatibility
- how-to/legacy-and-specialist-workflows/maintain-legacy-v2-replication
- how-to/legacy-and-specialist-workflows/maintain-legacy-v3-replication
- how-to/legacy-and-specialist-workflows/configure-legacy-replication-through-nat
- how-to/legacy-and-specialist-workflows/secure-legacy-replication-connections
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
---

Legacy v2/v3 replication uses the `riak_repl` command family. Its listeners, site connections, real-time streams, and fullsync controls are distinct from next-generation replication queues and consumers.

## Commands

{{< cli-command-index prefix="riak/repl" >}}

Use each command's metadata for availability, syntax, and help. Match the operation to the configured legacy generation before interpreting its status fields or changing it. Commands for Riak CS proxying or block providers are specialist interfaces, not general KV replication setup steps.
