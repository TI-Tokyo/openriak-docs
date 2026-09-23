# Metadata

command: erlang:riak_client:repair_node/0
versions: 3.4.0, 3.4.1

# Summary

Request repair of the partitions owned by this node.

# Description

Schedules vnode repair for the node’s owned partitions and returns without waiting for all repairs to finish. Use node-repair status on releases that provide it.

# Arguments

# Reviewed against

3.4.0: 9356a9ff8aef171cc9086af60271a0b657a47dbab970cf72edf1d33aa7f562ca
3.4.1: 9356a9ff8aef171cc9086af60271a0b657a47dbab970cf72edf1d33aa7f562ca

# Tags

feature: read-repair
repository: riak_kv
module: riak_client
concept: replica-repair
