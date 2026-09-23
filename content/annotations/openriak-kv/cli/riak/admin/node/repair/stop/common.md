# Metadata

command: shell:riak admin node repair stop *
versions: 3.4.1

# Summary

Stop partition repair on a node.

# Description

Repair runs asynchronously. Inspect node repair status for progress or to confirm cancellation.

# Arguments

## REASON

datatype: text
required: true
repeatable: false

### Description

Reason for stopping, for example `maintenance`. Quote text containing spaces.

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

datatype: Erlang node name or all
required: false
repeatable: false
default: local node

### Description

Full Erlang node name, or `all` to select all available nodes. Omit to select the local node.

# Reviewed against

3.4.1: c9773b4038ccf3e7a6a613567882ee8d4c1648e6d96249efa1f4c32886e0d593

# Tags

feature: read-repair
repository: riak
module: riak
concept: replica-repair
