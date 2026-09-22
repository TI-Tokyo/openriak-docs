# Metadata

command: shell:riak admin cluster partition-count
versions: 3.4.0, 3.4.1

# Summary

Show the ring size or the partition count of a selected node.

# Description

With no node option, print the cluster-wide partition count. With `--node`, report ownership on that node.

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

datatype: Erlang node name
required: false
repeatable: false

### Description

Report the partition count owned by this node instead of the cluster-wide ring size. Use a full node name, such as `openriak-kv@node1.test`.

# Reviewed against

3.4.0: 75f5fce0ee51292fa6f98e021604764127d538d501f39174a10a3db5c0338eea
3.4.1: 75f5fce0ee51292fa6f98e021604764127d538d501f39174a10a3db5c0338eea
