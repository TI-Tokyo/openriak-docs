# Metadata

command: shell:riak admin tictacaae rebuild-soon
versions: 3.4.0, 3.4.1

# Summary

Request an AAE tree rebuild after a delay.

# Description

Requests work on the selected controllers. An acknowledgment does not mean that rebuilding has completed; inspect treestatus for progress.

# Arguments

## DELAY

datatype: non-negative integer
required: true
repeatable: false

### Description

Seconds from now at which the next rebuild should become eligible. For example, `60`.

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

3.4.0: c8380f29394e50a3fe55405bdb5160c8feb826cbeffaf3382e7c4d450a8f399d
3.4.1: c8380f29394e50a3fe55405bdb5160c8feb826cbeffaf3382e7c4d450a8f399d
