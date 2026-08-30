---
title: 'Erase keys with AAE fold'
description: 'Show operators how to erase keys with aae fold and interpret the outcome.'
weight: 4
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\erase-keys.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#erase_keys'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to erase keys with aae fold and interpret the outcome.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Erase Keys

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
[filters]: ../../tictac-aae-fold/filters
[filter-by bucket]: ../../tictac-aae-fold/filters#filter-by-bucket-name
[filter-by key-range]: ../{{< product-version-root >}}eference/aae-fold-api/filters/#filter-by-key-range
[filter-by segment]: ../../tictac-aae-fold/filters#filter-by-segment
[filter-by modified]: ../../tictac-aae-fold/filters#filter-by-date-modified
[filter-by sibling-count]: {{< product-version-root >}}how-to/operate/aae-fold/find-keys//#the-sibling-count-filter
[filter-by object-size]: {{< product-version-root >}}how-to/operate/aae-fold/find-keys//#the-object-size-filter

Erases keys that meet the filter parameters.

See the [TicTac AAE `aae_folds`][tictacaae folds-overview] documentation for configuration, tuning and troubleshootings help.

This function allows you to delete many keys in a single pass based on the supplied filters. The Riak keys will be converted to Riak tombstones after which the normal Riak reaping functions take over. Manual dev ops intervention using this function is required.

Use the `erase_keys` function to delete these keys.

#### The `erase_keys` function

Run this using [`riak attach`][riak attach].

This function has three available operational methods that are selected via the `method` value. The `local` method for deleting keys is detailed below. The general format for the function is:

```riakattach
riak_client:aae_fold({
    erase_keys,
    bucket_filter,
    key_range_filter,
    segment_filter
    modified_filter,
    method
    }, Client).
```

Please see the list of [available filters](#available-filters) below.

**Other `method`s**
There are two other `method`s, `count` and `job`:

- `count` is used to count the keys that would have been deleted (see [Count Objects]({{< product-version-root >}}how-to/operate/aae-fold/count-keys/) for more information).
- `job` is used internally by TicTac AAE. Do not use it unless you know what you are doing.

**Note:**
How to get the value for `Client` is detailed in [The Riak Client]({{< product-version-root >}}how-to/operate/aae-fold/#the-riak-client).

#### The `local` method

Deletes keys that meet the filter parameters so that they can then be reaped. Returns the number of keys deleted by calling this function.

```riakattach
riak_client:aae_fold({
    erase_keys,
    bucket_filter,
    key_range_filter,
    segment_filter
    modified_filter,
    local
    }, Client).
```

For example, the following snippet will delete keys with the filters:

- in the bucket "dogs" of bucket type "animals"
- whose keys are between "A" and "N"
- which were modified in January 2022

```riakattach
riak_client:aae_fold({
    erase_keys,
    {<<"animals">>,<<"dogs">>},
    {<<"A">>,<<"N">>},
    all,
    {date,{{2022,1,1},{0,0,0}},{{2022,2,1},{0,0,0}}},
    local
    }, Client).
```

#### The response for the `local` method

The response will look something like this:

```erlang
{ok,5}
```

This indicates that 5 keys were found meeting the filter parameters and were deleted by Riak. Remember that a deleted Riak key is really converted to a Riak tombstone object, and will be actually removed from the backend at a later point based on your `delete_mode` setting.

#### Available filters

These filters are detailed in the [Filters][filters] documentation and can be used to limit the keys considered for deleting.

These filters will reduce the keys to be searched:

- [`bucket_filter`][filter-by bucket]
- [`key_range_filter`][filter-by key-range]
- [`segment_filter`][filter-by segment]

These filters will reduce the number of keys considered for deleting:

- [`modified_filter`][filter-by modified]

#### erase_keys

Prompts for a list of matching keys in the bucket to be erased via the `riak_kv_eraser`, potentially limited by key range or modified date range.

- Uses the `riak_kv_eraser` queue, and consumption from that queue is constrained by having a single process per node handling queued repairs, and by the configuration of the `tombstone_pause` within riak.conf.
- The queue has a small in-memory part but a large on-disk part.  The size of the on-disk component is controlled in `riak.conf` via `eraser_overflow_limit`.
- Uses the AF4 queue when running node worker pools in `dscp` mode.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
