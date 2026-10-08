# Metadata

command: erlang:riak_client:replrtq_reset_all_workercounts/2
versions: 3.4.0, 3.4.1

# Summary

Reset sink worker defaults on available nodes.

# Description

Returns the nodes on which the new worker count and per-peer limit were applied.

# Arguments

## WorkerC

datatype: non-negative integer
required: true
repeatable: false

### Description

Number of sink workers.

## PerPeerL

datatype: non-negative integer
required: true
repeatable: false

### Description

Maximum workers per peer. Keep no greater than WorkerC.

# Reviewed against

3.4.0: 1ea0228b02c6fd89303dc07ebf8fec2f84cab0736800bef0da6cd9db9ba54fde
3.4.1: 1ea0228b02c6fd89303dc07ebf8fec2f84cab0736800bef0da6cd9db9ba54fde

# Tags

feature: queue-replication
repository: riak_kv
module: riak_client
concept: concurrency, cross-cluster-replication
