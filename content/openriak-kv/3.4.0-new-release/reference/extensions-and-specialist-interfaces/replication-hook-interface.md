---
title: Replication hook interface
weight: 1260
product: OpenRiak KV
product_version: 3.4.0
diataxis: reference
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Legacy replication hooks filter or supplement objects on a `riak_repl` path. They are registered as
  replication helpers and are distinct from current-generation queue filters.
related:
- how-to/legacy-and-specialist-workflows/implement-a-legacy-replication-hook
- reference/extensions-and-specialist-interfaces/custom-code-and-hook-interfaces
- reference/replication-interfaces/legacy-riak-repl-runtime-controls
- how-to/replication-and-reconciliation/configure-replication-queues-and-filters
- foundations/storage-and-performance/storage-backend-trade-offs
---

Legacy replication hooks filter or supplement objects on a `riak_repl` path. They are registered as replication helpers and are distinct from current-generation queue filters.

## Callback contracts

`send_realtime(Object, RiakClient)` and `send(Object, RiakClient)` return `ok`, `cancel`, or a list of Riak objects. `ok` permits the original object, `cancel` suppresses it, and a list sends those additional objects before the original. The first callback is for real-time delivery and the second for legacy fullsync.

`recv(Object)` returns `ok` or `cancel` for the received object.

## Execution constraints

Callbacks run within the replication path and must be bounded. Slow external work can delay delivery, and recursive writes can cause feedback loops. Deploy compatible code on every node that can execute the hook. Intentionally filtering objects changes the expected convergence scope and must be accounted for in monitoring.

These callback signatures are extension interfaces, not standalone shell commands. Use [Implement a legacy replication hook]({{< product-version-root >}}how-to/legacy-and-specialist-workflows/implement-a-legacy-replication-hook/) for deployment and verification.
