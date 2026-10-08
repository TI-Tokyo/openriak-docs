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

3.4.0: 26b24401e440c45ca29e10b5c6bf63f6ef104a8723c7023270096dc83fc30d5c
3.4.1: 26b24401e440c45ca29e10b5c6bf63f6ef104a8723c7023270096dc83fc30d5c

# Tags

feature: queue-replication
repository: riak_kv
module: riak_client
concept: cross-cluster-replication
