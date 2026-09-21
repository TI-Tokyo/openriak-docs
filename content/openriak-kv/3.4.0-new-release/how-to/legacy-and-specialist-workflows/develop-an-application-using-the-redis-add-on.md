---
title: Develop an application using the Redis add-on
description: Design application behaviour around the verified Redis add-on contract, including stale values and
  failures. Complete the compatibility and read-through checks before making the add-on a production dependency.
weight: 1480
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
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\add-ons\redis\developing-rra.md
tags:
- diataxis
- kv
- how-to
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- how-to/redis-add-on/develop.md
related:
- how-to/legacy-and-specialist-workflows/set-up-a-compatible-redis-add-on-deployment
- how-to/legacy-and-specialist-workflows/use-and-monitor-the-redis-add-on
- how-to/application-data/update-an-object-with-causal-context
- how-to/application-data/resolve-concurrent-object-updates
- reference/extensions-and-specialist-interfaces/redis-add-on-commands-and-configuration
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

Design application behaviour around the verified Redis add-on contract, including stale values and failures. Complete the compatibility and read-through checks before making the add-on a production dependency.

## Define the mapping

Document how application keys map to OpenRiak type, bucket, and key identifiers. Verify binary values, media types, and the largest expected payload. Do not assume Redis command names imply support for every Redis operation or atomicity guarantee.

## Preserve write semantics

Use the add-on's documented context and sibling handling, or keep writes on the direct OpenRiak API and treat the cache as a separate read path. Test concurrent updates and uncertain retries. Define how stale cached values are invalidated after writes and deletions.

## Test degraded operation

Exercise cache eviction, timeout, upstream failure, and reconnects. Confirm that the application distinguishes a missing key from an unavailable service. Bound retry and fallback load so a cache outage cannot overwhelm the database.

Keep direct API tests in the acceptance suite and record the exact supported add-on command subset with [Redis add-on commands and configuration]({{< product-version-root >}}reference/extensions-and-specialist-interfaces/redis-add-on-commands-and-configuration/).
