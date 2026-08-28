---
title: 'Resynchronize a bucket'
description: 'Show operators how to request and monitor optimized reconciliation for one bucket in OpenRiak KV 3.4.1.'
weight: 29
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'source-code-release-notes-3.4'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/ReplicationGuide.html#re-sync-a-bucket'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to request and monitor optimized reconciliation for one bucket in OpenRiak KV 3.4.1.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Re-Sync a Bucket

Full-sync reconciliation is designed to be fast and efficient for confirming that clusters are in sync, but is relatively slow to resolve deltas between clusters.  The common case, when the delta is associated with a recent window of last-modified-dates (e.g. due to a recent temporary failure of replication or nodes) is optimised through the `auto_check` process; and also [re-replication]({{< baseurl >}}kv/3.4.1/how-to/operate/rereplicate-time-window/) may be used to accelerate this.  However, if the delta is not restricted to a given time range of modified dates, and the delta is large, there is a need for alternative intervention to close the delta in a timely manner.

For small buckets (in terms of object count), simply re-replicating the bucket could be the easiest solution, especially where it is clear the replication failure is uni-directional.  For larger buckets, and for handling bi-directional deltas, then it is possible to manually intervene to re-sync a bucket.

The re-sync can be triggered from any node, from either cluster - assuming that bi-directional replication is configured.  The re-sync is cluster-wide, it is not a re-sync of data local to the node. The re-sync can handle, as with other nextgenrepl features, clusters with different configurations (e.g. `n_val` settings).

A bucket re-sync will suspend the local full-sync process on the node from which it is triggered, and roll through segment slices of the bucket performing bucket-specific `range_check` operations.  As each loop covers only a single slice of the segment space, this is much quicker to repair than the standard full-sync per-bucket check, which needs to read the whole bucket space to build AAE trees for comparison.

The re-sync bucket can be called via [remote_console]({{< baseurl >}}kv/3.4.1/how-to/operate/use-remote-console/):

```console
riak_client:resync_bucket({<<"BucketType">>, <<"BucketName">>}).
```

Or, for untyped buckets:

```console
riak_client:resync_bucket(<<"BucketName">>).
```

> In small buckets, of o(10m) keys, it would be normal to have a bucket resync operation repair deltas at a rate exceeding 1,000 per second.

As well as the helper function in `riak_client`, there is a configurable `riak_kv_ttaaefs_manager:resync_bucket/6` function exported.  For much larger buckets, this configurable version can be used to optimise the process e.g. use a smaller width (the size of the slice of the segment space), fix a specific key range or within a modified date range.

> It is possible to have multiple nodes running resync_bucket concurrently - to sync different buckets, or different key ranges within a bucket.  The limiting factor to horizontal scaling of resync_bucket is usually the size of [AF3 worker pool]({{< baseurl >}}kv/3.4.1/how-to/operate/monitor-worker-pools/).  Once all workers in the pool are continuously busy, no further scaling can be achieved, without running larger pools (on all clusters).

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
