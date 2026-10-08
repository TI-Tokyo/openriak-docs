# Metadata

command: erlang:riak_client:new/2
versions: 3.4.0, 3.4.1

# Summary

Construct an Erlang client handle.

# Description

This constructs a handle without checking whether the node is reachable. Use riak:client_connect/1 when you need a connectivity check.

# Arguments

## Node

datatype: Erlang node atom
required: true
repeatable: false

### Description

Full Erlang node name as an atom, for example `'openriak-kv@node1.test'`. `node()` selects the current node.

## ClientId

datatype: undefined or four-byte binary
required: false
repeatable: false

### Description

Client identifier. Use `undefined` for the normal server-managed vector-clock behaviour. The legacy explicit identifier is a four-byte binary.

# Reviewed against

3.4.0: 34299e1f0c6676eb2c83bbc22c0e79f69815f73d4e8d3a5814119150390c85a6
3.4.1: 34299e1f0c6676eb2c83bbc22c0e79f69815f73d4e8d3a5814119150390c85a6

# Tags

feature: client-operations
repository: riak_kv
module: riak_client
concept: data-access
