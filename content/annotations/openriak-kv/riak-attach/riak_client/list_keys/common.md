# Metadata

command: erlang:riak_client:list_keys/2
versions: 3.4.0, 3.4.1

# Summary

List keys in a bucket.

# Description

This performs a cluster-wide listing and can be expensive on large buckets. Prefer an indexed query when you need a selective lookup.

# Arguments

## Bucket

datatype: binary or pair of binaries
required: true
repeatable: false

### Description

See the shared `Bucket` argument on the parent module page.

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

3.4.0: 72a5956ee60cc2534c557d4581f207551b7938561726e9b1ce061c27ecccd5fe
3.4.1: 72a5956ee60cc2534c557d4581f207551b7938561726e9b1ce061c27ecccd5fe

# Tags

feature: query-processing
repository: riak_kv
module: riak_client
concept: querying
