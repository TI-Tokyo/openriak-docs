---
title: 'Read and write quorums'
description: 'Explain how quorum choices affect latency, availability, durability, and stale reads.'
weight: 3
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'architects'
  - 'developers'
  - 'operators'
source_material:
  - 'live-3.2.5'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/RiakTheoryGuide.html#quorum-on-read-write-and-query'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Explain how quorum choices affect latency, availability, durability, and stale reads.

## Overview

### Quorum on Read, Write and Query

The default GET and PUT options are based on validating quorum within the cluster before returning a response to the client.  Quorum meaning that a majority of vnodes within a preflist must have provided acknowledged input to the transaction.  So although Riak offers a guarantee that data will be eventually consistent; within a single, stable cluster an application will still [read its own writes](https://jepsen.io/consistency/models/read-your-writes).  There are tunable consistency [properties in Riak](/kv/3.4.1/reference/configuration/bucket-properties/), that can be used to extend this guarantee to clusters during individual node failures.

> Quorum is the default for [the Object API](/kv/3.4.1/reference/http-api/), but not the default for [the Query API](/kv/3.4.1/tutorials/query-api/).

All index updates within a vnode are transactional to the object change; so that in a single, stable cluster, queries will immediately reflect the latest update.  There is no post-update delay for indices to be updated. However queries have to be distributed across a covering set of primary vnodes, and this covering set will include a single replica of each object.  If a primary vnode is active but not up-to-date (i.e. due to a recent recovery from failure or corruption), query results are not validated by checking results between replicas.

The issue of missing data in coverage queries during the recovery process, can be mitigated by relying on operator intervention, using the `participate_in_coverage` setting to block a recovering node from participating in queries.

It is possible to use inverted indexes for queries within Riak, so that queries can also use quorum reads.  However, using inverted indexes in Riak 3.4 requires management from within the application, not the database.
