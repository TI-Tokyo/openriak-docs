# Metadata

command: shell:riak repl fullsync max_fssink_node
versions: 3.4.0, 3.4.1

# Summary

Read or change the maximum full-sync sink workers per node.

# Description

Omit the value to read the current limit. A new value is sent to cluster members as a runtime setting; preserve the desired value in persistent configuration separately.

# Arguments

## value

datatype: positive integer
required: false
repeatable: false

### Description

New worker limit, for example `2`. Choose a positive value suited to disk and network capacity.

# Results

## outcome

### Description

With no value, this prints the current concurrency limit. With an integer, it changes the limit and prints the new value. The examples also read the value back.

# Reviewed against

3.4.0: 6508ca8ccbb0afeb07c4b47679e3d9760e5d17383c73fd5076452a5379ffdfcc
3.4.1: 6508ca8ccbb0afeb07c4b47679e3d9760e5d17383c73fd5076452a5379ffdfcc
