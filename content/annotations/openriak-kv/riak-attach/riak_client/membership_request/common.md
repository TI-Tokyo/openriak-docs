# Metadata

command: erlang:riak_client:membership_request/1
versions: 3.4.0, 3.4.1

# Summary

List client API endpoints of available KV nodes.

# Description

Only nodes advertising the KV service are included. The selected protocol determines which listener is returned.

# Arguments

## Protocol

datatype: atom
required: true
repeatable: false

### Valid values

- pb
- http

### Description

API listener protocol to discover.

# Reviewed against

3.4.0: e8a03640663f735b038dba038b732e5b17eb02426b747bb66654e3137cccd906
3.4.1: e8a03640663f735b038dba038b732e5b17eb02426b747bb66654e3137cccd906
