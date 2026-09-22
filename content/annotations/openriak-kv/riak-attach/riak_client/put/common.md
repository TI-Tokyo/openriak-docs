# Metadata

command: erlang:riak_client:put/2
versions: 3.4.0, 3.4.1

# Summary

Store or update a Riak object.

# Description

Construct a new object for a new key. For updates, read the existing object and modify it with riak_object accessors so its causal context is retained.

# Arguments

## RObj

datatype: riak_object record
required: true
repeatable: false

### Description

Object constructed with `riak_object:new/3`, or an object returned by a read and updated with riak_object accessors. Preserve its vector clock when updating existing data.

## Options

datatype: Erlang option list
required: false
repeatable: false
default: []

### Description

Supply an Erlang list, for example `[returnbody, {w, quorum}, {dw, quorum}, {timeout, 5000}]`.

- `{w, Value}` requires that many write acknowledgments; `{dw, Value}` requires durable acknowledgments; `{pw, Value}` requires primary owners.
- `returnbody` includes the stored object in the result. Without it, a successful ordinary write returns `ok`.
- `{timeout, Milliseconds}` bounds the request. `{recv_timeout, Milliseconds}` separately bounds the caller’s wait; if omitted, the caller allows the request timeout plus 100 milliseconds.
- `{details, true}` or `{details, [timing]}` adds diagnostic details to the result; `false` omits them.
- `{sloppy_quorum, true | false}` controls fallback replicas. `{n_val, PositiveInteger}` overrides the replication factor for this request; use it consistently with the bucket’s data placement.
- `{sync_on_write, backend | one | all}` selects the backend policy, coordinator synchronization, or synchronization on all participating replicas.
- `disable_hooks` skips commit hooks. `asis` preserves the supplied vector clock; it is for specialized replication/import work, not ordinary client updates.
- `{retry_put_coordinator_failure, true | false}` controls coordinator retry; disable it for operations that cannot tolerate an automatic retry. `{mbox_check, true | false}` controls the coordinator mailbox check.
- `{counter_op, Operation}` and `{crdt_op, Operation}` carry internal datatype operations; their values must match the datatype module’s operation format.
- `{if_none_match, true}` requests creation only for a strongly consistent object. Existing causal context selects the consistent update path.

Quorum values accept an integer or `one`, `quorum`, `all`, or `default`; `default` uses the bucket policy. Values cannot exceed the effective replication factor. Timeout values are milliseconds.

## W

datatype: quorum
required: false
repeatable: false

### Description

Number of successful write acknowledgments required: a count or `one`, `quorum`, `all`, or `default`.

## DW

datatype: quorum
required: false
repeatable: false

### Description

Number of durable write acknowledgments required. Use a count or `one`, `quorum`, `all`, or `default`.

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

3.4.0: 19af3f51fee50ca84e0ff5146b9f161691fc04f82772598dd465838dd428e45f
3.4.1: 19af3f51fee50ca84e0ff5146b9f161691fc04f82772598dd465838dd428e45f
