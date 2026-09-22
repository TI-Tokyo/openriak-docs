# Metadata

command: shell:riak admin cluster partition
versions: 3.4.0, 3.4.1

# Summary

Convert between a ring partition ID and its full index.

# Description

Supply exactly one assignment: `id=N` for a small ring ID, or `index=N` for its full 160-bit ring position.

# Arguments

## id

datatype: integer from 0 to ring size minus one
required: false
repeatable: false

### Description

Small zero-based ring ID. For example, `id=0` selects the first partition. Supply either id or index.

## index

datatype: 160-bit unsigned integer
required: false
repeatable: false

### Description

Full decimal partition index, such as `index=0`. Supply either index or id.

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

# Reviewed against

3.4.0: 4117def24c042d5f05e8ff33d370e85fdde1fefae0556535b0cd410103ed9775
3.4.1: 4117def24c042d5f05e8ff33d370e85fdde1fefae0556535b0cd410103ed9775
