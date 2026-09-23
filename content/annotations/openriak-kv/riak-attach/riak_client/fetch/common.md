# Metadata

command: erlang:riak_client:fetch/2
versions: 3.4.0, 3.4.1

# Summary

Fetch the next item from a source replication queue.

# Description

Returns an object, deletion/reap marker, or `{ok, queue_empty}`. Consumers must handle each result form.

# Arguments

## QueueName

datatype: Erlang atom
required: true
repeatable: false

### Description

Replication queue name as an atom, for example `cli_reference`.

## Client

datatype: riak_client handle
required: true
repeatable: false

### Description

See the shared `Client` argument on the parent module page.

# Errors

## reference-error-1

### Condition

The operation exceeds its configured timeout.

### Description

The API can return `{error, timeout}`. A timed-out write or delete may still complete on replicas.

### Remedy

Check node availability and load. Read back state before retrying a mutation, and choose an appropriate timeout.

# Reviewed against

3.4.0: 46f2bcd83787cdd570891d25ca5df6ee71920925ed13b855d41da57e8a12bbca
3.4.1: 46f2bcd83787cdd570891d25ca5df6ee71920925ed13b855d41da57e8a12bbca

# Tags

feature: client-operations
repository: riak_kv
module: riak_client
concept: data-access
