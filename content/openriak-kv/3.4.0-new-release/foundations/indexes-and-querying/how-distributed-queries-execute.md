---
title: How distributed queries execute
description: The Query API distributes index work across the vnodes covering the requested bucket. Each vnode scans
  its local index range, evaluates and filters terms, and contributes results to the requested accumulation.
weight: 180
diataxis: explanation
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- architects
- developers
source_material:
- source-code-release-notes-3.4
- openriak-quickdocs-3.4
- openriak-discussions
quickdocs_sources:
- https://openriak.github.io/riak/QueryAPI.html#further-improvements
- https://openriak.github.io/riak/QueryAPI.html#notes-on-implementation
- https://openriak.github.io/riak/QueryAPI.html#querying---functional-summary
- https://openriak.github.io/riak/QueryAPI.html#riak-kv---query-api
tags:
- diataxis
- kv
- explanation
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- foundations/data-model/query-api.md
related:
- foundations/indexes-and-querying/query-consistency-and-snapshots
- foundations/indexes-and-querying/query-cost-and-result-delivery
- reference/query-api/endpoints-and-request-schema
- reference/query-api/accumulation-modes
- reference/query-api/continuations-and-result-delivery
- how-to/indexes-and-queries/combine-queries-and-accumulate-results
---

The Query API distributes index work across the vnodes covering the requested bucket. Each vnode scans its local index range, evaluates and filters terms, and contributes results to the requested accumulation.

## The query pipeline

The range selects candidate index entries. An evaluation expression extracts projected attributes from each term. A filter expression decides which candidates match. Accumulation determines whether the result contains keys, terms, counts, or grouped values.

Combination queries run multiple scans and combine their matches with set operations. Performing those operations close to the partition avoids sending every intermediate result to one cluster-wide coordinator.

## Parallelism and limits

Partitions can work in parallel, but the response still depends on the participating work completing. A slow backend, broad range, expensive expression, or large result can dominate the request. Adding client concurrency can increase queueing rather than reduce the cost of an individual query.

## Results are an interface choice

Choose an accumulation that returns the information the application needs. Counting inside the query avoids transporting a large key list solely to count it at the client. Result delivery, continuation handling, and release-specific asynchronous behaviour are separate API contracts.
