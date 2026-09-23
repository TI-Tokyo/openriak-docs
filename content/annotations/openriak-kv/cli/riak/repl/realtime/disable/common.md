# Metadata

command: shell:riak repl realtime disable
versions: 3.4.0, 3.4.1

# Summary

Disable realtime for a remote cluster.

# Description

Realtime replication forwards new writes; enabled configuration and active streaming are separate states.

# Arguments

## clustername

datatype: cluster name
required: true
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

3.4.0: a9dc2e14862c62a66120fbb299ee92f7a275754771c00f7c92fb867843419178
3.4.1: a9dc2e14862c62a66120fbb299ee92f7a275754771c00f7c92fb867843419178

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
