# Summary

Use the riak_kv_replrtq_snk Erlang interface.

# Shared arguments

## QueueName

datatype: atom

### Description

Name of the sink replication queue, for example `cli_reference`. Sink and source queue names must match the intended replication route.

## PerPeerLimit

datatype: positive integer

### Description

Maximum concurrent sink workers assigned to one peer. It must fit the total worker count.

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk
concept: cross-cluster-replication
