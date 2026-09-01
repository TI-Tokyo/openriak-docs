---
title: 'Performance concepts'
description: 'Introduce the resource, topology, workload, and runtime factors that shape OpenRiak performance.'
weight: 1
diataxis: 'explanation'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'performance-engineers'
  - 'architects'
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#aae-fold-efficiency'
  - 'https://openriak.github.io/riak/OtherAPI.html#performance-and-efficiency'
tags: ['diataxis', 'kv', 'explanation']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce the resource, topology, workload, and runtime factors that shape OpenRiak performance.

## Overview

### Performance and Efficiency

The AAE Fold implementation has similarities to [the Query API]({{< product-version-root >}}foundations/performance/query-execution/).  The sequence of operations for the fold is:

- On the local node that received the request, a query server is started to orchestrate the fold across the cluster;
  - In Riak 3.4 the query server has a different underlying implementation to the query server used in the Query API; but this may change to use a common implementation in a future release.
- Folds are run over a covering set of vnodes, i.e. either `RingSize div n_val` or `(RingSize div n_val) + 1`.
- Folds will first take a snapshot of each vnode, before running each vnode query against the snapshot.
  - When running in parallel mode, this will be a snapshot of the parallel keystore, in native mode this will be a snapshot of the leveled ledger (the native keystore).
  - The snapshot requests will need to wait in the vnode queue, but operations on the snapshot are not constrained by the queue.
  - The snapshots have a timeout, and a fold that runs after the timeout is likely to fail;
    - On native stores the timeout for AAE folds is configured via `leveled.snapshot_timeout_long`.  On parallel stores it defaults to 2 days.
- The folds will then scan across the keys and metadata using the filters provided, accumulate results, and return the results to the controlling node for the query once complete.
  - Unlike the Query API, there is no sending of partial results, and waiting for acknowledgement.
  - AAE folds will continue to run, even when the query server for the request has timed out.
  - If a queue-type accumulator is used, the results are sent to the queue in batches during the fold, and the final result returned to the query server is just a count.
- Once all vnode folds have completed and sent results, the query server will combine the results and return the final result-set back to the requester.

#### AAE Fold efficiency

Some considerations on the efficiency of AAE Folds:

- Using a restricted key_range is the most reliable method of improving the speed and efficiency of AAE Folds;
- A modified date range will reduce the volume of data to be processed and returned, but significant gains are only made when setting a "high" low modified date.  Old content below the low modified data can be skipped over without reading, but new content since the high modified date must still be read and deserialised.
- The segment_filter can skip the reading and deserialising of slots (each slot contains 128 keys, split into 5 blocks) by checking in the slot header, with approximately 99.6% of blocks skipped when checking for a single segment.
- The segment_filter can be used for sampling, or approximations.  With the standard tree size, there are a `1024 * 1024` segments, so choosing a random slice of 64 segments in that integer space will give results from `1 / (8 * 1024)`th of the key-space.
  - Use of a contiguous slice is more efficient than selecting random slices, as when checking Segments only the first 15 of the 20 bits (assuming standard tree size) in a segment ID are used.
  - When folds are used with Riak anti-entropy mechanisms, the `max_results` settings are used to control the size of the list of segment IDs passed into a fold.

The AAE folds will scan over blocks of keys and metadata.  The performance of AAE fold requests are impacted by the volume of metadata per key, and the throughput per CPU core is likely to be lower than with the [Query API]({{< product-version-root >}}foundations/performance/query-execution/) - where only blocks of index entities need to be scanned.  Unlike the Query API, none of the accumulators are required to deduplicate, so there is no related impact on performance.

Where a fold is returning a list of keys, or keys and clocks, it is necessary for the node coordinating the fold to hold the full result-set in memory; and on conclusion of the fold the results will need to be copied at least once to produce an API response.  The performance of the fold will also be impacted by an accumulator which grows with the number of entries covered.

> It is important to consider the memory impact of running an AAE fold on the node that handles the request, especially when using a `find_keys` fold.

## In this section

- [The Erlang runtime and OpenRiak]({{< product-version-root >}}foundations/performance/erlang-runtime/) — Explain the erlang runtime and openriak and how its trade-offs influence measurement and tuning decisions.
- [Latency, throughput, and capacity]({{< product-version-root >}}foundations/performance/latency-throughput-and-capacity/) — Explain latency, throughput, and capacity and how its trade-offs influence measurement and tuning decisions.
- [Multi-datacenter performance]({{< product-version-root >}}foundations/performance/multi-datacenter-performance/) — Explain multi-datacenter performance and how its trade-offs influence measurement and tuning decisions.
- [Query execution performance]({{< product-version-root >}}foundations/performance/query-execution/) — Explain how query distribution, scanning, filtering, buffering, and collation affect latency and capacity.
- [Storage and filesystem effects]({{< product-version-root >}}foundations/performance/storage-and-filesystem-effects/) — Explain storage and filesystem effects and how its trade-offs influence measurement and tuning decisions.
