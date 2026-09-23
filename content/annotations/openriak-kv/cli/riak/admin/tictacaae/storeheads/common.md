# Metadata

command: shell:riak admin tictacaae storeheads
versions: 3.4.0, 3.4.1

# Summary

Read or change whether AAE stores object heads.

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

3.4.0: a8035f4cd9446829e9dbb8eaf79ca6fd17d9854795c97b23b81670ffa49cc889
3.4.1: a8035f4cd9446829e9dbb8eaf79ca6fd17d9854795c97b23b81670ffa49cc889

# Tags

feature: tictac-aae
repository: riak
module: riak
concept: replica-repair
