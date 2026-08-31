---
title: 'Query API response reference'
description: 'Define Query API response fields, ordering, pagination, and error representations.'
weight: 4
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
  - 'https://openriak.github.io/riak/QueryAPI.html#query-responses'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define Query API response fields, ordering, pagination, and error representations.

## Details

### Query Responses

The responses to all query requests, including fetches from query result queues, are JSON objects.  For synchronous queries (i.e. requests with an `accumulation_option` other than `queue_raw_keys` or `queue_raw_terms`), the results will be sent under a single JSON key within the JSON object - with that key set to be the `accumulation_option` for the request e.g.

```json
{
    "keys" : [ "990011234", "990011235" ]
}
```

If the `accumulation_option` is `terms` or `raw_keys`, and a `max_results` constraint has been added to the query, then a `continuation` header (`X-Riak-Continuation`) may be added to the response to be used as the `continuation` in a subsequent request (to see the next batch of results).

For queries using an `accumulation_option` of `queue_raw_keys` or `queue_raw_terms` the response is a JSON object containing only a `result_queue` key with its associated value (to be used in subsequent fetch requests).  Fetch requests from the result queue, will return a JSON object with four keys:

- `raw_keys`/`raw_terms`; a batch of results, no bigger than `max_results`.
- `returned_count`; an integer count of results that have been returned via this API for this query (including the results in this response);
- `queued_count`; an integer count of results that have been queued so far in response to the query (including any results already returned);
- `query_complete`; a boolean value which will be `true` when the query has been complete and there will be no more results to be queued.

When the `queued_count` is equal to the `returned_count` and also `query_complete` is true - then there are no more results to be fetched, and all subsequent requests will contain an empty list of `raw_keys` or `raw_terms`, and unchanged results for `returned_count`, `queued_count` and `query_complete`.

e.g.

```json
[{<<"query_complete">>,true},{<<"raw_keys">>,[ "990011234", "990011235" ]},{<<"received_count">>,1000},{<<"responses_count">>,0}]
```
