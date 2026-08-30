---
title: 'Count tombstones with AAE fold'
description: 'Show operators how to count tombstones with aae fold and interpret the outcome.'
weight: 3
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\count-tombs.md'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to count tombstones with aae fold and interpret the outcome.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Count Tombstones

[code riak_kv_vnode]: https://github.com/basho/riak_kv/blob/develop-3.0/src/riak_kv_vnode.erl
[riak attach]: ../{{< product-version-root >}}eference/commands/riak/#attach
[config reference]: {{< product-version-root >}}reference/configuration/#tictac-active-anti-entropy
[config tictacaae]: ../../../configuring/active-anti-entropy/tictac-aae
[tictacaae folds-overview]: ../
[tictacaae system]: ../../tictac-active-anti-entropy
[tictacaae client]: {{< product-version-root >}}how-to/operate/aae-fold/#the-riak-client
[tictacaae find-keys]: {{< product-version-root >}}how-to/operate/aae-fold/find-keys/
[tictacaae find-tombs]: ../../tictac-aae-fold/find-tombs
[tictacaae list-buckets]: ../../tictac-aae-fold/list-buckets
[tictacaae object-stats]: {{< product-version-root >}}how-to/operate/aae-fold/object-statistics/
[tictacaae reap-tombs]: {{< product-version-root >}}how-to/operate/aae-fold/reap-tombstones/
[tictacaae count-tombs]: {{< product-version-root >}}how-to/operate/aae-fold/count-tombstones/
[filters]: ../../tictac-aae-fold/filters
[filter-by bucket]: ../../tictac-aae-fold/filters#filter-by-bucket-name
[filter-by key-range]: ../{{< product-version-root >}}eference/aae-fold-api/filters/#filter-by-key-range
[filter-by segment]: ../../tictac-aae-fold/filters#filter-by-segment
[filter-by modified]: ../../tictac-aae-fold/filters#filter-by-date-modified
[filter-by sibling-count]: {{< product-version-root >}}how-to/operate/aae-fold/find-keys//#the-sibling-count-filter
[filter-by object-size]: {{< product-version-root >}}how-to/operate/aae-fold/find-keys//#the-object-size-filter

Counts the Riak tombstone objects that meet the filter parameters.

See the [TicTac AAE `aae_folds`][tictacaae folds-overview] documentation for configuration, tuning and troubleshootings help.

Unreaped Riak tombstones are Riak objects that have been deleted, but have not been removed from the backend. Riak tracks this through tombstones. If automatic reaping is turned off (for example, by setting `delete_mode` = `keep`), then a large number of deleted objects can accumulate that Riak will never automatically remove. Manual dev ops intervention using this function is required.

Use the `reap_tombs` function to count these objects.

#### The `reap_tombs` function

Run this using [`riak attach`][riak attach].

This function has three available operational methods that are selected via the `method` value. The `count` method for counting tombstones is detailed below. The general format for the function is:

```riakattach
riak_client:aae_fold({
    reap_tombs,
    bucket_filter,
    key_range_filter,
    segment_filter
    modified_filter,
    method
    }, Client).
```

Please see the list of [available filters](#available-filters) below.

**Other `method`s**
There are two other `method`s, `local` and `job`:

- `local` is used to actually reap the tombstones (see [Reap Tombstones]({{< product-version-root >}}how-to/operate/aae-fold/reap-tombstones/) for more information).
- `job` is used internally by TicTac AAE. Do not use it unless you know what you are doing.

**Note:**
How to get the value for `Client` is detailed in [The Riak Client]({{< product-version-root >}}how-to/operate/aae-fold/#the-riak-client).

#### The `count` method

Returns a count of tombstones that meet the filter parameters. Does NOT reap the tombstones.

```riakattach
riak_client:aae_fold({
    reap_tombs,
    bucket_filter,
    key_range_filter,
    segment_filter
    modified_filter,
    count
    }, Client).
```

For example, the following snippet will count all tombstones with the filters:

- in the bucket "dogs" of bucket type "animals"
- whose keys are between "A" and "N"
- which were modified in January 2022

```riakattach
riak_client:aae_fold({
    reap_tombs,
    {<<"animals">>,<<"dogs">>},
    {<<"A">>,<<"N">>},
    all,
    {date,{{2022,1,1},{0,0,0}},{{2022,2,1},{0,0,0}}},
    count
    }, Client).
```

#### The response for the `count` method

The response will look something like this:

```erlang
{ok,5}
```

This indicates that 5 tombstones were found meeting the filter parameters.

#### Available filters

These filters are detailed in the [Filters][filters] documentation and can be used to limit the keys considered for reaping or counting.

These filters will reduce the keys to be searched:

- [`bucket_filter`][filter-by bucket]
- [`key_range_filter`][filter-by key-range]
- [`segment_filter`][filter-by segment]

These filters will reduce the number of keys considered for reaping or counting:

- [`modified_filter`][filter-by modified]

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
