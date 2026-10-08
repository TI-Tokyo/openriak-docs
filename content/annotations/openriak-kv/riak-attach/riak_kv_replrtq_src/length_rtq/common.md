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

3.4.0: 9572acc636936117416640913a74962f71a7889f7162df8d7cc431f432468ebd
3.4.1: 9572acc636936117416640913a74962f71a7889f7162df8d7cc431f432468ebd

# Tags

feature: queue-replication
repository: riak_kv
module: riak_kv_replrtq_src
concept: cross-cluster-replication
