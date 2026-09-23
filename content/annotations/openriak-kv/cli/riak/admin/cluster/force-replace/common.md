# Metadata

command: shell:riak admin cluster force-replace
versions: 3.4.0, 3.4.1

# Summary

Stage replacement of an unavailable member.

# Description

This stages a topology change. Review `riak admin cluster plan`, then run `riak admin cluster commit` to apply the reviewed plan. Use member-status and transfers to monitor convergence. Forced changes cannot hand off data from the unavailable node; remaining replicas must provide the data.

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

3.4.0: 24e3b4f30574e9dd19a8b9fbf08678e6e8b5558a389faec55151c252fb1804c7
3.4.1: 24e3b4f30574e9dd19a8b9fbf08678e6e8b5558a389faec55151c252fb1804c7

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_console
concept: partition-placement
