---
title: Produce counts and grouped results
weight: 240
product: OpenRiak KV
product_version: 3.4.0
diataxis: tutorial
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Count the known people and group counts by city. Use the same three records so you can check the answer
  by inspection.
related:
- tutorials/indexes-and-querying/combine-query-conditions
- tutorials/indexes-and-querying/retrieve-a-larger-result-set
- reference/query-api/accumulation-modes
- how-to/indexes-and-queries/combine-queries-and-accumulate-results
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-cost-and-result-delivery
previous_page: tutorials/indexes-and-querying/combine-query-conditions
next_page: tutorials/indexes-and-querying/retrieve-a-larger-result-set
---

Count the known people and group counts by city. Use the same three records so you can check the answer by inspection.

## Count surname matches

Run the surname query from the first index lesson with `accumulation_option` set explicitly to `count`. There are two distinct keys for surname Ng, so the returned count should be two.

## Group by city

Create `query.json`:

```json
{
  "accumulation_option":"term_with_count",
  "query_list":[{
    "index_name":"city_bin",
    "start_term":"A",
    "end_term":"Z~"
  }]
}
```

Submit the saved query:

```sh
curl --fail -H 'Content-Type: application/json' --data-binary @query.json   "$RIAK_HTTP/types/docs/buckets/people/query"
```

Check the grouped result: Tokyo has two people and Osaka has one. This lesson's ASCII range covers the fixture, not an arbitrary Unicode naming scheme.

## Check what you are counting

A distinct-key count and a raw match count need not agree when one object has several matching index terms. Use the accumulation reference before applying the result as a business total.

Keep the dataset for the pagination exercise.
