---
title: Secondary-index terms and projected attributes
description: Secondary-index entries associate terms with an object key. A projected attribute is extracted from
  an index term during Query API evaluation; it is not automatically read from the stored object body.
weight: 390
diataxis: reference
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- developers
- operators
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\reference\secondary-indexes.md
source_material:
- legacy-3.2.5
- live-3.2.5
- proposed-kv
- openriak-quickdocs-3.4
quickdocs_sources:
- https://openriak.github.io/riak/ObjectAPI.html#index-entries
- https://openriak.github.io/riak/QueryAPI.html#secondary-indexes---adding-index-entries-to-an-object
tags:
- diataxis
- kv
- reference
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- reference/data/secondary-indexes.md
related:
- how-to/indexes-and-queries/add-and-query-secondary-indexes
- how-to/indexes-and-queries/filter-queries-using-projected-attributes
- reference/http-api/secondary-index-queries
- reference/query-api/endpoints-and-request-schema
- reference/query-api/expression-grammar-and-operators
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
---

Secondary-index entries associate terms with an object key. A projected attribute is extracted from an index term during Query API evaluation; it is not automatically read from the stored object body.

## Index names and terms

Binary index names end in `_bin`; integer index names end in `_int`. HTTP uses `X-Riak-Index-NAME` headers, while PB stores index pairs in object content metadata. An object may have multiple index entries. Supported backends and query features are listed in [Backend capability matrix]({{< product-version-root >}}reference/orientation-and-compatibility/backend-capability-matrix/).

## Ordering and ranges

Binary terms use their stored ordering; integer terms require integer encoding. Range bounds are inclusive. For composite binary terms, delimiter choice and boundary construction affect which terms fall within a range. Do not assume locale-aware text ordering.

## Projected attributes

The Query API begins evaluation with `$term` and `$key`. Its evaluation pipeline can split, convert, and classify the term into additional attributes, then its filter tests them. Define an unambiguous term encoding and test missing fields, delimiter collisions, and conversion failures.

## Updates and visibility

Send the intended index metadata with an object update and preserve causal context. Changing a value's JSON fields alone does not maintain corresponding index entries. Index/query results are not a multi-object transactional snapshot.
