# Metadata

command: shell:riak repl realtime start
versions: 3.4.0, 3.4.1

# Summary

Start realtime for a remote cluster.

# Description

Realtime replication forwards new writes; enabled configuration and active streaming are separate states.

# Arguments

## clustername

datatype: cluster name
required: false
repeatable: false

### Description

Remote symbolic cluster name, for example `cli_remote`. This is distinct from an Erlang node name or a generated cluster ID.

# Errors

## reference-error-1

### Condition

The remote cluster has no usable connection or its coordinator is unavailable.

### Description

Configuration may be accepted while no data is transferred. A failed coordinator RPC can also be printed by the launcher.

### Remedy

Inspect repl connections and repl status, confirm the remote name, and restore transport connectivity before expecting replication progress.

# Reviewed against

3.4.0: f7a24aab84686242e455b5589bde865775273c10a4fc33c0b7bc04a8e6f9b12b
3.4.1: f7a24aab84686242e455b5589bde865775273c10a4fc33c0b7bc04a8e6f9b12b
