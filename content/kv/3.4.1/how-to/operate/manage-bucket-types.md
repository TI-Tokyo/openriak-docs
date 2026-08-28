---
title: 'Create and activate bucket types'
description: 'Show operators how to create and activate bucket types with prechecks, verification, and recovery guidance.'
weight: 9
diataxis: 'how-to'
product: 'OpenRiak KV'
product_version: '3.4.1'
status: 'editorially-rewritten'
draft: true
audience:
  - 'operators'
legacy_3_2_5_sources:
  - 'C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\using\cluster-operations\bucket-types.md'
source_material:
  - 'legacy-3.2.5'
  - 'live-3.2.5'
  - 'proposed-kv'
  - 'openriak-quickdocs-3.4'
quickdocs_sources:
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#configuration-of-riak---bucket-properties'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#property---allow_mult'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#property---dvv_enabled'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#property---general-readwrite-parameters'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#property---last_write_wins'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#property---n_val'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#property---node_confirms'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#property---notfound_ok'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#property---pr-and-pw'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#property---small_vclock'
  - 'https://openriak.github.io/riak/InstallAndStartGuide.html#property---sync_on_write'
tags: ['diataxis', 'kv', 'how-to']
editorial_review: 'complete'
technical_review: 'required'
last_reviewed: '2026-08-28'
review_scope: 'editorial-and-site-integration'
---

Show operators how to create and activate bucket types with prechecks, verification, and recovery guidance.

## Before you begin

A healthy cluster, current backups, and access to cluster status and logs. Record the starting state before making an operational change.

## Overview

### Bucket Types

Buckets are essentially a flat namespace in Riak. They allow the same
key name to exist in multiple buckets and enable you to apply
configurations across keys.

**How Many Buckets Can I Have?**
Buckets come with virtually no cost _except for when you modify the default
bucket properties_. Modified bucket properties are gossiped around the cluster
and therefore add to the amount of data sent around the network. In other
words, buckets using the `default` bucket type are free. More on that in the
next section.

In Riak versions 2.0 and later, Basho suggests that you [use bucket types](/kv/3.4.1/how-to/develop/use-bucket-types/) to namespace and configure all buckets you use. Bucket types have a lower overhead within the cluster than the
default bucket namespace but require an additional setup step on the
command line.

#### Creating a Bucket Type

When creating a new bucket type, you can create a bucket type without
any properties and set individual buckets to be indexed. The step below
creates and activates the bucket type:

```bash
riak admin bucket-type create animals '{"props":{}}'
riak admin bucket-type activate animals
```

And this step applies the index to the `cats` bucket, which bears the
`animals` bucket type we just created and activated:

```curl
curl -XPUT $RIAK_HOST/types/animals/buckets/cats/props \
     -H 'Content-Type: application/json' \
     -d '{"props":{"search_index":"famous"}}'
```

Another possibility is to set the `search_index` as a default property
of the bucket type. This means _any_ bucket under that type will
inherit that setting and have its values indexed.

```bash
riak admin bucket-type create animals '{"props":{"search_index":"famous"}}'
riak admin bucket-type activate animals
```

#### Configuration of Riak - Bucket Properties

Riak objects are placed into buckets.  The configuration of the handling of buckets is managed using bucket properties.  There are two types of Buckets in Riak - non-typed buckets, and typed buckets.  Typed buckets were introduced to make it easier to expand the number of buckets that can be supported with non-default properties.  Other than for maintenance of legacy data added prior to typed buckets, typed buckets should always be used.

For help in enabling properties on typed buckets see:

```console
rel/riak/bin/riak admin bucket-type --help
```

The majority of defaults for bucket properties are configurable via `riak.conf`, for example:

- `buckets.default.n_val = 3`
- `buckets.default.merge_strategy = 2`
- `buckets.default.pw = 1`
- `buckets.default.allow_mult = true`

Configuring these defaults will impact only non-typed buckets.  So any bucket name used where no type is specified will inherit these defaults, but any typed bucket created will NOT inherit these configured defaults - typed buckets instead have fixed, pre-defined defaults.

Two pre-defined defaults changed with the introduction of typed buckets (the merge strategy aka `dvv_enabled`, and the `allow_mult` configuration).  Having this delta in behaviour is a common cause of confusion in application developers using Riak, and so it is recommended to configure your clusters to have the same default properties for non-typed buckets as with typed buckets.  This can be achieved by adding to your `riak.conf`:

- `buckets.default.merge_strategy = 2`
- `buckets.default.allow_mult = true`

As any change made to `buckets.default.*` configuration in `riak.conf` is not inherited for typed buckets, there is no way of changing the defaults for typed buckets, so the operator is required to ensure that all default properties are manually set on every type.  For example if you wish to change the default n_val to 5 - this needs to be changed in riak.conf `buckets.default.n_val = 5` but ALSO the property `{n_val, 5}` has to be added on every single bucket type created.

> In general, setting bespoke bucket properties should be done using typed buckets due to the relative efficiency of the implementation with types, but changes to defaults should be considered very carefully.  Bespoke properties allow for bespoke behaviours, but bespoke behaviours add to the cognitive load of future operators.

Default changes made via riak.conf need to be set consistently across a cluster.  No bucket properties are gossipped between clusters, so properties are cluster-specific.  In general any cluster setting related to vector clocks MUST be configured consistently across replicating clusters e.g. `dvv_enabled`, `old_vclock`, `young_vclock`, `big_vclock` and `small_vclock`.  Other properties can be different between clusters.

Some changes can be applied using GET/PUT specific parameters, which will override the default bucket property i.e. a bucket could be configured to use `{sync_on_write, one}`, but a specific PUT can override this by setting `{sync_on_write, all}`.

> Although the use of GET/PUT specific parameters is supported on individual requests, it is not recommended.  Operation-specific parameters that override defaults are not logged, and can increase the operator-challenges associated with troubleshooting intermittent problems.

#### Property - dvv_enabled

In Riak 2.0 the handling of siblings was improved by the enabling of dotted [version vectors](/kv/3.4.1/explanation/data-model/version-vectors-and-siblings/).  All buckets should use `{dvv_enabled, true}`.  The introduction of DVV did not force non-typed buckets to use DVV, and by default non-typed buckets will continue to use legacy vector clocks.

To correct this the following configuration should be added to the `riak.conf`:  `buckets.default.merge_strategy = 2`.

> If vector clock sizes are approaching the `small_vclock` limit, then it is important that `{dvv_enabled, true}` before pruning is applied, or pruning may lead to unexpected siblings.

#### Property - allow_mult

The `allow_mult` bucket property has a default value of `true`, for any typed bucket, but a default value of `false` for any untyped bucket.  It is recommended to use the value of `true`.

The internal workings of Riak are identical for the two `allow_mult` settings, with the exception of the case when an unresolvable conflict is discovered in the object change history.  If `{allow_mult, true}`, all unresolvable conflicting versions are returned to the client to determine the correct version, potentially by merging the conflicting versions.  The client will then resolve existing conflicts on the next PUT. If `{allow_mult, false}` only the object with the most recent last_modified_date is returned, and conflicting versions will be discarded by Riak.

The last_modified_date is a timestamp that depends on the accuracy of the clock on the node that processed the update request.  The timestamp is recorded to a microsecond level, although it is only visible to an accuracy of one second when read via the HTTP Object API.  If conflicting versions of the same object have matching timestamps, then an arbitrary choice is made, although there is a preference for changes with values over deletions.

> Due to the potential use of timestamps to make comparisons when using `{allow_mult, false}`, the use of reliable time sources to co-ordinate time within and across clusters is recommended.

When using [conflict-free replicated data types](/kv/3.4.1/reference/specialized-apis/data-type-api/), `{allow_mult, true}` must always be used.

Unless the non-existence of an object can be guaranteed by the application using Riak, it is recommended that applications always read before writing, and include the vector clock from the read in the write.  This ensures that even when using `{allow_mult, false}`, fallback to time comparison is kept to a minimum.

#### Property - last_write_wins

The `last_write_wins` bucket property has a default value of `false`.  It should only ever be changed when the `allow_mult` bucket property is set to `false`.

In general, the default of `false` should be used, even when `{allow_mult, false}` is set.  Setting `{last_write_wins, true}` changes the vnode-level behaviour on PUT so that an incoming write is assumed to be superior to an existing write, without checking the change history of the existing object.  Internally within Riak, the actual order with which PUTs are applied is non-deterministic, and there are many situations (replication, anti-entropy, handoffs) where old PUTs may be received after new PUTs.  In these cases setting `{last_write_wins, true}` may have unexpected consequences

There is a small performance advantage from setting `{last_write_wins, true}` if, and only if: the bitcask backend is used, and objects are being updated and not simply inserted, and there is no use of TicTac AAE.

> It is recommended that `{last_write_wins, true}` only be used for once-only PUTs (of immutable objects) into the bitcask backend, if and only if, the consequences of out-of-order writes have been fully considered.

#### Property - n_val

The `n_val` bucket property has a default value of `3`, and can be set to any positive integer: though only values of `1`, `3` and `5` are commonly used.

Setting distinct `n_val`s on a per-bucket basis is not recommended, it is preferable to have a consistent `n_val` across a cluster.  This is because:

- related configuration settings `target_n_val` and `target_location_n_val` are cluster-wide and not bucket-specific;
- the scope of the anti-entropy system grows with every unique n_val;
- nextgenrepl full-sync configuration is specific to each n_val, having multiple nvals requires different nodes in the cluster to reconcile for different nvals.

The value of `1` is sometimes used in read-only clusters, to reduce storage costs in clusters used only for backups or offline-reporting.  The value of `5` may sometimes be used in very large clusters in terms of node count; either as the probability of concurrent failures requires higher redundancy, or because there is a need to improve the efficiency of secondary index queries.

> Changing an n_val on a bucket which already contains data will have unexpected and untested consequences, especially when contracting the n_val.

#### Property - node_confirms

The `node_confirms` bucket property has a default value of `0`, and may be set to any non-negative integer less than or equal to the `n_val`.  The purpose of `node_confirms` is to offer a guarantee that the data is available on multiple machines, for example setting node_confirms to 2 will guarantee that at least two machines have the data - and the risk of the data being lost can be considered accordingly.

> By default, a request will be confirmed when the data is in a quorum of vnodes.  However, if multiple nodes have failed in the cluster, the data may still only be on one node. With `node_confirms` the request is only confirmed once the required physical diversity is supported, not just the logical diversity.

The `node_confirms` property is applied on both reads and writes.  The parameter is also applied on reads so that an application can understand on read that a previous put has indeed reached the required level of diversity.  If a `PUT` request fails due to `node_confirms`, a successful `GET` is sufficient to confirm that through eventual consistency the required diversity has been achieved.

#### Property - sync_on_write

Available from Riak 3.0.8

The `sync_on_write` bucket property has a default value of `backend`, and allows for more flexible guarantees about data being flushed to disk.  By default, Riak backends will confirm a PUT once a file write has been completed, but that write may only be resident in memory in the file-system page cache; so at this stage the data is not safe (for example if a power failure simultaneously killed multiple nodes).  Riak backends can be configured to flush all writes to disk, but this has a significant impact on throughput, both in normal operation (each PUT prompts n_val flushes per cluster) and also when managing transfers between nodes.

The `sync_on_write` bucket property can be configured to `backend` (default - revert back to original behaviour, and use only the backend setting), `one` or `all`.  It is assumed when using `sync_on_write` the backend will be configured not to flush to disk on every write.  In this case a write to a bucket with `backend` may be resident in memory on all nodes after the PUT is confirmed to the application client.  If `all` is set, all writes that have been confirmed will also have been flushed (by default 2 of 3 writes must be confirmed before the client receives a positive response).  If `one` is used, the first location to process the PUT will flush to disk, where other locations are allowed to hold it in memory in the file system page cache.

The `sync_on_write` property is used only for PUTs via the API.  Internal PUTs (e.g. for transfers) will ignore the property and use the backend configuration, and so will not carry the overhead of flushing.

It is recommended not to use backend sync configuration, and instead control flushing only through use of this bucket property.

If replicating between clusters and `one` is used as the `sync_on_write` bucket property, then the cluster that receives the PUT from the application will flush to disk on one node - but all clusters receiving the PUT via replication will not be required to flush to disk on any node.  The properties of `backend` or `all` are treated equally in source and sink clusters.

#### Property - small_vclock

The `small_vclock` bucket property has a default value of `50`, and that sets the size of version vectors before pruning will take place. Version vectors will initially tend to be the size of the total of all nvals in all clusters accepting writes for that value (two clusters with n_val of 3 will lead to version vectors of size 6 if objects are subject to sufficient updates).  However, when nodes are replaced, and when clusters are expanded or contracted, new potential vnodes are generated which may lead to the version vector expanding.

It is not recommended to change the `small_vclock`, unless specific problems are seen with objects reaching the pruning limit - and in this case increasing the size may be used as a workaround to those issues.  Any change must be reflected in all connected clusters.

Other vclock settings - `old_vclock`, `young_vclock`, `big_vclock` - should not be changed from defaults without careful analysis of the vclock pruning code.

#### Property - notfound_ok

The `notfound_ok` bucket property has a default value of `true`, and this means when calculating the `r` value of a read, a response from an individual vnode of `not_found` will count as a valid read, and so will count towards quorum being reached.

It is recommended to set `notfound_ok` to `false`, so that a vnode with a missing value will not count towards quorum, especially when the application never expects to read keys that are not present, and so `not_found` is definitively a failure.

#### Property - pr and pw

The `pr` and `pw` bucket properties default to `0`, and are used to require primary vnodes to be involved in reads and writes.  Setting higher values may prevent writing to minority partitions, however when `{n_val, 3}` this will probably lead to intermittent failures when only two nodes fail in a cluster.  As clusters grow the probability of two concurrent failures will increase significantly.

Although configuring `pr`/`pw` to values greater than 1 may be used to indirectly set stronger data reliability guarantees, or to adjust consistency guarantees - there are better ways of achieving this in Riak, which have fewer negative side effects.  Consider using [`node_confirms`](/kv/3.4.1/reference/configuration/bucket-properties/) or [`sync_on_write`](/kv/3.4.1/reference/configuration/bucket-properties/) to manage data reliability.  The use of [token-based conditional PUTs](/kv/3.4.1/reference/http-api/conditional-requests/) is the preferred approach, rather than `pr`/`pw` adjustments for tuning consistency.

> It is normally best practice to configure either `{pr, 1}` or `{notfound_ok, false}`, rather than rely on defaults.

If both `pr` and `notfound_ok` are left at defaults, there is a potential issue when at least two nodes have failed and for some objects 2 of the 3 vnodes are unpopulated fallbacks.  In this case, without changing defaults, the two unpopulated fallback vnodes can return `not_found` and the GET request can achieve quorum and return a false `not_found` to the client.  By configuring either `{pr, 1}` or `{notfound_ok, false}`, when there is only one populated/primary vnode, the GET request must wait for this vnode to respond.

As a consequence though, in the case where there are at least three node failures, and for an unfortunate preflist all three primaries are down - this will then lead to failing requests, though this may be preferable to false `not_found` responses.

#### Property - General read/write parameters

There are read and write parameters that can be used to control the balance between consistency, performance and availability - `r`, `w`, `dw`, `rw`, `basic_quorum`, `sloppy_quorum`.  Read and write parameters default to quorum, and maintaining this default is preferred.  Any attempt to re-configure to improve speed of response to clients, will increase the risk of overloading vnode mailboxes and causing unnecessary failures.

There may be rare circumstances where a cluster is repeatedly suffering `vnode mailbox overload` error responses, because individual vnodes are developing backlog queues larger than their peers in the preflist.  Setting `r` and `w` values to the configured `n_val` can be used as a workaround to temporarily alleviate these scenarios, by slowing the application down to the pace of the slowest vnode.  However, in the long term, the preferred solution to overload scenarios is to address the root cause of these deltas between vnode busyness.

## Verify the result

Compare cluster health and workload behaviour with the recorded starting state, and confirm that all affected nodes have converged.
