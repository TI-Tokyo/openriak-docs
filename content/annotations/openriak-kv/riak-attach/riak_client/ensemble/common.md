# Metadata

command: erlang:riak_client:ensemble/1
versions: 3.4.0, 3.4.1

# Summary

Find the strong-consistency ensemble responsible for a key.

# Description

Returns `{kv, Partition, NVal}` from the current ring and bucket properties.

# Arguments

## BKey

datatype: bucket/key tuple
required: true
repeatable: false

### Description

Pair `{Bucket, Key}`, for example `{<<"cli_reference">>, <<"present">>}`.

# Reviewed against

3.4.0: a240d3389e957cd5f65c8e4bd2559a8c38c125e0400785c0374173652500b168
3.4.1: a240d3389e957cd5f65c8e4bd2559a8c38c125e0400785c0374173652500b168

# Tags

feature: client-operations
repository: riak_kv
module: riak_client
concept: data-access
