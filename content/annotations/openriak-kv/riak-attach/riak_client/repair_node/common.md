# Metadata

command: erlang:riak_client:repair_node/0
versions: 3.4.0, 3.4.1

# Summary

Request repair of the partitions owned by this node.

# Description

Schedules vnode repair for the node’s owned partitions and returns without waiting for all repairs to finish. Use node-repair status on releases that provide it.

# Arguments

# Reviewed against

3.4.0: 2295019480360e9edb93a759654fbef09c3a27eb6960e752eaec85c0f942e2a0
3.4.1: 2295019480360e9edb93a759654fbef09c3a27eb6960e752eaec85c0f942e2a0

# Tags

feature: read-repair
repository: riak_kv
module: riak_client
concept: replica-repair
