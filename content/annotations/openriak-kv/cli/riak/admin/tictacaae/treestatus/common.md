# Metadata

command: shell:riak admin tictacaae treestatus
versions: 3.4.0, 3.4.1

# Summary

List AAE trees and their rebuild state.

# Description

The default report includes partial trees and trees currently building or rebuilding. Select all states to include completed and empty trees.

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

## --show

datatype: comma-separated state list
required: false
repeatable: false
default: partial,rebuilding,building

### Valid values

- empty
- partial
- built
- rebuilding
- building
- all

### Description

Comma-separated tree states, or `all`. For example, `partial,rebuilding` selects two states.

# Reviewed against

3.4.0: fdb5d86426faad9554b8db81190964022b428fbf47f5fa7dcebd6745d1065a1a
3.4.1: fdb5d86426faad9554b8db81190964022b428fbf47f5fa7dcebd6745d1065a1a
