# Metadata

command: shell:riak admin tictacaae rebuild-now
versions: 3.4.0, 3.4.1

# Summary

Request an AAE tree rebuild now.

# Description

Requests work on the selected controllers. An acknowledgment does not mean that rebuilding has completed; inspect treestatus for progress.

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

Full Erlang node name, or `all` to select all available nodes. Omit to select the local node.

## --partition

datatype: partition index or all
required: false
repeatable: false
default: all

### Description

Full decimal partition index, or `all`. For example, `0` selects the zero index. Omit to select all partitions on the chosen node.

# Reviewed against

3.4.0: 0fb160f60951a3be230a36e27e3bddcf7d63b8bb85cfd9d01ca7322195e72a69
3.4.1: 0fb160f60951a3be230a36e27e3bddcf7d63b8bb85cfd9d01ca7322195e72a69

# Tags

feature: tictac-aae
repository: riak
module: riak
concept: replica-repair
