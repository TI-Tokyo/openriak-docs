# Metadata

command: shell:riak repl fullsync enable
versions: 3.4.0, 3.4.1

# Summary

Enable fullsync for a remote cluster.

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

3.4.0: e486d63c3730e5e82525078334567903536eed739135ae3b5bb7aa7411e71738
3.4.1: e486d63c3730e5e82525078334567903536eed739135ae3b5bb7aa7411e71738
