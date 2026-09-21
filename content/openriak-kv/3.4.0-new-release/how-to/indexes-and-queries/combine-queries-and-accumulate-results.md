---
title: Combine queries and accumulate results
weight: 570
product: OpenRiak KV
product_version: 3.4.0
diataxis: how-to
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Combine index queries with set operations, then choose the result accumulation required by the application.
related:
- reference/query-api/endpoints-and-request-schema
- reference/query-api/expression-grammar-and-operators
- reference/query-api/accumulation-modes
- tutorials/indexes-and-querying/combine-query-conditions
- tutorials/indexes-and-querying/produce-counts-and-grouped-results
- foundations/indexes-and-querying/secondary-indexes-and-projected-attributes
- foundations/indexes-and-querying/how-distributed-queries-execute
- foundations/indexes-and-querying/query-cost-and-result-delivery
---

Combine index queries with set operations, then choose the result accumulation required by the application.

## Build and verify the constituent queries

Run each range independently against a known dataset. Give each entry in `query_list` a distinct `aggregation_tag`. Record the expected overlap before introducing an aggregation expression.

## Combine them

Use `aggregation_expression` with references such as `$1` and `$2`. An example expression is `($1 INTERSECT $2) SUBTRACT $3`; the numbers must match the submitted tags. Use parentheses to make the intended grouping clear.

## Select accumulation

Choose a mode supported for combination queries in the selected release. Use keys to inspect membership before switching to a count. Raw match counts and distinct-object counts are different when more than one index entry matches a key.

## Verify and retain the query

Compare the combined result with the expected intersection, union, or subtraction of your independent query results. Include duplicate terms and an empty constituent result. Save the query body and expected answer as an application fixture so changes to the term encoding do not silently change its meaning.
