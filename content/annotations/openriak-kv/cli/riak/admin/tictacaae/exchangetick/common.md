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

3.4.0: ca909170a170bfcdc329a48569ede1b3be30a80c14b28246c2c72fd2df8aa8d4
3.4.1: ca909170a170bfcdc329a48569ede1b3be30a80c14b28246c2c72fd2df8aa8d4
