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

3.4.0: a83857736fde18aacd26f4702247acee7de5f4402932b67b1a7caf008884a705
3.4.1: a83857736fde18aacd26f4702247acee7de5f4402932b67b1a7caf008884a705

# Tags

feature: legacy-replication
repository: riak_repl
module: riak_repl_console
concept: cross-cluster-replication
