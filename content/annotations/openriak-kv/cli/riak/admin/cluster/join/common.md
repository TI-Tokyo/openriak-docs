# Metadata

command: shell:riak admin cluster join
versions: 3.4.0, 3.4.1

# Summary

Stage this node to join an existing cluster.

# Description

This stages a topology change. Review `riak admin cluster plan`, then run `riak admin cluster commit` to apply the reviewed plan. Use member-status and transfers to monitor convergence.

# Arguments

## node

datatype: Erlang node name
required: true
repeatable: false

### Description

Full Erlang node name, for example `openriak-kv@node2.test`.

# Results

## outcome

### Description

A successful call stages a join; `cluster plan` shows the proposed membership change before commit. The example invokes the bundled release launcher and verifies the resulting membership.

# Reviewed against

3.4.0: ac82cfe7499936cd791688c36eabc26c93aa75dacc52d06d0570e2d66d5c494f
3.4.1: 2283a355587d9b2b50f1ae9a39fe45e347724718dabad9117c288fa781556552

# Tags

feature: cluster-management
repository: riak_kv
module: riak_kv_console
concept: partition-placement
