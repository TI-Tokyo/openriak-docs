# Metadata

command: shell:riak admin node repair status
versions: 3.4.1

# Summary

Show the status of partition repairs on a node.

# Description

An idle node reports no active repairs. Select a node or `all`; use `-f json` for this command’s JSON layout. The long `--format` flag belongs to the global Clique writer.

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

datatype: Erlang node name or all
required: false
repeatable: false
default: local node

### Description

Node to inspect, or `all` to inspect every node. Omit to inspect the current node.

## -f

datatype: result layout
required: false
repeatable: false
default: table

### Valid values

- table
- json

### Description

Select the repair-status layout. Use `-f json` for JSON; the long `--format` selects the separate Clique output writer.

# Reviewed against

3.4.1: 2c25cf9428c9fecfa37f047eb8a694743880b605b5a9442df90bfc1cd88ee811

# Tags

feature: observability
repository: riak
module: riak
concept: diagnostics
