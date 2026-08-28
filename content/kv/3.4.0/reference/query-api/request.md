---
title: 'Query API request reference'
description: 'Define Query API request paths, JSON fields, defaults, and validation rules.'
weight: 2
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'developers'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/QueryAPI.html#api-endpoint---the-uri'
  - 'https://openriak.github.io/riak/QueryAPI.html#continuation-optional'
  - 'https://openriak.github.io/riak/QueryAPI.html#inactivity_timeout-optional'
  - 'https://openriak.github.io/riak/QueryAPI.html#max_results-optional'
  - 'https://openriak.github.io/riak/QueryAPI.html#query_list-required'
  - 'https://openriak.github.io/riak/QueryAPI.html#query---definition'
  - 'https://openriak.github.io/riak/QueryAPI.html#query-json---definition'
  - 'https://openriak.github.io/riak/QueryAPI.html#substitutions-optional'
  - 'https://openriak.github.io/riak/QueryAPI.html#timeout-optional'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define Query API request paths, JSON fields, defaults, and validation rules.

## Details

### API Endpoint - THe URI

All query requests must be sent to the query endpoint for the Bucket (and Bucket Type where typed-buckets are used).

```console
POST /types/BucketType/buckets/Bucket/query
```

For legacy (untyped) buckets:

```console
POST /buckets/Bucket/query
```

For query requests the `POST` method should be used.

If the accumulation options `queue_raw_keys` or `queue_raw_terms` are used then an opaque reference will be returned as the `result_queue` in the JSON response to the query request.  Results may be fetched from the same URI, using the `GET` method with the reference to the `result_queue` passed as a query parameter.  There is also an optional query parameter `max_results` which puts an upper limit on the number of results sent back in the batch:  For example:

```console
GET types/BucketType/buckets/Bucket/query?result_queue=g2gDdw5kZXYxQDEyNy4wLjAuMVh3DmRldjFAMTI3LjAuMC4xAAAMdwAAAABpPGQWbQAAAARkjfJI?max_results=1000
```

> The `result_queue` reference can be decoded by any node in the cluster.  The result requests for queued batches can be distributed across the cluster.

#### Query JSON - Definition

The query should be posted as the HTTP body, to the query API for the relevant bucket, where there are the following JSON keys at the root of the document

#### max_results (optional)

The potential to limit the number of results returned by the query, to the first N results.  The query will terminate once sufficient results have been returned, and a `continuation` term will be returned along with the results, which can be passed into a subsequent query to return the next set of results after this point.  This allows for pagination of results.

- The Max results option is only supported with an `accumulation_option` of `terms` or `raw_keys`.
  - Only the `terms` accumulator is able to make a reliable continuation point.
  - Internally if using `raw_keys` with `max_results`, then the query will run as a `terms` query, with the terms being stripped immediately prior to returning a response.

Note that as the query is distributed, and there is minimal difference for the performance of fetching 1 or 10K results, then pagination will not be efficient for user-facing page sizes (e.g. small batches of o(10)).

> For pagination to the end user, it is normally better to fetch larger result sets to be cached and paginated within the application.

#### continuation (optional)

A string returned from a previous query constrained by `max_results`, used to indicate the starting point for the next page of results.

#### substitutions (optional)

An array of key/value pairs that are referred to in filter or evaluation expressions.  Where a substitution key is present in an expression (prefixed by `:`), the substitution value will be used to replace those keys before the query process parses the expression.  For example, `{"low_dob" : "19550301", "high_dob" : "19560630"}` can be passed as substitutions to populate an evaluation of `"$dob" BETWEEN ":low_dob" AND ":high_dob"`.  The values of substitutions should all be strings.

#### timeout (optional)

The timeout in seconds to wait for the query to complete, before a timeout error is returned.

- This is the timeout used by the server, other HTTP timeouts may exist on the path to Riak, in particular in the Riak client.

#### inactivity_timeout (optional)

Relevant only  in `queue_raw_keys` and `queue_raw_terms` queries, where the results are queued on disk to be available for fetch requests.  If no requests are made to fetch from that specific queue within the inactivity timeout (in seconds), the process managing the queue will expire and the disk footprint of the queue will be removed.

There is no API call to close or delete the queue when all the results have been consumed.  Garbage collection is dependent on the inactivity timeout.

The location of the queues on disk is set using the `query_dataroot` option in riak.conf.  Performance of queries with queued result sets may be impacted by the read and write latency to that disk partition, but all reading and writing is batched for efficiency and so the overhead of query queues on disk utilisation should be limited.

#### query_list (required)

A list of one or more queries.  This should be a list of just one query unless an `aggregation_expression` has been included in the main query block.

Each query has the following parts:

- `aggregation_tag` (optional)
  - required if an only if an `aggregation_expression` is used
- `index_name` (required - should be a binary index)
- `start_term` (required)
- `end_term` (required)
- `evaluation_expression` (optional)
  - an expression to extract projected attributes from the term.
- `filter_expression` (optional)
  - an expression to filter results based on those projected attributes.
  - Must be included if an `evaluation_expression` is included in the query, but can simply test `attribute_exists($key)` if no filter is required.
- `regular expression` (optional)
  - alternative to using evaluation or filter expressions, which can potentially be used to improve the performance of queries.
  - must not be included if filter/evaluation expressions form part of the query.
