# Metadata

command: erlang:riak:local_client/0
versions: 3.4.0, 3.4.1

# Summary

Create an Erlang client for the current node.

# Description

Returns `{ok, Client}`. Use the handle with riak_client functions; it is not an HTTP or Protocol Buffers connection.

# Arguments

## ClientId

datatype: undefined or four-byte binary
required: false
repeatable: false

### Description

See the shared `ClientId` argument on the parent module page.

# Reviewed against

3.4.0: c26cb82e223a976349aae70721bc51662c04760bef91846355ea5b29b32a8894
3.4.1: c26cb82e223a976349aae70721bc51662c04760bef91846355ea5b29b32a8894
