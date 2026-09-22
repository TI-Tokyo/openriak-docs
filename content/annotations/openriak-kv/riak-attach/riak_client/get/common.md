# Metadata

command: erlang:riak_client:get/3

# Summary

Read an object by bucket and key through an Erlang client handle.

# Description

Read an object by bucket and key through an Erlang client handle. The shortest form uses the bucket read policy. Use the option-list form to select quorums, timeouts and diagnostic output; the legacy longer form takes R and Timeout separately.

# Arguments

## Bucket

required: true
repeatable: false
datatype: binary or {binary, binary}

### Description

See the shared `Bucket` argument on the parent module page.

## Key

required: true
repeatable: false
datatype: binary

### Description

See the shared `Key` argument on the parent module page.

## Client

required: true
repeatable: false
datatype: Riak client handle

### Description

See the shared `Client` argument on the parent module page.

## Options

required: false
repeatable: false
datatype: Erlang option list

### Description

Supply an Erlang list, for example `[{r, quorum}, {notfound_ok, false}, {timeout, 5000}]`.

- `{r, Value}` is the required read quorum; `{pr, Value}` is the required number of primary-owner responses.
- `{basic_quorum, true | false}` allows an early failure once the required quorum cannot be reached. `{notfound_ok, true | false}` controls whether missing-object responses count toward the quorum.
- `{timeout, Milliseconds}` bounds the request. `{recv_timeout, Milliseconds}` bounds the caller’s wait; otherwise that wait is the request timeout plus 100 milliseconds.
- `{details, true}`, `details`, or `{details, [timing, vnodes]}` requests diagnostics in the result. Select only the detail categories needed.
- `{sloppy_quorum, true | false}` controls fallback replicas; `{n_val, PositiveInteger}` overrides the replication factor for this read.
- `deletedvclock` returns a tombstone clock as `{error, {deleted, VClock}}` instead of hiding it as notfound.
- `{crdt_op, true}` requests datatype-specific handling and is intended for the datatype client path.

Quorum values accept an integer or `one`, `quorum`, `all`, or `default`; `default` uses the bucket policy. Values cannot exceed the effective replication factor. Timeout values are milliseconds.

## R

required: false
repeatable: false
datatype: quorum

### Description

Legacy positional read quorum in the longer form. Use a count or `one`, `quorum`, `all`, or `default`.

## Timeout

required: false
repeatable: false
datatype: timeout in milliseconds

### Description

See the shared `Timeout` argument on the parent module page.

# Notes

To prepare the successful example in a disposable cluster, open an Erlang shell and run:

```erlang
{ok, Client} = riak:local_client().
riak_client:put(riak_object:new(<<"cli_reference">>, <<"present">>, <<"example value">>), Client).
```

The `missing` key must not exist. Do not use production data for this exercise.

# Examples

## erlang-get:with-options

### Description

Read an object with a quorum, exclude notfound replies from successful responses, and bound the request to five seconds.

# Reviewed against

3.4.0: 1e0cf7425b910050d191eec3d6df13447f0c21bc14bd37ae383bf0a3be1c4cb8
3.4.1: 1e0cf7425b910050d191eec3d6df13447f0c21bc14bd37ae383bf0a3be1c4cb8
