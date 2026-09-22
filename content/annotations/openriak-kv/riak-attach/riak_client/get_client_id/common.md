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

3.4.0: 2a39d7f5568522e2761cfbc6cb9f0e011e0bb2aaab9e8ac5b87668496e5d8fa9
3.4.1: 2a39d7f5568522e2761cfbc6cb9f0e011e0bb2aaab9e8ac5b87668496e5d8fa9
