# Metadata

command: erlang:riak_client:replrtq_reset_all_peers/1
versions: 3.4.0, 3.4.1

# Summary

Refresh discovered replication peers on available nodes.

# Description

Returns the nodes on which the change was applied. Missing nodes are not evidence of a successful refresh.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

Replication queue name as an atom, for example `cli_reference`.

# Reviewed against

3.4.0: eca6cfd96545e9c427ca29b5335443c19b628c6fd9ab9a5660b7ad748415bebc
3.4.1: eca6cfd96545e9c427ca29b5335443c19b628c6fd9ab9a5660b7ad748415bebc

# Tags

feature: queue-replication
repository: riak_kv
module: riak_client
concept: cross-cluster-replication
