# Metadata

command: shell:riak admin cluster location
versions: 3.4.0, 3.4.1

# Summary

Set a node’s physical-location label.

# Description

Location labels let the ring planner distinguish failure domains. Use meaningful labels for racks or availability zones, consistently across members.

# Arguments

## new_location

datatype: text
required: true
repeatable: false

### Description

Location label, for example `tokyo-a`.

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
default: local node

### Description

Run the operation on the named node, such as `openriak-kv@node1.test`. Use the full Erlang node name. Omit it to target the local node. Do not combine with `--all` where that flag is available.

# Reviewed against

3.4.0: 8601f1ec3d706bb2462a395300be3ed8810d54e82a31b32f180d1b8f3af7c541
3.4.1: 8601f1ec3d706bb2462a395300be3ed8810d54e82a31b32f180d1b8f3af7c541
