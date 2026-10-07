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

3.4.0: 2565b61ede4e5475ca9f2072114372c9127529f695591721e2d8921b21fc5bfa
3.4.1: aec8b8ba5d4119e650cef06026d778f2262c26036fd0f6199cfac3115dff86ce

# Tags

feature: client-operations
repository: riak_kv
module: riak_client
concept: data-access
