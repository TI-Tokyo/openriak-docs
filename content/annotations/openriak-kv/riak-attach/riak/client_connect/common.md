# Metadata

command: erlang:riak:client_connect/1
versions: 3.4.0, 3.4.1

# Summary

Create a client handle for a reachable Erlang node.

# Description

Checks distributed-Erlang reachability before returning `{ok, Client}`. The node name and cookie must match the target.

# Arguments

## Node

datatype: Erlang node atom
required: true
repeatable: false

### Description

See the shared `Node` argument on the parent module page.

## ClientId

datatype: undefined or four-byte binary
required: false
repeatable: false

### Description

See the shared `ClientId` argument on the parent module page.

# Reviewed against

3.4.0: 311ffd98d6b8da72672e65aacceba94804634ca55addbca4d17dfbfa9bc4492f
3.4.1: 311ffd98d6b8da72672e65aacceba94804634ca55addbca4d17dfbfa9bc4492f

# Tags

feature: client-operations
repository: riak_kv
module: riak
concept: data-access
