---
title: 'Find keys with AAE fold'
description: 'Show operators how to find keys with aae fold and interpret the outcome.'
weight: 5
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\find-keys.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#find_keys'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to find keys with aae fold and interpret the outcome.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Find keys

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

Returns a list of keys that meet the filter parameters.

See the [TicTac AAE `aae_folds`][tictacaae folds-overview] documentation for configuration, tuning and troubleshootings help.

#### The `find_keys` function

Run this using [`riak attach`][riak attach].

This function will find all keys that meet the common filters as well as one of two function-specific filters (`function_filter`) that filter by minimum sibling count or by minimum object size (but not both at the same time).

```riakattach
riak_client:aae_fold({
    find_keys,
    bucket_filter,
    key_range_filter,
    modified_filter,
    function_filter
    }, Client).
```

Please see the list of [available standard filters](#available-standard-filters) below.

`function_filter` can be either the `sibling_count` filter or the `object_size` filter, detailed below.

#### The `sibling_count` filter

This filter will only include keys that have more than the specified siblings.

Note that a value of `5` will mean only objects with 6 or more siblings will be returned.

```riakattach
riak_client:aae_fold({
    find_keys,
    bucket_filter,
    key_range_filter,
    modified_filter,
    {sibling_count, count}
    }, Client).
```

For example, the following snippet will return all keys with the filters:

- in the bucket "dogs" of bucket type "animals"
- whose keys are between "A" and "N"
- which were modified in January 2022
- which have more than 5 siblings

```riakattach
riak_client:aae_fold({
    find_keys,
    {<<"animals">>,<<"dogs">>},
    {<<"A">>,<<"N">>},
    {date,{{2022,1,1},{0,0,0}},{{2022,2,1},{0,0,0}}},
    {sibling_count, 5}
    }, Client).
```

**Note:**
How to get the value for `Client` is detailed in [The Riak Client](../../tictac-aae-fold#the-riak-client).

#### The response using the `sibling_count` filter

The response will be an array of `{bucket_name,key_name,sibling_count}` tuples that will look something like this:

```erlang
{ok,[{{<<"animals">>,<<"dogs">>},<<"Barkie">>,15},
    {{<<"animals">>,<<"dogs">>},<<"Lord Snuffles III">>,6}]}
```

This indicates that two objects were found with more than 5 siblings:

- "Barkie" in the bucket "dogs" of bucket type "animals" has 15 siblings
- "Lord Snuffles III" in the bucket "dogs" of bucket type "animals" has 6 siblings

For each object found, an additional `{bucket_name,key_name,sibling_count}` tuple will be added to the array.

Field | Example | Description
:-------|:--------|:--------
bucket_name | `<<"cars">>` or `{<<"animals">>,<<"dogs">>}` | The bucket name as an Erlang binary. In the case of a bucket with a bucket type, a tuple of bucket type and bucket name.
key_name | `<<"Barkie">>` | The key name as an Erlang binary.
sibling_count | 15 | The number of siblings of the object.

#### The `object_size` filter

This filter will include keys that have an object size of more than the specified size.

Note that a value of `1000` will mean only objects with a size of 1001 bytes or more will be returned.

```riakattach
riak_client:aae_fold({
    find_keys,
    bucket_filter,
    key_range_filter,
    modified_filter,
    {object_size, size}
    }, Client).
```

- in the bucket "dogs" of bucket type "animals"
- whose keys are between "A" and "N"
- which were modified in January 2022
- which are more than 1000 bytes in size

```riakattach
riak_client:aae_fold({
    find_keys,
    {<<"animals">>,<<"dogs">>},
    {<<"A">>,<<"N">>},
    {date,{{2022,1,1},{0,0,0}},{{2022,2,1},{0,0,0}}},
    {object_size, 1000}
    }, Client).
```

#### The response using the `object_size` filter

The response will be an array of `{bucket_name,key_name,object_size}` tuples that will look something like this:

```erlang
{ok,[{{<<"animals">>,<<"dogs">>},<<"Barkie">>,5000},
    {{<<"animals">>,<<"dogs">>},<<"Lord Snuffles III">>,10550400}]}
```

- "Barkie" in the bucket "dogs" of bucket type "animals" has a size of 5000 bytes
- "Lord Snuffles III" in the bucket "dogs" of bucket type "animals" has a size of 10,550,400 bytes

For each object found, an additional `{bucket_name,key_name,object_size}` tuple will be added to the array.

Field | Example | Description
:-------|:--------|:--------
bucket_name | `<<"cars">>` or `{<<"animals">>,<<"dogs">>}` | The bucket name as an Erlang binary. In the case of a bucket with a bucket type, a tuple of bucket type and bucket name.
key_name | `<<"Barkie">>` | The key name as an Erlang binary.
object_size | 5000 | The size of the object.

#### Available standard filters

These filters are detailed in the [Filters][filters] documentation and can be used to limit the keys counted.

These filters will reduce the keys to be searched:

- [`bucket_filter`][filter-by bucket]
- [`key_range_filter`][filter-by key-range]

These filters will reduce the number of objects included in the statistics:

- [`modified_filter`][filter-by modified]

#### find_keys

Outputs a list of keys in the bucket where the object has either a sibling_count or a size (in bytes) that exceeds a certain threshold, potentially limited by key range or modified date range.

- Commonly used as an operational query (e.g. "find all objects modified in the past 24 hours with more than one sibling").
- May also be used to list keys, where using a `$key` query is not supported.  It is much slower (but potentially safer) than `$key` query due to the constraints of the [node_worker_pools]({{< baseurl >}}kv/3.4.0/how-to/operate/monitor-worker-pools/).
- Uses the AF4 queue when running node worker pools in `dscp` mode.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
