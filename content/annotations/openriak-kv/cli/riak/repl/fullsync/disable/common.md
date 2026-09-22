# Metadata

command: shell:riak repl fullsync disable
versions: 3.4.0, 3.4.1

# Summary

Disable fullsync for a remote cluster.

# Description

Full-sync compares existing data. Enabling a destination and starting a comparison are separate operations.

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

3.4.0: 5ffda45c5745da74728fed564ad1bba130629b73eb1ef348f7f5da7daab1330e
3.4.1: 5ffda45c5745da74728fed564ad1bba130629b73eb1ef348f7f5da7daab1330e
