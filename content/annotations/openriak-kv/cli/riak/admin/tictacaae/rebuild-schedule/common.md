# Metadata

command: shell:riak admin tictacaae rebuild-schedule
versions: 3.4.0, 3.4.1

# Summary

Read or change the AAE tree rebuild schedule.

# Description

Omit both values to read schedules. Supply both RW and RD to change the selected controllers.

# Arguments

## RW

datatype: integer hours
required: false
repeatable: false

### Description

Rebuild window in hours, from 0 to 43800. Supply together with RD.

## RD

datatype: integer seconds
required: false
repeatable: false

### Description

Rebuild delay in seconds, from 0 to 31536000. Supply together with RW.

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

3.4.0: 3a0919d4cb20b46299244abfe3b9396c623ec452b0798b198b965f562190abb1
3.4.1: 3a0919d4cb20b46299244abfe3b9396c623ec452b0798b198b965f562190abb1

# Tags

feature: tictac-aae
repository: riak
module: riak
concept: replica-repair
