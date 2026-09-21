---
title: Query consistency and snapshots
weight: 190
product: OpenRiak KV
product_version: 3.4.0
diataxis: explanation
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: A distributed query observes partition-local snapshots, not one transactionally consistent instant
  across the cluster. Concurrent object changes can therefore affect what the overall result represents.
related:
- foundations/indexes-and-querying/how-distributed-queries-execute
- reference/query-api/continuations-and-result-delivery
- reference/query-api/limits-and-behavioural-constraints
- how-to/indexes-and-queries/retrieve-paginated-or-asynchronous-query-results
---

A distributed query observes partition-local snapshots, not one transactionally consistent instant across the cluster. Concurrent object changes can therefore affect what the overall result represents.

## A snapshot within a vnode

Combination queries use one snapshot per vnode for their constituent scans. This keeps the local set operations consistent for a potential key within that vnode's work. Other vnodes can take their snapshots at different times.

## Across the cluster

If an application updates related objects on different partitions, a query may see one change before another. There is no cross-object transaction connecting those changes. Inter-cluster replication introduces further timing differences between the datasets queried at each destination.

## Retrieving objects after a query

An index query returns discovery results. A later object fetch is another request and can encounter an updated value, siblings, or a missing object. Applications should tolerate that gap rather than treating a returned key as a reservation on the value.

## Repeated and continued queries

Use the API's continuation contract for a larger result set. Do not assume that restarting the same query or using an unrelated request reproduces the original snapshot. For an audit requiring a stable dataset, control writes and define the observation window explicitly.
