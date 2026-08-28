---
title: 'Query API design'
description: 'Explain the Query API execution pipeline, expressiveness, consistency, and performance trade-offs.'
weight: 11
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'developers'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
  - 'openriak-discussions'
quickdocs_sources:
  - 'https://openriak.github.io/riak/QueryAPI.html#further-improvements'
  - 'https://openriak.github.io/riak/QueryAPI.html#notes-on-implementation'
  - 'https://openriak.github.io/riak/QueryAPI.html#querying---functional-summary'
  - 'https://openriak.github.io/riak/QueryAPI.html#riak-kv---query-api'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain the Query API execution pipeline, expressiveness, consistency, and performance trade-offs.

## Overview

### OpenRiak KV - Query API

**Available from OpenRiak KV 3.4.0.**

Secondary indexes may be added to Riak objects, and Riak provides a Query API for those indexes.  The API supports range queries, to be run across the sorted terms on an index, but the terms may also contain projected attributes appended to the sort key.  The Query API can be passed evaluation and filter expressions: to first evaluate the term to extract the attributes, and then filter the terms by testing the attribute values against query conditions.

Through this combination of querying ranges and filtering on projected attributes, the API can support conjunction queries.  The capability and efficiency of these conjunction queries is dependent on work in the application to map the object schema to a set of index terms with a suitable combination of sort keys and attributes.  The queries are distributed across the cluster, running in parallel across different partitions of the data (the vnodes); and through that parallelism offer low-latency responses to relatively complex queries, even where significant numbers of index entries are covered by the range of the query.

The result sets for queries are not limited to returning lists of object keys, there is also support in the Query API for different accumulation options.  As well as returning object keys, accumulation options can be used to efficiently count results, and group both results and counts by specific projected attributes.

Queries are by default synchronous with the full result-set sent directly back to the requesting process on completion of the query.  Queries may be asynchronous, with results queued on-disk (to control memory use) to be consumed in batches by one or more external processes, with results available for consumption prior to the completion of the query.

As well as single queries the API can also handle combination queries.  In combination queries, multiple queries are run as part of the same request and the results of each query are combined using a set operation before results are accumulated to construct the response.  Those set operations are also distributed across the cluster for efficiency; the application of a set operation happens at the scale of the vnode, not the scale of the cluster.  All combination queries are run on a single snapshot per vnode; so the results should always be consistent from the perspective of each potential key in the result set.

For further detail on the Query API:

- [Adding Index Entries to Objects](/kv/3.4.1/reference/data/secondary-indexes/)
- [Overview of querying those index entries](/kv/3.4.1/how-to/develop/query-with-query-api/)
- [An example people search](/kv/3.4.1/tutorials/query-api/build-search-index/)
- [An alternative example for people search](/kv/3.4.1/tutorials/query-api/build-search-index/)
- [An example using the API for reporting](/kv/3.4.1/tutorials/query-api/build-search-index/)
- [Setting performance expectations for queries](/kv/3.4.1/explanation/performance/query-execution/)
- [A more formal description of the Query API](/kv/3.4.1/reference/query-api/request/)
- [An overview of the expected performance of queries in Riak](/kv/3.4.1/explanation/performance/query-execution/)
- [Some notes on the underlying implementation](/kv/3.4.1/explanation/data-model/query-api/)

#### Querying - Functional Summary

A query consists of the [following components](/kv/3.4.1/reference/query-api/request/):

- An index field (required).
- A query range (required).
- An `evaluation_expression` (optional); used to decode projected attributes to provide a map of those attributes to be processed via a filter expression.
- A `filter_expression` (optional); used to filter results in/out of queries by applying checks to a map of projected attributes discovered on the index entry (i.e. the map being the output of an evaluation expression).
- A `regular_expression` (optional); a potentially less flexible, but sometimes more performant alternative to evaluation and filter expressions - where a regular expression is used to match against a whole term, including the unevaluated projected attributes, in order to filter the entry into the query results.
  - The regular expression is primarily provided for backwards compatibility with the [legacy index-query feature used prior to Riak 3.4](/kv/3.4.1/reference/specialized-apis/legacy-query-api/).  The use of evaluation and filter expressions is preferred to the use of regular expressions, and are often at least as performant as regular expressions.
  - Regular expressions are [PCRE-style regular expressions](https://www.pcre.org/), but are not compiled prior to being used.
  - Escaping regular expressions correctly, so that they can be passed via the JSON-based Query API, may add significant complexity to the development process.

Queries can be sent individually, but it is also possible to send multiple queries along with an aggregation expression to define how the query results will be combined (e.g. using `INTERSECT`, `UNION`, `NOT`) - where Riak will provide a single set of results as a response based on the aggregation expression.

Queries, both single and aggregated, also support an optional accumulation method; a mechanism for describing the type of results required, and how those results should be sorted (e.g. returning just object keys, keys by term, keys by specific projected attribute, counts, counts by attribute value etc).

The JSON query object can contain `substitutions`, a JSON array mapping keys with any string-based tag to values.  Substitutions are useful when a single query template is to be used within the application client (i.e. to substitute into a standard query the user input), or to avoid difficulty with escaping special characters embedded within query elements.  Within the API, a prefix of `:` to a reference indicates that the reference should be replaced using an entry in the `substitutions` map.

In the filter and evaluation expressions, projected attribute keys are identified through use of a `$` prefix.  All evaluations start with two default attributes: the whole term (`$term`) and the object key (`$key`).

The API also supports options to govern pagination of results, and timeout of queries.

Query requests are made by posting [a JSON object which defines the query](/kv/3.4.1/reference/query-api/request/) to a HTTP URI on Riak of `types/<BucketType>/buckets/<Bucket>/query`.  The results are returned as a JSON object, the format of those results is determined by the `accumulation_option` requested.

#### Further Improvements

Improving the functionality of the Query API is an active goal of the OpenRiak community.  Notifications on planned improvements will be added to the [OpenRiak discussions board](https://github.com/orgs/OpenRiak/discussions).
