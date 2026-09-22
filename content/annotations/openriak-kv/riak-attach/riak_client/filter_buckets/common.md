# Metadata

command: erlang:riak_client:filter_buckets/2
versions: 3.4.0, 3.4.1

# Summary

List buckets accepted by a predicate.

# Description

The predicate runs during a cluster-wide listing. Restrict this operation to administrative use on appropriately sized data sets.

# Arguments

## Fun

datatype: one-argument Erlang function
required: true
repeatable: false

### Description

Predicate called for each bucket or key. It must return `true` to retain the item and `false` to reject it; for example `fun(_) -> true end`.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Errors

## reference-error-1

### Condition

The operation exceeds its configured timeout.

### Description

The API can return `{error, timeout}`. A timed-out write or delete may still complete on replicas.

### Remedy

Check node availability and load. Read back state before retrying a mutation, and choose an appropriate timeout.

# Reviewed against

3.4.0: ca808f53a928003e36546c11b01a7f8c597086e692c0a7e4ff68a0f7bd9ceccd
3.4.1: ca808f53a928003e36546c11b01a7f8c597086e692c0a7e4ff68a0f7bd9ceccd
