# Metadata

command: erlang:riak_kv_replrtq_snk:remove_snkqueue/1
versions: 3.4.0, 3.4.1

# Summary

Remove a temporary sink queue configuration.

# Description

If the queue remains configured in riak.conf, it will be introduced again after a process restart.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

See the shared `QueueName` argument on the parent module page.

# Reviewed against

3.4.0: 608040c40074ef9b48129c621c6a24897e1c438806f5e32058bddbe0273572fd
3.4.1: 608040c40074ef9b48129c621c6a24897e1c438806f5e32058bddbe0273572fd

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk
concept: cross-cluster-replication, queueing
