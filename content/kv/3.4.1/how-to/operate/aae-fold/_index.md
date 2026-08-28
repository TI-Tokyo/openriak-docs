---
title: 'Run TicTac AAE fold operations'
description: 'Introduce operational recipes for inspecting and repairing data with TicTac AAE fold functions.'
weight: 1
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\tictac-aae-fold.md'
source_material:
  - 'legacy-3.2.5'
  - 'source-code-release-notes-3.4'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/OtherAPI.html#aae-fold-api'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Introduce operational recipes for inspecting and repairing data with TicTac AAE fold functions.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### TicTac AAE Folds

[code riak_kv_vnode]: https://github.com/basho/riak_kv/blob/develop-3.0/src/riak_kv_vnode.erl
[riak attach]: ../../admin/riak-cli/#attach
[config reference]: ../../../configuring/reference/#tictac-active-anti-entropy
[config tictacaae]: ../../../configuring/active-anti-entropy/tictac-aae
[tictacaae system]: ../tictac-active-anti-entropy
[tictacaae folds-overview]: ../tictac-aae-fold
[tictacaae client]: ../tictac-aae-fold#the-riak-client
[tictacaae find-keys]: ../tictac-aae-fold/find-keys
[tictacaae find-tombs]: ../tictac-aae-fold/find-tombs
[tictacaae list-buckets]: ../tictac-aae-fold/list-buckets
[tictacaae object-stats]: ../tictac-aae-fold/object-stats
[tictacaae count-tombs]: ../tictac-aae-fold/count-tombs
[tictacaae count-keys]: ../tictac-aae-fold/count-keys
[tictacaae reap-tombs]: ../tictac-aae-fold/reap-tombs
[tictacaae erase-keys]: ../tictac-aae-fold/erase-keys
[tictacaae repair-keys-range]: ../tictac-aae-fold/repair-keys-range
[filters]: ../tictac-aae-fold/filters
[filter-by bucket]: ../tictac-aae-fold/filters#filter-by-bucket-name
[filter-by key-range]: ../tictac-aae-fold/filters#filter-by-key-range
[filter-by segment]: ../tictac-aae-fold/filters#filter-by-segment
[filter-by modified]: ../tictac-aae-fold/filters#filter-by-date-modified
[filter-by sibling-count]: ../tictac-aae-fold/find-keys/#the-sibling-count-filter
[filter-by object-size]: ../tictac-aae-fold/find-keys/#the-object-size-filter

Since OpenRiak KV 2.9.1, the new AAE system, [TicTac AAE][tictacaae system], has added several useful functions that make performing keylisting and tombstone management tasks quicker and more efficient by using TicTacAAE's Merkle trees instead of iterating over the keys in a bucket.

These functions stablisied in OpenRiak KV 2.9.4, and so are not recommended before that version.

#### Configuration settings in `riak.conf`

For more TicTac AAE configuration settings, please see the [TicTac AAE configuration settings][config tictacaae] documentation.

##### TicTacAAE

Turn on TicTacAAE. It works independantly of the legacy AAE system, so can be run in parallel or without the legacy system.

```riak.conf
tictacaae_active = active
```

Note that this will use up more memory and disk space as more metadata is being stored.

##### Storeheads

Turn on TicTacAAE storeheads. This will ensure that TicTacAAE will store more information about each key, including the size, modified date, and tombstone status. Without setting this to `true`, the `aae_fold` functions on this page will not work as expected.

```riak.conf
tictacaae_storeheads = enabled
```

#### Tuning

You can increase the number of simultaneous workers by changing the `af4_worker_pool_size` value in `riak.conf`. The default is `1` per node.

```riak.conf
af4_worker_pool_size = 1
```

#### General usage

Use [Riak attach][riak attach] to run these commands.

The general format for calling `aae_fold` is:

```riakattach
riak_client:aae_fold(
    query,
    Client).
```

`query` is a tuple describing the function to run and the parameters to use. The first value in the tuple is always the function name. For example, if calling the `list_buckets` function the tuple would look like `{list_buckets, ...}`. The number of values in the tuple depends on the function being called.

As an example, this will call `list_buckets`, which takes a single parameter:

```riakattach
riak_client:aae_fold({
    list_buckets,
    3
    }, Client).
```

##### The Riak Client

For these calls to work, you will need a Riak client. This will create one in a reusable variable called `Client`:

```erlang
{ok, Client} = riak:local_client().
```

`Client` can now be used for the rest of the `riak attach` session.

#### Troubleshooting - timeouts

The calls to `aae_fold` are synchronous calls with a 1 hour timeout, but they start an asynchronous process in the background.

If your command takes longer than 1 hour, then you will get `{error,timeout}` as a response after 1 hour. Note that the requested command continues to run in the background, so re-calling the same method will take up more resources.

To timeout you typically have to have a very large number of keys in the bucket.

##### How to check if finished after a timeout

After experiencing a timeout, the current number of commands waiting to execute can be checked by asking for the size of the assured forwarding pool `af4_pool`. Once it reaches 0, there are no more workers as all commands have finished. The size of the pool can checked using this command:

```erlang
{_, _, _, [_, _, _, _, [_, _, {data, [{"StateData", {state, _, _, MM, _, _}}]}]]} =
    sys:get_status(af4_pool),
io:format("af4_pool has ~b workers\n", [length(MM)]),
f().
```

**Warning: existing variables cleared**
`f()` will unbind any existing variables, which may not be your intention. If you remove `f()` then please remember that `MM` will remain bound to the first value. For re-use, you should change the variable name or restart the `riak attach` session.

##### How to avoid timeouts

To reduce the chance of getting a timeout, reduce the number of keys checked by using the [bucket][filter-by bucket] and [key range][filter-by key-range] filters.

The [modified][filter-by modified] filter will not reduce the number of keys checked, and only acts as a filter on the result.

#### Filters

Please see the [TicTac AAE Filters][filters] documentation.

These filters are used by several functions:

- Filter by bucket name - [Learn More >>][filter-by bucket]
  - Without a bucket type
  - With a bucket type
  - All
- Filter by key range - [Learn More >>][filter-by key-range]
  - From -> To
  - All
- Filter by segment - [Learn More >>][filter-by segment]
- Filter by modified date - [Learn More >>][filter-by modified]
  - From -> To
  - All

These filters can only be used with the `find_keys` function:

- Filter by sibling count - [Learn More >>][filter-by sibling-count]
- Filter by object size - [Learn More >>][filter-by object-size]

#### Find keys

Function: `find_keys`

Returns a list of keys that meet the filter parameters.

[Learn More >>][tictacaae find-keys]

#### Find Riak tombstones

Function: `find_tombs`

Returns tuples of bucket name, keyname, and object size of Riak tombstone objects that meet the filter parameters.

[Learn More >>][tictacaae find-tombs]

#### List Buckets

Function: `list_buckets`

Returns a list of all buckets.

[Learn More >>][tictacaae list-buckets]

#### Count keys

Function: `erase_keys` with `count`

Counts the Riak keys that meet the filter parameters.

[Learn More >>][tictacaae count-keys]

#### Count tombstones

Function: `reap_tombs` with `count`

Counts the Riak tombstone objects that meet the filter parameters.

[Learn More >>][tictacaae count-tombs]

#### Get object statistics

Function: `object_stats`

Returns a count of Riak objects that meet the filter parameters.

[Learn More >>][tictacaae object-stats]

#### Erase keys

Function: `erase_keys` with `local`

Deletes Riak keys that meet the filter parameters.

[Learn More >>][tictacaae erase-keys]

#### Reap tombstones

Function: `reap_tombs` with `local`

Reaps the Riak tombstone objects that meet the filter parameters.

[Learn More >>][tictacaae reap-tombs]

#### Repair keys

Function: `repair_keys_range`

Performs a read-repair on the keys that meet the filter parameters.

[Learn More >>][tictacaae repair-keys-range]

#### Other functions not covered

`aae_fold` has various other functions that can be called, but are mostly for internal use by Riak. These functions should not be used without a good understanding of the source code, but are listed here for reference:

- `fetch_clocks_nval`
- `fetch_clocks_range`
- `merge_branch_nval`
- `merge_root_nval`
- `merge_tree_range`
- `repl_keys_range`

#### AAE Fold API

The AAE Fold API requires the configuration of `tictacaae_active = active`, otherwise folds will fail.  When using a single leveled backend, this should use the native keystore within leveled.

When using any other backend or multi-backend this will require an additional parallel keystore, which may have an impact on the achievable PUT throughput, and the memory used by Riak.  The use of a parallel backend also requires periodic keystore rebuilds, to ensure that the keystore correctly represents the content in the backend store.

> When using parallel mode, the parallel store must be configured with `tictacaae_storeheads = enabled` to use the full functionality of AAE Folds.

The AAE Fold API:

- Supports [more than ten different fold types]({{< baseurl >}}kv/3.4.1/reference/aae-fold-api/);
- [Are throttled to minimise the impact on other cluster operations, and have query options that may improve efficiency]({{< baseurl >}}kv/3.4.1/reference/aae-fold-api/).

The AAE Fold API has four potential interfaces:

- [AAE Folds via the Command Line]({{< baseurl >}}kv/3.4.1/how-to/operate/aae-fold/run-from-command-line/);
- [AAE Folds via remote_console]({{< baseurl >}}kv/3.4.1/how-to/operate/use-remote-console/);
- [AAE Folds via HTTP]({{< baseurl >}}kv/3.4.1/reference/aae-fold-api/);
- [AAE Folds via protocol buffers]({{< baseurl >}}kv/3.4.1/reference/aae-fold-api/).

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.

## In this section

- [Count keys with AAE fold]({{< baseurl >}}kv/3.4.1/how-to/operate/aae-fold/count-keys/) — Show operators how to count keys with aae fold and interpret the outcome.
- [Count tombstones with AAE fold]({{< baseurl >}}kv/3.4.1/how-to/operate/aae-fold/count-tombstones/) — Show operators how to count tombstones with aae fold and interpret the outcome.
- [Erase keys with AAE fold]({{< baseurl >}}kv/3.4.1/how-to/operate/aae-fold/erase-keys/) — Show operators how to erase keys with aae fold and interpret the outcome.
- [Find keys with AAE fold]({{< baseurl >}}kv/3.4.1/how-to/operate/aae-fold/find-keys/) — Show operators how to find keys with aae fold and interpret the outcome.
- [Find tombstones with AAE fold]({{< baseurl >}}kv/3.4.1/how-to/operate/aae-fold/find-tombstones/) — Show operators how to find tombstones with aae fold and interpret the outcome.
- [List buckets with AAE fold]({{< baseurl >}}kv/3.4.1/how-to/operate/aae-fold/list-buckets/) — Show operators how to list buckets with aae fold and interpret the outcome.
- [Collect object statistics with AAE fold]({{< baseurl >}}kv/3.4.1/how-to/operate/aae-fold/object-statistics/) — Show operators how to collect object statistics with aae fold and interpret the outcome.
- [Reap tombstones with AAE fold]({{< baseurl >}}kv/3.4.1/how-to/operate/aae-fold/reap-tombstones/) — Show operators how to reap tombstones with aae fold and interpret the outcome.
- [Repair a key range with AAE fold]({{< baseurl >}}kv/3.4.1/how-to/operate/aae-fold/repair-key-range/) — Show operators how to repair a key range with aae fold and interpret the outcome.
- [Run an AAE fold from the command line]({{< baseurl >}}kv/3.4.1/how-to/operate/aae-fold/run-from-command-line/) — Show operators how to start a long-running AAE fold and write its completed results to disk.
