---
title: 'Learn the Query API'
description: 'Introduce a guided learning path for indexing, querying, and interpreting a small search dataset.'
weight: 1
diataxis: 'tutorial'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/QueryAPI.html#riak-kv---query-api'
tags: ['diataxis', 'kv', 'tutorial']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce a guided learning path for indexing, querying, and interpreting a small search dataset.

## Overview

### OpenRiak KV - Query API

**Available from OpenRiak KV 3.4.0.**

Secondary indexes may be added to Riak objects, and Riak provides a Query API for those indexes.  The API supports range queries, to be run across the sorted terms on an index, but the terms may also contain projected attributes appended to the sort key.  The Query API can be passed evaluation and filter expressions: to first evaluate the term to extract the attributes, and then filter the terms by testing the attribute values against query conditions.

Through this combination of querying ranges and filtering on projected attributes, the API can support conjunction queries.  The capability and efficiency of these conjunction queries is dependent on work in the application to map the object schema to a set of index terms with a suitable combination of sort keys and attributes.  The queries are distributed across the cluster, running in parallel across different partitions of the data (the vnodes); and through that parallelism offer low-latency responses to relatively complex queries, even where significant numbers of index entries are covered by the range of the query.

The result sets for queries are not limited to returning lists of object keys, there is also support in the Query API for different accumulation options.  As well as returning object keys, accumulation options can be used to efficiently count results, and group both results and counts by specific projected attributes.

Queries are by default synchronous with the full result-set sent directly back to the requesting process on completion of the query.  Queries may be asynchronous, with results queued on-disk (to control memory use) to be consumed in batches by one or more external processes, with results available for consumption prior to the completion of the query.

As well as single queries the API can also handle combination queries.  In combination queries, multiple queries are run as part of the same request and the results of each query are combined using a set operation before results are accumulated to construct the response.  Those set operations are also distributed across the cluster for efficiency; the application of a set operation happens at the scale of the vnode, not the scale of the cluster.  All combination queries are run on a single snapshot per vnode; so the results should always be consistent from the perspective of each potential key in the result set.

For further detail on the Query API:

- [Adding Index Entries to Objects]({{< baseurl >}}kv/3.4.1/reference/data/secondary-indexes/)
- [Overview of querying those index entries]({{< baseurl >}}kv/3.4.1/how-to/develop/query-with-query-api/)
- [An example people search]({{< baseurl >}}kv/3.4.1/tutorials/query-api/build-search-index/)
- [An alternative example for people search]({{< baseurl >}}kv/3.4.1/tutorials/query-api/build-search-index/)
- [An example using the API for reporting]({{< baseurl >}}kv/3.4.1/tutorials/query-api/build-search-index/)
- [Setting performance expectations for queries]({{< baseurl >}}kv/3.4.1/explanation/performance/query-execution/)
- [A more formal description of the Query API]({{< baseurl >}}kv/3.4.1/reference/query-api/request/)
- [An overview of the expected performance of queries in Riak]({{< baseurl >}}kv/3.4.1/explanation/performance/query-execution/)
- [Some notes on the underlying implementation]({{< baseurl >}}kv/3.4.1/explanation/data-model/query-api/)

## What you will learn

By completing this tutorial, you will build the workflow described above and learn how to validate each stage before moving on.

## Before you begin

Use a disposable OpenRiak KV environment that matches this documentation version, and keep cluster status and logs available while you work.

## Verify the result

Repeat the completed workflow, inspect the stored or operational result, and confirm that the cluster remains healthy.

## Next steps

- [Build a search index with the Query API]({{< baseurl >}}kv/3.4.1/tutorials/query-api/build-search-index/)

## In this section

- [Build a search index with the Query API]({{< baseurl >}}kv/3.4.1/tutorials/query-api/build-search-index/) — Guide a developer through designing, loading, querying, and evaluating a small Query API search index.
