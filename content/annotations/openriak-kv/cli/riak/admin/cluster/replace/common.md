# Metadata

command: shell:riak admin cluster replace
versions: 3.4.0, 3.4.1

# Summary

Stage graceful replacement of a cluster member.

# Description

This stages a topology change. Review `riak admin cluster plan`, then run `riak admin cluster commit` to apply the reviewed plan. Use member-status and transfers to monitor convergence.

# Arguments

## node1

datatype: Erlang node name
required: true
repeatable: false

### Description

Existing node to replace. It must belong to this cluster.

## node2

datatype: Erlang node name
required: true
repeatable: false

### Description

Newly joining replacement node. It must not already be assigned as another node’s replacement.

# Errors

## reference-error-1

### Condition

A replacement node is not newly joining, or is already assigned to a replacement.

### Description

The replacement request is rejected.

### Remedy

Stage the new node’s join and choose a distinct replacement candidate.

# Results

## reference-result-1

### Description

On success, prints a staged-change confirmation. The membership change takes effect only after planning and committing it.

# Reviewed against

3.4.0: fb49691974a9f50b3ec943e65679c4c1bfe000b37b52ed4a9886e07033d0ca4a
3.4.1: 0e1adaac96b849e0e5d674418e3b4b327aa5dcfd8a80966a07961b2635bfb316

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_console
concept: partition-placement
