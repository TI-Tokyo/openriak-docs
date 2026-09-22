# Metadata

command: erlang:riak_kv_replrtq_src:delist_rtq/1
versions: 3.4.0, 3.4.1

# Summary

Remove a source replication queue and its pending work.

# Description

The queue is removed from the runtime configuration and outstanding entries are discarded.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

See the shared `QueueName` argument on the parent module page.

# Examples

## erlang-riak-kv-replrtq-src-delist-rtq:populated-queue

### Description

Prepare a queue with five stored objects to inspect or change pending replication work. Queue length and registration describe the source; check the destination separately to confirm delivery.

# Reviewed against

3.4.0: e562396ffbb0d76afca2f828f933b97a76b96147bb7aafb0bbdfc9a816300cea
3.4.1: e562396ffbb0d76afca2f828f933b97a76b96147bb7aafb0bbdfc9a816300cea
