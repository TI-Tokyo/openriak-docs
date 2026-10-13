# Metadata

command: erlang:riak_client:aae_fold/1:list_buckets
versions: 3.4.0, 3.4.1

# Summary

List buckets recorded in the AAE store.

# Description

Returns `{ok, Buckets}` for the selected replication factor.

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

## erlang-riak-client-aae-fold-list-buckets:seed-five-objects

title: Create five objects

### Description

Create five objects to follow the range-query examples. Wait for AAE to include all five before checking counts or applying a range operation.

# Reviewed against

3.4.0: 75d8b57bac2951ed55cd1b7a00e474f77ccc07b5eb0dbf224f4508935a225cae
3.4.1: 75d8b57bac2951ed55cd1b7a00e474f77ccc07b5eb0dbf224f4508935a225cae

# Tags

feature: tictac-aae
repository: riak_kv
module: riak_client
concept: replica-repair
