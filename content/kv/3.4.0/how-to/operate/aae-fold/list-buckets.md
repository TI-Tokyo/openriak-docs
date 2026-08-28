---
title: 'List buckets with AAE fold'
description: 'Show operators how to list buckets with aae fold and interpret the outcome.'
weight: 7
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.0'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold\list-buckets.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#list_buckets'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to list buckets with aae fold and interpret the outcome.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### List Buckets

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

Returns a list of bucket names stored in Riak.

See the [TicTac AAE `aae_folds`][tictacaae folds-overview] documentation for configuration, tuning and troubleshootings help.

#### The `list_buckets` function

Run this using [`riak attach`][riak attach].

```riakattach
riak_client:aae_fold({
    list_buckets,
    assumed_nval
    }, Client).
```
There are no available filters for this method.

`assumed_nval` should ideally be set to your cluster's default nval, but can be safely set to `1` for this purpose. Do not set it to below `1` or above your highest nval.

This will list all buckets:

```riakattach
riak_client:aae_fold({
    list_buckets,
    3
    }, Client).
```

**Note:**
How to get the value for `Client` is detailed in [The Riak Client](../../tictac-aae-fold#the-riak-client).

#### The response

The response will be an array of bucket names, or tuples of bucket types and bucket names, as Erlang binaries. It looks something like this:

```erlang
{ok,[{<<"animals">>,<<"dogs">>},
     <<"cars">>]}
```

This shows that there are two buckets:

- "dogs" of bucket type "animals"
- "cars" with no bucket type

#### list_buckets

Returns a list of buckets, assuming the given n_val.

- The list may be incomplete if the passed n_val is greater than the configured n_val of some buckets.
- will only return buckets that contain objects.
- Uses a skipping cursor in both `native` and the `leveled_ko` type of parallel store, so that the fold is much more efficient than folding over all keys.
- Uses the AF4 queue when running node worker pools in `dscp` mode.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
