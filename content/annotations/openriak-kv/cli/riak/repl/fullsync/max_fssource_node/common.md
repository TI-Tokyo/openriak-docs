# Metadata

command: shell:riak repl fullsync max_fssource_node
versions: 3.4.0, 3.4.1

# Summary

Read or change the maximum full-sync source workers per node.

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

3.4.0: 0cf81a320914c247a0cd37aa17e792dfff4bba707c70dfeb1b6cfd8ebbb45795
3.4.1: 0cf81a320914c247a0cd37aa17e792dfff4bba707c70dfeb1b6cfd8ebbb45795

# Tags

feature: full-sync
repository: riak_repl
module: riak_repl_console
concept: replica-repair
