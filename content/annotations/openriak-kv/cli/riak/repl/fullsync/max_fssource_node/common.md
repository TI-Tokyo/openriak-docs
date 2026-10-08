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

3.4.0: 724f871d8b73662fbd2ab73310985ee1f741b009a96e50daf2213c96acfc3f5b
3.4.1: 724f871d8b73662fbd2ab73310985ee1f741b009a96e50daf2213c96acfc3f5b

# Tags

feature: full-sync
repository: riak_repl
module: riak_repl_console
concept: replica-repair
