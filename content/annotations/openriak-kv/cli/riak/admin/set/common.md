# Metadata

command: shell:riak admin set
versions: 3.4.0, 3.4.1

# Summary

Change settings that support live reconfiguration.

# Description

Only settings on the runtime whitelist can be changed. In these releases that includes transfer_limit and the handoff.inbound/outbound flags. Runtime changes do not replace persistent configuration.

# Arguments

## variable=value

datatype: configuration assignment
required: true
repeatable: true

### Description

One or more assignments, such as `transfer_limit=2`. Values must satisfy the setting’s schema.

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

# Results

## outcome

### Description

Accepted settings take effect in the running application and can be checked with `show`. The examples preserve numeric arguments with the bundled release launcher and read back the configured transfer limit.

# Examples

## shell-riak-admin-set:all-nodes

### Description

Set the transfer limit across the cluster, then verify the local value is two.

# Reviewed against

3.4.0: e46102a7c3ce1549c2a9fce8aa95351b87c6f5c59729624d8b55d3e44c347e22
3.4.1: e46102a7c3ce1549c2a9fce8aa95351b87c6f5c59729624d8b55d3e44c347e22

# Tags

feature: node-operations
repository: riak_core
module: riak_core_console
concept: node-lifecycle
