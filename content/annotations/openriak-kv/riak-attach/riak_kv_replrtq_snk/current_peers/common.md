# Metadata

command: erlang:riak_kv_replrtq_snk:current_peers/1
versions: 3.4.0, 3.4.1

# Summary

Read the peers and state of a sink queue.

# Description

The result reports the runtime peer configuration; a queue may be suspended or disabled.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

See the shared `QueueName` argument on the parent module page.

# Reviewed against

3.4.0: a0770c682efc12006b9e39d510297a2f652b39602e6c1b0faf8c0c74f2fd6378
3.4.1: a0770c682efc12006b9e39d510297a2f652b39602e6c1b0faf8c0c74f2fd6378

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk
concept: cross-cluster-replication
