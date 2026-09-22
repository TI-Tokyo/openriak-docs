# Metadata

command: erlang:riak_client:reap/3
versions: 3.4.0, 3.4.1

# Summary

Request physical removal of a tombstone.

# Description

The three-argument form reads the key with deleted-vclock support and returns `false` if it does not find a tombstone. Reaping is an administrative operation; coordinate it with replication and retention policy.

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

## TombClock

datatype: vector clock
required: false
repeatable: false

### Description

Vector clock of the tombstone. The shorter arity discovers it by reading the key.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Examples

## erlang-riak-client-reap:reap-existing-tombstone

### Description

Delete the object to create one tombstone, reap it, and wait until the tombstone count is zero.

# Reviewed against

3.4.0: ad0feae088e750513109e872d3cb4804b8568f6457ed5ea852393f6b994b6f61
3.4.1: ad0feae088e750513109e872d3cb4804b8568f6457ed5ea852393f6b994b6f61
