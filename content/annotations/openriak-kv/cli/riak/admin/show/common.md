# Metadata

command: shell:riak admin show
versions: 3.4.0, 3.4.1

# Summary

Read current values of configuration settings.

# Description

Supply one or more setting names. Values come from the running node; they can differ from files that have been edited since startup.

# Notes

Use `describe` for schema documentation. Use `set` only for settings that support runtime changes.

# Arguments

## variable

datatype: configuration setting name
required: true
repeatable: true

### Description

One or more configuration setting names, for example `ring_size` or `storage_backend`. Do not supply a `name=value` assignment.

# Options

## --all

datatype: flag (no value)
required: false
repeatable: false

### Description

Apply to every node in the cluster. Omit it to use the local node or the node selected by `--node`. Do not combine with `--node`.

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

# Examples

## shell-riak-admin-show:a-single-setting

### Description

Print the ring size for the selected node. The node uses eight partitions.

## shell-riak-admin-show:all-nodes

### Description

Read the setting on all cluster members. On a single-member cluster, expect one result.

# Reviewed against

3.4.0: 2895fd58ab7e9bd404c2ac661706ee44e41d954357dbab5f09d39b2526e8aef6
3.4.1: 2895fd58ab7e9bd404c2ac661706ee44e41d954357dbab5f09d39b2526e8aef6
