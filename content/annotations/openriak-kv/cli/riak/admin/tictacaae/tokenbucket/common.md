# Metadata

command: shell:riak admin tictacaae tokenbucket
versions: 3.4.0, 3.4.1

# Summary

Read or change the AAE vnode token-bucket flag.

# Description

Omit VALUE to inspect the flag. Supply a boolean spelling to change the selected partitions. The result lists per-partition responses.

# Arguments

## VALUE

datatype: boolean spelling
required: false
repeatable: false

### Valid values

- true
- enabled
- on
- false
- disabled
- off

### Description

New flag value. Omit to read current values.

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

## --partition

datatype: partition index or all
required: false
repeatable: false
default: all

### Description

Full decimal partition index, or `all`. For example, `0` selects the zero index. Omit to select all partitions on the chosen node.

# Reviewed against

3.4.0: 3b5884d0a4f47015c6b4726563eeeed87b05f3d33e134f4b72ac1d4a25b7e790
3.4.1: 3b5884d0a4f47015c6b4726563eeeed87b05f3d33e134f4b72ac1d4a25b7e790

# Tags

feature: tictac-aae
repository: riak
module: riak
concept: replica-repair
