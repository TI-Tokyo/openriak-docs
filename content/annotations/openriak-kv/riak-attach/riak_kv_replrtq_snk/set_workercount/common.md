# Metadata

command: erlang:riak_kv_replrtq_snk:set_workercount/2
versions: 3.4.0, 3.4.1

# Summary

Change the worker counts for an existing sink queue.

# Description

A new worker set starts while existing workers finish outstanding requests, so temporary concurrency may exceed the new limit.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

See the shared `QueueName` argument on the parent module page.

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

3.4.0: b3ab33948232bc277d1f13c0507b0456145ad4cb809473438f35bb15ddb755f3
3.4.1: b3ab33948232bc277d1f13c0507b0456145ad4cb809473438f35bb15ddb755f3

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk
concept: concurrency, cross-cluster-replication
