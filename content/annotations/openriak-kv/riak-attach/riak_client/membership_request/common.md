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

3.4.0: ed26a920a2ffca1b298211500a9d7dbb729f889d4fdfd0b7e80bb8df4bad6cfd
3.4.1: ed26a920a2ffca1b298211500a9d7dbb729f889d4fdfd0b7e80bb8df4bad6cfd

# Tags

feature: cluster-management
repository: riak_kv
module: riak_client
concept: partition-placement
