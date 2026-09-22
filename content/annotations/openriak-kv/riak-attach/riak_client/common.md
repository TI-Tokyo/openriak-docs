# Summary

Read, write and administer OpenRiak KV through an Erlang client.

# Shared arguments

## Client

datatype: riak_client handle

### Description

Riak client handle returned by `{ok, Client} = riak:local_client().` for the current node, or `{ok, Client} = riak:client_connect('openriak-kv@node.example').` for another node. It is not a process ID. Pass it in the position shown in the call syntax. AAE fold's one-argument form creates its own local handle; the two-argument form accepts this argument.

## Bucket

datatype: binary or pair of binaries

### Description

A bucket name such as `<<"orders">>`, or a typed bucket pair `{<<"cli_examples">>, <<"orders">>}`. The first binary is the bucket type, and the second is the bucket name. Create and activate the type before writing to it.

For a disposable test node:

```erlang
ok = riak_core_bucket_type:create(<<"cli_examples">>, [{n_val, 3}, {allow_mult, false}]).
ok = riak_core_bucket_type:activate(<<"cli_examples">>).
{ok, Client} = riak:local_client().
Bucket = {<<"cli_examples">>, <<"orders">>}.
ok = riak_client:put(riak_object:new(Bucket, <<"order1">>, <<"example">>), Client).
```

## Key

datatype: binary

### Description

Object key within the selected bucket, for example `<<"order1">>`.

## Timeout

datatype: timeout in milliseconds

### Description

Maximum wait in milliseconds. For example, `5000` is five seconds. Defaults and supported arities are specific to each operation; use its syntax and option description.

## RW

datatype: quorum

### Description

Legacy combined read/write quorum for deletion. Prefer the operation option-list form for explicit read and write requirements.


## Recipient

datatype: Erlang pid

### Description

Process that receives stream messages, for example `self()` for the current Erlang shell. It is separate from the Riak client handle. Use the request ID returned by the operation to select its messages.
