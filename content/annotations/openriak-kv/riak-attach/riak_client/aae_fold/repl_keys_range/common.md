# Metadata

command: erlang:riak_client:aae_fold/1:repl_keys_range
versions: 3.4.0, 3.4.1

# Summary

Queue keys from a bucket range for replication.

# Description

Matching entries are added to the named source queue. Queueing is not confirmation that the destination has stored the objects.

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

## ModifiedRange

datatype: all or date tuple
required: true
repeatable: false

### Description

See the shared `ModifiedRange` argument on the AAE fold parent page.

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

Registered source queue name, for example `cli_reference`.

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

## erlang-riak-client-aae-fold-repl-keys-range:seed-five-objects

title: Create five objects

### Description

Create five objects to follow the range-query examples. Wait for AAE to include all five before checking counts or applying a range operation.

## erlang-riak-client-aae-fold-repl-keys-range:queue-five

### Description

Queue the five matching objects for replication. Expect five AAE entries in the source queue; check the destination separately to confirm delivery.

# Reviewed against

3.4.0: 982a933dfb9bd813be2e50379f4af5395dca3ba7d496e70eb42868a806733d6c
3.4.1: 982a933dfb9bd813be2e50379f4af5395dca3ba7d496e70eb42868a806733d6c

# Tags

feature: queue-replication
repository: riak_kv
module: riak_client
concept: cross-cluster-replication
