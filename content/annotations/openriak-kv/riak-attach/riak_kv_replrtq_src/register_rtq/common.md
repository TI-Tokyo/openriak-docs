# Metadata

command: erlang:riak_kv_replrtq_src:register_rtq/2
versions: 3.4.0, 3.4.1

# Summary

Register a source replication queue and its filter.

# Description

New coordinated puts are enqueued only when they match the filter. Registering a queue does not backfill historical objects.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

See the shared `QueueName` argument on the parent module page.

## QueueFilter

datatype: queue filter tuple or atom
required: true
repeatable: false

### Description

Use `any` for all objects, `{bucketname, <<"orders">>}` for one bucket, `{buckettype, <<"orders">>}` for a bucket type, or `{bucketprefix, <<"order">>}` for a prefix. `block_rtq` is the block-replication filter.

# Examples

## erlang-riak-kv-replrtq-src-register-rtq:populated-queue

### Description

Prepare a queue with five stored objects to inspect or change pending replication work. Queue length and registration describe the source; check the destination separately to confirm delivery.

# Reviewed against

3.4.0: 70b10c443eea5e9fa52868db9f432c56301dcb6be25d2c213ad5638d438411d8
3.4.1: 70b10c443eea5e9fa52868db9f432c56301dcb6be25d2c213ad5638d438411d8
