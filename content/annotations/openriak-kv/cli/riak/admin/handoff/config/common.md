# Metadata

command: shell:riak admin handoff config
versions: 3.4.0, 3.4.1

# Summary

Show handoff limits and enabled directions.

# Description

Read transfer limits and inbound/outbound enablement before changing handoff behaviour. Disabling a direction interrupts active transfers in that direction.

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

3.4.0: 6bae26851c81004efecd4fe118e2575d7a733d589d7970c8538c68f5031888c4
3.4.1: 6bae26851c81004efecd4fe118e2575d7a733d589d7970c8538c68f5031888c4
