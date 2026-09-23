# Summary

Use the riak Erlang interface.

# Shared arguments

## Node

datatype: Erlang node atom

### Description

Full Erlang node name, for example `'openriak-kv@node.example'`. The local node is `node()`. Remote access requires matching distribution cookies and connectivity.

## ClientId

datatype: client identifier

### Description

Identifier stored in the client handle. Use `undefined` for the normal server-coordinated client path; a supplied identifier changes vector-clock handling for writes.

# Tags

feature: node-operations
repository: riak_kv
module: riak
concept: node-lifecycle
