---
title: 'Monitor inter-cluster reconciliation'
description: 'Show operators how to observe reconciliation exchanges and diagnose incomplete convergence.'
weight: 24
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#monitoring-inter-cluster-reconciliation'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#monitoring-and-runtime-changes'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#monitoring-real-time-replication-via-logs'
  - 'https://openriak.github.io/riak/ReplicationGuide.html#monitoring-reconciliation-exchanges-via-logs'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to observe reconciliation exchanges and diagnose incomplete convergence.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Monitoring inter-cluster reconciliation

For information on monitoring inter-cluster reconciliation and repair [refer to the NextGen Repl guide]({{< baseurl >}}kv/3.4.1/how-to/operate/monitor-reconciliation/).

#### Monitoring real-time replication via logs

The size of replication queue is logged as follows:

`@riak_kv_replrtq_src:handle_info:414 QueueName=replq has queue sizes p1=0 p2=0 p3=0`

There is a log on each sink node of the replication timings:

`Queue=~w success_count=~w error_count=~w mean_fetchtime_ms=~s mean_pushtime_ms=~s mean_repltime_ms=~s lmdin_s=~w lmdin_m=~w lmdin_h=~w lmdin_d=~w lmd_over=~w`

The `mean_repltime` is a measure of the delta between the last-modified-date on the replicated object and the time the replication was completed - so this may vary if prompting replication due to real-time changes, reconciliation or seeding.  The `lmdin_<x>` counts are the counts of replicated objects which were replicated within a second, minute, hour, day or over a day.

#### Monitoring reconciliation exchanges via logs

When a cluster relationship has been seeded, and real-time replication has been enabled - reconciliation will generally be fast, and consistently return a result of `in_sync = true`.

Should a delta occur, there will be logs not just of the sync status, but with information about the deltas discovered. Following a `clock_compare`, a log will be generated for each bucket where repairs were required, with the low and high modification dates associated with the repairs:

{% raw %}
```console
riak_kv_ttaaefs_manager:report_repairs:1071 AAE exchange=122471781 work_item=all_check type=full repaired key_count=18 for bucket=<<"domainDocument_T9P3">> with low date {{2020,11,30},{21,17,40}} high date {{2020,11,30},{21,19,42}}
riak_kv_ttaaefs_manager:report_repairs:1071 AAE exchange=122471781 work_item=all_check type=full repaired key_count=2 for bucket=<<"domainDocument_T9P9">> with low date {{2020,11,30},{22,11,39}} high date {{2020,11,30},{22,15,11}}
```
{% endraw %}

If there is a need to investigate further what keys are the cause of the mismatch, all repairing keys can be logged by setting via `remote_console`:

```erlang
application:set_env(riak_kv, ttaaefs_logrepairs, true).
```

This will produce logs for each individual key:

{% raw %}
```console
@riak_kv_ttaaefs_manager:generate_repairfun:973 Repair B=<<"domainDocument_T9P3">> K=<<"000154901001742561">> SrcVC=[{<<170,167,80,233,12,35,181,35,0,49,73,147>>,{1,63773035994}},{<<170,167,80,233,12,35,181,35,0,97,246,69>>,{1,63773990260}}] SnkVC=[{<<170,167,80,233,12,35,181,35,0,49,73,147>>,{1,63773035994}}]

@riak_kv_ttaaefs_manager:generate_repairfun:973 Repair B=<<"domainDocument_T9P3">> K=<<"000154850002055021">> SrcVC=[{<<170,167,80,233,12,35,181,35,0,49,67,85>>,{1,63773035957}},{<<170,167,80,233,12,35,181,35,0,97,246,68>>,{1,63773990260}}] SnkVC=[{<<170,167,80,233,12,35,181,35,0,49,67,85>>,{1,63773035957}}]

@riak_kv_ttaaefs_manager:generate_repairfun:973 Repair B=<<"domainDocument_T9P3">> K=<<"000154817001656137">> SrcVC=[{<<170,167,80,233,12,35,181,35,0,49,71,90>>,{1,63773035982}},{<<170,167,80,233,12,35,181,35,0,97,246,112>>,{1,63773990382}}] SnkVC=[{<<170,167,80,233,12,35,181,35,0,49,71,90>>,{1,63773035982}}]

@riak_kv_ttaaefs_manager:generate_repairfun:973 Repair B=<<"domainDocument_T9P3">> K=<<"000154801000955371">> SrcVC=[{<<170,167,80,233,12,35,181,35,0,49,70,176>>,{1,63773035978}},{<<170,167,80,233,12,35,181,35,0,97,246,70>>,{1,63773990260}}] SnkVC=[{<<170,167,80,233,12,35,181,35,0,49,70,176>>,{1,63773035978}}]
```
{% endraw %}

At the end of each stage of a an exchange a log EX003 is produced which explains the outcome of the exchange:

```console
log_level=info log_ref=EX003 pid=<0.30710.6> Normal exit for full exchange purpose=day_check in_sync=true  pending_state=root_compare for exchange id=8c11ffa2-13a6-4aca-9c94-0a81c38b4b7a scope of mismatched_segments=0 root_compare_loops=2  branch_compare_loops=0  keys_passed_for_repair=0

log_level=info log_ref=EX003 pid=<0.13013.1264> Normal exit for full exchange purpose=range_check in_sync=false  pending_state=clock_compare for exchange id=921764ea-01ba-4bef-bf5d-5712f4d81ae4 scope of mismatched_segments=1 root_compare_loops=3  branch_compare_loops=2  keys_passed_for_repair=15
```

The mismatched_segments is an estimate of the scope of damage to the tree.  Even if `clock_compare` shows no deltas, clusters are not considered `in_sync` until deltas are not shown with tree comparisons (e.g. `root_compare` or `branch_compare` return 0).

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
