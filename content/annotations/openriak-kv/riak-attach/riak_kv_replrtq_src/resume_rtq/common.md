# Metadata

command: erlang:riak_kv_replrtq_src:resume_rtq/1
versions: 3.4.0, 3.4.1

# Summary

Resume accepting entries into a source replication queue.

# Description

Resuming an already active queue has no additional effect. It does not recover entries discarded during suspension.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

See the shared `QueueName` argument on the parent module page.

# Examples

## erlang-riak-kv-replrtq-src-resume-rtq:populated-queue

### Description

Prepare a queue with five stored objects to inspect or change pending replication work. Queue length and registration describe the source; check the destination separately to confirm delivery.

# Reviewed against

3.4.0: 548419247a6409fe3f2b585bf9549ca1785a6a5641dd6577522ed3a479b96975
3.4.1: 548419247a6409fe3f2b585bf9549ca1785a6a5641dd6577522ed3a479b96975

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_src
concept: cross-cluster-replication
