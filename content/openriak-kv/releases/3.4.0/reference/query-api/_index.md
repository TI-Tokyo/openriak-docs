---
title: 'Query API reference'
description: 'Define Query API endpoints, request expressions, responses, limits, and consistency behavior.'
weight: 1
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
  - 'openriak-discussions'
quickdocs_sources:
  - 'https://openriak.github.io/riak/QueryAPI.html#riak-kv---query-api'
  - 'https://openriak.github.io/riak/QueryAPI.html#secondary-indexes---querying-index-entries-overview'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define Query API endpoints, request expressions, responses, limits, and consistency behavior.

## Details

### OpenRiak KV - Query API

**Available from OpenRiak KV 3.4.0.**

Secondary indexes may be added to Riak objects, and Riak provides a Query API for those indexes.  The API supports range queries, to be run across the sorted terms on an index, but the terms may also contain projected attributes appended to the sort key.  The Query API can be passed evaluation and filter expressions: to first evaluate the term to extract the attributes, and then filter the terms by testing the attribute values against query conditions.

Through this combination of querying ranges and filtering on projected attributes, the API can support conjunction queries.  The capability and efficiency of these conjunction queries is dependent on work in the application to map the object schema to a set of index terms with a suitable combination of sort keys and attributes.  The queries are distributed across the cluster, running in parallel across different partitions of the data (the vnodes); and through that parallelism offer low-latency responses to relatively complex queries, even where significant numbers of index entries are covered by the range of the query.

The result sets for queries are not limited to returning lists of object keys, there is also support in the Query API for different accumulation options.  As well as returning object keys, accumulation options can be used to efficiently count results, and group both results and counts by specific projected attributes.

Queries are by default synchronous with the full result-set sent directly back to the requesting process on completion of the query.  Queries may be asynchronous, with results queued on-disk (to control memory use) to be consumed in batches by one or more external processes, with results available for consumption prior to the completion of the query.

As well as single queries the API can also handle combination queries.  In combination queries, multiple queries are run as part of the same request and the results of each query are combined using a set operation before results are accumulated to construct the response.  Those set operations are also distributed across the cluster for efficiency; the application of a set operation happens at the scale of the vnode, not the scale of the cluster.  All combination queries are run on a single snapshot per vnode; so the results should always be consistent from the perspective of each potential key in the result set.

For further detail on the Query API:

- [Adding Index Entries to Objects]({{< product-version-root >}}reference/data/secondary-indexes/)
- [Overview of querying those index entries]({{< product-version-root >}}how-to/develop/query-with-query-api/)
- [An example people search]({{< product-version-root >}}tutorials/query-api/build-search-index/)
- [An alternative example for people search]({{< product-version-root >}}tutorials/query-api/build-search-index/)
- [An example using the API for reporting]({{< product-version-root >}}tutorials/query-api/build-search-index/)
- [Setting performance expectations for queries]({{< product-version-root >}}explanation/performance/query-execution/)
- [A more formal description of the Query API]({{< product-version-root >}}reference/query-api/request/)
- [An overview of the expected performance of queries in Riak]({{< product-version-root >}}explanation/performance/query-execution/)
- [Some notes on the underlying implementation]({{< product-version-root >}}explanation/data-model/query-api/)

#### Secondary Indexes - Querying Index Entries Overview

The Query API is intended to provide flexible and performant functionality in the context of a Key-Value store:

> The aim of Riak development is to provide a database that performs efficient, scalable and predictable CRUD operations, and is just-queryable-enough to avoid the need of third party database integration in most use cases.

Riak does support via [an external replication API]({{< product-version-root >}}reference/replication-api/), the ability to manage replication and reconciliation to third party query engines (e.g. OpenSearch), should more complex query support be required.  The automation of such integration is outside of the current functional scope of Riak.

## In this section

- [Query API accumulation options]({{< product-version-root >}}reference/query-api/accumulation-options/) — Define the 3.4.0 Query API modes for returning keys, terms, counts, and counts by attribute.
- [Query API expression reference]({{< product-version-root >}}reference/query-api/expressions/) — Define supported Query API expressions, operators, composition rules, and Unicode behavior.
- [Query API limits and performance]({{< product-version-root >}}reference/query-api/limits/) — Record Query API scanning, filtering, buffering, aggregation, collation, and transformation limits.
- [Query API request reference]({{< product-version-root >}}reference/query-api/request/) — Define Query API request paths, JSON fields, defaults, and validation rules.
- [Query API response reference]({{< product-version-root >}}reference/query-api/responses/) — Define Query API response fields, ordering, pagination, and error representations.
