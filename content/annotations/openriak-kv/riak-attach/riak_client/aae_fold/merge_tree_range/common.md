# Metadata

command: erlang:riak_client:aae_fold/1:merge_tree_range
versions: 3.4.0, 3.4.1

# Summary

Build a merged AAE tree over a bucket range.

# Description

Returns a merged tree for comparing data over the selected key, segment and modification-time range.

# Notes

The named fields belong inside the query tuple in the order shown by the type declaration. These operations read the AAE store and can impose cluster-wide load.

# Arguments

## Bucket

datatype: bucket binary or typed bucket
required: true
repeatable: false

### Description

See the shared `Bucket` argument on the parent module page.

## KeyRange

datatype: all or binary key bounds
required: true
repeatable: false

### Description

See the shared `KeyRange` argument on the AAE fold parent page.

## TreeSize

datatype: tree size atom
required: true
repeatable: false

### Valid values

- xxsmall
- xsmall
- small
- medium
- large
- xlarge

### Description

Size of the merged tree.

## SegmentFilter

datatype: all or segment tuple
required: true
repeatable: false

### Description

See the shared `SegmentFilter` argument on the AAE fold parent page.

## ModifiedRange

datatype: all or date tuple
required: true
repeatable: false

### Description

See the shared `ModifiedRange` argument on the AAE fold parent page.

## HashMethod

datatype: hash method
required: true
repeatable: false

### Description

Use `pre_hash` to reuse stored hashes or `{rehash, Seed}` to calculate hashes with the supplied integer seed.

## Client

datatype: riak_client handle
required: false
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Errors

## reference-error-1

### Condition

The cluster-wide fold does not finish within its timeout.

### Description

The API can return `{error, timeout}` or another error term from its coverage workers.

### Remedy

Check node availability, AAE state and filter size. Reduce the range before retrying a costly operation.

# Examples

## erlang-riak-client-aae-fold-merge-tree-range:seed-five-objects

title: Create five objects

### Description

Create five objects to follow the range-query examples. Wait for AAE to include all five before checking counts or applying a range operation.

## erlang-riak-client-aae-fold-merge-tree-range:populated-aae

### Description

Inspect the range tree to compare AAE data for five stored objects. Expect a populated tree; its binary values depend on the node and object metadata.

# Reviewed against

3.4.0: e003112ba2d812bd8d82c74cd9f57d96143712385df4631561c4a25665a522cf
3.4.1: e003112ba2d812bd8d82c74cd9f57d96143712385df4631561c4a25665a522cf

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_client
concept: compaction, replica-repair
