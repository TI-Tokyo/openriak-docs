---
title: Accumulation modes
description: The accumulation option determines the response shape and whether repeated keys or terms are combined.
  It must be valid for the selected single or combination query.
weight: 790
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
source_material:
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/QueryAPI.html#accumulation_option-optional---default--keys
- https://openriak.github.io/riak/QueryAPI.html#accumulation_term-optional---default--term
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/query-api/accumulation-options.md
related:
- reference/query-api/endpoints-and-request-schema
- reference/query-api/responses-and-errors
- how-to/indexes-and-queries/combine-queries-and-accumulate-results
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-consistency-and-snapshots
---

The accumulation option determines the response shape and whether repeated keys or terms are combined. It must be valid for the selected single or combination query.

## Modes

{{< configuration-reference-table reference="query-modes" >}}{{< /configuration-reference-table >}}

For term-based results, `accumulation_term` selects the evaluated term or projected attribute to accumulate. Use explicit options in application requests when their semantics are part of the application contract.

Raw and distinct modes can give different counts when several index terms match the same key. A count of matches must not be presented as a count of distinct objects without checking that relationship.
