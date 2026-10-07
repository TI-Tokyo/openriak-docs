# Metadata

command: erlang:riak_kv_replrtq_snk:resume_snkqueue/1
versions: 3.4.0, 3.4.1

# Summary

Resume workers for a sink queue.

# Description

Workers resume fetching from all peers configured for this queue.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

See the shared `QueueName` argument on the parent module page.

# Reviewed against

3.4.0: 23716ed42a016491a5b4c23b04ed2763c6749013983ce391444495d721928aab
3.4.1: a24ee4aee204d95ab4664d9b3db9b14f9bed84f400e058f5fc302c901109cde0

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_snk
concept: cross-cluster-replication, queueing
