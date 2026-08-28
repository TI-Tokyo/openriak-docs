---
title: 'AAE fold API reference'
description: 'Define AAE fold request shapes, filters, responses, timeouts, and safety characteristics.'
weight: 1
diataxis: 'reference'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
  - 'developers'
migration_source_root: '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv'
migration_sources:
  - '\\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\configure\guides\tictac-active-anti-entropy\tictac-active-anti-entropy.md'
migration_review:
  - 'Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.'
source_material:
  - 'openriak-quickdocs-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#aae-fold-api'
  - 'https://openriak.github.io/riak/OtherAPI.html#aae-fold-efficiency'
  - 'https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-http'
  - 'https://openriak.github.io/riak/OtherAPI.html#aae-folds-via-pb'
  - 'https://openriak.github.io/riak/OtherAPI.html#fetch_clocks_nval'
  - 'https://openriak.github.io/riak/OtherAPI.html#fetch_clocks_range'
  - 'https://openriak.github.io/riak/OtherAPI.html#merge_branch_nval'
  - 'https://openriak.github.io/riak/OtherAPI.html#merge_root_nval'
  - 'https://openriak.github.io/riak/OtherAPI.html#merge_tree_range'
  - 'https://openriak.github.io/riak/OtherAPI.html#performance-and-efficiency'
  - 'https://openriak.github.io/riak/OtherAPI.html#repl_keys_range'
  - 'https://openriak.github.io/riak/OtherAPI.html#riak-kv---other-apis'
  - 'https://openriak.github.io/riak/OtherAPI.html#supported-fold-types'
tags: ['diataxis', 'kv', 'reference']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Define AAE fold request shapes, filters, responses, timeouts, and safety characteristics.

## Details

### OpenRiak KV - Other APIs

The majority of work within OpenRiak KV can be done using the [Object API](/kv/3.4.1/reference/http-api/), and the [Query API](/kv/3.4.1/tutorials/query-api/).  There are though additional APIs, with specific purposes:

- [The AAE Fold API](/kv/3.4.1/reference/aae-fold-api/)
- [The Fetch API used to access replication queues](/kv/3.4.1/reference/specialized-apis/fetch-api/)
- [The Data Type API](/kv/3.4.1/reference/specialized-apis/data-type-api/)
- [The Map/Reduce API](/kv/3.4.1/reference/http-api/mapreduce/)
- [The List API](/kv/3.4.1/reference/specialized-apis/list-api/)
- [The Strong Consistency API](/kv/3.4.1/reference/specialized-apis/strong-consistency-api/)
- [The Write Once Path API](/kv/3.4.1/reference/specialized-apis/write-once-api/)

#### AAE Fold API

The AAE Fold API requires the configuration of `tictacaae_active = active`, otherwise folds will fail.  When using a single leveled backend, this should use the native keystore within leveled.

When using any other backend or multi-backend this will require an additional parallel keystore, which may have an impact on the achievable PUT throughput, and the memory used by Riak.  The use of a parallel backend also requires periodic keystore rebuilds, to ensure that the keystore correctly represents the content in the backend store.

> When using parallel mode, the parallel store must be configured with `tictacaae_storeheads = enabled` to use the full functionality of AAE Folds.

The AAE Fold API:

- Supports [more than ten different fold types](/kv/3.4.1/reference/aae-fold-api/);
- [Are throttled to minimise the impact on other cluster operations, and have query options that may improve efficiency](/kv/3.4.1/reference/aae-fold-api/).

The AAE Fold API has four potential interfaces:

- [AAE Folds via the Command Line](/kv/3.4.1/how-to/operate/aae-fold/run-from-command-line/);
- [AAE Folds via remote_console](/kv/3.4.1/how-to/operate/use-remote-console/);
- [AAE Folds via HTTP](/kv/3.4.1/reference/aae-fold-api/);
- [AAE Folds via protocol buffers](/kv/3.4.1/reference/aae-fold-api/).

#### Supported fold types

All APIs support the following types of fold:

#### merge_root_nval

For a given n_val merge the root of a the merkle tree across all partitions, given a cluster-wide view of the tree root:

- Relatively fast, as uses cached trees;
- Intended for internal use within inter-cluster reconciliation.

#### merge_branch_nval

For a given `n_val` and list of `branch_id`'s (normally deltas discovered after comparing tree roots), merge the branches across all partitions, to give a cluster wide view of those branches within the merkle tree:

- Relatively fast, as uses cached trees;
- intended for internal use within inter_cluster reconciliation.

#### fetch_clocks_nval

For a given set of segment IDs return all the keys and clocks within those segments, potentially constrained by a modified date range.

- If a full-sync manager process detects a false delta, it will temporarily set enable the `aae_fetchclocks_repair` option, and this will cause this query to repair the cached tree for the given segment IDs, as well as collect the results to return.
  - It is possible to force this repair option via configuration or environment variable change.
- Uses the AF3 queue when running node worker pools in `dscp` mode.
  - These queries will bypass the pool, running immediately, when repair is required.

#### merge_tree_range

Outputs a full merkle tree representing the overall cluster state for a given bucket.

- Relatively slow compared to `_nval` equivalent queries, as no cached trees can be used; requiring a fold over the actual keys to calculate the tree.
- Setting filters is recommended to speed up the query (unless buckets are small).

#### fetch_clocks_range

Equivalent to fetch_clocks_nval but with Bucket and KeyRange constraints.

- Unlike fetch_clocks_nval, this will never result in a repair of cached trees.
- Uses the AF3 queue when running node worker pools in `dscp` mode.

#### repl_keys_range

Used to replicate a range of keys to another cluster (or indeed any consumer of a given replication queue).  To be used when seeding new clusters, or if there is a known delta that can be expressed and resolved more quickly by this mechanism rather than by waiting for inter-cluster reconciliation to auto-heal.

- When adding to the replication queue, will be added with a lower priority when compared to real-time replication.
- Each replication queue has a small in-memory part but a large on-disk part.  The size of the on-disk component is controlled in `riak.conf` via `replrtq_overflow_limit`.
- Uses the AF4 queue when running node worker pools in `dscp` mode.

#### Performance and Efficiency

The AAE Fold implementation has similarities to [the Query API](/kv/3.4.1/explanation/performance/query-execution/).  The sequence of operations for the fold is:

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

The AAE folds will scan over blocks of keys and metadata.  The performance of AAE fold requests are impacted by the volume of metadata per key, and the throughput per CPU core is likely to be lower than with the [Query API](/kv/3.4.1/explanation/performance/query-execution/) - where only blocks of index entities need to be scanned.  Unlike the Query API, none of the accumulators are required to deduplicate, so there is no related impact on performance.

Where a fold is returning a list of keys, or keys and clocks, it is necessary for the node coordinating the fold to hold the full result-set in memory; and on conclusion of the fold the results will need to be copied at least once to produce an API response.  The performance of the fold will also be impacted by an accumulator which grows with the number of entries covered.

> It is important to consider the memory impact of running an AAE fold on the node that handles the request, especially when using a `find_keys` fold.

#### AAE Folds via HTTP

AAE folds require a URL and potentially a filter.  The filter may be a base64 encoded list of JSON key/value pairs to pass key_range, date_range, segment_filter, hash_iv, or change_method.

| Query Type | URL | Filter |
|:-----------|:-----------|:-----------|
| merge_root_nval | `/cachedtrees/nvals/<NVal>/root`| no filter required |
| merge_branch_nval | `/cachedtrees/nvals/<NVal>/branch` | b64 encode json: list of integers |
| fetch_clocks_nval | `/cachedtrees/nvals/<NVal>/keysclocks` | b64 encode json: segment_filter, date_range |
| merge_tree_range | `/rangetrees/types/<BucketType>/buckets/<Bucket>/trees/<TreeSize>` | b64 encode json: key_range, segment_filter, date_range |
| fetch_clocks_range  | `/rangetrees/types/<BucketType>/buckets/<Bucket>/keysclocks`| b64 encode json: key_range, segment_filter, date_range |
| repl_keys_range | `/rangerepl/types/<BucketType>/buckets/<Bucket>` | b64 encode json: key_range, segment_filter, date_range |
| repair_keys_range | `/rangerepair/types/<BucketType>/buckets/<Bucket>` | b64 encode json: key_range, segment_filter, date_range  |
| find_keys (siblings) | `/siblings/types/<BucketType>/buckets/<Bucket>/counts/<Cnt>` | b64 encode json: key_range, date_range |
| find_keys (by size) | `/objectsizes/types/<BucketType>/buckets/<Bucket>/size/<Size>` | b64 encode json: key_range, date_range  |
| find_tombs  | `/tombs/types/<BucketType>/buckets/<Bucket>` | b64 encode json: key_range, segment_filter, date_range |
| erase_keys | `/erase/types/<BucketType>/buckets/<Bucket>` | b64 encode json: key_range, segment_filter, date_range |
| reap_tombs  | `/reap/types/<BucketType>/buckets/<Bucket>` | b64 encode json: key_range, segment_filter, date_range |
| list_buckets | `/aaebucketlist` | `filter=<NVal>` |

To run a query against an untyped bucket, remove the `types/<BucketType>` slice of the URL.

#### AAE Folds via PB

The [PB Object API is described in the riak_pb repository](https://github.com/OpenRiak/riak_pb/blob/e908ddaadc06cb56e248f197dc2dca7d759e53b2/src/riak_kv.proto#L409-L660).

> [!WARNING]
> Migration review required: Internal links still refer to the earlier documentation hierarchy and must be retargeted to the Diátaxis paths.

## In this section

- [Count keys operation](/kv/3.4.1/reference/aae-fold-api/count-keys/) — Document parameters, filters, response fields, limits, and risks for the count keys operation.
- [Count tombstones operation](/kv/3.4.1/reference/aae-fold-api/count-tombstones/) — Document parameters, filters, response fields, limits, and risks for the count tombstones operation.
- [Erase keys operation](/kv/3.4.1/reference/aae-fold-api/erase-keys/) — Document parameters, filters, response fields, limits, and risks for the erase keys operation.
- [AAE fold filters](/kv/3.4.1/reference/aae-fold-api/filters/) — Document parameters, filters, response fields, limits, and risks for the aae fold filters.
- [Find keys operation](/kv/3.4.1/reference/aae-fold-api/find-keys/) — Document parameters, filters, response fields, limits, and risks for the find keys operation.
- [Find tombstones operation](/kv/3.4.1/reference/aae-fold-api/find-tombstones/) — Document parameters, filters, response fields, limits, and risks for the find tombstones operation.
- [List buckets operation](/kv/3.4.1/reference/aae-fold-api/list-buckets/) — Document parameters, filters, response fields, limits, and risks for the list buckets operation.
- [Object statistics operation](/kv/3.4.1/reference/aae-fold-api/object-statistics/) — Document parameters, filters, response fields, limits, and risks for the object statistics operation.
- [Reap tombstones operation](/kv/3.4.1/reference/aae-fold-api/reap-tombstones/) — Document parameters, filters, response fields, limits, and risks for the reap tombstones operation.
- [Repair key range operation](/kv/3.4.1/reference/aae-fold-api/repair-key-range/) — Document parameters, filters, response fields, limits, and risks for the repair key range operation.
