# Metadata

command: erlang:riak_client:aae_fold/1:fetch_clocks_range
versions: 3.4.0, 3.4.1

# Summary

Fetch object clocks within a bucket range.

# Description

Returns matching bucket/key/vector-clock entries.

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

## erlang-riak-client-aae-fold-fetch-clocks-range:seed-five-objects

title: Create five objects

### Description

Create five objects to follow the range-query examples. Wait for AAE to include all five before checking counts or applying a range operation.

## erlang-riak-client-aae-fold-fetch-clocks-range:find-five

### Description

Count the returned entries; the selected key range contains exactly five matches.

# Reviewed against

3.4.0: 89a9e70dc7dd7778f95a808dacf702b3042b112b5f530556bcc3a74ac278dad1
3.4.1: 89a9e70dc7dd7778f95a808dacf702b3042b112b5f530556bcc3a74ac278dad1

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_client
concept: replica-repair
