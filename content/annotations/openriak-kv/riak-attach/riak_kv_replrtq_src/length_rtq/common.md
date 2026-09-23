# Metadata

command: erlang:riak_kv_replrtq_src:length_rtq/1
versions: 3.4.0, 3.4.1

# Summary

Read source queue lengths by priority.

# Description

The result contains the queue name and a three-element length tuple for fold, AAE and put priorities.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

See the shared `QueueName` argument on the parent module page.

# Examples

## erlang-riak-kv-replrtq-src-length-rtq:populated-queue

### Description

Prepare a queue with five stored objects to inspect or change pending replication work. Queue length and registration describe the source; check the destination separately to confirm delivery.

# Reviewed against

3.4.0: 7f9b3309ba25dda84eaf75a975a1dc38f9ca1f36130ada4523cfcf30adc4c168
3.4.1: 7f9b3309ba25dda84eaf75a975a1dc38f9ca1f36130ada4523cfcf30adc4c168

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_src
concept: cross-cluster-replication
