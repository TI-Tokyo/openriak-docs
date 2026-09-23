# Metadata

command: shell:riak admin handoff details
versions: 3.4.0, 3.4.1

# Summary

List active handoffs with their progress.

# Description

Use this when diagnosing a slow rebalance. An idle node prints `No ongoing transfers.`; this is a successful result.

# Arguments

# Options

## --all

datatype: flag (no value)
required: false
repeatable: false

### Description

Apply to every node in the cluster. Omit it to use the local node or the node selected by `--node`. Do not combine with `--node`.

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

3.4.0: 0249476f54bcfefb1ff2ce494a5483ae725baad817f5279ccea3a3e6390c93b0
3.4.1: 0249476f54bcfefb1ff2ce494a5483ae725baad817f5279ccea3a3e6390c93b0

# Tags

feature: handoff
repository: riak
module: riak
concept: partition-transfer
