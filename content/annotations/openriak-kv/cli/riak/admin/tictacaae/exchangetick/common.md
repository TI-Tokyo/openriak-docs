# Metadata

command: shell:riak admin tictacaae exchangetick
versions: 3.4.0, 3.4.1

# Summary

Read or change the AAE exchange tick interval.

# Description

Omit the value to read the runtime setting; supply a value to change it on the selected node. Persist the corresponding configuration separately if the change must survive restart.

# Arguments

## VALUE

datatype: milliseconds from 0 to 3600000000
required: false
repeatable: false

### Description

New value for AAE exchange tick interval. Omit to read the current setting.

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

# Results

## outcome

### Description

The packaged runtime returns usage and {error,1} for both tested forms. No exchange-tick value is read or changed by these examples.

# Reviewed against

3.4.0: 0e8f711113c0997af074df0682d36e1ad9328f7a0a308a6be141e385423c2d6f
3.4.1: 0e8f711113c0997af074df0682d36e1ad9328f7a0a308a6be141e385423c2d6f

# Tags

feature: tictac-aae
repository: riak
module: riak
concept: replica-repair, scheduling
