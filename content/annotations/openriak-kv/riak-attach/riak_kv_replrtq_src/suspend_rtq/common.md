# Metadata

command: erlang:riak_kv_replrtq_src:suspend_rtq/1
versions: 3.4.0, 3.4.1

# Summary

Stop accepting new entries into a source replication queue.

# Description

New updates are discarded while suspended. Consumers may continue draining existing entries. Resume the queue to accept future updates; suspension does not buffer missed updates.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

See the shared `QueueName` argument on the parent module page.

# Examples

## erlang-riak-kv-replrtq-src-suspend-rtq:populated-queue

### Description

Prepare a queue with five stored objects to inspect or change pending replication work. Queue length and registration describe the source; check the destination separately to confirm delivery.

# Reviewed against

3.4.0: 7e5955316851f8003f3de62564da382c22996d34479cd89b92f220814d48d13a
3.4.1: 7e5955316851f8003f3de62564da382c22996d34479cd89b92f220814d48d13a
