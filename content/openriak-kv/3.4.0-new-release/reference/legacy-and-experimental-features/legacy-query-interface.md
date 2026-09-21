---
title: Legacy query interface
description: The legacy secondary-index interface selects an exact term or inclusive range and returns matching
  keys. It is distinct from the current Query API's projected-attribute and set-expression requests.
weight: 1360
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/OtherAPI.html#legacy-query-api
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/specialized-apis/legacy-query-api.md
related:
- reference/http-api/secondary-index-queries
- reference/protocol-buffers-api/secondary-index-query-messages
- reference/query-api/endpoints-and-request-schema
- how-to/indexes-and-queries/add-and-query-secondary-indexes
- reference/orientation-and-compatibility/backend-capability-matrix
- foundations/replication-and-repair/replication-generations-and-compatibility
- foundations/storage-and-performance/storage-backend-trade-offs
---

The legacy secondary-index interface selects an exact term or inclusive range and returns matching keys. It is distinct from the current Query API's projected-attribute and set-expression requests.

## HTTP and PB contracts

Use [Secondary-index queries]({{< product-version-root >}}reference/http-api/secondary-index-queries/) for the index URL, pagination, and response forms. Use [Secondary-index query messages]({{< product-version-root >}}reference/protocol-buffers-api/secondary-index-query-messages/) for PB message fields. Both require an index-capable backend and correctly stored index metadata.

## Limits

An index result does not fetch each object's current value or create a transaction across the returned keys. Continuations are opaque and tied to the same logical query. For projection, expression filtering, combination, and accumulation, use [Endpoints and request schema]({{< product-version-root >}}reference/query-api/endpoints-and-request-schema/) and its version-specific constraints.
