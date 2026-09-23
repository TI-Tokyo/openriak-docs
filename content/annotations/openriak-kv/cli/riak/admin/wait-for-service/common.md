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

3.4.0: 76dac7b09e6f30cf5348e7a364ff82be12528e51fd8ef785c884565ff942ea34
3.4.1: 76dac7b09e6f30cf5348e7a364ff82be12528e51fd8ef785c884565ff942ea34

# Tags

feature: node-operations
repository: riak_core
module: erlang, riak_core_node_watcher
concept: node-lifecycle, scheduling
