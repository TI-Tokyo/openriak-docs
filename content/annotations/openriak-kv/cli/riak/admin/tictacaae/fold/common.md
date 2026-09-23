# Metadata

command: shell:riak admin tictacaae fold
versions: 3.4.0, 3.4.1

# Summary

Run an AAE range query and write its results as JSON.

# Description

Choose an operation and supply its required key=value filters. With --outfile, the query writes on the node’s filesystem asynchronously; an acknowledgment is not confirmation that the file is complete.

# Arguments

## operation

datatype: operation
required: true
repeatable: false

### Valid values

- list-buckets
- find-keys
- count-keys
- find-tombstones
- count-tombstones
- reap-tombstones
- object-stats
- erase-keys
- repair-keys

### Description

Select the range operation. Use count variants before data-removal operations.

## nval

datatype: positive integer
required: false
repeatable: false

### Description

Replication factor for list-buckets, supplied as `nval=3`.

## bucket

datatype: bucket name or type/name
required: false
repeatable: false

### Description

Bucket as `bucket=name` or `bucket=type/name`. Required by bucket-range operations.

## key_range

datatype: all or FROM,TO
required: false
repeatable: false

### Description

Use `key_range=all` or comma-separated lower and upper bounds.

## modified_range

datatype: all or timestamp bounds
required: false
repeatable: false

### Description

Use `modified_range=all` or comma-separated RFC3339 timestamps.

## segments

datatype: all or segment-list;tree-size
required: false
repeatable: false

### Description

Use `segments=all`, or a quoted segment list and tree size such as `segments=0,1;small`.

## sibling_count

datatype: non-negative integer
required: false
repeatable: false

### Description

Sibling-count threshold for key finding/counting. Supply this or object_size.

## object_size

datatype: non-negative integer
required: false
repeatable: false

### Description

Object-size threshold in bytes for key finding/counting. Supply this or sibling_count.

## change_method

datatype: change method
required: false
repeatable: false

### Valid values

- count
- local
- jobs:N

### Description

For destructive operations, start with `change_method=count`. The runtime also parses local and jobs:N; check the matching Erlang API before using a job mode.

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

## --outfile

datatype: filesystem path
required: false
repeatable: false

### Description

JSON destination path on the node. It must be writable by the Riak service account. The short spelling is `-o`.

# Reviewed against

3.4.0: c2f99fd8c18d29f53aa6558ece14b5e7a9e23246186a719dd8532400b83145ca
3.4.1: c2f99fd8c18d29f53aa6558ece14b5e7a9e23246186a719dd8532400b83145ca

# Tags

feature: tictac-aae
repository: riak
module: riak
concept: replica-repair
