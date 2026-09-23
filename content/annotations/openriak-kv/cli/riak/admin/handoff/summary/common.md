# Metadata

command: shell:riak admin handoff summary
versions: 3.4.0, 3.4.1

# Summary

Summarise active and known transfers between nodes.

# Description

Cells show active transfer counts and the total known count in parentheses. The Total column sums active transfers.

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

# Reviewed against

3.4.0: 05d119ad9fe01bc43b7112c8854181d73a1f9b93b843d15161ccf9c6db680732
3.4.1: 05d119ad9fe01bc43b7112c8854181d73a1f9b93b843d15161ccf9c6db680732

# Tags

feature: handoff
repository: riak
module: riak
concept: partition-transfer
