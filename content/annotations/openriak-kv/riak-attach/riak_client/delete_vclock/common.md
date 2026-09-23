# Metadata

command: erlang:riak_client:delete_vclock/4
versions: 3.4.0, 3.4.1

# Summary

Delete an object using its vector clock.

# Description

Read the object first and pass its vector clock to preserve causality when deleting.

# Arguments

## Bucket

datatype: binary or pair of binaries
required: true
repeatable: false

### Description

See the shared `Bucket` argument on the parent module page.

## Key

datatype: binary
required: true
repeatable: false

### Description

See the shared `Key` argument on the parent module page.

## VClock

datatype: vector clock
required: true
repeatable: false

### Description

Vector clock obtained with `riak_object:vclock(Object)`. Supply the clock from the object being deleted.

## Options

datatype: Erlang option list
required: false
repeatable: false
default: []

### Description

Supply a list of quorum and timeout options, for example `[{r, quorum}, {w, quorum}, {dw, quorum}, {timeout, 5000}]`.

- `{r, Value}` and `{pr, Value}` govern the read phase; `{w, Value}`, `{dw, Value}` and `{pw, Value}` govern writing the tombstone.
- `{rw, Value}` is the legacy combined read/write requirement when more specific values are omitted.
- `{timeout, Milliseconds}` bounds the operation; `{recv_timeout, Milliseconds}` bounds the caller’s wait. The explicit Timeout argument is also honored by the longer arity.

Quorum values accept an integer or `one`, `quorum`, `all`, or `default`; `default` uses the bucket policy. Values cannot exceed the effective replication factor. Timeout values are milliseconds.

## RW

datatype: quorum
required: false
repeatable: false

### Description

See the shared `RW` argument on the parent module page.

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

# Examples

## erlang-riak-client-delete-vclock:delete-and-read

### Description

Read the stored value, delete it with replica acknowledgments, then confirm the object is no longer readable. The tombstone remains until reaped.

# Reviewed against

3.4.0: 4bcca26b814942707257b154d1193626904bfc684eecf3f4b881d90a57a3612f
3.4.1: 4bcca26b814942707257b154d1193626904bfc684eecf3f4b881d90a57a3612f

# Tags

feature: deletion
repository: riak_kv
module: riak_client
concept: tombstones
