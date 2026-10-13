# Metadata

command: shell:riak admin wait-for-service
versions: 3.4.0, 3.4.1

# Summary

Wait for a named service to become available.

# Description

Useful in startup scripts that must wait beyond the first successful Erlang ping. The command can continue waiting when the service never starts.

# Arguments

## service_name

datatype: service name
required: true
repeatable: false

### Description

Service atom as text, for example `riak_kv` or `riak_repl`.

## target_node

datatype: Erlang node name
required: false
repeatable: false

### Description

Optional full node name. Omit to wait on the local node.

# Reviewed against

3.4.0: 2421fa6a3e65672014d1894f4cdb9fee08d89fca750697904e4e24b6ef63fc77
3.4.1: 2421fa6a3e65672014d1894f4cdb9fee08d89fca750697904e4e24b6ef63fc77

# Tags

feature: node-operations
repository: riak_core
module: erlang, riak_core_node_watcher
concept: node-lifecycle, scheduling
