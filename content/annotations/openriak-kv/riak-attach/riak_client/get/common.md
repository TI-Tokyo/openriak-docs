# Metadata

command: erlang:riak_client:get/3

# Summary

Read an object by bucket and key through an Erlang client handle.

# Description

Read an object by bucket and key through an Erlang client handle. The tested examples below use `get/3`; consult the signatures for other arities.

# Arguments

## Bucket

required: true
repeatable: false
datatype: binary or {binary, binary}

### Description

Bucket name as a binary, or a {BucketType, Bucket} tuple of binaries for a typed bucket.

## Key

required: true
repeatable: false
datatype: binary

### Description

Object key as a binary.

## Client

required: true
repeatable: false
datatype: Riak client handle

### Description

Client handle returned by riak:local_client(). Match its {ok, Client} result before calling get/3.

# Notes

To prepare the successful example in a disposable cluster, open an Erlang shell and run:

```erlang
{ok, Client} = riak:local_client().
riak_client:put(riak_object:new(<<"cli_reference">>, <<"present">>, <<"example value">>), Client).
```

The `missing` key must not exist. Do not use production data for this exercise.

# Reviewed against

3.4.0: f09001d5ce58d3a228abd4eda55a1adad98c0d473d14e2c38ddd959c0066de24
3.4.1: f09001d5ce58d3a228abd4eda55a1adad98c0d473d14e2c38ddd959c0066de24
