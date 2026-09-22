# Metadata

command: shell:riak repl fullsync stop
versions: 3.4.0, 3.4.1

# Summary

Stop fullsync for a remote cluster.

# Description

Full-sync compares existing data. Enabling a destination and starting a comparison are separate operations.

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

3.4.0: d86c0dbd0d64a1026a518a1767a4b052bdc0f636c5dfc3c59a2c6993f41f0b6e
3.4.1: d86c0dbd0d64a1026a518a1767a4b052bdc0f636c5dfc3c59a2c6993f41f0b6e
