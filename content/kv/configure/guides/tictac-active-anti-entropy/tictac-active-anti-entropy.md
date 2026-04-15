---
sidebar_position: 201
title: TicTac Active Anti-Entropy
sidebar_label: TicTac Active Anti-Entropy
sidebar_custom_props:
  icon: settings
pagination_label: Tictac AAE guide
sidebar_class_name: kv-configure-guides-tictac-active-anti-entropy
---
[root site]: [!site]
[root project]: [!project]
[root version]: [!version]
[enableTTAAE]: #enabling-tictac-active-anti-entropy
[enablestoreheads]: #enable-aae-storeheads
[generalusage]: #general-usage-and-interacting-with-the-riak-client
[troubletime]: #troubleshooting---timeouts
[foldfunctions]: #fold-functions

> [!MEMO]Overview
> TicTac Active Anti-Entropy makes two changes to the way Anti-Entropy has previously worked in Riak. The first change is to the way Merkle Trees are contructed so that they are built incrementally. The second change allows the underlying Anti-entropy key store to be key-ordered while still allowing faster access to keys via 
their Merkle tree location or the last modified date of the object.

Since Riak KV 2.9.1, the new AAE system, TicTac AAE, has added several useful functions that make performing keylisting and tombstone management tasks quicker and more efficient by using TicTacAAE’s Merkle trees instead of iterating over the keys in a bucket. These features were considered stable from V 2.9.4 onwards and should not be used in older versions.


## Enabling TicTac Active Anti-Entropy

>[!NOTE] Note on using Tic Tac AAE concurrently with Legacy AA
>TicTac AAE is independent of the Legacy AAE system, using none of the same systems and so it can be run in parallel or without the legacy AAE system.

To enable TicTac AAE, you need to change the value of the following line in your `riak.conf` file to `active`:

  ```bash
    tictacaae_active = active
  ```

Please note that the use of TicTac AAE will result in increased memory and disk utilisation as more metadata needs to be stored for TicTac AAE to function. It is recommend that you ensure your system has sufficient resources for this and run the appropriate testing in a non-production environment before enabling in live systems.

### Enable AAE storeheads

We recommend that TicTac AAE storeheads is also enabled as this will allow OpenRiak to store more metadata for each key, including the size, last modified date and the tombstone status. If storeheads is NOT enabled, the `aae_fold` function will not work as expected.
To enable storeheads, set the following value in your `riak.conf` file:

  ```bash
    tictacaae_storeheads = enabled
  ```

Please note that the use of AAE storeheads will result in increased memory and disk utilisation as more metadata will be stored. It is recommend that you ensure your system has sufficient resources for this and run the appropriate testing in a non-production environment before enabling in live systems.

## General usage and interacting with the Riak Client

### The Riak Client

For any of the calls in this guide to work, you need a Riak client. The following will create one in a reusable variable called `Client`:

  ```bash
    {ok, Client} = riak:local_client().
  ```

This allows `Client` to be used for the rest of the `riak attach` session:

### General usage

The general format for calling `aae_fold` is:

  ```bash
    riak_client:aae_fold(
        query,
        Client).
  ```

`query` is a tuple describing the function to run and the parameters to use. The first value in the tuple is always the function name. For example, if calling the `list_buckets` function the tuple would look like `{list_buckets, ...}`. The number of values in the tuple depends on the function being called.

As an example, this will call `list_buckets`, which takes a single parameter:

  ```bash
    riak_client:aae_fold({
      list_buckets,
      3
      }, Client).
  ```

## Troubleshooting - timeouts

`aae_fold` calls are synchronous calls, with a 1 hour timeout, but they start an asynchronous process in the background. If the required operation takes longer than the 1 hour default timeout then you will get an `{error,timeout}` response after the 1 hour period. 
The background process continues to run however, so calling the same method repeatedly will consume more resources. To hit the timeout, you will typically have had a very large number of keys in the bucket.

### Checking if process is finished after a timeout

Commands waiting to execute are stored in the assured forwarding pool `af4_pool`, so after experiencing a timeout, you can check the size of this pool to confirm whether your command(s) have finished or not. if the number of workers has reached 0, then all previous commands have finished. This can be checked with the following:

  ```bash
    {_, _, _, [_, _, _, _, [_, _, {data, [{"StateData", {state, _, _, MM, _, _}}]}]]} =
      sys:get_status(af4_pool),
    io:format("af4_pool has ~b workers\n", [length(MM)]),
    f().
  ```

>[!NOTE]Note on existing variables being cleared
>`f()` will unbind any existing variables, which may not be your intention. If you remove `f()` then please remember that `MM` will remain bound to the first value. For re-use, you should change the variable name or restart the `riak attach` session.

### Avoiding timeouts

To reduce the chances of getting a timeout, reduce the number of keys checked by using the bucket and key range filters 

The modified filter will not reduce the number of keys checked, and only acts as a filter on the result.

## Fold Functions

This section lists the different functions supported in `aae_fold`

### Find keys

Function: `find_keys`

Returns a list of keys that meet the filter parameters.

You can read more [here](./find-keys.md)

### Find OpenRiak Tombstones

Function: `find_tombs`

Returns tuples of bucket name, keyname, and object size of Riak tombstone objects that meet the filter parameters.

You can read more [here](./find-tombstones.md)

### List Buckets

Function: `list_buckets`

Returns a list of all buckets.

You can read more [here](./list-buckets.md)

### Count Keys

Function: `erase_keys` with `count`

Counts the Riak keys that meet the filter parameters.

You can read more [here](./count-keys.md)

### Count Tombstones

Function: `reap_tombs` with `count`

Counts the Riak tombstone objects that meet the filter parameters.

You can read more [here](./count-tombstones.md)

### Get object statistics

Function: `object_stats`

Returns a count of OpenRiak objects that meet the filter parameters.

You can read more [here](./object-statistics.md)

### Erase Keys

Function: `erase_keys` with `local`

Deletes OpenRiak keys that meet the filter parameters.

You can read more [here](./erase-keys.md)

### Reap Tombstones

Function: `reap_tombs` with `local`

Reaps the Riak tombstone objects that meet the filter parameters.

You can read more [here](./reap-tombs.md)

### Repair keys

Function: `repair_keys_range`

Performs a read-repair on the keys that meet the filter parameters.

You can read more [here](./repair-keys.md)

### Other functions
