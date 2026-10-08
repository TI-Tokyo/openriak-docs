# Metadata

command: erlang:riak_kv_replrtq_snk:suspend_snkqueue/1
versions: 3.4.0, 3.4.1

# Summary

Suspend workers for a sink queue.

# Description

Pause fetching for this queue across its configured peers. Resume when maintenance is complete.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

See the shared `QueueName` argument on the parent module page.

# Reviewed against

3.4.0: 5a53624299833aab1d103af9883b6693c5aabea5ebc52ccdab2a7343bc331567
3.4.1: 5a53624299833aab1d103af9883b6693c5aabea5ebc52ccdab2a7343bc331567

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk
concept: cross-cluster-replication, queueing
