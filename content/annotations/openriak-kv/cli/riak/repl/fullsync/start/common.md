# Metadata

command: shell:riak repl fullsync start
versions: 3.4.0, 3.4.1

# Summary

Start fullsync for a remote cluster.

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

3.4.0: e8e0707f50e3d41d5c3cb766ad1d0a804d2cbf28fa61edfb2a71a4cec6295f68
3.4.1: e8e0707f50e3d41d5c3cb766ad1d0a804d2cbf28fa61edfb2a71a4cec6295f68

# Tags

feature: full-sync
repository: riak_repl
module: riak_repl_console
concept: replica-repair
