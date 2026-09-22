# Metadata

command: erlang:riak_client:list_buckets/1
versions: 3.4.0, 3.4.1

# Summary

List buckets that contain keys.

# Description

This performs a cluster-wide listing and can be expensive. Bucket presence is updated asynchronously; a just-written bucket may not appear immediately.

# Arguments

## Filter

datatype: filter expression
required: false
repeatable: false

### Description

Bucket/key filter used by the selected arity. Use `none` where the implementation accepts no filtering; predicate-based filtering uses `fun(Item) -> boolean() end`.

## Timeout

datatype: timeout in milliseconds
required: false
repeatable: false

### Description

See the shared `Timeout` argument on the parent module page.

## Type

datatype: binary
required: false
repeatable: false

### Description

Bucket type as a binary, for example `<<"default">>`. It must exist and be active.

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

3.4.0: 04c5396b0fb616c3e1644b3878569555a632c588ebd177e5fd94ca588761b53e
3.4.1: 04c5396b0fb616c3e1644b3878569555a632c588ebd177e5fd94ca588761b53e
