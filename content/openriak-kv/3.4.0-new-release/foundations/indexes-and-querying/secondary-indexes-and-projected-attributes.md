---
title: Secondary indexes and projected attributes
description: Secondary indexes associate ordered terms with object keys. A query searches those terms to discover
  keys; it need not read and decode every object's value first.
weight: 170
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: Reviewed
draft: true
audience:
- architects
- developers
source_material:
- live-3.2.5
- proposed-kv
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: complete
last_reviewed: '2026-09-24'
review-by: TI Tokyo/JOM
review_scope: editorial & technical
restructured_from:
- foundations/data-model/secondary-indexes.md
related:
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-consistency-and-snapshots
- foundations/indexes-and-querying/query-cost-and-result-delivery
- reference/data-model-contracts/secondary-index-terms-and-projected-attributes
- how-to/indexes-and-queries/add-and-query-secondary-indexes
- tutorials/indexes-and-querying/build-and-query-a-people-search-index
---

Secondary indexes associate ordered terms with object keys. A query searches those terms to discover keys; it need not read and decode every object's value first.

## Index design follows the question

Choose an index term whose ordering makes the desired range small. For example, a people directory may sort an index by a location or name prefix. The application is responsible for writing index metadata consistently with the object content.

## Projected attributes

An index term can include attributes needed for filtering or reporting. The Query API evaluates the term to extract those attributes, then applies a filter expression. This can avoid fetching full objects just to reject them, at the cost of larger terms and additional index work on writes.

An attribute projected into an index is not automatically kept current by a relational schema. Updating the underlying value must include the corresponding index changes.

## Backend and consistency boundaries

Index capability depends on the selected backend. Distributed queries examine partition-local state; an index result is not a cluster-wide transactional snapshot. Fetching a returned key later can observe another version or a deletion.

You should use direct key lookup when the key is already known. For discovery, verify the index against known records and measure the size of the range scanned, not only the number of returned matches.
