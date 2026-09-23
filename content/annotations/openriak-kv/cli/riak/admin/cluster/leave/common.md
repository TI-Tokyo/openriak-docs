# Metadata

command: shell:riak admin cluster leave
versions: 3.4.0, 3.4.1

# Summary

Stage a graceful departure from the cluster.

# Description

This stages a topology change. Review `riak admin cluster plan`, then run `riak admin cluster commit` to apply the reviewed plan. Use member-status and transfers to monitor convergence.

# Arguments

## node

datatype: Erlang node name
required: false
repeatable: false

### Description

Full Erlang node name, for example `openriak-kv@node2.test`.

# Results

## reference-result-1

### Description

On success, prints a staged-change confirmation. The membership change takes effect only after planning and committing it.

# Reviewed against

3.4.0: c699f269b307dc1446769dd106c13987598bdfc0389c75b62a6d36c9f3b07ac0
3.4.1: c699f269b307dc1446769dd106c13987598bdfc0389c75b62a6d36c9f3b07ac0

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_console
concept: partition-placement
