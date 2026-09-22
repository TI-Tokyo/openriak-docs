# Metadata

command: erlang:riak_client:aae_fold/1:find_tombs
versions: 3.4.0, 3.4.1

# Summary

Find tombstones within a bucket range.

# Description

Returns tombstones matching the key, segment and modification-time filters.

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

## erlang-riak-client-aae-fold-find-tombs:seed-five-objects

title: Create five objects

### Description

Create five objects to follow the range-query examples. Wait for AAE to include all five before checking counts or applying a range operation.

## erlang-riak-client-aae-fold-find-tombs:delete-fixture

### Description

Delete the five objects to inspect the tombstones left by deletion. Expect five deletion markers until they are reaped.

## erlang-riak-client-aae-fold-find-tombs:find-five

### Description

Count the returned entries; the selected key range contains exactly five matches.

# Reviewed against

3.4.0: 0343faf6dc6a6c554cabcf155c4ff0d507959bd62230531d634be9e091ab2728
3.4.1: 0343faf6dc6a6c554cabcf155c4ff0d507959bd62230531d634be9e091ab2728
