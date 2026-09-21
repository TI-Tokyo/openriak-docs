---
title: Use and monitor the Redis add-on
description: Verify read-through and failure behaviour in an isolated Redis add-on deployment whose exact versions
  have been recorded with [[H145]].
weight: 1470
diataxis: how-to
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- legacy-3.2.5
- live-3.2.5
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\add-ons\redis\using-rra.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/redis-add-on/use.md
related:
- how-to/legacy-and-specialist-workflows/set-up-a-compatible-redis-add-on-deployment
- how-to/legacy-and-specialist-workflows/develop-an-application-using-the-redis-add-on
- reference/extensions-and-specialist-interfaces/redis-add-on-commands-and-configuration
- how-to/monitoring-and-diagnostics/perform-routine-cluster-health-checks
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Verify read-through and failure behaviour in an isolated Redis add-on deployment whose exact versions have been recorded with [Set up a compatible Redis add-on deployment]({{< product-version-root >}}how-to/legacy-and-specialist-workflows/set-up-a-compatible-redis-add-on-deployment/).

## Check the source of truth

Write a unique known object directly to OpenRiak, read it directly, then request it through the add-on's documented key mapping. Compare the bytes and content interpretation. Repeat after warming the cache.

## Exercise changes and failures

Update the value with causal context, delete it, and allow cache entries to expire. Observe when each change becomes visible through the add-on. Stop Redis, then the add-on, then one OpenRiak test member in separate runs; verify whether requests fail, fall back, or return stale data according to the candidate's contract.

## Monitor the full path

Measure cache hits and misses, evictions, memory, upstream errors, and request latency at both layers. Compare cached results with direct reads of known keys. A healthy Redis process alone does not establish that the backing data path works.

Retain the compatibility record and reset the disposable data when finished. Do not generalize the result to untested add-on or Redis versions.
