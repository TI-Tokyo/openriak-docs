# Metadata

command: erlang:riak_client:filter_keys/3
versions: 3.4.0, 3.4.1

# Summary

List bucket keys accepted by a predicate.

# Description

The predicate runs at the vnodes and receives each key. This still scans the bucket’s keys.

# Arguments

## Bucket

datatype: binary or pair of binaries
required: true
repeatable: false

### Description

See the shared `Bucket` argument on the parent module page.

## Fun

datatype: one-argument Erlang function
required: true
repeatable: false

### Description

Predicate called for each bucket or key. It must return `true` to retain the item and `false` to reject it; for example `fun(_) -> true end`.

## Timeout

datatype: timeout in milliseconds
required: false
repeatable: false

### Description

See the shared `Timeout` argument on the parent module page.

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

3.4.0: 49586eccad572470adee4e1baf3a29185598ba761e5057a8b8ee8e302527a5c4
3.4.1: 49586eccad572470adee4e1baf3a29185598ba761e5057a8b8ee8e302527a5c4
