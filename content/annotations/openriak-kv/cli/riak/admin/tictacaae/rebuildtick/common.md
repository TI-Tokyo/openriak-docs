# Metadata

command: shell:riak admin tictacaae rebuildtick
versions: 3.4.0, 3.4.1

# Summary

Read or change the AAE rebuild tick interval.

# Description

Omit the value to read the runtime setting; supply a value to change it on the selected node. Persist the corresponding configuration separately if the change must survive restart.

# Arguments

## VALUE

datatype: milliseconds from 0 to 3600000000
required: false
repeatable: false

### Description

New value for AAE rebuild tick interval. Omit to read the current setting.

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

3.4.0: b1bca0fa6751237327c44db94096860972f65dfef63f0bda9d591bc1be0c44c5
3.4.1: b1bca0fa6751237327c44db94096860972f65dfef63f0bda9d591bc1be0c44c5

# Tags

feature: tictac-aae
repository: riak
module: riak
concept: replica-repair, scheduling
