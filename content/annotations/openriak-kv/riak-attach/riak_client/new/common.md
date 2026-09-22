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

3.4.0: 690f99b45b3de9c11e212f5e1fd32e903b19cd22cf48dbfd4c1aa62b20318dac
3.4.1: 690f99b45b3de9c11e212f5e1fd32e903b19cd22cf48dbfd4c1aa62b20318dac
