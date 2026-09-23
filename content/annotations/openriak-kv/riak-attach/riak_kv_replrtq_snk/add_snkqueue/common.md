# Metadata

command: erlang:riak_kv_replrtq_snk:add_snkqueue/3
versions: 3.4.0, 3.4.1

# Summary

Add a temporary sink queue configuration.

# Description

The new configuration lasts until the sink process restarts. Persist the corresponding settings in riak.conf when they must survive restart.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

See the shared `QueueName` argument on the parent module page.

## Peers

datatype: list of peer tuples
required: true
repeatable: false

### Description

List of `{PeerId, Delay, Address, Port, Protocol}` tuples. Address is a string; Protocol is `http` or `pb`. For example, `[{1, 0, "127.0.0.1", 8098, http}]`. An empty list configures no remote peers.

## WorkerCount

datatype: positive integer
required: true
repeatable: false

### Description

Number of concurrent workers for this queue. For example, `2`. Changing it starts a new worker set; old workers finish in-flight work before exiting.

## PerPeerLimit

datatype: positive integer
required: false
repeatable: false

### Description

See the shared `PerPeerLimit` argument on the parent module page.

# Reviewed against

3.4.0: db250fe77f04cfbca3714755b05d9d973e6e13c844276f35a7db709d042115d9
3.4.1: db250fe77f04cfbca3714755b05d9d973e6e13c844276f35a7db709d042115d9

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk
concept: cross-cluster-replication, queueing
