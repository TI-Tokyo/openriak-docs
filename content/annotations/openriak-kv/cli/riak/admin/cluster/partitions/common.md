# Metadata

command: shell:riak admin cluster partitions
versions: 3.4.0, 3.4.1

# Summary

List partitions owned by a node.

# Description

The output distinguishes partition types and shows full partition indexes. Use these indexes when a command requests a partition rather than its small ring ID.

# Arguments

# Options

## --format

datatype: output writer
required: false
repeatable: false
default: human

### Valid values

- csv
- human
- json

### Description

Select the Clique output writer. `human` is readable terminal output; `csv` renders tables only; `json` renders structured status records. The launcher can append an `ok` line, so complete stdout is not necessarily a standalone JSON document. An unknown writer warns and falls back to `human`.

## --help

datatype: flag (no value)
required: false
repeatable: false

### Description

Print usage without executing the command. The short spelling is `-h`.

## --node

datatype: Erlang node name
required: false
repeatable: false
default: local node

### Description

Run the operation on the named node, such as `openriak-kv@node1.test`. Use the full Erlang node name. Omit it to target the local node. Do not combine with `--all` where that flag is available.

# Reviewed against

3.4.0: ce884baa9edba266ad4639b80eb8bef3b414f403f8bce173ddcee909841c03b6
3.4.1: ce884baa9edba266ad4639b80eb8bef3b414f403f8bce173ddcee909841c03b6

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_console
concept: partition-placement
