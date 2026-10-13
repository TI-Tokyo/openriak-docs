# Metadata

command: erlang:riak_client:get_client_id/1
versions: 3.4.0, 3.4.1

# Summary

Read the identifier associated with a client handle.

# Description

Server-managed vector clocks commonly use `undefined` as the client identifier.

# Arguments

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Reviewed against

3.4.0: 4eafd21638e61f94759249f2c6e074ac3a5c4d98ae705a3dcd071db2387eee78
3.4.1: 4eafd21638e61f94759249f2c6e074ac3a5c4d98ae705a3dcd071db2387eee78

# Tags

feature: client-operations
repository: riak_kv
module: riak_client
concept: data-access
