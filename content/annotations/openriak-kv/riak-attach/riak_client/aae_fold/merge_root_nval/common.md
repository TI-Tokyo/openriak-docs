# Metadata

command: erlang:riak_client:aae_fold/1:merge_root_nval
versions: 3.4.0, 3.4.1

# Summary

Merge the cached AAE root for a replication factor.

# Description

Returns `{ok, RootBinary}`. This is a compact comparison value, not a list of objects.

# Notes

The named fields belong inside the query tuple in the order shown by the type declaration. These operations read the AAE store and can impose cluster-wide load.

# Arguments

## NVal

datatype: positive integer
required: true
repeatable: false

### Description

See the shared `NVal` argument on the AAE fold parent page.

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

## erlang-riak-client-aae-fold-merge-root-nval:seed-five-objects

title: Create five objects

### Description

Create five objects to follow the range-query examples. Wait for AAE to include all five before checking counts or applying a range operation.

# Reviewed against

3.4.0: 036d2a93f3084ea182e22d0a303113d8c5b70a3c6fdd3a43d5e3a2ae819dabae
3.4.1: 036d2a93f3084ea182e22d0a303113d8c5b70a3c6fdd3a43d5e3a2ae819dabae
