# Metadata

command: erlang:riak_client:aae_fold/1:fetch_clocks_nval
versions: 3.4.0, 3.4.1

# Summary

Fetch clocks for selected cached-tree segments.

# Description

Returns bucket/key/vector-clock entries for the requested segments. The longer tuple additionally restricts modification time.

# Notes

The named fields belong inside the query tuple in the order shown by the type declaration. These operations read the AAE store and can impose cluster-wide load.

# Arguments

## NVal

datatype: positive integer
required: true
repeatable: false

### Description

See the shared `NVal` argument on the AAE fold parent page.

## Segments

datatype: list of non-negative integers
required: true
repeatable: false

### Description

List of segment IDs, for example `[0]`.

## ModifiedRange

datatype: all or date tuple
required: false
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

## erlang-riak-client-aae-fold-fetch-clocks-nval:seed-five-objects

title: Create five objects

### Description

Create five objects to follow the range-query examples. Wait for AAE to include all five before checking counts or applying a range operation.

## erlang-riak-client-aae-fold-fetch-clocks-nval:populated-aae

### Description

Compute the cached-tree segments for the five stored keys and verify five clocks are returned.

# Reviewed against

3.4.0: ca8993333e6d1a9c9e66a9408d33dcd65ebac15c08e69861e81d6b805716cdb9
3.4.1: ca8993333e6d1a9c9e66a9408d33dcd65ebac15c08e69861e81d6b805716cdb9
