# Metadata

command: erlang:riak_kv_replrtq_src:clear_rtq/1
versions: 3.4.0, 3.4.1

# Summary

Discard all queued source replication work.

# Description

This clears both the in-memory and overflow queues, then starts an empty queue using the current overflow limit. Discarded work will not be delivered by this queue.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

See the shared `QueueName` argument on the parent module page.

# Examples

## erlang-riak-kv-replrtq-src-clear-rtq:populated-queue

### Description

Prepare a queue with five stored objects to inspect or change pending replication work. Queue length and registration describe the source; check the destination separately to confirm delivery.

# Reviewed against

3.4.0: 9f9144d092fc1687a5c6f7876ffe145856e2f00ab95388ffb831f9bb6811191e
3.4.1: ae06a31e394af4ef4e2dbc8ba5ff8962eab47f235160e3ed3330765fed5a5794

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_src
concept: cross-cluster-replication
