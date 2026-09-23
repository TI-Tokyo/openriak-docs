# Metadata

command: shell:riak admin cluster resize-ring
versions: 3.4.0, 3.4.1

# Summary

Stage a change to the ring partition count.

# Description

Ring resizing changes partition ownership throughout the cluster. Plan and commit the staged resize, then monitor handoffs until completion.

# Arguments

## new-ring-size

datatype: positive power-of-two integer
required: true
repeatable: false

### Description

Desired partition count as a power of two, for example `16`. Choose the size for the entire cluster.

# Results

## outcome

### Description

A valid request stages a new ring size for plan and commit. The example uses a converged two-node test cluster and checks the proposed plan. A rejected request leaves no successful resize to commit.

# Examples

## shell-riak-admin-cluster-resize-ring:stage-a-larger-test-ring

title: Stage a larger ring

### Description

Stage a resize of the two-node ring. Review the resulting plan before committing.

# Reviewed against

3.4.0: 74129a97185fb3fcefd6f6cbaa92e7f57e21ad10502bf7a62613283a2515e49e
3.4.1: 74129a97185fb3fcefd6f6cbaa92e7f57e21ad10502bf7a62613283a2515e49e

# Tags

feature: cluster-management
repository: riak_core
module: riak_core_console
concept: partition-placement
