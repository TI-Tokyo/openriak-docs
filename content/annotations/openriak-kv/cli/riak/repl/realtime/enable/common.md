# Metadata

command: shell:riak repl realtime enable
versions: 3.4.0, 3.4.1

# Summary

Enable realtime for a remote cluster.

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

3.4.0: 19d5a21250e9222534a3603f0e8e30a4015fd0ea110d5ddeb82d4f2eba230496
3.4.1: 19d5a21250e9222534a3603f0e8e30a4015fd0ea110d5ddeb82d4f2eba230496
