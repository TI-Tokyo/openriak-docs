# Metadata

command: shell:riak repl clustername
versions: 3.4.0, 3.4.1

# Summary

Read or set the local replication cluster name.

# Description

With no argument, read the current name. Set a distinct name before configuring replication relationships; a fresh cluster can report `undefined`.

# Arguments

## clustername

datatype: cluster name
required: false
repeatable: false

### Description

Human-readable name for this cluster, for example `tokyo`. Omit to read the current name.

# Reviewed against

3.4.0: 82f95007fe73977523ec4d68ef95538bd9f0a4e31b5aed9f37e7345bb6ae535a
3.4.1: 82f95007fe73977523ec4d68ef95538bd9f0a4e31b5aed9f37e7345bb6ae535a

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
