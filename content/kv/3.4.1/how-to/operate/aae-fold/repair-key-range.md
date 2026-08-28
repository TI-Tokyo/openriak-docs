---
title: 'Repair a key range with AAE fold'
description: 'Show operators how to repair a key range with aae fold and interpret the outcome.'
weight: 10
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\repair-keys-range.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OperationsAndTroubleshootingGuide.html#repair-key-ranges'
  - 'https://openriak.github.io/riak/OtherAPI.html#repair_keys_range'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to repair a key range with aae fold and interpret the outcome.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Repair Keys

[code riak_kv_vnode]: https://github.com/basho/riak_kv/blob/develop-3.0/src/riak_kv_vnode.erl
[riak attach]: ../../../admin/riak-cli/#attach
[config reference]: ../../../configuring/reference/#tictac-active-anti-entropy
[config tictacaae]: ../../../configuring/active-anti-entropy/tictac-aae
[tictacaae folds-overview]: ../
[tictacaae system]: ../../tictac-active-anti-entropy
[tictacaae client]: ../../tictac-aae-fold#the-riak-client
[tictacaae find-keys]: ../../tictac-aae-fold/find-keys
[tictacaae find-tombs]: ../../tictac-aae-fold/find-tombs
[tictacaae list-buckets]: ../../tictac-aae-fold/list-buckets
[tictacaae object-stats]: ../../tictac-aae-fold/object-stats
[tictacaae reap-tombs]: ../../tictac-aae-fold/reap-tombs
[filters]: ../../tictac-aae-fold/filters
[filter-by bucket]: ../../tictac-aae-fold/filters#filter-by-bucket-name
[filter-by key-range]: ../../tictac-aae-fold/filters#filter-by-key-range
[filter-by segment]: ../../tictac-aae-fold/filters#filter-by-segment
[filter-by modified]: ../../tictac-aae-fold/filters#filter-by-date-modified
[filter-by sibling-count]: ../../tictac-aae-fold/find-keys/#the-sibling-count-filter
[filter-by object-size]: ../../tictac-aae-fold/find-keys/#the-object-size-filter

Performs a read-repair on the Riak objects that meet the filter parameters.

See the [TicTac AAE `aae_folds`][tictacaae folds-overview] documentation for configuration, tuning and troubleshootings help.

Occasionally, you want to perform a read-repair on a number of keys quickly an efficiently. Previously, you had to do a [`find_keys`][tictacaae find-keys] call followed by a read request on each key. This was inefficient as all the data had to be sent over the network to the client. Now, you can have Riak perform a read-repair without sending the data to the client.

Use the `repair_keys_range` function to remove these objects.

#### The `repair_keys_range` function

Run this using [`riak attach`][riak attach].

The format for the function is:

```riakattach
riak_client:aae_fold({
    repair_keys_range,
    bucket_filter,
    key_range_filter,
    modified_filter,
    all
    }, Client).
```

Please see the list of [available filters](#available-filters) below.

**Note:**
For the function `repair_keys_range`, only non-negative interger of seconds since `1970-01-01 00:00:00` works for `modified_filter` in this version. This is fixed in a later version.

For example, the following snippet will perform a read-repair on all Riak objects with the filters:

- in the bucket "dogs" of bucket type "animals"
- whose keys are between "A" and "N"
- which were modified in 2022

```riakattach
riak_client:aae_fold({
    repair_keys_range,
    {<<"animals">>,<<"dogs">>},
    {<<"A">>,<<"N">>},
    {date,1640995200,1672531200},
    all
    }, Client).
```

#### The response

The response will look something like this:

```erlang
{ok,{[],0,all,128}}
```

This indicates that:

- `ok`: the read repair request finished successfully
- `[]`: the remaining items, which should be an empty list
- `0`: the number of keys repairs, in this case none
- `all`: a constant
- `128`: the size of each batch of read repairs, which is 128

This indicates that the keys found meeting the filter parameters and were read-repaired.

#### Available filters

These filters are detailed in the [Filters][filters] documentation and can be used to limit the keys considered for reaping or counting.

These filters will reduce the keys to be searched:

- [`bucket_filter`][filter-by bucket]
- [`key_range_filter`][filter-by key-range]

These filters will reduce the number of keys considered for reaping or counting:

- [`modified_filter`][filter-by modified]

#### Repair key ranges

Outside of the circumstances covered in the previous sections, it is not expected that there should be a need for operator intervention in the recovery from failure.  There is though an additional process for handling any unexpected scenarios, to allow for cluster wide repair of key ranges.  The `repair_key_range` operation is targeted at a specific bucket, potentially combined with a key range or last modified date range: and triggers via an AAE fold the read repair process within the cluster for that range.

Refer to the [API guide for AAE Fold](/kv/3.4.1/reference/aae-fold-api/) for information on triggering a `repair_key_range` AAE fold.

The aae_fold will send repair events to the `riak_kv_reader` queue, and progress can be tracked by tracking the queue's log outputs.  There is an automated background process on each node that will consume repair events from the queue, and trigger read repair (if required) by a clientless GET of the object.  Each node's reader queue is limited to 1M requests, and requests over this limit will be discarded.  This limit is not configurable in Riak 3.4.  The `riak_kv_reader` process will dequeue items from the `riak_kv_reader` queue and prompt an internal GET request; which, should there be a discrepancy, prompt a repair via `read_repair`.

Repair key range operations are a potentially efficient method for repairing keys across a cluster following a known incident, the impact of which was restricted to a given time range; and may prove to be quicker in some circumstances than waiting for the delta to heal via active anti-entropy.

#### repair_keys_range

Available from Riak 3.0.8

Used to prompt read repair in a bucket, to fix an entropy problem within the cluster, potentially limited by key range or modified date range.

- Uses the `riak_kv_reader` queue, and consumption from that queue is constrained by having a single process per node handling queued repairs.
- The reader queue has a small in-memory part but a large on-disk part.  The `reader_overflow_limit` is not configurable via `riak.conf`.
- Uses the AF4 queue when running node worker pools in `dscp` mode.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
