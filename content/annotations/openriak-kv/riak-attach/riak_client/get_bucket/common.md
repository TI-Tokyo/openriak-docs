# Metadata

command: erlang:riak_client:get_bucket/2
versions: 3.4.0, 3.4.1

# Summary

Read a bucket’s effective properties.

# Description

The result includes defaults and bucket-specific properties. Reading properties does not require the bucket to contain an object.

# Arguments

## Bucket

datatype: binary or pair of binaries
required: true
repeatable: false

### Description

See the shared `Bucket` argument on the parent module page.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Reviewed against

3.4.0: efda2831084b64871f244dac6b3d782e7c99b22e506ab86a36fe64020cbfb0ee
3.4.1: efda2831084b64871f244dac6b3d782e7c99b22e506ab86a36fe64020cbfb0ee

# Tags

feature: client-operations
repository: riak_kv
module: riak_client
concept: data-access
