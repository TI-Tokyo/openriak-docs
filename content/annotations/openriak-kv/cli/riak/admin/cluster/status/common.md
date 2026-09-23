# Metadata

command: shell:riak admin cluster status
versions: 3.4.0, 3.4.1

# Summary

Summarise node membership and ring readiness.

# Description

Read the membership, availability and ownership information before planning a topology change. Ring readiness means the ring is ready for coordinated changes; it is not a data-integrity test.

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

3.4.0: 72b4ce51c28303b28a4dc8ec31273e451bfe651935b7772ed458c512d1afd098
3.4.1: 72b4ce51c28303b28a4dc8ec31273e451bfe651935b7772ed458c512d1afd098

# Tags

feature: observability
repository: riak_core
module: riak_core_console
concept: diagnostics
