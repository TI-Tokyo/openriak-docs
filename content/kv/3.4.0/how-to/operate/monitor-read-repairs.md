---
title: 'Monitor read repairs'
description: 'Show operators how to observe read-repair activity and identify abnormal repair rates.'
weight: 23
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#logging-and-monitoring-of-read-repairs'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to observe read-repair activity and identify abnormal repair rates.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Logging and monitoring of read repairs

Read repairs will be invoked directly when a user GET request reveals an out-of-date or missing object within the preflist

> Although GETs will by default respond to the client on quorum responses, all GET processes continue until all responses have returned or timed out.  The read repair is then triggered if required, based on all responses not just the quorum.

Each read repair, will update the `read_repairs` and `read_repairs_total` statistic available [via riak stats]({{< baseurl >}}kv/3.4.0/reference/operations/statistics-and-monitoring/).  Other stats updates are also made:

- `read_repairs_fallback_notfound`;
- `read_repairs_fallback_outofdate`;
- `read_repairs_primary_notfound`;
- `read_repairs_primary_outofdate`.

These stats indicate whether the vnode in need of repair was a primary or fallback, and whether it has been repaired as it had an out of date object, or the object was not found in that vnode.

During a node failure, `n_val` fallback vnodes will be started for every unavailable primary vnode.  As the fallback vnodes start empty, a large number of read repairs may be immediately triggered, assuming the cluster is subject to application read requests.  This will in the short term impact performance, and in the long term impact handoff times when the node recovers - but in the medium term it will mean that the vnode has frequently accessed data to contribute to quorum.  The [`read_repair_primaryonly` configuration option]({{< baseurl >}}kv/3.4.0/how-to/configure/basic-node-settings/) can be enabled to stop repairing fallback vnodes through read repair.

Read repairs are also invoked by active anti-entropy.  When an intra-cluster AAE process detects a delta, it does not prompt it directly, it instead will prompt a GET request so that read repair will happen indirectly.

If a repair has been prompted by a Tictac AAE anti-entropy exchange, setting the environment variable `riak_kv` `log_readrepair` to `true` will prompt the details of the Keys and compared Clocks to be logged for every repair.  This may be useful in trying to determine the root cause of discrepancies.

```console
riak eval "application:set_env(riak_kv, log_readrepair, true)"
```

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
