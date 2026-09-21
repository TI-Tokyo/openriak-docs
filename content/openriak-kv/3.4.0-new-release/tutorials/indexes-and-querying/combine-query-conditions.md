---
title: Combine query conditions
weight: 230
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Combine two independently verified index searches. Continue with the people dataset and find people
  whose surname is Ng and whose city is Tokyo.
related:
- tutorials/indexes-and-querying/search-projected-attributes
- tutorials/indexes-and-querying/produce-counts-and-grouped-results
- how-to/indexes-and-queries/combine-queries-and-accumulate-results
- reference/query-api/endpoints-and-request-schema
- reference/query-api/accumulation-modes
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-cost-and-result-delivery
previous_page: tutorials/indexes-and-querying/search-projected-attributes
next_page: tutorials/indexes-and-querying/produce-counts-and-grouped-results
---

Combine two independently verified index searches. Continue with the people dataset and find people whose surname is Ng and whose city is Tokyo.

## Define the two searches

Create `query.json`:

```json
{
  "accumulation_option":"keys",
  "aggregation_expression":"$1 INTERSECT $2",
  "query_list":[
    {"aggregation_tag":1,"index_name":"family_bin","start_term":"Ng","end_term":"Ng"},
    {"aggregation_tag":2,"index_name":"city_bin","start_term":"Tokyo","end_term":"Tokyo"}
  ]
}
```

Submit the saved query:

```sh
curl --fail -H 'Content-Type: application/json' --data-binary @query.json   "$RIAK_HTTP/types/docs/buckets/people/query"
```

The result contains only `aiko`. The surname search alone matches Aiko and Sam; the city search alone matches Aiko and Wei.

## Compare set operations

Change `INTERSECT` to `UNION` and expect all three keys. Change the expression to `$1 SUBTRACT $2` and expect only `sam`.

The numbered references are the entries' aggregation tags, not their positions in a response. Keep the tags distinct when adding another constituent query.

## Continue

Retain the same records. The next lesson changes the result accumulation rather than fetching every key.
